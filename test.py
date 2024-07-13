

import json

from aws_monitoring import AWSCostMonitor, AWSOrgMonitor
import datetime
from datetime import timedelta

org_cost = AWSOrgMonitor()


# Get The costs for last month
last_month = datetime.datetime.now() - timedelta(days=30)
start_date = last_month.replace(day=1)
end_date = start_date + timedelta(days=32)



service= org_cost.get_cost_per_service_graph(start=start_date.strftime(
    '%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
print(service)