import os
import zipfile
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routes.files import router as files_router

from utils.zipper import update_all_zips

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run zipping logic on startup for all folders
    update_all_zips("./files")
    yield

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

app.include_router(files_router)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    path = "./files/"
    folder = []

    if os.path.exists(path):
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                folder.append(entry)

    return templates.TemplateResponse("index.html", {"request": request, "folder": folder})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

