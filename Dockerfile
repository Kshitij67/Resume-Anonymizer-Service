FROM python:3.10-slim

# 1️⃣ Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    poppler-utils

# 2️⃣ Copy package definitions first (these rarely change)
COPY requirements.txt .

# 3️⃣ Install dependencies and spaCy model (cached unless requirements.txt changes)
RUN pip install -r requirements.txt
RUN python -m pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.8.0/en_core_web_lg-3.8.0-py3-none-any.whl

# 4️⃣ Copy your application last (changes often)
COPY . .

# Run app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
