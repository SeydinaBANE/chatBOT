"""Tests du chargeur PDF."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from rag.loader import PDFLoader


def test_splitter_configured_with_custom_params():
    loader = PDFLoader(chunk_size=500, chunk_overlap=50)
    assert loader._splitter._chunk_size == 500
    assert loader._splitter._chunk_overlap == 50


def test_splitter_default_params():
    loader = PDFLoader()
    assert loader._splitter._chunk_size == 1000
    assert loader._splitter._chunk_overlap == 200


def test_load_from_bytes_calls_load():
    loader = PDFLoader()
    expected_docs = [MagicMock()]
    with patch.object(loader, "load", return_value=expected_docs) as mock_load:
        result = loader.load_from_bytes(b"fake pdf", "test.pdf")
        assert mock_load.called
        assert result == expected_docs


def test_load_from_bytes_cleans_up_temp_file():
    loader = PDFLoader()
    captured_path = {}

    def fake_load(path: Path):
        captured_path["path"] = path
        assert path.exists()
        return [MagicMock()]

    with patch.object(loader, "load", side_effect=fake_load):
        loader.load_from_bytes(b"fake pdf", "test.pdf")

    assert not captured_path["path"].exists()


def test_load_from_bytes_temp_file_has_pdf_suffix():
    loader = PDFLoader()
    captured_path = {}

    def fake_load(path: Path):
        captured_path["path"] = path
        return []

    with patch.object(loader, "load", side_effect=fake_load):
        loader.load_from_bytes(b"content", "doc.pdf")

    assert str(captured_path["path"]).endswith(".pdf")
