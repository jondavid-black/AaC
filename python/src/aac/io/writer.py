"""AaC Module for easy file io."""

import logging
from os import linesep, path, makedirs

from aac.lang.definitions.definition import Definition
from aac.io.constants import YAML_DOCUMENT_SEPARATOR


def write_file(uri: str, content: str, overwrite: bool = False) -> None:
    """
    Write string content to a file.

    Args:
        uri (str): the file's full uri
        content (str): contents of the file to write
        overwrite (bool): True to overwrite an existing file or false to not.
    """
    does_file_exist = path.exists(uri)
    file_parent_dir = path.dirname(uri)

    if not (does_file_exist or path.exists(file_parent_dir)):
        makedirs(file_parent_dir, exist_ok=True)

    if not overwrite and does_file_exist:
        logging.info(f"{uri} already exists, skipping write.")
        return

    try:
        with open(uri, "w") as file:
            file.writelines(content)
    except IOError as error:
        logging.error(f"Failed to write file {uri} do to error: {error}")


def write_definitions_to_file(definitions: list[Definition], file_uri: str, is_user_editable: bool = True) -> None:
    """
    Given a list of definitions, write them to file uri. Updates the source for definitions passed in.

    Args:
        definitions (list[Definition]): The definitions to write to file.
        file_uri (str): The URI of the file to write the definitions to.
        is_user_editable (bool): True if the AaC file can be edited by users.
    """
    def sort_definitions_by_lexeme_line(definition_a: Definition, definition_b: Definition) -> int:
        definition_a_starting_line = next(iter(definition_a.lexemes, -1))
        definition_b_starting_line = next(iter(definition_b.lexemes, -1))
        return definition_a_starting_line - definition_b_starting_line

    definitions.sort(key=sort_definitions_by_lexeme_line)

    file_content = ""
    for definition in definitions:
        definition.source.uri = file_uri
        definition.source.is_user_editable = is_user_editable

        yaml_doc_separator = f"{linesep}{YAML_DOCUMENT_SEPARATOR}{linesep}" if file_content else ""
        file_content += f"{yaml_doc_separator}{definition.to_yaml()}"

    write_file(file_uri, file_content, True)
