"""Command used to deploy/update a cloudformation stack."""

import click


from cloudformation_helper.utils.aws import (
    create_changeset,
    delete_changeset,
    execute_changeset,
    get_changeset,
    has_changeset,
    stack_exists,
    create_stack,
    update_stack,
)
from cloudformation_helper.utils.formatter import (
    display_changeset,
)


def update_using_changeset(stack_name, stack_file):
    click.echo('Creating changeset for existing stack')
    create_changeset(stack_name, stack_file, False)
    changeset = get_changeset(stack_name)
    display_changeset(changeset)
    if click.confirm('Execute stack changes? ', default=False):
        execute_changeset(stack_name, False)
    else:
        if click.confirm('Keep pending changes? ', default=False):
            click.echo('Aborted')
        else:
            delete_changeset(stack_name)


def create_using_changeset(stack_name, stack_file):
    click.echo('Creating changeset for new stack')
    create_changeset(stack_name, stack_file, True)
    changeset = get_changeset(stack_name)
    display_changeset(changeset)
    if click.confirm('Execute stack changes? ', default=False):
        execute_changeset(stack_name, True)
    else:
        if click.confirm('Keep pending changes? ', default=False):
            click.echo('Aborted')
        else:
            delete_changeset(stack_name)


def deploy_or_update(stack_name, stack_file, use_changesets):
    click.echo(f"Processing {stack_name} using {stack_file}")

    if use_changesets and has_changeset(stack_name):
        if click.confirm('Stack already has a changeset; delete it? ', default=False):
            click.echo(f"Deleting changeset for stack {stack_name}")
            delete_changeset(stack_name)
        else:
            click.echo('Aborted')
            return

    if stack_exists(stack_name):
        if use_changesets:
            update_using_changeset(stack_name, stack_file)
        else:
            update_stack(stack_name, stack_file)
    else:
        if use_changesets:
            create_using_changeset(stack_name, stack_file)
        else:
            create_stack(stack_name, stack_file)
