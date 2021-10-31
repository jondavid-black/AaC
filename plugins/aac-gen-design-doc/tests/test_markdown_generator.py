from unittest import TestCase

from markdown_generator import (InvalidLevelError,
                                MarkdownDesignDocumentGenerator)

from aac import parser


class MarkdownDesignDocumentGeneratorTest(TestCase):
    markdown = None
    title = "test title"

    def setUp(self):
        self.markdown = MarkdownDesignDocumentGenerator()

    def test_can_make_headings_one_through_six(self):
        def assertion(i):
            title = self.title
            make_heading = self.markdown.make_heading
            self.assertEqual(make_heading(title, i), f"{'#' * i} {title}")

        list(map(assertion, range(1, 7)))

    def test_make_heading_fails_when_given_level_out_of_bounds(self):
        title = self.title
        make_heading = self.markdown.make_heading

        self.assertRaisesRegex(InvalidLevelError, "invalid.*0.*1", make_heading, title, 0)
        self.assertRaisesRegex(InvalidLevelError, "invalid.*7.*6", make_heading, title, 7)

    def test_can_make_section_with_headings(self):
        def assertion(i):
            title = self.title
            content = "some test content"
            make_section = self.markdown.make_section
            self.assertEqual(
                make_section(title, i, content),
                f"{self.markdown.make_heading(title, i)}\n\n{content}",
            )

        list(map(assertion, range(1, 7)))

    def test_make_section_fails_when_given_level_out_of_bounds(self):
        title = self.title
        make_section = self.markdown.make_section

        self.assertRaisesRegex(InvalidLevelError, "invalid.*0.*1", make_section, title, 0, "text")
        self.assertRaisesRegex(InvalidLevelError, "invalid.*7.*6", make_section, title, 7, "text")

    def test_can_make_unordered_list_given_list_of_strings(self):
        items = ["a", "b", "c"]
        expected = ["", "- a", "- a\n- b", "- a\n- b\n- c"]

        for i in range(1 + len(items)):
            self.assertEqual(self.markdown.make_unordered_list(items[:i]), expected[i])


class MarkdownDesignDocumentGeneratorFunctionalTest(TestCase):
    markdown = None

    def setUp(self):
        self.markdown = MarkdownDesignDocumentGenerator()

    def test_can_generate_design_document_in_markdown_for_model(self):
        make_document_outline = self.markdown.make_document_outline

        model = parser.parse_str(TEST_MODEL, "markdown-generator-test")
        doc = make_document_outline(model)
        self.assertEqual(doc, TEST_MARKDOWN_DOC)


TEST_MODEL = """
data:
  name: Message
  fields:
  - name: body
    type: string
  - name: sender
    type: string
---
model:
  name: EchoService
  description: This is a message mirror.
  behavior:
    - name: echo
      type: request-response
      description: This is the one thing it does.
      input:
        - name: inbound
          type: Message
      output:
        - name: outbound
          type: Message
      acceptance:
        - scenario: onReceive
          given:
           - The EchoService is running.
          when:
            - The user sends a message to EchoService.
          then:
            - The user receives the same message from EchoService.
---
usecase:
  name: Everything is working.
  description: Something happens.
  participants:
    - name: user
      type: User
    - name: msg
      type: Message
    - name: echo
      type: EchoService
  steps:
    - step: The user sends the message.
      source: user
      target: echo
      action: echo-message
"""

TEST_MARKDOWN_DOC = """
# Model: EchoService

This is a message mirror.

# Usecase: Everything is working.

Something happens.
"""
