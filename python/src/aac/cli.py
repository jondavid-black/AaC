"""The command line processor for aac."""
import argparse
import inspect
import itertools
import sys
from typing import Callable

from pluggy import PluginManager

from aac import parser, plugins
from aac.AacCommand import AacCommand, AacCommandArgument
from aac.plugins.plugin_execution import (
    PluginExecutionResult,
    plugin_result,
)
from aac.spec.core import get_aac_spec_as_yaml
from aac.validator import validation


def run_cli():
    """
    Run the specified AaC command.

    This method parses the command line and performs the requested user command or outputs usage.
    """
    plugin_manager = plugins.get_plugin_manager()

    arg_parser, aac_plugin_commands = _setup_arg_parser(plugin_manager)

    args = arg_parser.parse_args()

    for command in aac_plugin_commands:
        if args.command == command.name:

            keyword_args = {}
            args_dict = vars(args)

            # Leverage inspect here to make sure that the arg names we're trying to access are
            # sourced from the target function itself
            parameters = inspect.signature(command.callback).parameters.keys()
            for argument in parameters:
                keyword_args[argument] = args_dict[argument]

            result = command.callback(**keyword_args)
            print(f"{result.name}: {result.status_code.name.lower()}\n\n" + "\n".join(result.messages))
            if not result.is_success():
                sys.exit(result.status_code.value)


def _validate_cmd(model_file: str) -> PluginExecutionResult:
    """Run the built-in validate command."""

    def validate_model() -> str:
        with validation(parser.parse_file, model_file):
            return f"{model_file} is valid"

    with plugin_result("validate", validate_model) as result:
        return result


def _core_spec_cmd() -> PluginExecutionResult:
    """Run the built-in aac-core-spec command."""
    with plugin_result("aac-core-spec", get_aac_spec_as_yaml) as result:
        return result


def _setup_arg_parser(
    plugin_manager: PluginManager,
) -> tuple[argparse.ArgumentParser, list[Callable]]:

    def help_formatter(prog):
        return argparse.HelpFormatter(prog, max_help_position=30)

    arg_parser = argparse.ArgumentParser(formatter_class=help_formatter)
    command_parser = arg_parser.add_subparsers(dest="command")

    # Built-in commands
    aac_commands = [
        # Temporarily disabled.
        # AacCommand(
        #     "ui",
        #     "Run the AaC Graphical User Interface",
        #     ui.run_ui,
        # ),
        AacCommand(
            "validate",
            "Ensures the AaC yaml is valid per the AaC core spec",
            _validate_cmd,
            [AacCommandArgument("model_file", "The path to the AaC model yaml file to validate")],
        ),
        AacCommand(
            "aac-core-spec",
            "Prints the AaC model describing core AaC data types and enumerations",
            _core_spec_cmd,
        ),
    ]

    results = plugin_manager.hook.get_commands()
    aac_and_plugin_commands = aac_commands + list(itertools.chain(*results))

    for command in aac_and_plugin_commands:
        command_subparser = command_parser.add_parser(command.name, help=command.description)

        for argument in command.arguments:
            command_subparser.add_argument(
                argument.name, help=argument.description, nargs=argument.number_of_arguments, choices=argument.choices
            )

    return arg_parser, aac_and_plugin_commands
