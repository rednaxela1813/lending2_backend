#!/bin/bash

echo "⏳ Ожидание базы данных..."
until nc -z db 5432; do
  echo "⏱️ Ждём PostgreSQL (db:5432)..."
  sleep 1
done

echo "✅ База доступна. Применяем миграции..."
python manage.py migrate --noinput

echo "⚡ Устанавливаем зависимости Tailwind..."
npm install --prefix theme/static_src

echo "⚡ Строим Tailwind CSS..."
python manage.py tailwind build

echo "📂 Собираем статические файлы..."
python manage.py collectstatic --noinput

echo "🚀 Запускаем Gunicorn (production)..."
exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000
