```python
import boto3
from datetime import datetime, timedelta
from aws_monitoring.config import AWSConfig
import json
from typing import Dict, List, Any

class AWSCostMonitor:
    """
    Monitors AWS costs using the Cost Explorer API.
    """

    def __init__(self, config: AWSConfig = AWSConfig()) -> None:
        """
        Initializes the AWSCostMonitor with AWS credentials and region.

        Args:
            config (AWSConfig, optional): AWS configuration object. Defaults to AWSConfig().
        """
        self.client = boto3.client(
            'ce', 
            region_name=config.DEFAULT_REGIONS[0], 
            aws_access_key_id=config.AWS_ACCESS_KEY_ID, 
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
        )

    def get_cost(self, start: str, end: str, granularity: str, metrics: List[str], group_by: List[str] = []) -> Dict[str, Any]:
        """
        Retrieves AWS cost and usage data.

        Args:
            start (str): Start date in YYYY-MM-DD format.
            end (str): End date in YYYY-MM-DD format.
            granularity (str): Granularity of the data (e.g., DAILY, MONTHLY).
            metrics (List[str]): List of metrics to retrieve (e.g., UnblendedCost, UsageQuantity).
            group_by (List[str], optional): List of dimensions to group the data by (e.g., SERVICE, REGION). Defaults to [].

        Returns:
            Dict[str, Any]: The raw response from the Cost Explorer API.
        """
        response = self.client.get_cost_and_usage(
            TimePeriod={
                'Start': start,
                'End': end
            },
            Granularity=granularity,
            Metrics=metrics,
            GroupBy=[{'Type': 'COST_CATEGORY', 'Key': item} for item in group_by]
        )

        return response

    @staticmethod
    def to_json(response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts the raw Cost Explorer API response to a more readable JSON format and saves it to a file.

        Args:
            response (Dict[str, Any]): The raw response from the Cost Explorer API.

        Returns:
            Dict[str, Any]: A transformed dictionary with 'ResultsByTime' containing time periods, totals, and grouped metrics.
        """
        with open('response.json', 'w') as f:
            json.dump(response, f, indent=4)

        transformed_data = {
            "ResultsByTime": [
                {
                    "TimePeriod": result["TimePeriod"],
                    "Total": result["Total"],
                    "Groups": [
                        {
                            "Keys": group["Keys"],
                            "Metrics": {
                                metric_key: float(group["Metrics"][metric_key]["Amount"])
                                for metric_key in group["Metrics"]
                            }
                        }
                        for group in result["Groups"]
                    ]
                }
                for result in response["ResultsByTime"]
            ]
        }
        return transformed_data
```