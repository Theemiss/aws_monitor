import pathlib
import os
import json


class AWSConfig():
    """
    Set up the environment for a script that interacts with AWS resources.

    Inputs:
    - The code snippet does not have any explicit inputs. It relies on environment variables defined in a `.env` file or in the system environment.

    Outputs:
    - The code snippet does not produce any explicit outputs. It sets up the environment for a script that interacts with AWS resources by assigning values to various variables.
    """

    # Load environment variables from .env file

    # Get the current directory
    CURRENT_DIR = str(pathlib.Path().absolute())

    # Get the AWS profile
    PROFILE = os.environ.get("AWS_PROFILE", "default")

    # Get the AWS access key ID
 

    # Get the file for resources types
    FILE_FOR_RESOURCES_TYPES = os.environ.get(
        "FILE_FOR_RESOURCES_TYPES", "students/aws/resource_types.json")

    # Set the default regions
    DEFAULT_REGIONS = ["us-east-1", "us-east-2", "eu-north-1", 'global']

    ENV = os.environ.get("ENV", "dev")
