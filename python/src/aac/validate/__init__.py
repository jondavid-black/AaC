"""Contains classes and functionality to support validating AaC architecture files."""

from aac.validate._validator_plugin import ValidatorPlugin
from aac.validate._validation_error import ValidationError
from aac.validate._validation_result import ValidationResult
from aac.validate._validate import validate_definitions
from aac.validate._collect_validators import get_applicable_validators_for_definition

__all__ = (
    ValidationError.__name__,
    ValidationResult.__name__,
    ValidatorPlugin.__name__,
    validate_definitions.__name__,
    get_applicable_validators_for_definition.__name__,
)