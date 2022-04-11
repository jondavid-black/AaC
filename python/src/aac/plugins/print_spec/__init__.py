"""The aac-core-spec plugin module."""
# NOTE: It is safe to edit this file.
# This file is only initially generated by aac gen-plugin, and it won't be overwritten if the file already exists.

from aac.cli.aac_command import AacCommand
from aac.plugins import hookimpl
from aac.plugins.print_spec.print_spec_impl import print_spec


@hookimpl
def get_commands() -> list[AacCommand]:
    """
    Return a list of AacCommands provided by the plugin to register for use.

    This function is automatically generated. Do not edit.

    Returns:
        list of AacCommands
    """

    plugin_commands = [
        AacCommand(
            "aac-core-spec",
            "Print the AaC model describing core AaC data types and enumerations.",
            print_spec
        ),
    ]

    return plugin_commands
