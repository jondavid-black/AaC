"""Generated AaC Plugin hookimpls module for the aac-gen-protobuf plugin."""
# WARNING - DO NOT EDIT - YOUR CHANGES WILL NOT BE PROTECTED
# This file is auto-generated by the aac gen-plugin and may be overwritten.

from importlib import resources

from aac.AacCommand import AacCommand, AacCommandArgument
from aac.plugins import hookimpl
from aac.plugins.gen_plugin.gen_plugin_impl import generate_plugin


@hookimpl
def get_commands() -> list[AacCommand]:
    """
    Returns the gen-plugin command type to the plugin infrastructure.

    Returns:
        A list of AacCommands
    """

    command_arguments = [
        AacCommandArgument(
            "architecture_file",
            "The yaml file containing the AaC DSL of the plugin architecture.",
        )
    ]

    plugin_commands = [
        AacCommand(
            "gen-plugin",
            "Generates an AaC plugin from an AaC model of the plugin",
            generate_plugin,
            command_arguments,
        )
    ]

    return plugin_commands


@hookimpl
def get_base_model_extensions() -> str:
    """
    Returns the CommandBehaviorType modeling language extension to the plugin infrastructure.

    Returns:
        string representing yaml extensions and data definitions employed by the plugin
    """
    with resources.open_text(__package__, "gen_plugin.yaml") as plugin_model_file:
        return plugin_model_file.read()

