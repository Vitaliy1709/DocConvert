from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path
from app.logger import logger
import secrets

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="DocConvert")

# Сесії
app.add_middleware(
    SessionMiddleware,
    secret_key=secrets.token_hex(16)
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Шаблони
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Статика
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Підключаємо маршрути
from app import routes

app.include_router(routes.router)

logger.info("DocConvert запущено...")
