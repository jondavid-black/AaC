"""AaC Plugin implementation module for the report plugin."""
# NOTE: It is safe to edit this file.
# This file is only initially generated by the aac gen-plugin, and it won't be overwritten if the file already exists.

from aac.plugins.plugin_execution import PluginExecutionResult, plugin_result
from aac.validate import validated_source
from aac.lang.definition_helpers import get_definitions_by_root_key
from aac.lang.definitions.definition import Definition
from aac.lang.definition_helpers import convert_parsed_definitions_to_dict_definition, get_definitions_by_source_uri

import yaml
import csv
import io

plugin_name = "report"


def report(report_definition_file: str, architecture_file: str, output_file: str) -> PluginExecutionResult:
    """
    Generate YAML output from an Arch-as-Code report definition.

    Args:
        report_definition_file (str): The yaml file containing the report model.
        architecture_file (str): The yaml file containing the AaC model to interrogate.
        output_file (str): The file to write the generated YAML report. (Optional)
    """
    def _gen_yaml_report():
        ret_val = ""
        report_content_list = _generate_report(report_definition_file, architecture_file)
        for report in report_content_list:
            yaml_content = yaml.dump(report, default_flow_style=False)
            if len(ret_val) > 0:
                ret_val += "---\n"
            ret_val += yaml_content

        # TODO if output_file is provided, write ret_val to file.  Should we also provide content for cli output?
        print(f"YAML = {yaml_content}")
        return yaml_content

    with plugin_result(plugin_name, _gen_yaml_report) as result:
        return result


def report_csv(report_definition_file: str, architecture_file: str, output_file: str) -> PluginExecutionResult:
    """
    Generate CSV output from an Arch-as-Code report definition.

    Args:
        report_definition_file (str): The yaml file containing the report model.
        architecture_file (str): The yaml file containing the AaC model to interrogate.
        output_file (str): The file to write the generated CSV report. (Optional)
    """
    def _gen_csv_report():
        ret_val = ""
        report_content_list = _generate_report(report_definition_file, architecture_file)
        for report in report_content_list:
            # convert report content to csv
            field_names = []
            for cont in report["content"]:
                for fn in cont:
                    field_names.append(fn)
            header_names = set(field_names)
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=header_names, delimiter=',')
            writer.writeheader()
            writer.writerows(report["content"])

            csv_report = output.getvalue()

            if len(ret_val) > 0:
                ret_val += "\n\n"
            ret_val += csv_report

            # TODO if output_file is provided, write ret_val to file.  Should we also provide content for cli output?

        return ret_val

    with plugin_result(plugin_name, _gen_csv_report) as result:
        return result


def _get_report_field_content(definition: Definition, reference: str) -> str:
    return "nothing yet"


def _generate_report(report_file: str, architecture_file: str) -> dict:
    print(f"_generate_report processing {architecture_file}")

    report_defs = []
    report_results = []
    with validated_source(report_file) as report_result:
        # get reports defined in the report file
        report_defs = get_definitions_by_root_key("report", get_definitions_by_source_uri(report_file, report_result.definitions))

        print(f"report_defs = {[entry.name for entry in report_defs]}")

        for report_def in report_defs:  # TODO fix magic string
            report_result = {}
            fields = report_def.get_fields()

            # get report result metadata
            report_result["title"] = fields["name"]  # TODO fix magic string
            report_result["description"] = fields["description"]  # TODO fix magic string

            # get data content
            content = []

            for get_me in fields["data"]:
                column_name = get_me["name"]
                column_desc = get_me["description"]
                column_value = get_me["source"]  # TODO fix magic string)

            report_result["content"] = content

            report_results.append(report_result)

    with validated_source(architecture_file) as validation_result:
        definitions_as_dictionary = convert_parsed_definitions_to_dict_definition(validation_result.definitions)

        for report_def in get_definitions_by_root_key("report", validation_result.definitions):  # TODO fix magic string

            report_result = {}
            fields = report_def.get_fields()

            # get report result metadata
            report_result["title"] = fields["name"]  # TODO fix magic string
            report_result["description"] = fields["description"]  # TODO fix magic string
            # get data types to extract report content from
            source_types = []
            things_to_get = fields["retrieve"]  # TODO fix magic string
            for get_me in things_to_get:
                found_type = get_me["source_type"]  # TODO fix magic string
                source_types.append(found_type)
            source_types = set(source_types)

            # assemble content data
            content_source = []  # list of dicts for the source types
            if len(source_types) == 1:
                # this is the simple case we'll start with
                root_key = list(source_types)[0]
                # get parsed dicts that match the root key
                for name in definitions_as_dictionary:
                    if root_key in definitions_as_dictionary[name]:
                        content_source.append(definitions_as_dictionary[name])
            else:
                # don't have this completely worked out yet
                raise NotImplementedError("complex reports not implemented yet")

            # populate report content
            content = []
            for content_source_item in content_source:
                content_item = {}
                for get_item in things_to_get:
                    report_field_name = get_item["name"]
                    report_field_value = content_source_item[get_item["source_type"]][get_item["source_field_name"]]

                    content_item[report_field_name] = report_field_value
                content.append(content_item)
            report_result["content"] = content

            reports.append(report_result)
    return reports
