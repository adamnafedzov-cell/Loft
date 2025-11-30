FROM python:3.11-slim

# Устанавливаем зависимости системы (если нужны)
RUN apt-get update && apt-get install -y build-essential libpq-dev --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем файлы
COPY . /app

# Создаем папки для БД и логов
RUN mkdir -p /app/data /app/logs

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Переменная порта (Render задаёт PORT)
ENV PORT=8000

EXPOSE 8000

# Запуск
CMD ["python", "bot.py"]
