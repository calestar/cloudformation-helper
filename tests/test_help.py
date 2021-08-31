#!/usr/bin/env python

"""Tests for `cloudformation_helper` package."""

from .helpers import call_cfhelper


def test_get_help():
    """Test the CLI."""
    result = call_cfhelper([])
    assert result.exit_code == 0
    assert "Usage: cfhelper [OPTIONS] COMMAND [ARGS]..." in result.output
    help_result = call_cfhelper(["--help"])
    assert help_result.exit_code == 0
    assert "Usage: cfhelper [OPTIONS] COMMAND [ARGS]..." in help_result.output
