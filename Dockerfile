# Usa una imagen oficial de Python 3.11
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala las dependencias
RUN pip install --upgrade pip \
    && pip install flet supabase

# Puerto donde correrá la app
EXPOSE 8501

# Comando para ejecutar tu app (ajústalo si tu archivo principal no se llama main.py)
CMD ["python", "main.py"]
