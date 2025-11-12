# FastAPI-Ecommerce — Full-Stack Backend for E-Commerce

> **Цель проекта**: Создание полнофункционального backend-сервиса для интернет-магазина с использованием современных инструментов: FastAPI, PostgreSQL, Alembic, Poetry и Docker. Автоматизированная CI/CD (без этапа диплоя) с GitHub Actions.

---

### 🔧 Стек технологий

- **Python 3.13**
- **FastAPI** — веб-фреймворк для API
- **Uvicorn** — ASGI-сервер
- **Pytest**, **httpx** — тестирование
- **GitHub Actions** — CI/CD
- **Poetry** — управление зависимостями
- **Docker** — сборка образов
- **PostgreSQL** — база данных
- **SQLAlchemy** — ORM
- **Alembic** — миграции базы данных

---

### 📦 Файлы проекта

| Файл | Назначение                                                                               |
|------|------------------------------------------------------------------------------------------|
| `app/main.py` | Основной файл приложения с обработчиками `/`                                             |
| `app/backend/main.py` | Основной файл приложения с обработчиками `/auth`, `/categories`, `/products`, `/reviews` |
| `app/backend/models/__init__.py` | Модели SQLAlchemy                                                                        |
| `app/backend/routers/__init__.py` | Роутеры для API                                                                          |
| `app/backend/db.py` | Подключение к PostgreSQL                                                                 |
| `app/backend/settings.py` | Настройки через `pydantic-settings`                                                      |
| `tests/test_main.py` | Тесты с использованием `pytest`, `AsyncClient`, `httpx`                                  |
| `pyproject.toml` | Конфигурация Poetry                                                                      |
| `poetry.lock` | Блокировка версий зависимостей                                                           |
| `Dockerfile` | Сборка Docker-образа                                                                     |
| `.github/workflows/ci.yml` | Автоматический CI/CD пайплайн                                                            |
| `docker-compose.yml` | Запуск PostgreSQL и приложения                                                           |

---

### 🛠 Как запустить локально

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/gewog/FastAPI-Ecommerce.git
   cd FastAPI-Ecommerce
   
### Создайте .env файл:
```bash
cp app/backend/.env.example app/backend/.env
```

Отредактируйте `app/backend/.env` с данными для PostgreSQL.

### Установите зависимости:

```bash
pip install poetry
poetry install
```

### Запустите приложение:

poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


### Проверьте работу:
- `http://localhost:8000/` → `{"STATUS": "OK"}`
- `http://localhost:8000/categories` → список категорий
- `http://localhost:8000/products` → работа с товарами
- `http://localhost:8000/reviews` → отзывы

### 🐳 Как собрать Docker-образ

```bash
docker build -t fastapi-ecommerce:latest .
```

Запустите контейнер: 
```bash
docker run -p 8000:8000 fastapi-ecommerce:latest
```

Или используйте Docker Compose: 
```
docker-compose up --build
```

### 🔁 Как работает CI/CD
При каждом `push` или `pull_request` на ветку `master`:

- Запускается runner `ubuntu-latest`
- Устанавливается Python 3.13
- Устанавливается Poetry
- Выполняется `poetry install`
- Запускаются тесты: `poetry run pytest tests/`
- Собирается Docker-образ
- Проверяется корректность структуры проекта

✅ Все шаги выполняются автоматически.

### 🧪 Тестирование
Запуск тестов:
```
poetry run pytest tests/
```

Тесты проверяют:
- Корректность ответов от эндпоинтов
- Валидацию входных данных (в разработке)
- Асинхронные операции (в разработке)

### 📂 Структура проекта
```
FastAPI-Ecommerce/
описание будет позже
```

### 🔗 Полезные ссылки
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/)
- [GitHub Actions](https://docs.github.com/en/actions)

### 📝 Автор
gewog  
📧 gewoggewog@gmail.com

### 📄 Лицензия
Проект распространяется под лицензией MIT.

<!-- Картинка -->
<div align="center">
  <img src="https://media.tenor.com/PdQfH0XTvfcAAAAj/monster-alien.gif" alt="Демо" width="200" />
</div>

