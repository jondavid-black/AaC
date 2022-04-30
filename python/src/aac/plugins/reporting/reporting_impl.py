"""AaC Plugin implementation module for the reporting plugin."""
# NOTE: It is safe to edit this file.
# This file is only initially generated by the aac gen-plugin, and it won't be overwritten if the file already exists.

from aac.plugins.plugin_execution import PluginExecutionResult, plugin_result

plugin_name = "reporting"


def report(architecture_file: str, output_file: str) -> PluginExecutionResult:
    """
    Generate YAML output from an Arch-as-Code report definition.

    Args:
        architecture_file (str): The yaml file containing the report model.
        output_file (str): The file to write the generated YAML report.
    """
    # TODO add implementation here
    def _implement_and_rename_me():
        raise NotImplementedError("report is not implemented.")

    with plugin_result(plugin_name, _implement_and_rename_me) as result:
        return result


def report_csv(architecture_file: str, output_file: str) -> PluginExecutionResult:
    """
    Generate CSV output from an Arch-as-Code report definition.

    Args:
        architecture_file (str): The yaml file containing the report model.
        output_file (str): The file to write the generated CSV report.
    """
    # TODO add implementation here
    def _implement_and_rename_me():
        raise NotImplementedError("report_csv is not implemented.")

    with plugin_result(plugin_name, _implement_and_rename_me) as result:
        return result