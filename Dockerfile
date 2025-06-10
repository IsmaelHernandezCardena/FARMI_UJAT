FROM python:3.11-slim

WORKDIR /app

# Copiar requerimientos e instalarlos
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

EXPOSE 8501

# Iniciar la app con Flet
CMD ["python", "main.py"]
