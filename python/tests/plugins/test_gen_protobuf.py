import os
from unittest import TestCase
from unittest.mock import patch
from tempfile import TemporaryDirectory, NamedTemporaryFile
from nose2.tools import params
from aac.lang.active_context_lifecycle_manager import get_active_context
from aac.plugins.plugin_execution import plugin_result
from aac.plugins.gen_protobuf.gen_protobuf_impl import (
    gen_protobuf,
    _convert_camel_case_to_snake_case,
    _collect_template_generation_properties,
)

from tests.helpers.assertion import assert_plugin_failure, assert_plugin_success
from tests.helpers.io import temporary_test_file
from tests.helpers.parsed_definitions import create_enum_definition, create_field_entry, create_data_definition


class TestGenerateProtobufPlugin(TestCase):
    def setUp(self):
        get_active_context(reload_context=True)



        with TemporaryDirectory() as temp_dir, temporary_test_file(TEST_ARCH_YAML_STRING) as temp_arch_file:
            with plugin_result("", gen_protobuf, temp_arch_file.name, temp_dir) as result:
                pass

            # The assert needs to be outside of the plugin_result context manager or the assertion error is masked.
            assert_plugin_success(result)

            # Assert each data message has its own file.
            generated_file_names = os.listdir(temp_dir)
            self.assertEqual(5, len(generated_file_names))

            # Assert each expected file is present
            self.assertIn("data_a.proto", generated_file_names)
            self.assertIn("data_b.proto", generated_file_names)
            self.assertIn("data_c.proto", generated_file_names)
            self.assertIn("message_metadata_data.proto", generated_file_names)
            self.assertIn("message_type.proto", generated_file_names)

            # Assert data_a.proto contents
            with open(os.path.join(temp_dir, "data_a.proto")) as data_a_proto_file:
                data_a_proto_file_contents = data_a_proto_file.read()
                # Assert imports for component classes
                self.assertIn('import "message_metadata_data.proto"', data_a_proto_file_contents)
                self.assertIn('import "message_type.proto"', data_a_proto_file_contents)

                # Assert data_a structure
                self.assertIn("MessageMetadataData metadata", data_a_proto_file_contents)
                self.assertIn("optional string msg", data_a_proto_file_contents)
                self.assertIn("optional MessageType message_type", data_a_proto_file_contents)

            # Assert data_b.proto contents
            with open(os.path.join(temp_dir, "data_b.proto")) as data_b_proto_file:
                data_b_proto_file_contents = data_b_proto_file.read()
                # Assert imports for component classes
                self.assertIn('import "message_metadata_data.proto"', data_b_proto_file_contents)

                # Assert data_b structure
                self.assertIn("MessageMetadataData metadata", data_b_proto_file_contents)
                self.assertIn("string transformed_msg", data_b_proto_file_contents)

            # Assert data_c.proto contents
            with open(os.path.join(temp_dir, "data_c.proto")) as data_c_proto_file:
                data_c_proto_file_contents = data_c_proto_file.read()
                # Assert imports for component classes
                self.assertIn('import "message_metadata_data.proto"', data_c_proto_file_contents)

                # Assert data_b structure
                self.assertIn("MessageMetadataData metadata", data_c_proto_file_contents)
                self.assertIn("repeated fixed64 code", data_c_proto_file_contents)

            # Assert message_metadata_data.proto contents
            with open(os.path.join(temp_dir, "message_metadata_data.proto")) as message_metadata_data_proto_file:
                message_metadata_data_proto_file_contents = message_metadata_data_proto_file.read()

                # Assert data_b structure
                self.assertIn("message MessageMetadataData", message_metadata_data_proto_file_contents)
                self.assertIn("int64 message_id", message_metadata_data_proto_file_contents)

            # Assert message_type.proto contents
            with open(os.path.join(temp_dir, "message_type.proto")) as message_type_proto_file:
                message_type_proto_file_contents = message_type_proto_file.read()

                # Assert message_type structure
                self.assertIn("enum MessageType", message_type_proto_file_contents)
                self.assertIn("TYPE_1", message_type_proto_file_contents)
                self.assertIn("TYPE_2", message_type_proto_file_contents)
                self.assertIn("TYPE_3", message_type_proto_file_contents)

    @patch("aac.plugins.gen_protobuf.gen_protobuf_impl.load_default_templates")
    def test_gen_protobuf_fails_with_multiple_message_templates(self, load_default_templates):
        with TemporaryDirectory() as temp_dir, NamedTemporaryFile("w") as arch_file:
            arch_file.write(TEST_ARCH_YAML_STRING)
            arch_file.seek(0)

            load_default_templates.return_value = ["a", "b"]
            result = gen_protobuf(arch_file.name, temp_dir)
            assert_plugin_failure(result)

    @params(
        ("DataA", "data_a"),
        ("somethingSimple", "something_simple"),
        ("SomethingComplex!To.Test", "something_complex!_to._test"),
        ("whataboutnocamelcases?", "whataboutnocamelcases?"),
    )
    def test__convert_camel_case_to_snake_case(self, test_string, expected_string):
        self.assertEqual(expected_string, _convert_camel_case_to_snake_case(test_string))

    def test__generate_protobuf_details_from_data_message_model(self):
        expected_result = {
            "name": "DataA",
            "file_type": "data",
            "fields": [{"name": "msg", "type": "int64", "optional": True, "repeat": False}],
        }
        test_message_field_name = "msg"
        test_message_field_type = "number"
        test_message_field_prototype = "int64"
        test_message_field = create_field_entry(test_message_field_name, test_message_field_type)
        test_message_field["protobuf_type"] = test_message_field_prototype

        test_message_name = "DataA"
        test_message_definition = create_data_definition(test_message_name, [test_message_field])

        actual_result = _collect_template_generation_properties({test_message_definition.name: test_message_definition})
        self.assertDictEqual(expected_result, actual_result[0])

    def test__generate_protobuf_details_from_data_message_model_wth_repeated_fields(self):
        expected_result = {
            "name": "DataA",
            "file_type": "data",
            "fields": [{"name": "msg", "type": "int64", "optional": True, "repeat": False}],
        }

        test_message_field_name = "msg"
        test_message_field_type = "number"
        test_message_field_prototype = "int64"
        test_message_field = create_field_entry(test_message_field_name, test_message_field_type)
        test_message_field["protobuf_type"] = test_message_field_prototype

        test_message_name = "DataA"
        test_message_definition = create_data_definition(test_message_name, [test_message_field])

        actual_result = _collect_template_generation_properties({test_message_definition.name: test_message_definition})
        self.assertDictEqual(expected_result, actual_result[0])

    def test__generate_protobuf_details_from_data_message_model_with_required_fields(self):
        expected_result = {
            "name": "DataA",
            "file_type": "data",
            "fields": [
                {"name": "id", "type": "int64", "optional": True, "repeat": False},
                {"name": "msg", "type": "string", "optional": False, "repeat": False},
            ],
        }

        test_message_field_name = "msg"
        test_message_field_type = "string"
        test_message_field_prototype = "string"
        test_message_field = create_field_entry(test_message_field_name, test_message_field_type)
        test_message_field["protobuf_type"] = test_message_field_prototype

        test_id_field_name = "id"
        test_id_field_type = "number"
        test_id_field_prototype = "int64"
        test_id_field = create_field_entry(test_id_field_name, test_id_field_type)
        test_id_field["protobuf_type"] = test_id_field_prototype

        test_message_name = "DataA"
        test_message_definition = create_data_definition(test_message_name, [test_id_field, test_message_field], [test_message_field_name])

        actual_result = _collect_template_generation_properties({test_message_definition.name: test_message_definition})
        self.assertDictEqual(expected_result, actual_result[0])

    def test__generate_protobuf_details_from_data_message_model_with_nested_types_and_imports(self):
        expected_result = [
            {
                "name": "DataA",
                "file_type": "data",
                "fields": [
                    {"name": "metadata", "type": "DataB", "optional": True, "repeat": False},
                    {"name": "msg", "type": "string", "optional": True, "repeat": False},
                ],
                "imports": ["data_b.proto"],
            },
            {
                "name": "DataB",
                "file_type": "data",
                "fields": [{"name": "id", "type": "int64", "optional": True, "repeat": False}],
            },
        ]

        test_message_a_name = "DataA"
        test_message_b_name = "DataB"

        test_message_field_name = "msg"
        test_message_field_type = "string"
        test_message_field_prototype = "string"
        test_message_field = create_field_entry(test_message_field_name, test_message_field_type)
        test_message_field["protobuf_type"] = test_message_field_prototype

        test_metadata_field_name = "metadata"
        test_metadata_field_type = test_message_b_name
        test_metadata_field = create_field_entry(test_metadata_field_name, test_metadata_field_type)

        test_id_field_name = "id"
        test_id_field_type = "number"
        test_id_field_prototype = "int64"
        test_id_field = create_field_entry(test_id_field_name, test_id_field_type)
        test_id_field["protobuf_type"] = test_id_field_prototype

        test_message_a_definition = create_data_definition(test_message_a_name, [test_metadata_field, test_message_field])
        test_message_b_definition = create_data_definition(test_message_b_name, [test_id_field])

        test_definitions_dict = {d.name: d for d in [test_message_a_definition, test_message_b_definition]}
        actual_result = _collect_template_generation_properties(test_definitions_dict)
        for i in range(len(actual_result)):
            self.assertDictEqual(expected_result[i], actual_result[i])

    def test__generate_protobuf_details_from_data_message_model_with_enums(self):
        expected_result = [
            {
                "name": "DataA",
                "file_type": "data",
                "fields": [
                    {"name": "message_type", "type": "Enum", "optional": True, "repeat": False},
                    {"name": "msg", "type": "string", "optional": True, "repeat": False},
                ],
                "imports": ["enum.proto"],
            },
            {"name": "Enum", "file_type": "enum", "enums": ["VAL_1", "VAL_2"]},
        ]

        test_enum_name = "Enum"
        test_enum_definition = create_enum_definition(test_enum_name, ["VAL_1", "VAL_2"])

        test_message_field_name = "msg"
        test_message_field_type = "string"
        test_message_field_prototype = "string"
        test_message_field = create_field_entry(test_message_field_name, test_message_field_type)
        test_message_field["protobuf_type"] = test_message_field_prototype

        test_message_type_field_name = "message_type"
        test_message_type_field_type = test_enum_name
        test_message_type_field = create_field_entry(test_message_type_field_name, test_message_type_field_type)

        test_message_a_name = "DataA"
        test_message_a_definition = create_data_definition(test_message_a_name, [test_message_type_field, test_message_field])

        test_definitions_dict = {d.name: d for d in [test_message_a_definition, test_enum_definition]}
        actual_result = _collect_template_generation_properties(test_definitions_dict)
        for i in range(len(actual_result)):
            self.assertDictEqual(expected_result[i], actual_result[i])


