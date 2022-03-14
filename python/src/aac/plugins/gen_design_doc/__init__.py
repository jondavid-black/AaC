"""Generated AaC Plugin hookimpls module for the aac-gen-design-doc plugin."""
# WARNING - DO NOT EDIT - YOUR CHANGES WILL NOT BE PROTECTED
# This file is auto-generated by the aac gen-plugin and may be overwritten.

from aac.AacCommand import AacCommand, AacCommandArgument
from aac.package_resources import get_resource_file_contents
from aac.plugins import hookimpl
from aac.plugins.gen_design_doc.gen_design_doc_impl import gen_design_doc


@hookimpl
def get_commands() -> list[AacCommand]:
    """
    Return a list of AacCommands provided by the plugin to register for use.

    This function is automatically generated. Do not edit.

    Returns:
        list of AacCommands
    """
    gen_design_doc_arguments = [
        AacCommandArgument(
            "architecture_files",
            "A comma-separated list of yaml file(s) containing the modeled system for which to generate the System Design document.",
        ),
        AacCommandArgument(
            "output_directory",
            "The directory to which the System Design document will be written.",
        ),
        AacCommandArgument(
            "--template_file",
            "The name of the Jinja2 template file to use for generating the document. (optional)",
        ),
    ]

    plugin_commands = [
        AacCommand(
            "gen-design-doc",
            "Generate a System Design Document from Architecture-as-Code models.",
            gen_design_doc,
            gen_design_doc_arguments,
        ),
    ]

    return plugin_commands


@hookimpl
def get_plugin_aac_definitions() -> str:
    """
    Return the plugins Aac definitions.

    Returns:
         string representing yaml extensions and data definitions employed by the plugin
    """

    return get_resource_file_contents(__package__, "gen_design_doc.yaml")
