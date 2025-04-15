#!/bin/bash

# Ждём, пока база будет доступна
echo "⏳ Ожидание базы данных..."
until nc -z db 5432; do
  echo "⏱️ Ждём PostgreSQL (db:5432)..."
  sleep 1
done

echo "✅ База доступна. Применяем миграции..."
python manage.py migrate --noinput

echo "📂 Собираем статические файлы..."
python manage.py collectstatic --noinput

echo "🚀 Запускаем Gunicorn..."
exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000
