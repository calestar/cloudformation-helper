"""Helpers to access AWS information."""

import botocore
import boto3


CHANGESET_NAME = "cfhelper-changeset"


def get_cloudformation_client(selected_profile, selected_region):
    session = boto3.Session(
        profile_name=selected_profile,
        region_name=selected_region,
    )
    return session.client("cloudformation")


def stack_exists(stack_name, selected_profile, selected_region):
    client = get_cloudformation_client(selected_profile, selected_region)

    try:
        client.describe_stacks(StackName=stack_name)
    except botocore.exceptions.ClientError as error:
        if (
            error.response["Error"]["Code"] == "ValidationError"
            and "does not exist" in error.response["Error"]["Message"]
        ):
            return False
        raise error

    return True


def create_stack(
    stack_name, stack_file, capabilities, selected_profile, selected_region
):
    client = get_cloudformation_client(selected_profile, selected_region)
    with open(stack_file) as f:
        template = f.read()

    client.create_stack(
        StackName=stack_name,
        TemplateBody=template,
        Capabilities=sorted(capabilities),
    )
    waiter = client.get_waiter("stack_create_complete")

    waiter.wait(StackName=stack_name, WaiterConfig={"Delay": 15, "MaxAttempts": 120})


def update_stack(
    stack_name, stack_file, capabilities, selected_profile, selected_region
):
    client = get_cloudformation_client(selected_profile, selected_region)
    with open(stack_file) as f:
        template = f.read()

    # TODO, handle errors
    # botocore.errorfactory.InsufficientCapabilitiesException: An error occurred (InsufficientCapabilitiesException)
    # when calling the UpdateStack operation: Requires capabilities : [CAPABILITY_IAM]
    # botocore.exceptions.ClientError: An error occurred (ValidationError) when calling the UpdateStack operation: No updates are to be performed.
    client.update_stack(
        StackName=stack_name,
        TemplateBody=template,
        Capabilities=sorted(capabilities),
    )

    waiter = client.get_waiter("stack_update_complete")
    waiter.wait(StackName=stack_name, WaiterConfig={"Delay": 15, "MaxAttempts": 120})


def has_changeset(stack_name, selected_profile, selected_region):
    try:
        get_changeset(stack_name, selected_profile, selected_region)
    except botocore.exceptions.ClientError as error:
        if (
            error.response["Error"]["Code"] == "ValidationError"
            and "does not exist" in error.response["Error"]["Message"]
        ):
            return False
        if error.response["Error"]["Code"] == "ChangeSetNotFound":
            return False
        raise error

    return True


def get_changeset(stack_name, selected_profile, selected_region):
    client = get_cloudformation_client(selected_profile, selected_region)

    return client.describe_change_set(
        StackName=stack_name,
        ChangeSetName=CHANGESET_NAME,
    )


def create_changeset(
    stack_name, stack_file, is_creation, capabilities, selected_profile, selected_region
):
    client = get_cloudformation_client(selected_profile, selected_region)
    changeset_type = "CREATE" if is_creation else "UPDATE"
    with open(stack_file) as f:
        template = f.read()

    client.create_change_set(
        StackName=stack_name,
        TemplateBody=template,
        Capabilities=sorted(capabilities),
        ChangeSetName=CHANGESET_NAME,
        ChangeSetType=changeset_type,
    )

    waiter = client.get_waiter("change_set_create_complete")
    waiter.wait(
        ChangeSetName=CHANGESET_NAME,
        StackName=stack_name,
        WaiterConfig={"Delay": 15, "MaxAttempts": 120},
    )


def execute_changeset(stack_name, is_creation, selected_profile, selected_region):
    client = get_cloudformation_client(selected_profile, selected_region)
    client.execute_change_set(
        StackName=stack_name,
        ChangeSetName=CHANGESET_NAME,
    )

    waiter_type = "stack_create_complete" if is_creation else "stack_update_complete"
    waiter = client.get_waiter(waiter_type)
    waiter.wait(StackName=stack_name, WaiterConfig={"Delay": 15, "MaxAttempts": 120})


def delete_changeset(stack_name, selected_profile, selected_region):
    client = get_cloudformation_client(selected_profile, selected_region)

    client.delete_change_set(
        StackName=stack_name,
        ChangeSetName=CHANGESET_NAME,
    )
