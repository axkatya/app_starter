from io import BytesIO
from pathlib import Path

from markitdown import MarkItDown, StreamInfo
from pydantic import Field


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    path: str = Field(
        description="Filesystem path to a PDF or DOCX document. Accepts absolute or relative paths; the file extension determines the conversion format."
    ),
) -> str:
    """Read a document from disk and convert its contents to markdown.

    Loads the file at the given path, infers the document format from the
    path's extension, and returns the converted markdown text.

    When to use:
    - When the model has a path to a local PDF or DOCX file and needs its
      textual content as markdown.
    - When the caller already has bytes in memory, prefer
      `binary_document_to_markdown` instead.

    Examples:
    >>> document_path_to_markdown("docs/report.pdf")  # doctest: +SKIP
    '# Report\\n\\n...'
    """
    file_path = Path(path)
    extension = file_path.suffix.lstrip(".").lower()
    return binary_document_to_markdown(file_path.read_bytes(), extension)
