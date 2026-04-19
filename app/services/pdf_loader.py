import os
from pdf2image import convert_from_path
from app.core.config import settings

def save_pdf(file, filename: str):
    os.makedirs(settings.TEMP_DIR, exist_ok=True)
    path = os.path.join(settings.TEMP_DIR, filename)

    with open(path, "wb") as f:
        f.write(file.file.read())

    return path


def pdf_to_images(pdf_path: str):
    images = convert_from_path(pdf_path)
    image_paths = []

    for i, img in enumerate(images):
        path = f"{pdf_path}_page_{i}.png"
        img.save(path, "PNG")
        image_paths.append(path)

    return image_paths