FROM python:3.11-slim

WORKDIR /app

# 1. Copy and install dependencies first (for caching!)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy all  backend code, folders (Model, Schema), and files
COPY . /app

EXPOSE 8000

# 3. Start your FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]