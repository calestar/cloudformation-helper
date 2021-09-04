#!/usr/bin/env python

"""Tests for valid calls to deploy."""

import mock
import os

from cloudformation_helper.utils import aws

from ..helpers import call_cfhelper, cfhelper_mocks

HERE = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIR = os.path.join(HERE, "..", "data", "config")


@mock.patch.object(aws, "stack_exists", return_value=False)
def test_create(mock_aws_stack_exists):
    """Create a new stack"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--config",
                os.path.join(CONFIG_DIR, "valid_multistacks.cfh"),
                "deploy",
                "MyStackAlias",
            ],
        )

        client_mock.create_stack.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=[],
        )


@mock.patch.object(aws, "stack_exists", return_value=True)
def test_update(mock_aws_stack_exists):
    """Update an existing stack"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--config",
                os.path.join(CONFIG_DIR, "valid_multistacks.cfh"),
                "deploy",
                "MyStackAlias",
            ],
        )

        client_mock.update_stack.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=[],
        )


@mock.patch.object(aws, "stack_exists", return_value=False)
@mock.patch.object(aws, "has_changeset", return_value=False)
def test_create_with_changeset(mock_aws_has_changeset, mock_aws_stack_exists):
    """Create a new stack using changesets"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--config",
                os.path.join(CONFIG_DIR, "valid_with_changeset.cfh"),
                "deploy",
                "MyStackAlias",
            ],
            input="y\n",
        )

        client_mock.create_change_set.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=[],
            ChangeSetName=aws.CHANGESET_NAME,
            ChangeSetType="CREATE",
        )

        client_mock.execute_change_set.assert_called_once_with(
            StackName="MyStackName",
            ChangeSetName=aws.CHANGESET_NAME,
        )


@mock.patch.object(aws, "stack_exists", return_value=False)
@mock.patch.object(aws, "has_changeset", return_value=False)
def test_create_with_changeset_no_execute(
    mock_aws_has_changeset, mock_aws_stack_exists
):
    """Create a new stack using changesets, but don't execute"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--config",
                os.path.join(CONFIG_DIR, "valid_with_changeset.cfh"),
                "deploy",
                "MyStackAlias",
            ],
            input="n\ny\n",
        )

        client_mock.create_change_set.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=[],
            ChangeSetName=aws.CHANGESET_NAME,
            ChangeSetType="CREATE",
        )

        client_mock.execute_change_set.assert_not_called()
        client_mock.delete_change_set.assert_not_called()


@mock.patch.object(aws, "stack_exists", return_value=False)
@mock.patch.object(aws, "has_changeset", return_value=False)
def test_create_with_changeset_no_execute_cleanup(
    mock_aws_has_changeset, mock_aws_stack_exists
):
    """Create a new stack using changesets, don't execute and delete changeset"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--config",
                os.path.join(CONFIG_DIR, "valid_with_changeset.cfh"),
                "deploy",
                "MyStackAlias",
            ],
            input="n\nn\n",
        )

        client_mock.create_change_set.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=[],
            ChangeSetName=aws.CHANGESET_NAME,
            ChangeSetType="CREATE",
        )

        client_mock.execute_change_set.assert_not_called()
        client_mock.delete_change_set.assert_called_once_with(
            StackName="MyStackName",
            ChangeSetName=aws.CHANGESET_NAME,
        )


@mock.patch.object(aws, "stack_exists", return_value=True)
@mock.patch.object(aws, "has_changeset", return_value=False)
def test_update_with_changeset(mock_aws_has_changeset, mock_aws_stack_exists):
    """Update an existing stack using changesets"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--config",
                os.path.join(CONFIG_DIR, "valid_with_changeset.cfh"),
                "deploy",
                "MyStackAlias",
            ],
            input="y\n",
        )

        client_mock.create_change_set.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=[],
            ChangeSetName=aws.CHANGESET_NAME,
            ChangeSetType="UPDATE",
        )

        client_mock.execute_change_set.assert_called_once_with(
            StackName="MyStackName",
            ChangeSetName=aws.CHANGESET_NAME,
        )


