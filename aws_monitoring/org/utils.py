
from aws_monitoring.utils import AWSCostMonitor


class AWSOrgMonitor(AWSCostMonitor):
    def __init__(self):
        super().__init__()

    def get_cost(self, start: str, end: str, granularity: str, metrics: list, group_by: list = [], json=False) -> dict:
        group_by = ["LINKED_ACCOUNT"] + group_by
        response = self.client.get_cost_and_usage(
            TimePeriod={
                'Start': start,
                'End': end
            },
            Granularity=granularity,
            Metrics=metrics,
            GroupBy=[{'Type': 'COST_CATEGORY', 'Key': item}
                     for item in group_by]
        )
        if json:
            return self.to_json(response)
        return response

    def get_billed_accounts(self, start: str, end: str) -> dict:
        response = self.client.get_dimension_values(
            TimePeriod={
                'Start': start,
                'End': end
            },
            Dimension='LINKED_ACCOUNT',
            Context='COST_AND_USAGE',
            SearchString="*"
        )
        users = [{"id":  item['Value'], "name": item['Attributes']
                  ['description']} for item in response['DimensionValues']]

        return users

    def get_cost_per_account(self, start, end) -> dict:
        billed_accounts = self.get_billed_accounts(start, end)
        response = self.client.get_cost_and_usage(
            TimePeriod={
                'Start': start,
                'End': end
            },
            Granularity='MONTHLY',
            Metrics=['UNBLENDED_COST'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}
            ]
        )

        accounts_cost = {}
        for group in response['ResultsByTime'][0]['Groups']:
            account_id = group['Keys'][0]
            cost = group['Metrics']['UnblendedCost']['Amount']
            account_name = next(
                (account['name'] for account in billed_accounts if account['id'] == account_id), account_id)
            accounts_cost[account_name] = cost

        return accounts_cost

    def get_cost_per_account_graph(self, start, end):
        import matplotlib.pyplot as plt

        accounts_cost = self.get_cost_per_account(start, end)
        accounts = list(accounts_cost.keys())
        costs = list(accounts_cost.values())
        sorted_accounts_cost = sorted(zip(costs, accounts), reverse=False)
        sorted_costs, sorted_accounts = zip(*sorted_accounts_cost)

        fig, ax = plt.subplots()
        ax.bar(sorted_accounts, sorted_costs)
        ax.set_xlabel('Accounts')
        ax.set_ylabel('Cost (USD)')
        ax.set_title(f'Cost per Account From {start} to {end}')

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        plt.tight_layout()

        return plt.show()

    def get_cost_per_service(self, start: str, end: str, linked_account: str = None) -> dict:
        group_by = [{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        if linked_account:
            group_by.append({'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'})

        response = self.client.get_cost_and_usage(
            TimePeriod={
                'Start': start,
                'End': end
            },
            Granularity='DAILY',
            Metrics=['UNBLENDED_COST'],
            GroupBy=group_by
        )

        service_cost = {}
        for group in response['ResultsByTime'][0]['Groups']:
            service_name = group['Keys'][0]
            cost = group['Metrics']['UnblendedCost']['Amount']
            service_cost[service_name] = cost
        service_cost = {k: v for k, v in service_cost.items() if v != 0}
        return service_cost

    def get_cost_per_service_graph(self, start: str, end: str, linked_account: str = None):
        import matplotlib.pyplot as plt
        service_cost = self.get_cost_per_service(start, end, linked_account)
        services = list(service_cost.keys())
        costs = list(service_cost.values())
        sorted_service_cost = sorted(zip(costs, services), reverse=False)
        sorted_costs, sorted_services = zip(*sorted_service_cost)
        fig, ax = plt.subplots()
        ax.bar(sorted_services, sorted_costs)
        ax.set_xlabel('Services')
        ax.set_ylabel('Cost (USD)')
        ax.set_title(f'Cost per Service From {start} to {end}')

        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.show()
