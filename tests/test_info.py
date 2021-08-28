#!/usr/bin/env python

"""Tests for `cloudformation_helper` info command."""

from click.testing import CliRunner

from cloudformation_helper import cli


def test_info():
    """Not much to test, simply check result from the call"""
    runner = CliRunner()

    runner.invoke(
        cli.cfhelper,
        [
            "info",
        ],
        catch_exceptions=False,
    )
