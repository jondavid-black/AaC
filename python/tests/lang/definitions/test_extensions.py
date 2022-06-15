from unittest import TestCase
from aac.lang.active_context_lifecycle_manager import get_initialized_language_context
from aac.lang.definitions.extensions import apply_extension_to_definition, remove_extension_from_definition
from aac.plugins.validators.required_fields import REQUIRED_FIELDS_VALIDATION_STRING

from tests.helpers.parsed_definitions import (
    create_schema_definition,
    create_schema_ext_definition,
    create_enum_definition,
    create_enum_ext_definition,
    create_field_entry,
)


class TestDefinitionExtensions(TestCase):

    def test_apply_and_remove_extension_from_definition(self):
        test_schema_field = create_field_entry("TestField", "string")
        test_schema_name = "myDef"
        test_schema = create_schema_definition(test_schema_name, fields=[test_schema_field])

        schema_ext_field_name = "extField"
        schema_ext_field_type = "ExtField"
        ext_field = create_field_entry(schema_ext_field_name, schema_ext_field_type)
        test_schema_ext = create_schema_ext_definition("mySchemaExt", test_schema_name, fields=[ext_field], required=[schema_ext_field_name])

        enum_val1 = "val1"
        enum_val2 = "val2"
        test_enum_name = "myEnum"
        test_enum = create_enum_definition(test_enum_name, values=[enum_val1, enum_val2])

        test_enum_ext_value = "extVal"
        test_enum_ext = create_enum_ext_definition("myEnumExt", test_enum_name, values=[test_enum_ext_value])

        language_context = get_initialized_language_context(core_spec_only=True)
        language_context.add_definitions_to_context([test_schema, test_enum])

        self.assertIn(test_schema, language_context.definitions)
        self.assertIn(test_enum, language_context.definitions)

        self.assertEqual(1, len(test_schema.structure["schema"]["fields"]))
        self.assertNotIn(REQUIRED_FIELDS_VALIDATION_STRING, test_schema.structure["schema"]["validation"])
        self.assertEqual(2, len(test_enum.structure["enum"]["values"]))

        apply_extension_to_definition(test_schema_ext, test_schema)
        apply_extension_to_definition(test_enum_ext, test_enum)

        # Assert Altered Extension State
        required_fields_validation, *_ = [validation for validation in test_schema.structure["schema"]["validation"]]
        self.assertEqual(2, len(test_schema.structure["schema"]["fields"]))
        self.assertEqual(REQUIRED_FIELDS_VALIDATION_STRING, required_fields_validation.get("name"))
        self.assertEqual(1, len(required_fields_validation.get("arguments")))
        self.assertIn(schema_ext_field_name, test_schema.to_yaml())
        self.assertIn(schema_ext_field_type, test_schema.to_yaml())

        self.assertEqual(3, len(test_enum.structure["enum"]["values"]))
        self.assertIn(test_enum_ext_value, test_enum.to_yaml())

        remove_extension_from_definition(test_schema_ext, test_schema)
        remove_extension_from_definition(test_enum_ext, test_enum)

        # Assert Removed Extension State
        self.assertEqual(1, len(test_schema.structure["schema"]["fields"]))
        self.assertNotIn(REQUIRED_FIELDS_VALIDATION_STRING, test_schema.structure["schema"]["validation"])
        self.assertNotIn(schema_ext_field_name, test_schema.to_yaml())
        self.assertNotIn(schema_ext_field_type, test_schema.to_yaml())

        self.assertEqual(2, len(test_enum.structure["enum"]["values"]))
        self.assertNotIn(test_enum_ext_value, test_enum.to_yaml())
