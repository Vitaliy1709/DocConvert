import pytest
from pathlib import Path
from app.services.converter import convert_doc_to_pdf, process_uploaded_file
from app.exeptions import EmptyArchiveError, UnsupportedFormatError
import zipfile

BASE_DIR = Path(__file__).resolve().parent
SAMPLE_DIR = BASE_DIR / "samples"
SAMPLE_DIR.mkdir(exist_ok=True)


def test_docx_to_pdf(tmp_path):
    input_file = SAMPLE_DIR / "test.docx"
    output_file = tmp_path / "test.pdf"

    # Створюємо фейковий docx
    input_file.write_text("Fake DOCX content")

    convert_doc_to_pdf(input_file, output_file)

    assert output_file.exists()


def test_empty_zip(tmp_path):
    zip_path = tmp_path / "empty.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        pass  # Створюємо порожній архів

    with pytest.raises(EmptyArchiveError):
        process_uploaded_file(zip_path)


def test_unsupported_format(tmp_path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("hello")

    with pytest.raises(UnsupportedFormatError):
        process_uploaded_file(file_path)
