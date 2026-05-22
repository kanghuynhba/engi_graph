FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false && poetry install --no-root
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
