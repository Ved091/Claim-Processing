from fastapi import APIRouter, UploadFile, File, Form
from app.services.pdf_loader import save_pdf, pdf_to_images
from app.graph.workflow import run_workflow

router = APIRouter()

@router.post("/api/process")
async def process_claim(
    claim_id: str = Form(...),
    file: UploadFile = File(...)
):
    pdf_path = save_pdf(file, file.filename)
    pages = pdf_to_images(pdf_path)

    result = run_workflow(claim_id, pages)

    return result