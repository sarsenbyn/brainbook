from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.concurrency import run_in_threadpool
import aiofiles
import os
import uuid
from config.database.database import get_db, AsyncSession
from fastapi.responses import FileResponse
from src.services.services import process_pdf_content, split_text_into_chunks
from src.ai import get_embedding
from src.models.models import Document

router = APIRouter(prefix="/file", tags=["pdf-loader"])

folder = "static"

@router.post("/upload")
async def upload(file: UploadFile, db: AsyncSession = Depends(get_db)):
    if not file:
        raise HTTPException(status_code = 400, detail = "Отправьте File!")
    file_exists = os.path.exists(f"static/{file.filename}")
    if file_exists:
        raise HTTPException(status_code = 400, detail = "Файл с таким названием уже существует!")
    file_path = os.path.join(folder, file.filename)
    content = await file.read()
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)

    data = await run_in_threadpool(process_pdf_content, file_path)
    for page_info in data:
        text = page_info["content"]
        page_num = page_info["page"]
        chunks = split_text_into_chunks(text)
        for chunk in chunks:
            vector = await get_embedding(chunk)

            new_doc = Document(
                text=chunk,
                embedding=vector,
                page_number=page_num
            )
            db.add(new_doc)
        await db.commit()
    return {"message": "PDF успешно загружен", "filename": file.filename}