"""Command used to display information about this tool."""

import platform
import os
import sys

import click

import cloudformation_helper


def displayInfo(config):
    click.echo(f"Platform: {platform.platform()}")
    click.echo(f'Python version: {sys.version.replace(os.linesep, "")}')
    click.echo(
        f"{os.linesep}cloudformation-helper: {cloudformation_helper.__version__}"
    )
