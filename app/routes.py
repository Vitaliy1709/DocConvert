from pathlib import Path

from fastapi import APIRouter, Request, UploadFile, File, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, RedirectResponse

from app.main import templates
from app.tasks import create_task, run_conversion, tasks_status

router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
CONVERTED_DIR = Path("data/converted")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CONVERTED_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    if not file.filename or "." not in file.filename:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Не коректна назва файлу!"})
    if not file.filename.lower().endswith((".doc", ".docx", ".pdf", ".zip")):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Непідтримуваний формат файлу!"
        })

    save_path = UPLOAD_DIR / file.filename
    with open(save_path, "wb") as f:
        f.write(await file.read())

    # Створюємо task_id та запускаємо фонову конвертацію
    task_id = create_task(save_path)
    background_tasks.add_task(run_conversion, save_path, task_id)

    form_reloaded = request.headers.get("referer", "").endswith("/upload")
    if form_reloaded:
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "success": f"Файл '{file.filename}' загружено і конвертовано. Зачекайте коли з'являться посилання!",
        "task_id": task_id
    })


@router.get("/progress/{task_id}")
async def progress(task_id: str):
    progress = tasks_status.get(task_id, {}).get("progress", 0)
    return JSONResponse({"progress": progress})


@router.get("/result/{task_id}")
async def result(task_id: str):
    files = tasks_status.get(task_id, {}).get("files", [])
    return JSONResponse({"files": [f.name for f in files]})


@router.get("/download/{filename}")
async def download_file(filename: str):
    file_path = CONVERTED_DIR / filename
    if file_path.exists():
        return FileResponse(file_path, filename=filename)
    return JSONResponse({"error": "Файл не знайдено"})
