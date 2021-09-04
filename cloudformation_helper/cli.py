"""Console script for cloudformation_helper."""
import sys
import click

import cloudformation_helper.commands.deploy as deployModule
import cloudformation_helper.commands.info as infoModule
from cloudformation_helper.utils.config import read_config


@click.group()
def cfhelper():
    pass


@cfhelper.group()
@click.option("--config", default="stacks.cfh")
@click.option("--aws-profile", envvar="AWS_PROFILE")
@click.option("--aws-region", envvar="AWS_REGION")
@click.pass_context
def stack(ctx, config, aws_profile, aws_region):
    ctx.obj = read_config(config, aws_profile, aws_region)


@stack.command()
@click.argument("stack_alias")
@click.pass_obj
def deploy(config, stack_alias):
    (
        stack_name,
        stack_file,
        use_changesets,
        capabilities,
        selected_profile,
        selected_region,
    ) = config.get_stack(stack_alias)
    deployModule.deploy_or_update(
        stack_name,
        stack_file,
        use_changesets,
        capabilities,
        selected_profile,
        selected_region,
    )


@cfhelper.command()
@click.pass_obj
def info(config):
    infoModule.displayInfo(config)


def run():
    sys.exit(cfhelper(auto_envvar_prefix="CFHELPER"))  # pragma: no cover


if __name__ == "__main__":
    run()
