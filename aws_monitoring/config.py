```python
import pathlib
import os
import json


class AWSConfig:
    """
    Configures the environment for interacting with AWS resources.

    This class retrieves AWS credentials and configurations from environment variables,
    providing a centralized access point for these settings.  It prioritizes environment
    variables, falling back to defaults where necessary.

    Attributes:
        CURRENT_DIR (str): The absolute path to the current directory.
        PROFILE (str): The AWS profile name. Defaults to "default".
        AWS_ACCESS_KEY_ID (str): The AWS access key ID. Defaults to an empty string.
        AWS_SECRET_ACCESS_KEY (str): The AWS secret access key. Defaults to an empty string.
        FILE_FOR_RESOURCES_TYPES (str): Path to the JSON file defining AWS resource types.
            Defaults to "students/aws/resource_types.json".
        DEFAULT_REGIONS (list): A list of default AWS regions to use.
        ENV (str): The environment (e.g., "dev", "prod"). Defaults to "dev".
    """

    CURRENT_DIR = str(pathlib.Path().absolute())
    PROFILE = os.environ.get("AWS_PROFILE", "default")
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    FILE_FOR_RESOURCES_TYPES = os.environ.get(
        "FILE_FOR_RESOURCES_TYPES", "students/aws/resource_types.json"
    )
    DEFAULT_REGIONS = ["us-east-1", "us-east-2", "eu-north-1", "global"]
    ENV = os.environ.get("ENV", "dev")
```