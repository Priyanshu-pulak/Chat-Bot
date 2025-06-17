
# 💬 PDF Chatbot using Local LLM (Ollama + LlamaIndex)

This project allows you to chat with one or more PDF documents **fully offline**, using **Ollama + LlamaIndex**. It supports **text-based** and **image-based (scanned)** PDFs by applying OCR automatically. It builds a searchable index using **local embeddings** and answers your questions in real time.

---

## 📁 Project Structure
```
Project/
├── chatbot.py              # Chatbot interface using LlamaIndex & Ollama
├── ocrExtract.py           # Extracts text from PDFs (OCR fallback)
├── environment.yml         # Conda environment with all dependencies
├── data/                   # Put your PDF files here
├── extracted/pdf_text.txt  # Output of extracted text
└── index_store/            # Persistent vector index for fast reuse
```

---

## ✅ Features

- 🔍 Supports both **text** and **scanned image** PDFs  
- 🧠 Uses **Ollama local models** like `llama3` or `mistral`  
- 📦 Fully offline (no internet required)  
- ♻️ Persistent vector index for fast reloading  
- 🔒 Runs in an isolated conda environment  
- 📊 Embeddings & LLM both run locally  

---

## ⚙️ Setup Instructions

### 1. Install Anaconda or Miniconda  
Download and install from the official site.

### 2. Create & activate the conda environment
```bash
conda env create -f environment.yml
conda activate myenv
```

### 3. Install & start Ollama
```bash
ollama serve &
ollama pull llama3     # or: ollama pull mistral
```

---

## 📝 Processing PDFs
Put your PDF files inside **`data/`** and run:
```bash
python ocrExtract.py
```
This creates **`extracted/pdf_text.txt`**.

---

## 🚀 Start the Chatbot
```bash
python chatbot.py
```

Type questions, e.g.:
```
What penalties are mentioned in the SLA?
```
Type `exit` to quit.

---

## 🔄 Rebuild the Index
```bash
rm -r index_store/
python chatbot.py
```

---

## 🛠 Command Cheat‑Sheet
| Purpose                      | Command                                    |
|------------------------------|--------------------------------------------|
| Create env                   | `conda env create -f environment.yml`      |
| Activate env                 | `conda activate myenv`                     |
| Extract PDF text             | `python ocrExtract.py`                     |
| Start chatbot                | `python chatbot.py`                        |
| Pull new Ollama model        | `ollama pull mistral` (or any)             |
| Test model directly          | `ollama run mistral`                       |
| Stop Ollama server           | `pkill -f "ollama"`                        |

---

## 📦 `environment.yml` (explained)
```yaml
name: myenv
channels:
  - conda-forge
dependencies:
  - python=3.11          # Base Python version
  - tesseract            # OCR engine backend
  - poppler              # PDF → image conversion tools
  - libtiff              # Image codec dependency
  - pip
  - pip:
      - pytesseract                      # Python wrapper for Tesseract
      - pillow                           # Image handling (PIL)
      - pdf2image                        # Convert PDF pages to images
      - pymupdf                          # Fast PDF text extraction (`fitz`)
      - llama-index>=0.10.34             # Indexing & retrieval library
      - llama-index-llms-ollama          # LlamaIndex ↔ Ollama LLM connector
      - llama-index-embeddings-ollama    # Local embedding model via Ollama
      - ollama                           # Python client for Ollama
      - jupyter                          # Optional notebook support
```

---

## ⚠️ Troubleshooting
- **TypeError None × float** → switch to `mistral` and upgrade `llama-index`.  
- **Timeout on first query** → increase `request_timeout` in `chatbot.py` or pre‑warm: `ollama run model`.
