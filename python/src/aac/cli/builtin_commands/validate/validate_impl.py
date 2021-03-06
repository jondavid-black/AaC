"""AaC Plugin implementation module for the validate plugin."""
# NOTE: It is safe to edit this file.
# This file is only initially generated by the aac gen-plugin, and it won't be overwritten if the file already exists.

from aac.plugins.plugin_execution import PluginExecutionResult, plugin_result
from aac.validate import validated_source

plugin_name = "validate"


def validate(architecture_file: str) -> PluginExecutionResult:
    """
    Validate the AaC definition file.

    Args:
        architecture_file (str): The path to the AaC file to be validated.
    """

    def validate_model() -> str:
        with validated_source(architecture_file):
            return f"{architecture_file} is valid"

    with plugin_result(plugin_name, validate_model) as result:
        return result
