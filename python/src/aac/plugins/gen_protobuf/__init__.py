"""Generated AaC Plugin hookimpls module for the aac-gen-protobuf plugin."""
# WARNING - DO NOT EDIT - YOUR CHANGES WILL NOT BE PROTECTED
# This file is auto-generated by the aac gen-plugin and may be overwritten.

from aac.AacCommand import AacCommand, AacCommandArgument
from aac.package_resources import get_resource_file_contents
from aac.plugins import hookimpl
from aac.plugins.gen_protobuf.gen_protobuf_impl import gen_protobuf


@hookimpl
def get_commands() -> list[AacCommand]:
    """
    Return a list of AacCommands provided by the plugin to register for use.

    This function is automatically generated. Do not edit.

    Returns:
        list of AacCommands
    """
    gen_protobuf_arguments = [
        AacCommandArgument(
            "architecture_file",
            "The yaml file containing the data models to generate as Protobuf messages.",
        ),
        AacCommandArgument(
            "output_directory", "The directory to write the generated Protobuf messages to."
        ),
    ]

    plugin_commands = [
        AacCommand(
            "gen-protobuf",
            "Generate protobuf messages from Arch-as-Code models.",
            gen_protobuf,
            gen_protobuf_arguments,
        ),
    ]

    return plugin_commands


@hookimpl
def get_plugin_aac_definitionss() -> str:
    """
    Returns the CommandBehaviorType modeling language extension to the plugin infrastructure.

    Returns:
        string representing yaml extensions and data definitions employed by the plugin
    """
    return get_resource_file_contents(__package__, "gen_protobuf.yaml")
