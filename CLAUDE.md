# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A Python MCP (Model Context Protocol) server that exposes document-related tools (e.g., binary-to-markdown conversion via `markitdown`) to AI assistants. Built on `FastMCP` from the `mcp` SDK.

## Commands

```bash
# Environment setup (uv-managed; pyproject.toml is the source of truth)
uv venv
source .venv/bin/activate         # PowerShell: .venv\Scripts\Activate.ps1
uv pip install -e .

# Run the MCP server (stdio transport via FastMCP defaults)
uv run main.py

# Tests
uv run pytest                                              # all
uv run pytest tests/test_document.py                       # single file
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_pdf  # single test
```

## Architecture

- `main.py` — server entry point. Instantiates `FastMCP("docs")`, registers tool functions via `mcp.tool()(fn)`, then calls `mcp.run()`. **Registration is explicit** — a function in `tools/` is not exposed until it is wired up here. `tools/document.py:binary_document_to_markdown` exists but is not currently registered; `tools/math.py:add` is.
- `tools/` — plain Python functions, one per file by domain (`math.py`, `document.py`). Functions are pure / framework-agnostic so they can be unit-tested directly without going through MCP. Tests import from `tools.*`, not through the server.
- `tests/fixtures/` — binary sample documents (`mcp_docs.docx`, `mcp_docs.pdf`) used by `test_document.py`. New document-conversion tests should add fixtures here.

## Defining MCP Tools (from README)

Tools are ordinary Python functions registered with the server:

```python
mcp.tool()(my_function)
```

Conventions for tool **descriptions** (the docstring becomes the tool description surfaced to the model — write it for an LLM consumer, not just a human reader):

- Begin with a one-line summary.
- Provide a detailed explanation of functionality.
- Explain **when to use** (and when **not** to use) the tool.
- Include usage examples with expected input/output.

Conventions for tool **parameters** — use `pydantic.Field` for per-parameter descriptions (these become the parameter schemas the model sees):

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does"),
) -> ReturnType:
    """Comprehensive docstring here — summary line, details, when-to-use, examples."""
    ...
```

See `tools/math.py:add` for a reference implementation that follows all of the above (summary line, when-to-use bullets, `>>>` examples, `Field`-annotated params).

To add a new tool:
1. Write the function in `tools/<domain>.py` with `Field`-annotated params and a full docstring per the conventions above.
2. Import and register it in `main.py` with `mcp.tool()(fn)`.
3. Add direct unit tests under `tests/` importing from `tools.*` (do not test through the MCP server).