@mock.patch.object(aws, "stack_exists", return_value=True)
@mock.patch.object(aws, "has_changeset", return_value=False)
def test_update_with_changeset_no_execute(
    mock_aws_has_changeset, mock_aws_stack_exists
):
    """Update an existing stack using changesets but don't execute"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--config",
                os.path.join(CONFIG_DIR, "valid_with_changeset.cfh"),
                "deploy",
                "MyStackAlias",
            ],
            input="n\ny\n",
        )

        client_mock.create_change_set.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=[],
            ChangeSetName=aws.CHANGESET_NAME,
            ChangeSetType="UPDATE",
        )

        client_mock.execute_change_set.assert_not_called()
        client_mock.delete_change_set.assert_not_called()


@mock.patch.object(aws, "stack_exists", return_value=True)
@mock.patch.object(aws, "has_changeset", return_value=False)
def test_update_with_changeset_no_execute_cleanup(
    mock_aws_has_changeset, mock_aws_stack_exists
):
    """Update an existing stack using changesets, don't execute but delete changeset"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--config",
                os.path.join(CONFIG_DIR, "valid_with_changeset.cfh"),
                "deploy",
                "MyStackAlias",
            ],
            input="n\nn\n",
        )

        client_mock.create_change_set.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=[],
            ChangeSetName=aws.CHANGESET_NAME,
            ChangeSetType="UPDATE",
        )

        client_mock.execute_change_set.assert_not_called()
        client_mock.delete_change_set.assert_called_once_with(
            StackName="MyStackName",
            ChangeSetName=aws.CHANGESET_NAME,
        )


@mock.patch.object(aws, "stack_exists", return_value=False)
def test_create_with_capabilities(mock_aws_stack_exists):
    """Create a new stack"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--config",
                os.path.join(
                    CONFIG_DIR, "valid_singlestack_with_multiple_capabilities.cfh"
                ),
                "deploy",
                "MyStackAlias",
            ],
        )

        client_mock.create_stack.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=["CAPABILITY_IAM", "CAPABILITY_NAMED_IAM"],
        )


@mock.patch.object(aws, "stack_exists", return_value=True)
def test_update_with_capabilities(mock_aws_stack_exists):
    """Update an existing stack"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--config",
                os.path.join(
                    CONFIG_DIR, "valid_singlestack_with_multiple_capabilities.cfh"
                ),
                "deploy",
                "MyStackAlias",
            ],
        )

        client_mock.update_stack.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=["CAPABILITY_IAM", "CAPABILITY_NAMED_IAM"],
        )


@mock.patch.object(aws, "stack_exists", return_value=False)
@mock.patch.object(aws, "has_changeset", return_value=False)
def test_create_with_changeset_and_capabilities(
    mock_aws_has_changeset, mock_aws_stack_exists
):
    """Create a new stack using changesets"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--config",
                os.path.join(
                    CONFIG_DIR, "valid_singlestack_capabilities_and_changeset.cfh"
                ),
                "deploy",
                "MyStackAlias",
            ],
            input="y\n",
        )

        client_mock.create_change_set.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=["CAPABILITY_IAM", "CAPABILITY_NAMED_IAM"],
            ChangeSetName=aws.CHANGESET_NAME,
            ChangeSetType="CREATE",
        )

        client_mock.execute_change_set.assert_called_once_with(
            StackName="MyStackName",
            ChangeSetName=aws.CHANGESET_NAME,
        )


@mock.patch.object(aws, "stack_exists", return_value=True)
@mock.patch.dict(os.environ, {"AWS_PROFILE": "MyProfile"})
def test_update_profile_override_env(mock_aws_stack_exists):
    """Update an existing stack"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--config",
                os.path.join(CONFIG_DIR, "valid_multistacks.cfh"),
                "deploy",
                "MyStackAlias",
            ],
        )

        boto3_mock.Session.assert_called_once_with(
            profile_name="MyProfile",
            region_name=None,
        )

        client_mock.update_stack.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=[],
        )


@mock.patch.object(aws, "stack_exists", return_value=True)
@mock.patch.dict(os.environ, {"AWS_PROFILE": "MyProfile"})
def test_update_profile_override_both(mock_aws_stack_exists):
    """Update an existing stack"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--aws-profile",
                "MyOtherProfile",
                "--config",
                os.path.join(CONFIG_DIR, "valid_multistacks.cfh"),
                "deploy",
                "MyStackAlias",
            ],
        )

        boto3_mock.Session.assert_called_once_with(
            profile_name="MyOtherProfile",
            region_name=None,
        )

        client_mock.update_stack.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=[],
        )


@mock.patch.object(aws, "stack_exists", return_value=True)
def test_update_profile_override_cli(mock_aws_stack_exists):
    """Update an existing stack"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--aws-profile",
                "MyOtherProfile",
                "--config",
                os.path.join(CONFIG_DIR, "valid_multistacks.cfh"),
                "deploy",
                "MyStackAlias",
            ],
        )

        boto3_mock.Session.assert_called_once_with(
            profile_name="MyOtherProfile",
            region_name=None,
        )

        client_mock.update_stack.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=[],
        )


