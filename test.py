```python
import json
import datetime
from datetime import timedelta

from aws_monitoring import AWSOrgMonitor


def get_last_month_dates():
    """
    Calculates the start and end dates for the previous month.

    Returns:
        tuple: A tuple containing the start and end dates as strings in 'YYYY-MM-DD' format.
    """
    today = datetime.datetime.now()
    first_day_current_month = today.replace(day=1)
    last_day_previous_month = first_day_current_month - timedelta(days=1)
    first_day_previous_month = last_day_previous_month.replace(day=1)

    start_date = first_day_previous_month.strftime('%Y-%m-%d')
    end_date = last_day_previous_month.strftime('%Y-%m-%d')  # corrected end date

    return start_date, end_date


def main():
    """
    Retrieves and prints the cost per service graph for the previous month from AWS Org.
    """
    org_cost = AWSOrgMonitor()
    start_date, end_date = get_last_month_dates()
    service_costs = org_cost.get_cost_per_service_graph(start=start_date, end=end_date)
    print(service_costs)


if __name__ == "__main__":
    main()
```