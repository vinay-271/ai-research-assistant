FROM python:3.10-slim

# Prevent python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build dependencies for compiling packages if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first to cache dependency layers
COPY requirements.txt .

# Install CPU-only PyTorch first (to prevent CUDA download size bloat)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install remaining backend requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy application folders
COPY app/ ./app/

# Copy local data states and reports to bake them into the image
COPY chroma_db/ ./chroma_db/
COPY reports/ ./reports/
COPY alpha_vantage_data/ ./alpha_vantage_data/

# Expose port FastAPI runs on
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
