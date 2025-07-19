#!/bin/bash

echo "⏳ Ожидание базы данных..."
until nc -z db 5432; do
  echo "⏱️ Ждём PostgreSQL (db:5432)..."
  sleep 1
done

echo "✅ База доступна. Применяем миграции..."
python manage.py migrate --noinput

echo "📂 Собираем статические файлы..."
python manage.py collectstatic --noinput

if [ "$ENV" = "production" ]; then
  echo "🚀 Запускаем Gunicorn (production)..."
  exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000
else
  echo "🚀 Запускаем Django dev server + Tailwind watcher..."
  # запустить tailwind watcher в фоне
  python manage.py tailwind start &
  # запустить Django dev server
  exec python manage.py runserver 0.0.0.0:8000
fi