TEST_ARCH_YAML_STRING = """
model:
  name: System
  description: A simple distributed system model
  components:
    - name: svc1
      type: ServiceOne
    - name: svc2
      type: ServiceTwo
  behavior:
    - name: doFlow
      type: request-response
      description:  process DataA and respond with DataD
      input:
        - name: in
          type: DataA
      output:
        - name: out
          type: DataC
      acceptance:
        - scenario: go
          given:
            - The System is running.
          when:
            - The System receives input.in
          then:
            - The System responds with output.out
---
model:
  name: ServiceOne
  behavior:
    - name: ProcessDataA
      type: request-response
      input:
        - name: in
          type: DataA
      output:
        - name: out
          type: DataB
      acceptance:
        - scenario: go
          given:
            - ServiceOne is running.
          when:
            - The user sends a DataA request
          then:
            - The user receives a DataB response
---
model:
  name: ServiceTwo
  behavior:
    - name: Process DataB
      type: request-response
      input:
        - name: in
          type: DataB
      output:
        - name: out
          type: DataC
      acceptance:
        - scenario: go
          given:
            - The ServiceTwo is running
          when:
            - The user makes a request with DataB
          then:
            - The user receives a response with DataC
---
data:
  name: DataA
  fields:
  - name: metadata
    type: MessageMetadataData
  - name: msg
    type: string
    protobuf_type: string
  - name: message_type
    type: MessageType
  required:
  - metadata
---
data:
  name: DataB
  fields:
  - name: metadata
    type: MessageMetadataData
  - name: transformed_msg
    type: string
    protobuf_type: string
  required:
  - metadata
  - transformed_msg
---
data:
  name: DataC
  fields:
  - name: metadata
    type: MessageMetadataData
  - name: code
    type: number[]
    protobuf_type: fixed64
  required:
  - metadata
---
data:
  name: MessageMetadataData
  fields:
  - name: message_id
    type: number
    protobuf_type: int64
  required:
  - message_id
---
enum:
  name: MessageType
  values:
  - type_1
  - type_2
  - type_3
"""
