#!/usr/bin/env python

"""Tests for `cloudformation_helper` config management."""

import mock
import os
import pytest
import yaml

from cloudformation_helper.commands import deploy

from .helpers import call_cfhelper

HERE = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIR = os.path.join(HERE, "data", "config")


def test_config_file_does_not_exist():
    """Pass a file path that does not exist"""
    with pytest.raises(FileNotFoundError, match=r"No such file or directory"):
        call_cfhelper(
            ["stack", "--config", "not-a-valid-file", "deploy"],
        )


def test_wrong_config_format():
    """Pass a file that has the wrong format"""
    with pytest.raises(yaml.parser.ParserError):
        call_cfhelper(
            [
                "stack",
                "--config",
                os.path.join(CONFIG_DIR, "not_valid_yaml.cfh"),
                "deploy",
            ],
        )


@mock.patch.object(deploy, "deploy_or_update")
def test_valid_multistacks_config(mock_deploy):
    """Pass a file that contains multiple valid stacks"""
    call_cfhelper(
        [
            "stack",
            "--config",
            os.path.join(CONFIG_DIR, "valid_multistacks.cfh"),
            "deploy",
            "MyStackAlias",
        ],
    )
    mock_deploy.assert_called_once_with(
        "MyStackName", mock.ANY, mock.ANY, mock.ANY, None, None
    )


@mock.patch.object(deploy, "deploy_or_update")
def test_valid_singlestack_config(mock_deploy):
    """Pass a file that contains a single valid stacks"""
    call_cfhelper(
        [
            "stack",
            "--config",
            os.path.join(CONFIG_DIR, "valid_singlestack.cfh"),
            "deploy",
            "MyStackAlias",
        ],
    )
    mock_deploy.assert_called_once_with(
        "MyStackName", mock.ANY, False, set(), None, None
    )


@mock.patch.object(deploy, "deploy_or_update")
def test_bad_capability(mock_deploy):
    """Pass a file that contains an invalid capability"""
    with pytest.raises(Exception):
        call_cfhelper(
            [
                "stack",
                "--config",
                os.path.join(CONFIG_DIR, "valid_singlestack_bad_capability.cfh"),
                "deploy",
                "MyStackAlias",
            ],
        )

    mock_deploy.assert_not_called()


@mock.patch.object(deploy, "deploy_or_update")
def test_with_capability(mock_deploy):
    """Pass a file that contains one valid capability"""
    call_cfhelper(
        [
            "stack",
            "--config",
            os.path.join(CONFIG_DIR, "valid_singlestack_with_capability.cfh"),
            "deploy",
            "MyStackAlias",
        ],
    )

    mock_deploy.assert_called_once_with(
        "MyStackName", mock.ANY, False, {"CAPABILITY_IAM"}, None, None
    )


@mock.patch.object(deploy, "deploy_or_update")
def test_with_multiple_capabilities(mock_deploy):
    """Pass a file that contains multiple valid capabilities"""
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

    mock_deploy.assert_called_once_with(
        "MyStackName",
        mock.ANY,
        False,
        {"CAPABILITY_IAM", "CAPABILITY_NAMED_IAM"},
        None,
        None,
    )
