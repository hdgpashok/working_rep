FROM python:3.11-slim

# Установка необходимых инструментов для pip и psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем только requirements для кэширования
COPY requirements.txt .

# Устанавливаем зависимости через pip
RUN pip install -r requirements.txt

# Копируем весь проект
COPY . .

ENV PYTHONPATH=/app

CMD ["python", "src/main.py"]
