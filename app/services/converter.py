import zipfile
from pathlib import Path

import aspose.words as aw

from app.exeptions import UnsupportedFormatError, EmptyArchiveError
from app.logger import logger
from app.progress import tasks_status

UPLOAD_DIR = Path("data/uploads")
CONVERTED_DIR = Path("data/converted")


def convert_doc_to_pdf(input_path: Path, output_path: Path, task_id: str = None):
    logger.info(f"Конвертуєм DOC/DOCX: {input_path.name} -> {output_path.name}")
    doc = aw.Document(str(input_path))
    doc.save(str(output_path))
    logger.info(f"Файл {output_path.name} готовий.")
    if task_id:
        update_progress(task_id, 100, [output_path])


def convert_pdf_to_docx(input_path: Path, output_path: Path, task_id: str = None):
    logger.info(f"Конвертуєм PDF: {input_path.name} -> {output_path.name}")
    doc = aw.Document(str(input_path))
    doc.save(str(output_path))
    logger.info(f"Файл {output_path.name} готовий.")
    if task_id:
        update_progress(task_id, 100, [output_path])


def make_zip(files: list[Path], archive_name: str) -> Path:
    zip_path = CONVERTED_DIR / f"{archive_name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            zipf.write(file, arcname=file.name)
    logger.info(f"Створено архів {zip_path.name}")
    return zip_path


def update_progress(task_id: str, progress: int, files: list[Path] = None):
    tasks_status[task_id] = {"progress": progress, "files": files or []}


def process_uploaded_file(file_path: Path, task_id: str = None):
    results = []

    if file_path.suffix.lower() in [".doc", ".docx"]:
        output_file = CONVERTED_DIR / (file_path.stem + ".pdf")
        convert_doc_to_pdf(file_path, output_file, task_id)
        results.append(output_file)

    elif file_path.suffix.lower() == ".pdf":
        output_file = CONVERTED_DIR / (file_path.stem + ".docx")
        convert_pdf_to_docx(file_path, output_file, task_id)
        results.append(output_file)

    elif file_path.suffix.lower() == ".zip":
        extract_dir = CONVERTED_DIR / file_path.stem
        extract_dir.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        files_inside = list(extract_dir.rglob("*.*"))
        if not files_inside:
            raise EmptyArchiveError("Завантажений архів порожній!")

        converted_files = []
        total_files = len(files_inside)
        for idx, inner_file in enumerate(files_inside, 1):
            if inner_file.suffix.lower() in [".doc", ".docx"]:
                output_file = extract_dir / (inner_file.stem + ".pdf")
                convert_doc_to_pdf(inner_file, output_file)
                converted_files.append(output_file)
            elif inner_file.suffix.lower() == ".pdf":
                output_file = extract_dir / (inner_file.stem + ".docx")
                convert_pdf_to_docx(inner_file, output_file)
                converted_files.append(output_file)

            if task_id:
                update_progress(task_id, int(idx / total_files * 100), converted_files)

        if not converted_files:
            raise UnsupportedFormatError("В архіві немає підтримуваних файлів!")

        archive = make_zip(converted_files, file_path.stem + "_converted")
        results.append(archive)
        if task_id:
            update_progress(task_id, 100, [archive])

    else:
        raise UnsupportedFormatError(f"Формат {file_path.suffix} не підтримується!")

    if task_id:
        update_progress(task_id, 100, results)
    return results
