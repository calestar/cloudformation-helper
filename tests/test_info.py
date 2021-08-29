#!/usr/bin/env python

"""Tests for `cloudformation_helper` info command."""

from click.testing import CliRunner

import cloudformation_helper
from cloudformation_helper import cli


def test_info():
    """Not much to test, simply check result from the call"""
    runner = CliRunner()

    result = runner.invoke(
        cli.cfhelper,
        [
            "info",
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert (
        f"cloudformation-helper: {cloudformation_helper.__version__}" in result.output
    )
