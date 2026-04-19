import base64
from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

DOC_TYPES = [
    "claim_forms",
    "cheque_or_bank_details",
    "identity_document",
    "itemized_bill",
    "discharge_summary",
    "prescription",
    "investigation_report",
    "cash_receipt",
    "other"
]

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def classify_page(image_path: str) -> str:
    base64_img = encode_image(image_path)

    prompt = f"""
You are a document classification system.

Classify the document into EXACTLY one of the following:
{DOC_TYPES}

Return ONLY the label.
"""

    response = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{base64_img}"
                }}
            ]}
        ]
    )

    label = response.choices[0].message.content.strip()

    if label not in DOC_TYPES:
        return "other"

    return label


def segregate_pages(pages):
    document_map = {}

    for i, page in enumerate(pages):
        label = classify_page(page)
        document_map[i] = label

    return document_map