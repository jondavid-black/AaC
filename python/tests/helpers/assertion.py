"""Provide some general unit test assertion helpers to address recurring and duplicated testing patterns."""
from aac.plugins.plugin_execution import (
    PluginExecutionResult,
    PluginExecutionStatusCode
)
from aac.plugins.validators import ValidatorResult


def assert_plugin_success(plugin_result: PluginExecutionResult):
    """
    Asserts that the plugin result indicates a plugin failure status.

    In the event that the plugin status does not match the expected value,
    print the error messages in the assertion message.
    """
    _assert_plugin_state(plugin_result, PluginExecutionStatusCode.SUCCESS)


def assert_plugin_failure(plugin_result: PluginExecutionResult):
    """
    Asserts that the plugin result indicates a plugin failure status.

    In the event that the plugin status does not match the expected value,
    print the error messages in the assertion message.
    """
    _assert_plugin_state(plugin_result, PluginExecutionStatusCode.PLUGIN_FAILURE)


def assert_general_failure(plugin_result: PluginExecutionResult):
    """
    Asserts that the plugin result indicates a general failure status.

    In the event that the plugin status does not match the expected value,
    print the error messages in the assertion message.
    """
    _assert_plugin_state(plugin_result, PluginExecutionStatusCode.GENERAL_FAILURE)


def assert_validation_failure(plugin_result: PluginExecutionResult):
    """
    Asserts that the plugin result indicates a validation failure status.

    In the event that the plugin status does not match the expected value,
    print the error messages in the assertion message.
    """
    _assert_plugin_state(plugin_result, PluginExecutionStatusCode.VALIDATION_FAILURE)


def _assert_plugin_state(plugin_result: PluginExecutionResult, code: PluginExecutionStatusCode):
    if plugin_result.status_code != code:
        raise AssertionError(f"PluginResult did not return {code} as expected. Messages:\n{plugin_result.messages}")


def assert_validator_result_failure(validator_result: ValidatorResult, *expected_error_message_contents):
    """Asserts that the validator result indicates a failure status and contains the defined error message content."""
    if validator_result.is_valid:
        raise AssertionError(f"ValidatorResult did not return as unsuccessful status as expected. Messages:\n{validator_result.messages}")

    error_message = validator_result.get_messages_as_string()
    for error_string in expected_error_message_contents:
        if error_string not in error_message:
            raise AssertionError(f"ValidatorResult does not contain expected error message content '{error_string}'. Error message:\n{error_message}")


def assert_validator_result_success(validator_result: ValidatorResult):
    """Asserts that the validator result indicates a successful status."""
    if not validator_result.is_valid:
        raise AssertionError(f"ValidatorResult did not return as successful status as expected. Messages:\n{validator_result.messages}")
