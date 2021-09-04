#!/usr/bin/env python

"""Tests for bad calls to deploy."""

import pytest
import mock
import os

from cloudformation_helper.utils import aws

from ..helpers import call_cfhelper, cfhelper_mocks

HERE = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIR = os.path.join(HERE, "..", "data", "config")


@mock.patch.object(aws, "stack_exists", return_value=False)
def test_stack_wrong_name(mock_aws_stack_exists):
    """Create a new stack"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        with pytest.raises(
            Exception, match=r"Could not find stack config named 'IamNotAStack'"
        ):
            call_cfhelper(
                [
                    "stack",
                    "--config",
                    os.path.join(CONFIG_DIR, "valid_multistacks.cfh"),
                    "deploy",
                    "IamNotAStack",
                ],
            )


@mock.patch.object(aws, "stack_exists", return_value=True)
@mock.patch.object(aws, "has_changeset", return_value=True)
def test_update_with_existing_changeset(mock_aws_has_changeset, mock_aws_stack_exists):
    """Try to update an existing changeset; but a changeset already exists, bail out"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--config",
                os.path.join(CONFIG_DIR, "valid_with_changeset.cfh"),
                "deploy",
                "MyStackAlias",
            ],
            input="n\n",
        )

        client_mock.create_change_set.assert_not_called()
        client_mock.execute_change_set.assert_not_called()


@mock.patch.object(aws, "stack_exists", return_value=True)
@mock.patch.object(aws, "has_changeset", return_value=True)
def test_update_with_existing_changeset_and_continue(
    mock_aws_has_changeset, mock_aws_stack_exists
):
    """Try to update an existing changeset; but a changeset already exists, delete it and continue"""
    with cfhelper_mocks() as (boto3_mock, session_mock, client_mock):
        call_cfhelper(
            [
                "stack",
                "--config",
                os.path.join(CONFIG_DIR, "valid_with_changeset.cfh"),
                "deploy",
                "MyStackAlias",
            ],
            input="y\ny\n",
        )

        client_mock.create_change_set.assert_called_once_with(
            StackName="MyStackName",
            TemplateBody=mock.ANY,
            Capabilities=mock.ANY,
            ChangeSetName=aws.CHANGESET_NAME,
            ChangeSetType="UPDATE",
        )

        client_mock.delete_change_set.assert_called_once_with(
            StackName="MyStackName", ChangeSetName=aws.CHANGESET_NAME
        )
        client_mock.execute_change_set.assert_called_once_with(
            StackName="MyStackName", ChangeSetName=aws.CHANGESET_NAME
        )
