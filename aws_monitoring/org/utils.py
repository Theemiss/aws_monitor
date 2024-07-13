
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
            Granularity='MONTHLY',
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

    def generate_report(self, start: str, end: str, report_type: str = 'csv', file_name: str = 'aws_cost_report') -> None:
        """
        Generates a customizable report of AWS costs.

        :param start: Start date in 'YYYY-MM-DD' format.
        :param end: End date in 'YYYY-MM-DD' format.
        :param granularity: Granularity of the data (DAILY, MONTHLY).
        :param metrics: List of metrics to fetch (e.g., ['UNBLENDED_COST']).
        :param group_by: List of dimensions to group by.
        :param report_type: Type of the report to generate ('csv' or 'json').
        :param file_name: Name of the report file.
        """
        group_by = []
        group_by = ["LINKED_ACCOUNT"] + group_by
        response = self.client.get_cost_and_usage(
            TimePeriod={
                'Start': start,
                'End': end
            },
            Granularity="MONTHLY",
            Metrics=['UNBLENDED_COST'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': item} for item in group_by]
        )

        if report_type == 'csv':
            self._generate_csv_report(response, file_name)
        elif report_type == 'json':
            self._generate_json_report(response, file_name)
        else:
            raise ValueError("Unsupported report type. Use 'csv' or 'json'.")

    def _generate_csv_report(self, data: dict, file_name: str) -> None:
        import csv
        with open(f'{file_name}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["TimePeriod", "Group", "Amount", "Unit"])
            for result in data['ResultsByTime']:
                time_period = f"{result['TimePeriod']['Start']} - {result['TimePeriod']['End']}"
                for group in result['Groups']:
                    group_name = ', '.join(group['Keys'])
                    amount = group['Metrics']['UnblendedCost']['Amount']
                    unit = group['Metrics']['UnblendedCost']['Unit']
                    writer.writerow([time_period, group_name, amount, unit])

    def _generate_json_report(self, data: dict, file_name: str) -> None:
        import json
        with open(f'{file_name}.json', 'w') as jsonfile:
            json.dump(data, jsonfile, indent=4)

    def get_cost_per_region(self, start: str, end: str) -> dict:
        response = self.client.get_cost_and_usage(
            TimePeriod={
                'Start': start,
                'End': end
            },
            Granularity='MONTHLY',
            Metrics=['UNBLENDED_COST'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'REGION'}]
        )

        region_cost = {}
        for group in response['ResultsByTime'][0]['Groups']:
            region_name = group['Keys'][0]
            cost = group['Metrics']['UnblendedCost']['Amount']
            region_cost[region_name] = cost
        return region_cost

    def get_cost_per_region_graph(self, start: str, end: str):
        import matplotlib.pyplot as plt
        region_cost = self.get_cost_per_region(start, end)
        regions = list(region_cost.keys())
        costs = list(region_cost.values())
        sorted_region_cost = sorted(zip(costs, regions), reverse=False)
        sorted_costs, sorted_regions = zip(*sorted_region_cost)
        fig, ax = plt.subplots()
        ax.bar(sorted_regions, sorted_costs)
        ax.set_xlabel('Regions')
        ax.set_ylabel('Cost (USD)')
        ax.set_title(f'Cost per Region From {start} to {end}')

        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.show()

    def set_cost_alert(self, start: str, end: str, threshold: float, email: str, granularity: str = 'MONTHLY'):
        """
        Sets an alert for AWS costs.

        :param start: Start date in 'YYYY-MM-DD' format.
        :param end: End date in 'YYYY-MM-DD' format.
        :param threshold: Cost threshold for the alert.
        :param email: Email address to send the alert.
        :param granularity: Granularity of the data (DAILY, MONTHLY).
        """
        total_cost = self.get_total_cost(start, end, granularity)
        if total_cost > threshold:
            self.send_alert_email(email, total_cost, threshold)

    def get_total_cost(self, start: str, end: str, granularity: str = 'MONTHLY') -> float:
        response = self.client.get_cost_and_usage(
            TimePeriod={
                'Start': start,
                'End': end
            },
            Granularity=granularity,
            Metrics=['UNBLENDED_COST']
        )
        total_cost = sum(float(result['Total']['UnblendedCost']['Amount'])
                         for result in response['ResultsByTime'])
        return total_cost

    def send_alert_email(self, email: str, total_cost: float, threshold: float):
        sender_email = "your_email@example.com"
        sender_password = "your_email_password"
        subject = "AWS Cost Alert"
        body = f"Alert: Your AWS cost has exceeded the threshold.\n\nTotal Cost: ${total_cost}\nThreshold: ${threshold}"
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.example.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, email, text)
            server.quit()
            print(f"Alert email sent to {email}")
        except Exception as e:
            print(f"Failed to send alert email: {e}")
