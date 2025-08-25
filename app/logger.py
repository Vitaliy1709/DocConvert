"""
Налаштування логування:
- Пише події у файл logs/app.log
"""
import logging
from pathlib import Path

# Папка для логів
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Конфігурація логування
logging.basicConfig(
    filename=LOG_DIR / "app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)
