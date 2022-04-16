"""AaC Plugin implementation module for the start-lsp plugin."""
# NOTE: It is safe to edit this file.
# This file is only initially generated by the aac gen-plugin, and it won't be overwritten if the file already exists.

import aac.lang.lsp.server as lsp_server
from aac.plugins.plugin_execution import PluginExecutionResult, plugin_result

plugin_name = "start-lsp"


# Temporary until issue #227 is complete
def start_lsp(host=None, port=None) -> PluginExecutionResult:
    """Start the IO LSP server."""
    # Temporary until issue #227 is complete
    with plugin_result(plugin_name, lsp_server.start_lsp, host, port) as result:
        result.messages = [m for m in result.messages if m]
        return result