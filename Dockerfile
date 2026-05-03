# — Etapa base ————————————————————————————————————————————
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# — Dependencias Python ———————————————————————————————————
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# — Código fuente —————————————————————————————————————————
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
