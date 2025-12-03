# Resume Redactor Service

A privacy-focused microservice that automatically redacts sensitive personal information (names, emails, phone numbers, URLs) from resume PDFs using advanced NLP and computer vision techniques.

## 🚀 Features

- **Automated PII Detection**: Identifies and redacts personal information using Microsoft Presidio
- **PDF Processing**: Converts PDF resumes to images, redacts sensitive data, and reconstructs PDFs
- **REST API**: Simple HTTP endpoint for easy integration
- **Docker-Ready**: Fully containerized with Docker Compose for one-command deployment
- **Production-Grade**: Includes health checks, persistent storage, and automatic restart policies

## 📋 Prerequisites

- Docker 20.10 or higher
- Docker Compose 1.29 or higher
- 2GB+ available RAM (for OCR and NLP models)

## 🏃 Quick Start

### 1. Clone or Download the Project

```bash
git clone <your-repo-url>
cd RedactService
```

### 2. Start the Service

```bash
docker-compose up -d
```

The service will be available at `http://localhost:8000`

### 3. Verify Service is Running

```bash
curl http://localhost:8000/docs
```

You should see the FastAPI interactive documentation (Swagger UI).

## 📡 API Usage

### Endpoint: `POST /anonymize`

Accepts a PDF resume and returns a redacted version with sensitive information removed.

**Using cURL:**

```bash
curl -X POST "http://localhost:8000/anonymize" \
  -H "accept: application/pdf" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/resume.pdf" \
  --output anonymized_resume.pdf
```

**Using Python:**

```python
import requests

with open("resume.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/anonymize",
        files={"file": f}
    )

with open("anonymized_resume.pdf", "wb") as out:
    out.write(response.content)
```

**Using Postman:**

1. Set method to `POST`
2. URL: `http://localhost:8000/anonymize`
3. Body → form-data
4. Key: `file` (type: File)
5. Value: Select your PDF file
6. Send → Save response as PDF

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Available options:
- `SERVICE_MODE`: Operation mode (`production` or `development`)
- `CLEANUP_AFTER_HOURS`: Hours before temporary files are cleaned up (default: 6)

### Redacted Entities

The service currently redacts:
- `PERSON`: Names and personal identifiers
- `EMAIL_ADDRESS`: Email addresses
- `PHONE_NUMBER`: Phone numbers (all formats)
- `URL`: Website URLs

To customize, modify the `entities_to_redact_` list in `app.py`.

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────────┐      ┌─────────────┐
│   Client    │─────▶│  FastAPI Server  │─────▶│  Presidio   │
│  (Upload)   │      │   (Port 8000)    │      │  Analyzer   │
└─────────────┘      └──────────────────┘      └─────────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │  Image Redactor │
                     │   + Tesseract   │
                     └─────────────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │   PDF Rebuild   │
                     │   (img2pdf)     │
                     └─────────────────┘
```

**Technology Stack:**
- **FastAPI**: High-performance async web framework
- **Presidio**: Microsoft's data protection framework
- **Tesseract OCR**: Text extraction from images
- **pdf2image & Pillow**: PDF manipulation
- **spaCy**: NLP model for entity recognition

## 🛠️ Development

### Local Development (without Docker)

```bash
# Install dependencies
pip install -r requirements.txt
python -m pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.8.0/en_core_web_lg-3.8.0-py3-none-any.whl

# Run server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Viewing Logs

```bash
docker-compose logs -f resume-redactor
```

### Stopping the Service

```bash
docker-compose down
```

### Rebuilding After Changes

```bash
docker-compose up -d --build
```

## 📦 Deployment

### Production Considerations

1. **Environment Variables**: Set appropriate values in `.env` or docker-compose.yml
2. **Reverse Proxy**: Use nginx or Traefik for SSL termination and load balancing
3. **Resource Limits**: Configure memory/CPU limits in docker-compose.yml
4. **Monitoring**: Add health check endpoints and integrate with monitoring tools
5. **Persistent Storage**: Volume `resume_data` persists across container restarts

### Scaling

For high-volume deployments:
- Use `docker-compose up --scale resume-redactor=3` to run multiple instances
- Add a load balancer (nginx, HAProxy)
- Consider Kubernetes for orchestration

## 🐛 Troubleshooting

**Container won't start:**
```bash
docker-compose logs resume-redactor
```

**Port 8000 already in use:**
Edit `docker-compose.yml` and change `"8000:8000"` to `"8001:8000"` (or any free port)

**Out of memory errors:**
Increase Docker's memory allocation (Docker Desktop: Settings → Resources)

**OCR not working:**
Ensure Tesseract is properly installed in the container (check Dockerfile)

## 📄 License

[Add your license here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📧 Contact

[Add contact information here]