@mock.patch.object(aws, "stack_exists", return_value=True)
@mock.patch.dict(os.environ, {"AWS_REGION": "us-east-1"})
def test_update_region_override_env(mock_aws_stack_exists):
    """Update an existing stack"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--config",
                os.path.join(CONFIG_DIR, "valid_multistacks.cfh"),
                "deploy",
                "MyStackAlias",
            ],
        )

        boto3_mock.Session.assert_called_once_with(
            profile_name=None,
            region_name="us-east-1",
        )

        client_mock.update_stack.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=[],
        )


@mock.patch.object(aws, "stack_exists", return_value=True)
@mock.patch.dict(os.environ, {"AWS_REGION": "us-east-1"})
def test_update_region_override_both(mock_aws_stack_exists):
    """Update an existing stack"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--aws-region",
                "us-west-2",
                "--config",
                os.path.join(CONFIG_DIR, "valid_multistacks.cfh"),
                "deploy",
                "MyStackAlias",
            ],
        )

        boto3_mock.Session.assert_called_once_with(
            profile_name=None,
            region_name="us-west-2",
        )

        client_mock.update_stack.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=[],
        )


@mock.patch.object(aws, "stack_exists", return_value=True)
def test_update_region_override_cli(mock_aws_stack_exists):
    """Update an existing stack"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--aws-region",
                "us-west-2",
                "--config",
                os.path.join(CONFIG_DIR, "valid_multistacks.cfh"),
                "deploy",
                "MyStackAlias",
            ],
        )

        boto3_mock.Session.assert_called_once_with(
            profile_name=None,
            region_name="us-west-2",
        )

        client_mock.update_stack.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=[],
        )


@mock.patch.object(aws, "stack_exists", return_value=True)
@mock.patch.dict(os.environ, {"AWS_PROFILE": "MyProfile"})
def test_update_mixed_override(mock_aws_stack_exists):
    """Update an existing stack"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--aws-region",
                "us-west-2",
                "--config",
                os.path.join(CONFIG_DIR, "valid_multistacks.cfh"),
                "deploy",
                "MyStackAlias",
            ],
        )

        boto3_mock.Session.assert_called_once_with(
            profile_name="MyProfile",
            region_name="us-west-2",
        )

        client_mock.update_stack.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=[],
        )


@mock.patch.object(aws, "stack_exists", return_value=True)
def test_update_config_override(mock_aws_stack_exists):
    """Update an existing stack"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--config",
                os.path.join(
                    CONFIG_DIR, "valid_singlestack_with_region_and_profile.cfh"
                ),
                "deploy",
                "MyStackAlias",
            ],
        )

        boto3_mock.Session.assert_called_once_with(
            profile_name="MyCanadianProfile",
            region_name="ca-central-1",
        )

        client_mock.update_stack.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=[],
        )


@mock.patch.object(aws, "stack_exists", return_value=True)
@mock.patch.dict(os.environ, {"AWS_PROFILE": "MyProfile"})
def test_update_config_and_profile_override(mock_aws_stack_exists):
    """Update an existing stack"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--config",
                os.path.join(
                    CONFIG_DIR, "valid_singlestack_with_region_and_profile.cfh"
                ),
                "deploy",
                "MyStackAlias",
            ],
        )

        boto3_mock.Session.assert_called_once_with(
            profile_name="MyProfile",
            region_name="ca-central-1",
        )

        client_mock.update_stack.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=[],
        )


@mock.patch.object(aws, "stack_exists", return_value=True)
@mock.patch.dict(os.environ, {"AWS_PROFILE": "MyProfile"})
def test_update_all_override(mock_aws_stack_exists):
    """Update an existing stack"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--aws-profile",
                "MyExplicitProfile",
                "--config",
                os.path.join(
                    CONFIG_DIR, "valid_singlestack_with_region_and_profile.cfh"
                ),
                "deploy",
                "MyStackAlias",
            ],
        )

        boto3_mock.Session.assert_called_once_with(
            profile_name="MyExplicitProfile",
            region_name="ca-central-1",
        )

        client_mock.update_stack.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=[],
        )
