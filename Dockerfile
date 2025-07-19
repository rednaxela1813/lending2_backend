FROM python:3.13-slim-bullseye

# Установить зависимости для curl и nodejs
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    ca-certificates \
    && curl -fsSL https://deb.nodesource.com/setup_current.x | bash - \
    && apt-get install -y nodejs

# Рабочая директория
WORKDIR /app

# Установить netcat (если нужно для wait-for-db)
RUN apt-get update && apt-get install -y netcat-openbsd

# Установить зависимости Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Скопировать проект
COPY . .

# Настроить entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
