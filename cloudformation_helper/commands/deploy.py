"""Command used to deploy/update a cloudformation stack."""

import click


import cloudformation_helper.utils.aws as aws
import cloudformation_helper.utils.formatter as formatter


def update_using_changeset(
    stack_name, stack_file, capabilities, selected_profile, selected_region
):
    click.echo("Creating changeset for existing stack")
    aws.create_changeset(
        stack_name, stack_file, False, capabilities, selected_profile, selected_region
    )
    changeset = aws.get_changeset(stack_name, selected_profile, selected_region)
    formatter.display_changeset(changeset)
    if click.confirm("Execute stack changes? ", default=False):
        aws.execute_changeset(stack_name, False, selected_profile, selected_region)
    else:
        if click.confirm("Keep pending changes? ", default=False):
            click.echo("Aborted")
        else:
            aws.delete_changeset(stack_name, selected_profile, selected_region)


def create_using_changeset(
    stack_name, stack_file, capabilities, selected_profile, selected_region
):
    click.echo("Creating changeset for new stack")
    aws.create_changeset(
        stack_name, stack_file, True, capabilities, selected_profile, selected_region
    )
    changeset = aws.get_changeset(stack_name, selected_profile, selected_region)
    formatter.display_changeset(changeset)
    if click.confirm("Execute stack changes? ", default=False):
        aws.execute_changeset(stack_name, True, selected_profile, selected_region)
    else:
        if click.confirm("Keep pending changes? ", default=False):
            click.echo("Aborted")
        else:
            aws.delete_changeset(stack_name, selected_profile, selected_region)


def deploy_or_update(
    stack_name,
    stack_file,
    use_changesets,
    capabilities,
    selected_profile,
    selected_region,
):
    click.echo(f"Processing {stack_name} using {stack_file}")

    if use_changesets and aws.has_changeset(
        stack_name, selected_profile, selected_region
    ):
        if click.confirm("Stack already has a changeset; delete it? ", default=False):
            click.echo(f"Deleting changeset for stack {stack_name}")
            aws.delete_changeset(stack_name, selected_profile, selected_region)
        else:
            click.echo("Aborted")
            return

    if aws.stack_exists(stack_name, selected_profile, selected_region):
        if use_changesets:
            update_using_changeset(
                stack_name, stack_file, capabilities, selected_profile, selected_region
            )
        else:
            click.echo("Stack already exists, updating it")
            aws.update_stack(
                stack_name, stack_file, capabilities, selected_profile, selected_region
            )
    else:
        if use_changesets:
            create_using_changeset(
                stack_name, stack_file, capabilities, selected_profile, selected_region
            )
        else:
            click.echo("Stack not found, creating new one")
            aws.create_stack(
                stack_name, stack_file, capabilities, selected_profile, selected_region
            )
