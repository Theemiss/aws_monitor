```python
from aws_monitoring.utils import AWSCostMonitor
import matplotlib.pyplot as plt
import csv
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class AWSOrgMonitor(AWSCostMonitor):
    """
    Monitors AWS costs and provides functionalities for cost analysis, reporting, and alerting.
    Inherits from AWSCostMonitor.
    """

    def __init__(self):
        """
        Initializes the AWSOrgMonitor class.  Calls the constructor of the parent class (AWSCostMonitor).
        """
        super().__init__()

    def get_cost(self, start: str, end: str, granularity: str, metrics: list, group_by: list = [], json=False) -> dict:
        """
        Retrieves cost and usage data from AWS Cost Explorer.

        :param start: Start date in 'YYYY-MM-DD' format.
        :param end: End date in 'YYYY-MM-DD' format.
        :param granularity: Granularity of the data (DAILY, MONTHLY).
        :param metrics: List of metrics to fetch (e.g., ['UNBLENDED_COST']).
        :param group_by: List of dimensions to group by. Defaults to grouping by 'LINKED_ACCOUNT'.
        :param json:  If True, returns the response in JSON format. Defaults to False.
        :return: A dictionary containing the cost and usage data.
        """
        effective_group_by = ["LINKED_ACCOUNT"] + group_by
        response = self.client.get_cost_and_usage(
            TimePeriod={
                'Start': start,
                'End': end
            },
            Granularity=granularity,
            Metrics=metrics,
            GroupBy=[{'Type': 'DIMENSION', 'Key': item}
                     for item in effective_group_by]
        )
        if json:
            return self.to_json(response)
        return response

    def get_billed_accounts(self, start: str, end: str) -> list:
        """
        Retrieves a list of billed AWS accounts within a specified time period.

        :param start: Start date in 'YYYY-MM-DD' format.
        :param end: End date in 'YYYY-MM-DD' format.
        :return: A list of dictionaries, where each dictionary contains the account ID and name.
        """
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

    def get_cost_per_account(self, start: str, end: str) -> dict:
        """
        Calculates the cost per AWS account for a given time period.

        :param start: Start date in 'YYYY-MM-DD' format.
        :param end: End date in 'YYYY-MM-DD' format.
        :return: A dictionary where keys are account names and values are the corresponding costs.
        """
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

    def get_cost_per_account_graph(self, start: str, end: str) -> None:
        """
        Generates and displays a bar graph of cost per AWS account.

        :param start: Start date in 'YYYY-MM-DD' format.
        :param end: End date in 'YYYY-MM-DD' format.
        :return: None. Displays the graph using matplotlib.pyplot.show().
        """

        accounts_cost = self.get_cost_per_account(start, end)
        accounts = list(accounts_cost.keys())
        costs = list(accounts_cost.values())
        sorted_accounts_cost = sorted(zip(costs, accounts), reverse=True)  # Sort in descending order
        sorted_costs, sorted_accounts = zip(*sorted_accounts_cost)

        fig, ax = plt.subplots()
        ax.bar(sorted_accounts, sorted_costs)
        ax.set_xlabel('Accounts')
        ax.set_ylabel('Cost (USD)')
        ax.set_title(f'Cost per Account From {start} to {end}')

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45, ha="right")  # Rotate and align right for readability
        plt.tight_layout()

        plt.show()

    def get_cost_per_service(self, start: str, end: str, linked_account: str = None) -> dict:
        """
        Calculates the cost per AWS service for a given time period, optionally filtered by linked account.

        :param start: Start date in 'YYYY-MM-DD' format.
        :param end: End date in 'YYYY-MM-DD' format.
        :param linked_account: (Optional) The ID of the linked account to filter by. Defaults to None.
        :return: A dictionary where keys are service names and values are the corresponding costs.
        """
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

        # Filter out services with zero cost.
        service_cost = {k: v for k, v in service_cost.items() if float(v) != 0}
        return service_cost

    def get_cost_per_service_graph(self, start: str, end: str, linked_account: str = None) -> None:
        """
        Generates and displays a bar graph of cost per AWS service, optionally filtered by linked account.

        :param start: Start date in 'YYYY-MM-DD' format.
        :param end: End date in 'YYYY-MM-DD' format.
        :param linked_account: (Optional) The ID of the linked account to filter by. Defaults to None.
        :return: None. Displays the graph using matplotlib.pyplot.show().
        """

        service_cost = self.get_cost_per_service(start, end, linked_account)
        services = list(service_cost.keys())
        costs = list(service_cost.values())
        sorted_service_cost = sorted(zip(costs, services), reverse=True) # Sort in descending order
        sorted_costs, sorted_services = zip(*sorted_service_cost)

        fig, ax = plt.subplots()
        ax.bar(sorted_services, sorted_costs)
        ax.set_xlabel('Services')
        ax.set_ylabel('Cost (USD)')
        ax.set_title(f'Cost per Service From {start} to {end}')

        plt.xticks(rotation=45, ha="right") # Rotate and align right for readability
        plt.tight_layout()

        plt.show()

    def generate_report(self, start: str, end: str, report_type: str = 'csv', file_name: str = 'aws_cost_report') -> None:
        """
        Generates a customizable report of AWS costs in CSV or JSON format.

        :param start: Start date in 'YYYY-MM-DD' format.
        :param end: End date in 'YYYY-MM-DD' format.
        :param report_type: Type of the report to generate ('csv' or 'json'). Defaults to 'csv'.
        :param file_name: Name of the report file. Defaults to 'aws_cost_report'.
        :raises ValueError: If an unsupported report type is specified.
        :return: None. Generates a report file.
        """

        response = self.client.get_cost_and_usage(
            TimePeriod={
                'Start': start,
                'End': end
            },
            Granularity="MONTHLY",
            Metrics=['UNBLENDED_COST'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}]
        )

        if report_type == 'csv':
            self._generate_csv_report(response, file_name)
        elif report_type == 'json':
            self._generate_json_report(response, file_name)
        else:
            raise ValueError("Unsupported report type. Use 'csv' or 'json'.")

    def _generate_csv_report(self, data: dict, file_name: str) -> None:
        """
        Generates a CSV report from cost and usage data.

        :param data: A dictionary containing cost and usage data.
        :param file_name: Name of the CSV file to generate.
        :return: None. Generates a CSV file.
        """

        with open(f'{file_name}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["TimePeriod", "Group", "Amount", "Unit"])  # Header row
            for result in data['ResultsByTime']:
                time_period = f"{result['TimePeriod']['Start']} - {result['TimePeriod']['End']}"
                for group in result['Groups']:
                    group_name = ', '.join(group['Keys'])
                    amount = group['Metrics']['UnblendedCost']['Amount']
                    unit = group['Metrics']['UnblendedCost']['Unit']
                    writer.writerow([time_period, group_name, amount, unit])

    def _generate_json_report(self, data: dict, file_name: str) -> None:
        """
        Generates a JSON report from cost and usage data.

        :param data: A dictionary containing cost and usage data.
        :param file_name: Name of the JSON file to generate.
        :return: None. Generates a JSON file.
        """

        with open(f'{file_name}.json', 'w') as jsonfile:
            json.dump(data, jsonfile, indent=4)

    def get_cost_per_region(self, start: str, end: str) -> dict:
        """
        Calculates the cost per AWS region for a given time period.

        :param start: Start date in 'YYYY-MM-DD' format.
        :param end: End date in 'YYYY-MM-DD' format.
        :return: A dictionary where keys are region names and values are the corresponding costs.
        """
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

    def get_cost_per_region_graph(self, start: str, end: str) -> None:
        """
        Generates and displays a bar graph of cost per AWS region.

        :param start: Start date in 'YYYY-MM-DD' format.
        :param end: End date in 'YYYY-MM-DD' format.
        :return: None. Displays the graph using matplotlib.pyplot.show().
        """

        region_cost = self.get_cost_per_region(start, end)
        regions = list(region_cost.keys())
        costs = list(region_cost.values())
        sorted_region_cost = sorted(zip(costs, regions), reverse=True)  # Sort in descending order
        sorted_costs, sorted_regions = zip(*sorted_region_cost)

        fig, ax = plt.subplots()
        ax.bar(sorted_regions, sorted_costs)
        ax.set_xlabel('Regions')
        ax.set_ylabel('Cost (USD)')
        ax.set_title(f'Cost per Region From {start} to {end}')

        plt.xticks(rotation=45, ha="right")  # Rotate and align right for readability
        plt.tight_layout()

        plt.show()

    def set_cost_alert(self, start: str, end: str, threshold: float, email: str, granularity: str = 'MONTHLY') -> None:
        """
        Sets an alert for AWS costs.  Sends an email if the total cost exceeds the specified threshold.

        :param start: Start date in 'YYYY-MM-DD' format.
        :param end: End date in 'YYYY-MM-DD' format.
        :param threshold: Cost threshold for the alert.
        :param email: Email address to send the alert.
        :param granularity: Granularity of the data (DAILY, MONTHLY). Defaults to 'MONTHLY'.
        :return: None. Sends an email if the cost exceeds the threshold.
        """
        total_cost = self.get_total_cost(start, end, granularity)
        if total_cost > threshold:
            self.send_alert_email(email, total_cost, threshold)

    def get_total_cost(self, start: str, end: str, granularity: str = 'MONTHLY') -> float:
        """
        Calculates the total AWS cost for a given time period.

        :param start: Start date in 'YYYY-MM-DD' format.
        :param end: End date in 'YYYY-MM-DD' format.
        :param granularity: Granularity of the data (DAILY, MONTHLY). Defaults to 'MONTHLY'.
        :return: The total AWS cost as a float.
        """
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

    def send_alert_email(self, email: str, total_cost: float, threshold: float) -> None:
        """
        Sends an email alert when the AWS cost exceeds a specified threshold.

        :param email: Email address to send the alert to.
        :param total_cost: The total AWS cost.
        :param threshold: The cost threshold.
        :return: None. Sends an email alert.
        """
        sender_email = "your_email@example.com"  # Replace with your email
        sender_password = "your_email_password"  # Replace with your password
        subject = "AWS Cost Alert"
        body = f"Alert: Your AWS cost has exceeded the threshold.\n\nTotal Cost: ${total_cost:.2f}\nThreshold: ${threshold:.2f}"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP('smtp.example.com', 587) as server: # Replace with your SMTP server
                server.starttls()
                server.login(sender_email, sender_password)
                text = msg.as_string()
                server.sendmail(sender_email, email, text)
            print(f"Alert email sent to {email}")
        except Exception as e:
            print(f"Failed to send alert email: {e}")
```