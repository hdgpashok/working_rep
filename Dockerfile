FROM python:3.11

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-root --no-interaction --no-ansi

COPY . .

ENV PYTHONPATH=/app

CMD ["python", "src/main.py"]
