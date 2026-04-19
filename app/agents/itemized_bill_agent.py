import base64
from openai import OpenAI
from app.core.config import settings
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def extract_bill_data(pages):
    if not pages:
        return {}

    images = []
    for p in pages:
        with open(p, "rb") as f:
            images.append(base64.b64encode(f.read()).decode())

    prompt = """
Extract:
- items (list of {description, quantity, price, total})
- subtotal
- tax
- total_amount

Return JSON only.
"""

    response = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}] +
                [
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{img}"
                    }}
                    for img in images
                ]
            }
        ]
    )

    return json.loads(response.choices[0].message.content)