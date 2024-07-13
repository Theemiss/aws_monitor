# AWS Cost Monitoring Package

This package provides tools for monitoring and analyzing AWS costs, both at the organizational level and individual account level. It includes functionality to get detailed cost breakdowns by linked accounts and AWS services, along with visualizations.

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

### Example Usage

```python
from aws_monitoring.utils import AWSOrgMonitor

monitor = AWSOrgMonitor()
start_date = '2023-06-01'
end_date = '2023-06-30'

# Get cost per service
service_costs = monitor.get_cost_per_service(start_date, end_date)
print(service_costs)

# Visualize cost per service
monitor.get_cost_per_service_graph(start_date, end_date)

# Get cost per account
account_costs = monitor.get_cost_per_account(start_date, end_date)
print(account_costs)

# Visualize cost per account
monitor.get_cost_per_account_graph(start_date, end_date)
```

## License

This package is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
