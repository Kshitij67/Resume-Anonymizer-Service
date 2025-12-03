from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.openapi.models import Response
from fastapi import Response as FastAPIResponse
from presidio_image_redactor import ImageRedactorEngine
from pdf2image import convert_from_path
import img2pdf
import uuid
import os
from PIL import Image

counter = 0
entities_to_redact_ = [ "PERSON","EMAIL_ADDRESS", "PHONE_NUMBER" ,"URL"]

app = FastAPI()

redactor = ImageRedactorEngine()

@app.post(
    "/anonymize",
    responses={200: {"content": {"application/pdf": {}}}}
)
async def anonymize_resume(file: UploadFile = File(...)):
    global counter
    print("Received file for anonymization:", file.filename)
    job_id = str(uuid.uuid4())

    input_path = f"/tmp/{job_id}.pdf"
    output_path = f"/tmp/{job_id}_anon.pdf"
    temp_dir = f"/tmp/{job_id}_pages"
    os.makedirs(temp_dir, exist_ok=True)

    with open(input_path, "wb") as f:
        f.write(await file.read())

    pages = convert_from_path(input_path, dpi=300)
    redacted_pages = []

    for idx, page in enumerate(pages):
        page_path = f"{temp_dir}/page_{idx}.png"
        redacted_path = f"{temp_dir}/redacted_page_{idx}.png"

        page.save(page_path)

        img = Image.open(page_path)
        redacted_img = redactor.redact(img,entities = entities_to_redact_)


        redacted_img.save(redacted_path)
        redacted_pages.append(redacted_path)

    with open(output_path, "wb") as f:
        f.write(img2pdf.convert(redacted_pages))

    counter += 1

    return FileResponse(
        output_path,
        media_type="application/pdf",
        filename=f"anonymized_resume_{counter}.pdf"
    )
