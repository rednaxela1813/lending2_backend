#!/bin/bash
set -e

echo "⏳ Ожидание базы данных..."
until nc -z db 5432; do
  echo "⏱️ Ждём PostgreSQL (db:5432)..."
  sleep 1
done

echo "✅ База доступна. Применяем миграции..."
python manage.py migrate --noinput

ENVIRONMENT=${ENV:-development}

if [ "$ENVIRONMENT" = "development" ]; then
  echo "⚡ DEV: Устанавливаем зависимости Tailwind..."
  npm install --prefix theme/static_src

  echo "⚡ DEV: Строим Tailwind CSS..."
  python manage.py tailwind build
else
  echo "⚡ PROD: Устанавливаем зависимости Tailwind..."
  npm install --prefix theme/static_src

  echo "⚡ PROD: Строим Tailwind CSS..."
  python manage.py tailwind build

  echo "📂 PROD: Собираем статические файлы..."
  python manage.py collectstatic --noinput
fi

echo "🚀 Запускаем Gunicorn..."
exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000
