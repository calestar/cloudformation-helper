#!/usr/bin/env python

"""Tests for `cloudformation_helper` info command."""

import cloudformation_helper

from .helpers import call_cfhelper


def test_info():
    """Not much to test, simply check result from the call"""
    result = call_cfhelper(
        [
            "info",
        ],
    )

    assert result.exit_code == 0
    assert (
        f"cloudformation-helper: {cloudformation_helper.__version__}" in result.output
    )
