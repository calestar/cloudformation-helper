"""Helpers to interact with the config file."""
import os

import yaml


class Config:
    def __init__(self, root, raw_config):
        self.root = root
        self.raw_config = raw_config

    def get_stack(self, name):
        stack = self.raw_config.get(name)
        if stack is None:
            raise Exception(f"Could not find stack config named '{name}'")

        stack_name = stack.get('stack')
        stack_file = stack.get('file')
        use_changesets = stack.get('use_changesets')

        if not os.path.isabs(stack_file):
            stack_file = os.path.join(self.root, stack_file)

        if not os.path.exists(stack_file):
            raise Exception(f"Could not find stack file: '{stack_file}'")

        return stack_name, stack_file, use_changesets


def read_config(config_file_name):
    config_file = os.path.abspath(config_file_name)
    root = os.path.dirname(config_file)

    try:
        with open(config_file, 'r') as stream:
            config = yaml.safe_load(stream)
            return Config(root, config)
    except Exception:
        return None
