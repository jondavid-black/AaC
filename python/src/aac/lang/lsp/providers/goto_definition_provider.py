"""Module for the Goto Definition Provider which handles all goto definition requests."""

from pygls.server import LanguageServer
from pygls.lsp.types.basic_structures import Location, Position, Range
from pygls.lsp.types.language_features.definition import DefinitionParams
from pygls.workspace import Document

from aac.lang.lsp.providers.lsp_provider import LspProvider


class GotoDefinitionProvider(LspProvider):
    """Resolve the location where a specified name is defined."""

    def handle_request(self, ls: LanguageServer, params: DefinitionParams) -> list[Location]:
        """Return the location at which the specified item is found."""
        return self.get_definition_location(ls.workspace.documents, params.text_document.uri, params.position)

    def get_definition_location(self, documents: dict[str, Document], current_uri: str, position: Position) -> list[Location]:
        """Return the location where the AaC definition is defined."""
        name = documents.get(current_uri).word_at_position(position)
        if not name:
            return []

        locations = []
        for doc in documents.values():
            ranges = self.get_ranges_containing_name(doc.source, name)
            definition_ranges = [text_range for text_range in ranges if f"name: {name}" in doc.source.splitlines()[text_range.start.line]]
            locations.extend([Location(uri=doc.uri, range=definition_range) for definition_range in definition_ranges])
        return locations

    def get_ranges_containing_name(self, content: str, name: str) -> list[Range]:
        """
        Return the cursor position of the item in content.

        Args:
            content (str): The content from the workspace document in which to find the named item.
            name (str): The item to search for in the document's content.

        Returns:
            A list of Ranges where in the content
        """

        def get_end_position(position: Position) -> Position:
            end_position = position.copy()
            end_position.character += len(name)
            return end_position

        lines = content.splitlines()
        starting_positions = [Position(line=i, character=lines[i].find(name)) for i, line in enumerate(lines) if name in line]
        return [Range(start=start_pos, end=get_end_position(start_pos)) for start_pos in starting_positions]