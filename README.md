# AWS Cost Monitoring Package

This package provides tools for monitoring and analyzing AWS costs, both at the organizational level and individual account level. It includes functionality to get detailed cost breakdowns by linked accounts, AWS services, and regions, along with visualizations and alerting.

## Installation

To install the package, use pip:

```bash
pip install aws-monitor
```

This will also install the following dependencies:

- `boto3`
- `matplotlib`

## Usage

### AWSOrgMonitor Class

This class inherits from `AWSCostMonitor` and provides methods to fetch and analyze AWS cost data.

#### Initialization

```python
from aws_monitoring.utils import AWSCostMonitor

class AWSOrgMonitor(AWSCostMonitor):
    def __init__(self):
        super().__init__()
```

#### Get Cost

Fetches the cost data within the specified time period and granularity.

```python
def get_cost(self, start: str, end: str, granularity: str, metrics: list, group_by: list = [], json=False) -> dict:
```

- **start**: Start date in `YYYY-MM-DD` format.
- **end**: End date in `YYYY-MM-DD` format.
- **granularity**: Granularity of the data (DAILY, MONTHLY).
- **metrics**: List of metrics to fetch (e.g., ['UNBLENDED_COST']).
- **group_by**: List of dimensions to group by.
- **json**: Whether to return the response in JSON format.

#### Get Billed Accounts

Fetches the list of billed accounts within the specified time period.

```python
def get_billed_accounts(self, start: str, end: str) -> dict:
```

#### Get Cost Per Account

Fetches the cost per account within the specified time period.

```python
def get_cost_per_account(self, start, end) -> dict:
```

#### Get Cost Per Account Graph

Displays a bar graph of the cost per account within the specified time period.

```python
def get_cost_per_account_graph(self, start, end):
```

#### Get Cost Per Service

Fetches the cost per AWS service within the specified time period and optionally for a specific linked account.

```python
def get_cost_per_service(self, start: str, end: str, linked_account: str = None) -> dict:
```

#### Get Cost Per Service Graph

Displays a bar graph of the cost per AWS service within the specified time period and optionally for a specific linked account.

```python
def get_cost_per_service_graph(self, start: str, end: str, linked_account: str = None):
```

#### Generate Customizable Reports

Generates customizable reports of AWS costs.

```python
def generate_report(self, start: str, end: str, granularity: str, metrics: list, group_by: list = [], report_type: str = 'csv', file_name: str = 'aws_cost_report') -> None:
```

- **start**: Start date in `YYYY-MM-DD` format.
- **end**: End date in `YYYY-MM-DD` format.
- **granularity**: Granularity of the data (DAILY, MONTHLY).
- **metrics**: List of metrics to fetch (e.g., ['UNBLENDED_COST']).
- **group_by**: List of dimensions to group by.
- **report_type**: Type of the report to generate ('csv' or 'json').
- **file_name**: Name of the report file.

#### Get Cost Per Region

Fetches the cost per AWS region within the specified time period.

```python
def get_cost_per_region(self, start: str, end: str) -> dict:
```

#### Get Cost Per Region Graph

Displays a bar graph of the cost per AWS region within the specified time period.

```python
def get_cost_per_region_graph(self, start: str, end: str):
```

#### Set Cost Alert

Sets an alert for AWS costs and sends an email notification if the cost exceeds the specified threshold.

```python
def set_cost_alert(self, start: str, end: str, threshold: float, email: str, granularity: str = 'MONTHLY'):
```

- **start**: Start date in `YYYY-MM-DD` format.
- **end**: End date in `YYYY-MM-DD` format.
- **threshold**: Cost threshold for the alert.
- **email**: Email address to send the alert.
- **granularity**: Granularity of the data (DAILY, MONTHLY).

## Example

Here is a basic example of how to use the `AWSOrgMonitor` class:

```python
from aws_monitoring.utils import AWSOrgMonitor

monitor = AWSOrgMonitor()

# Get cost data
cost_data = monitor.get_cost(start='2023-01-01', end='2023-01-31', granularity='MONTHLY', metrics=['UNBLENDED_COST'])
print(cost_data)

# Get billed accounts
billed_accounts = monitor.get_billed_accounts(start='2023-01-01', end='2023-01-31')
print(billed_accounts)

# Get cost per account
cost_per_account = monitor.get_cost_per_account(start='2023-01-01', end='2023-01-31')
print(cost_per_account)

# Display cost per account graph
monitor.get_cost_per_account_graph(start='2023-01-01', end='2023-01-31')

# Get cost per service
cost_per_service = monitor.get_cost_per_service(start='2023-01-01', end='2023-01-31')
print(cost_per_service)

# Display cost per service graph
monitor.get_cost_per_service_graph(start='2023-01-01', end='2023-01-31')

# Generate a report
monitor.generate_report(start='2023-01-01', end='2023-01-31', granularity='MONTHLY', metrics=['UNBLENDED_COST'], group_by=['SERVICE'], report_type='csv', file_name='aws_cost_report')

# Set a cost alert
monitor.set_cost_alert(start='2023-01-01', end='2023-01-31', threshold=1000.0, email='your_email@example.com')
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Author

Ahmed Belhaj - [GitHub](https://github.com/Theemiss)
