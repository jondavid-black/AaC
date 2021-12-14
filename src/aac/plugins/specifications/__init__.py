"""Generated AaC Plugin hookimpls module for the aac-spec plugin."""
# WARNING - DO NOT EDIT - YOUR CHANGES WILL NOT BE PROTECTED
# This file is auto-generated by the aac gen-plugin and may be overwritten.

from importlib import resources

from aac.AacCommand import AacCommand, AacCommandArgument
from aac.plugins import hookimpl
from aac.plugins.specifications.specifications_impl import spec_validate


@hookimpl
def get_commands() -> list[AacCommand]:
    """
    Return a list of AacCommands provided by the plugin to register for use.

    This function is automatically generated. Do not edit.

    Returns:
        list of AacCommands
    """
    spec_validate_arguments = [
        AacCommandArgument("architecture_file", "The file to validate for spec cross-references."),
    ]

    plugin_commands = [
        AacCommand(
            "spec-validate",
            "Validates spec traces within the AaC model.",
            spec_validate,
            spec_validate_arguments
        ),
    ]

    return plugin_commands


@hookimpl
def get_base_model_extensions() -> str:
    """
    Return data and ext definitions to apply to the AaC base.

    Returns:
        string representing yaml extensions and data definitions employed by the plugin
    """
    with resources.open_text(__package__, "specifications.yaml") as plugin_model_file:
        return plugin_model_file.read()
