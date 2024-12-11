FROM python:3.11-slim

RUN pip install psycopg2-binary

COPY app.py /app.py

# Definisce il comando da eseguire quando il container viene avviato
CMD ["python", "/app.py"]