FROM python:3.13-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir uv && uv sync --frozen --no-dev
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
