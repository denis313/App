import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from config import db_config
from requets import DatabaseManager

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


def _get_db() -> DatabaseManager | None:
    try:
        dsn = db_config()
    except Exception:
        return None
    return DatabaseManager(dsn=dsn)


@app.get("/")
async def index():
    # Проверяем, существует ли файл, чтобы избежать ошибки 500
    if os.path.exists("templates/index.html"):
        return FileResponse("templates/index.html")
    return {"error": "Файл index.html не найден в папке проекта"}


@app.get("/api/commands")
async def get_commands():
    db = _get_db()
    if db is None:
        return JSONResponse(
            status_code=500,
            content={"error": "DATABASE_URL is not configured"},
        )
    buttons = await db.get_buttons()
    return [
        {
            "id": b.id_button,
            "name": b.name,
            "path": b.path,
        }
        for b in buttons
    ]


if __name__ == "__main__":
    # В FastAPI используется uvicorn.run вместо app.run
    uvicorn.run(app, host="0.0.0.0", port=8000)