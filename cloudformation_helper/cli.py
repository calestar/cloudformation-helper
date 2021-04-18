"""Console script for cloudformation_helper."""
import sys
import click

from cloudformation_helper.commands.deploy import deploy_or_update
from cloudformation_helper.utils.config import read_config


@click.group()
@click.option('--config', default='stacks.cfh')
@click.pass_context
def cfhelper(ctx, config):
    ctx.obj = read_config(config)


@cfhelper.command()
@click.argument("args", nargs=-1)
@click.pass_obj
def deploy(config, args):
    if len(args) == 1:
        if not config:
            raise Exception('Could not find configuration file')
        config_name, = args
        stack_name, stack_file, use_changesets = config.get_stack(config_name)
        deploy_or_update(stack_name, stack_file, use_changesets)
    elif len(args) == 2:
        stack_name, stack_file = args
        deploy_or_update(stack_name, stack_file, True)
    else:
        click.echo('Missing arguments')


def run():
    sys.exit(cfhelper(auto_envvar_prefix='CFHELPER'))  # pragma: no cover


if __name__ == "__main__":
    run()
