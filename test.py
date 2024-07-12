

from aws_monitoring import AWSCostMonitor
import datetime
from datetime import timedelta

cost = AWSCostMonitor()


data = cost.get_cost_and_usage(start='2024-01-01', end='2024-06-30',
                     granularity='MONTHLY', metrics=['BlendedCost'], group_by=[])

print(data)
print('\n\n\n')

# Get the costs for the last 30 days
end_date = datetime.datetime.now()
start_date = end_date - timedelta(days=30)

data = cost.get_cost_and_usage(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'),
                     granularity='DAILY', metrics=['BlendedCost'], group_by=[])

# Get The costs for last 30 days and group them by service
end_date = datetime.datetime.now()
start_date = end_date - timedelta(days=30)
data = cost.get_cost_and_usage(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'),
                     granularity='DAILY', metrics=['BlendedCost'], group_by=["Service","Linked account"])
