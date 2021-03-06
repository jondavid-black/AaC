"""AaC Plugin implementation module for the start-lsp plugin."""
# NOTE: It is safe to edit this file.
# This file is only initially generated by the aac gen-plugin, and it won't be overwritten if the file already exists.

from typing import Callable
from aac.lang.lsp.language_server import AacLanguageServer
from aac.plugins.plugin_execution import PluginExecutionResult, plugin_result

plugin_name = "start-lsp"


def start_lsp_io():
    """Start the LSP server in IO mode."""
    aac_language_server = AacLanguageServer()
    return _start_lsp(aac_language_server.start_io)


def start_lsp_tcp(host: str, port: int):
    """Start the LSP server in TCP mode."""
    aac_language_server = AacLanguageServer()
    function_kwargs = {
        "host": host or "127.0.0.1",
        "port": port or 5007
    }
    return _start_lsp(aac_language_server.start_tcp, **function_kwargs)


def _start_lsp(language_server_start_function: Callable, **start_function_kwargs) -> PluginExecutionResult:
    """Start the LSP server."""
    with plugin_result(plugin_name, language_server_start_function, **start_function_kwargs) as result:
        result.messages = [m for m in result.messages if m]
        return result
