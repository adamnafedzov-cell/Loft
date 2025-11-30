# Loft Cafe — Telegram feedback bot

Сбор отзывов через QR-коды на столах. Бот принимает отзыв, сохраняет в SQLite и пересылает в админ-группу. Встроенная простая админ-панель (FastAPI) для просмотра/удаления отзывов.

## Что в репозитории
- `bot.py` — основной запуск (бот + веб-админпанель)
- `handlers/` — обработчики aiogram
- `utils/` — временное состояние
- `db.py` — работа с SQLite
- `admin_app.py` — админ-панель (FastAPI)
- `requirements.txt` — зависимости
- `Dockerfile` — контейнеризация

## Быстрый старт (локально)
1. Скопируйте репозиторий.
2. Создайте виртуальное окружение:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS / Linux
   .venv\Scripts\activate     # Windows
