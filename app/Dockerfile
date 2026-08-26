FROM python:3.12-slim

# Prevent Python from writing .pyc files
# and buffer logs inside containers.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Install dependencies first to maximize Docker layer caching.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application source.
COPY src ./src

# Create non-root application user.
RUN useradd \
    --create-home \
    --shell /usr/sbin/nologin \
    appuser

USER appuser

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

