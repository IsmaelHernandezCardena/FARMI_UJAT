FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip \
    && pip install flet supabase

EXPOSE 8501

CMD ["python", "main.py"]
