#!/usr/bin/env python

"""Tests for `cloudformation_helper` package."""

import mock
import os
import pytest
import yaml

from click.testing import CliRunner

from cloudformation_helper import cli
from cloudformation_helper.utils import aws
from cloudformation_helper.commands import deploy

HERE = os.path.dirname(os.path.realpath(__file__))


def test_config_file_does_not_exist():
    """Pass a file path that does not exist"""
    runner = CliRunner()
    with pytest.raises(FileNotFoundError, match=r"No such file or directory"):
        runner.invoke(cli.cfhelper, ['--config', 'not-a-valid-file', 'deploy'], catch_exceptions=False)


def test_wrong_config_format():
    """Pass a file that has the wrong format"""
    runner = CliRunner()
    with pytest.raises(yaml.parser.ParserError):
        runner.invoke(cli.cfhelper, ['--config', os.path.join(HERE, 'data', 'config', 'not_valid_yaml.cfh'), 'deploy'], catch_exceptions=False)


@mock.patch('cloudformation_helper.utils.aws.boto3')
@mock.patch.object(aws, 'stack_exists', return_value=False)
def test_valid_multistacks_config(mock_aws, mock_boto3):
    """Pass a file that contains multiple valid stacks"""
    runner = CliRunner()

    result = runner.invoke(cli.cfhelper, ['--config', os.path.join(HERE, 'data', 'config', 'valid_multistacks.cfh'), 'deploy', 'MyStackAlias'], catch_exceptions=False)
    mock_boto3.client.return_value.create_stack.assert_called_once_with(StackName='MyStackName', TemplateBody=mock.ANY, Capabilities=mock.ANY)
