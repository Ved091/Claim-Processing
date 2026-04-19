# 🧠 Claim Processing Pipeline (LangGraph + FastAPI)

## 🚀 Overview

This project implements an **AI-powered claim processing pipeline** using **LangGraph** to orchestrate multiple agents for document classification and data extraction.

The system processes multi-page PDF claims and extracts structured information by:

* Classifying each page into document types
* Routing pages to specialized extraction agents
* Aggregating results into a final JSON response

---

## 🏗️ Architecture

```
START
  ↓
Segregator Agent (LLM Vision)
  ↓
 ├── ID Agent
 ├── Discharge Summary Agent
 └── Itemized Bill Agent
  ↓
Aggregator
  ↓
END
```

---

## 🧩 Workflow Explanation

### 1. PDF Processing

* PDF is uploaded via API
* Converted into individual page images using `pdf2image`

### 2. Segregator Agent

* Uses LLM vision model
* Classifies each page into one of:

  * claim_forms
  * cheque_or_bank_details
  * identity_document
  * itemized_bill
  * discharge_summary
  * prescription
  * investigation_report
  * cash_receipt
  * other

### 3. Extraction Agents

Each agent processes **only relevant pages**:

#### 🔹 ID Agent

* Extracts:

  * patient_name
  * date_of_birth
  * id_number
  * policy_number

#### 🔹 Discharge Summary Agent

* Extracts:

  * diagnosis
  * admission_date
  * discharge_date
  * physician_name

#### 🔹 Itemized Bill Agent

* Extracts:

  * items (description, quantity, price, total)
  * subtotal
  * tax
  * total_amount

### 4. Aggregator

* Combines all extracted data into final JSON

---

## 📦 API

### POST `/api/process`

#### Input

* `claim_id` (string)
* `file` (PDF)

#### Output

```json
{
  "claim_id": "CLM-001",
  "document_map": {
    "0": "claim_forms",
    "2": "identity_document"
  },
  "extracted_data": {
    "identity": {},
    "discharge_summary": {},
    "itemized_bill": {}
  },
  "status": "success"
}
```

---

## ⚙️ Local Setup

### 1. Clone Repo

```bash
git clone <your-repo-url>
cd claim-processing-pipeline
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

#### Activate:

**Mac/Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

---

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Install System Dependencies

#### Mac

```bash
brew install poppler tesseract
```

#### Ubuntu / Linux

```bash
sudo apt update
sudo apt install poppler-utils tesseract-ocr
```

#### Windows

* Install Poppler: https://github.com/oschwartz10612/poppler-windows
* Install Tesseract: https://github.com/tesseract-ocr/tesseract
* Add both to PATH

---

### 5. Setup Environment Variables

```bash
cp .env.example .env
```

Edit `.env`:

```
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4o-mini
```

---

## ▶️ Run the Server

```bash
uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## 🧪 Testing

```bash
pytest
```

---

## 🐳 Docker Setup

### Build Image

```bash
docker build -t claim-api .
```

### Run Container

```bash
docker run -p 8000:8000 claim-api
```

---

## 🧪 API Testing

### Swagger UI

* Go to: `http://127.0.0.1:8000/docs`
* Upload PDF and test

### cURL

```bash
curl -X POST "http://127.0.0.1:8000/api/process" \
  -F "claim_id=test123" \
  -F "file=@sample.pdf"
```

---

## 👨‍💻 Author

Vedansh Gupta
