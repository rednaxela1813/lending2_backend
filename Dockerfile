FROM python:3.13-slim-bullseye

# Установить зависимости
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    ca-certificates \
    python3-pip \
    netcat-openbsd \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Установить зависимости Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Скопировать весь проект
COPY . .

# Настроить entrypoint
RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
