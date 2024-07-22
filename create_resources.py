import sys
import random
import string
from azure.identity import DefaultAzureCredential
from azureml.core import Workspace
from azure.mgmt.resource import ResourceManagementClient

def create_random_suffix(length=6):
    """ Generate a random string of letters and digits """
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def register_resource_provider(credential, subscription_id):
    """ Register an Azure resource provider """
    client = ResourceManagementClient(credential, subscription_id)
    # Register the machine learning resource provider
    provider = client.providers.register('Microsoft.MachineLearningServices')
    print(f"Registered resource provider: {provider.namespace}")

def create_aml_workspace():
    # Get credentials and subscription ID from Azure environment
    credential = DefaultAzureCredential()
    subscription_id = credential.get_token("https://management.azure.com/").claims['xms_mirid'].split('/')[4]

    # Register resource providers
    register_resource_provider(credential, subscription_id)

    # Generate unique names for the resource group and workspace
    suffix = create_random_suffix()
    resource_group = f"aml_rg_{suffix}"
    workspace_name = f"aml_ws_{suffix}"
    location = "westus2"

    try:
        # Create the resource group and workspace
        print(f"Creating resource group '{resource_group}' and workspace '{workspace_name}' in {location}")
        ws = Workspace.create(name=workspace_name,
                              subscription_id=subscription_id,
                              resource_group=resource_group,
                              create_resource_group=True,
                              location=location,
                              exist_ok=True)

        print("Workspace created successfully.")
    except Exception as e:
        print(f"Failed to create workspace: {e}")
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(create_aml_workspace())
