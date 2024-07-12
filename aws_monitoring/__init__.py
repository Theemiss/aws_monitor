import boto3
from datetime import datetime, timedelta
from aws_monitoring.config import AWSConfig


class AWSCostMonitor():
    def __init__(self, config: AWSConfig = AWSConfig()) -> None:
        self.client = boto3.client(
            'ce', region_name=config.DEFAULT_REGIONS[0], aws_access_key_id=config.AWS_ACCESS_KEY_ID, aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY)

    def get_cost_and_usage(self, start: str, end: str, granularity: str, metrics: list, group_by: list) -> dict:
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
        return response
