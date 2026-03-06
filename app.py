import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

@app.get("/")
async def index():
    # Проверяем, существует ли файл, чтобы избежать ошибки 500
    if os.path.exists("templates/index.html"):
        return FileResponse("templates/index.html")
    return {"error": "Файл index.html не найден в папке проекта"}

if __name__ == "__main__":
    # В FastAPI используется uvicorn.run вместо app.run
    uvicorn.run(app, host="0.0.0.0", port=8000)