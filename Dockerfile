FROM python:3.11

WORKDIR /app

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Отключаем виртуальные окружения
RUN poetry config virtualenvs.create false

# Копируем зависимости
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости без установки самого проекта
RUN poetry install --only main --no-root --no-interaction --no-ansi

# Копируем весь код
COPY . .

# Указываем Python, где искать пакеты
ENV PYTHONPATH=/app

# Запуск
CMD ["python", "src/main.py"]
