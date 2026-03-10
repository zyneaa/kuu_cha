import os
import markdown
from typing import List
from fastapi import APIRouter, Request, HTTPException, File, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from utils.zipper import zip_folder

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/d/{folder_name}")
async def download_folder(folder_name: str):
    file_path = f"./files/{folder_name}.zip"
    if not os.path.exists(file_path):
        # Try zipping it now if it exists as a directory
        folder_path = f"./files/{folder_name}"
        if os.path.isdir(folder_path):
            zip_folder(os.path.abspath(folder_path), folder_name)
        else:
            raise HTTPException(status_code=404, detail="Folder not found")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Zip file not found")
        
    return FileResponse(file_path, filename=f"{folder_name}.zip")

@router.post("/u")
async def upload_files(_: Request, folder: str = Form(...), files: List[UploadFile] = File(...)):
    folder_path = f"./files/{folder}"
    os.makedirs(folder_path, exist_ok=True)

    for file in files:
        file_path = os.path.join(folder_path, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

    # Re-zip the folder
    zip_folder(os.path.abspath(folder_path), folder)

    # Redirect back or return success
    return HTMLResponse(content=f"<script>alert('Files uploaded to {folder}'); window.location.href='/';</script>")

@router.get("/d")
async def download_all():
    file_path = "./files/files.zip"
    if not os.path.exists(file_path):
        # For now, let's just zip the whole files dir if it's missing
        # But the user wants per-folder. Maybe this is redundant.
        # I'll keep it pointing to files.zip if it exists.
        raise HTTPException(status_code=404, detail="Global zip not found")
    return FileResponse(file_path, filename="files.zip")

@router.get("/{folder}", response_class=HTMLResponse)
async def get_all_files(request: Request, folder: str):
    path = f"./files/{folder}"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Folder not found")
    files = os.listdir(path)
    return templates.TemplateResponse("files.html", {"request": request, "files": files, "folder": folder})

@router.get("/content/{folder}/{file_name}", response_class=HTMLResponse)
async def get_content(request: Request, folder: str, file_name: str):
    path = f"./files/{folder}/{file_name}"
    try:
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="File not found")
        with open(path, 'r') as file: 
            content = file.read()
            html_content = markdown.markdown(content)
            return templates.TemplateResponse("content.html", {
                "request": request, 
                "content": html_content, 
                "file_name": file_name, 
                "folder": folder
            })
    except Exception as e:
        print(f"Error reading file: {e}")
        return HTMLResponse(content="Internal server error", status_code=500)

