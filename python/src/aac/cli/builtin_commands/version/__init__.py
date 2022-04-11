"""The version plugin module."""
# NOTE: It is safe to edit this file.
# This file is only initially generated by aac gen-plugin, and it won't be overwritten if the file already exists.

from aac.plugins import hookimpl
from aac.cli.aac_command import AacCommand
from aac.cli.builtin_commands.version.version_impl import version


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
            "version",
            "Print the AaC package version.",
            version
        ),
    ]

    return plugin_commands
