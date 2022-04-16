"""AaC Plugin implementation module for the material_model plugin."""
# NOTE: It is safe to edit this file.
# This file is only initially generated by the aac gen-plugin, and it won't be overwritten if the file already exists.

import os

from aac.lang.definition_helpers import get_models_by_type, convert_parsed_definitions_to_dict_definition
from aac.plugins.plugin_execution import (
    PluginExecutionResult,
    PluginExecutionStatusCode,
    plugin_result,
)
from aac.validate import validated_source

plugin_name = "material_model"


def gen_bom(architecture_file: str, output_directory: str) -> PluginExecutionResult:
    """
    Generate a Bill of Material from Arch-as-Code material models.

    Args:
        architecture_file (str): The yaml file containing the material models to generate the BOM.
        output_directory (str): The directory to write the generated BOM to.
    """
    def _process_deployment(deployment: dict, context: str) -> list(dict()):
        return [{"not": "real"}]

    def _process_assembly(assembly: dict, context: str) -> list(dict()):
        return [{"not": "real"}]

    def to_bom_csv(architecture_file: str, output_directory: str) -> str:
        architecture_file_path = os.path.abspath(architecture_file)
        file_name, _ = os.path.splitext(os.path.basename(architecture_file_path))

        with validated_source(architecture_file_path) as result:
            definitions_as_dict = convert_parsed_definitions_to_dict_definition(result.definitions)
            # TODO use the dict to generate BOM line items

            # TODO need to add in the design context by looking at the deployment/assembly structure and adding fields
            #      note:  this does not have to be of consistent depth for everything, so may need blanks in some cases
            #      note:  for now, let's just aggregate it into a single context field for simplicity
            bom_header = ["make", "model", "description", "unit_cost", "quantity", "total_cost", "location", "need_date", "context"]

            # Initial algorithm thoughts
            # 1) get a list of the deployments
            deployment_types = get_models_by_type(models, "deployment")

            # 2) remove any deployment listed as a sub-deployment in another deployment to get the root deployment(s)
            deployment_names = list(deployment_types.keys())
            for root_deployment_name in deployment_types.keys():
                # TODO figure out how to get
                continue
            # 3) loop through the root deployment list, keeping track of context by appending deployment names
            # 4) for each deployment, process assemblies recursively in a depth first manner
            # 5) for each part in an assembly, generate a bom_item dict entry (be careful about quantities in assembly and part refs)

            if output_directory:
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)

                output_file_path = os.path.join(output_directory, f"{file_name}.csv")
                with open(output_file_path, "w") as out_file:
                    out_file.write(bom_csv)
                    return f"Wrote BOM to {output_file_path}."

            return f"File: {architecture_file_path}\n{bom_csv}\n"

    status = PluginExecutionStatusCode.SUCCESS
    messages = []
    for arch_file in architecture_files:
        with plugin_result(plugin_name, to_bom_csv, arch_file, output_directory) as result:
            messages += result.messages
            if not result.is_success():
                status = result.status_code

    return PluginExecutionResult(plugin_name, status, messages)
