"""The validate plugin module."""
# NOTE: It is safe to edit this file.
# This file is only initially generated by aac gen-plugin, and it won't be overwritten if the file already exists.

from aac.plugins import hookimpl
from aac.cli.aac_command import AacCommand, AacCommandArgument
from aac.cli.builtin_commands.validate.validate_impl import validate


@hookimpl
def get_commands() -> list[AacCommand]:
    """
    Return a list of AacCommands provided by the plugin to register for use.

    This function is automatically generated. Do not edit.

    Returns:
        list of AacCommands
    """
    validate_arguments = [
        AacCommandArgument("architecture_file", "The path to the AaC file to be validated.", data_type="file"),
    ]

    plugin_commands = [
        AacCommand(
            "validate",
            "Validate the AaC definition file.",
            validate,
            validate_arguments
        ),
    ]

    return plugin_commands
