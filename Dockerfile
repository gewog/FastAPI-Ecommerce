# Используем официальный образ Python
FROM python:3.13-slim as builder

# Устанавливаем Poetry
RUN pip install poetry

# Копируем только файлы, необходимые для установки зависимостей
WORKDIR /app
COPY app/backend/.env /app/app/backend/.env
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости (включая dev-зависимости для тестов)
RUN poetry config virtualenvs.create false && \
    poetry install --with dev

# Копируем остальные файлы проекта
COPY . .

# Собираем финальный образ
FROM python:3.13-slim

# Устанавливаем системные зависимости (если нужны)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Копируем установленные зависимости из builder-образа
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app .

# Запускаем приложение
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
