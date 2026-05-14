import os
import shutil
from pathlib import Path

import pytest

from tools.document import binary_document_to_markdown, document_path_to_markdown


class TestBinaryDocumentToMarkdown:
    # Define fixture paths
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_fixture_files_exist(self):
        """Verify test fixtures exist."""
        assert os.path.exists(self.DOCX_FIXTURE), (
            f"DOCX fixture not found at {self.DOCX_FIXTURE}"
        )
        assert os.path.exists(self.PDF_FIXTURE), (
            f"PDF fixture not found at {self.PDF_FIXTURE}"
        )

    def test_binary_document_to_markdown_with_docx(self):
        """Test converting a DOCX document to markdown."""
        # Read binary content from the fixture
        with open(self.DOCX_FIXTURE, "rb") as f:
            docx_data = f.read()

        # Call function
        result = binary_document_to_markdown(docx_data, "docx")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result

    def test_binary_document_to_markdown_with_pdf(self):
        """Test converting a PDF document to markdown."""
        # Read binary content from the fixture
        with open(self.PDF_FIXTURE, "rb") as f:
            pdf_data = f.read()

        # Call function
        result = binary_document_to_markdown(pdf_data, "pdf")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result


class TestDocumentPathToMarkdown:
    FIXTURES_DIR = Path(__file__).parent / "fixtures"
    DOCX_FIXTURE = FIXTURES_DIR / "mcp_docs.docx"
    PDF_FIXTURE = FIXTURES_DIR / "mcp_docs.pdf"

    def test_pdf_contains_known_phrase(self):
        result = document_path_to_markdown(str(self.PDF_FIXTURE))
        assert isinstance(result, str)
        assert len(result) > 0
        assert "Model Context Protocol" in result

    def test_docx_contains_known_phrase(self):
        result = document_path_to_markdown(str(self.DOCX_FIXTURE))
        assert isinstance(result, str)
        assert len(result) > 0
        assert "Model Context Protocol" in result

    @pytest.mark.parametrize(
        "fixture_name,ext",
        [("mcp_docs.pdf", "pdf"), ("mcp_docs.docx", "docx")],
    )
    def test_matches_binary_document_to_markdown(self, fixture_name, ext):
        path = self.FIXTURES_DIR / fixture_name
        from_path = document_path_to_markdown(str(path))
        from_bytes = binary_document_to_markdown(path.read_bytes(), ext)
        assert from_path == from_bytes

    def test_accepts_absolute_path(self):
        absolute = self.PDF_FIXTURE.resolve()
        assert absolute.is_absolute()
        result = document_path_to_markdown(str(absolute))
        assert isinstance(result, str)
        assert "Model Context Protocol" in result

    def test_accepts_relative_path(self, monkeypatch):
        monkeypatch.chdir(self.FIXTURES_DIR)
        result = document_path_to_markdown("mcp_docs.pdf")
        assert isinstance(result, str)
        assert "Model Context Protocol" in result

    def test_uppercase_extension(self, tmp_path):
        uppercase_copy = tmp_path / "mcp_docs.PDF"
        shutil.copy(self.PDF_FIXTURE, uppercase_copy)
        result = document_path_to_markdown(str(uppercase_copy))
        assert isinstance(result, str)
        assert "Model Context Protocol" in result
