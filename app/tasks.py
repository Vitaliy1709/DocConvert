import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from multipart import file_path

from app.logger import logger
from app.progress import tasks_status
from app.services.converter import process_uploaded_file

# Словник для збереження прогресу завдань {task_id: 0-100}
progress_store: dict[str, int] = {}
progress_lock = threading.Lock()

# ThreadPoolExecutor для багатопоточності
executor = ThreadPoolExecutor(max_workers=4)


def create_task(filepath: Path) -> str:
    task_id = str(uuid.uuid4())
    tasks_status[task_id] = {"progress": 0, "files": []}
    logger.info(f"Створено задачу {task_id} для {file_path.name}")
    return task_id


def run_conversion(filepath: Path, task_id: str):
    try:
        tasks_status[task_id] = {"progress": 0, "files": []}
        results = process_uploaded_file(filepath, task_id)
        tasks_status[task_id] = {"progress": 100, "files": results}
    except Exception as e:
        logger.error(f"Помилка конвертації {filepath.name}: {e}")
        tasks_status[task_id] = {"progress": -1, "files": []}
