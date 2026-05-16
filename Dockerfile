# DieKomiteeApp – Dockerfile (Multi-Stage Build)
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final Stage
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5003

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5003
ENV SECRET_KEY=dev-secret-key-bitte-aendern-in-produktion
ENV DATABASE_URL=sqlite:////app/instance/wortmeldung.db

RUN mkdir -p /app/instance

CMD ["python", "-m", "flask", "run"]
