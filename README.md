# Telegram Channel Forwarder Bot

Бот для автоматической пересылки (копирования) всех сообщений из одного Telegram канала в другой.

## Возможности

- Копирование всех типов сообщений (текст, фото, видео, аудио, документы, голосовые, стикеры и т.д.)
- Работает в реальном времени
- Логирование всех операций
- Поддержка Docker для развёртывания на сервере

---

## Установка

### Способ 1: Клонирование только этой папки (sparse checkout)

```bash
# Создаём директорию и инициализируем репозиторий
mkdir Telegram-Channel-Forwarder-Bot && cd Telegram-Channel-Forwarder-Bot
git init
git remote add origin https://github.com/jesusweb3/Python-Scripts.git

# Настраиваем sparse checkout для загрузки только нужной папки
git sparse-checkout init --cone
git sparse-checkout set Telegram-Channel-Forwarder-Bot

# Загружаем
git pull origin main

# Переходим в папку проекта
cd Telegram-Channel-Forwarder-Bot
```

## Настройка

### 1. Создайте файл `.env`

```bash
cp env.example .env
```

### 2. Заполните переменные окружения

Откройте `.env` и укажите:

```env
# Токен бота от @BotFather
BOT_TOKEN=your_bot_token_here

# ID канала-источника (откуда брать сообщения)
SOURCE_CHANNEL_ID=-1001234567890

# ID канала-назначения (куда пересылать сообщения)
TARGET_CHANNEL_ID=-1001234567890
```

---

## Запуск

### Локальный запуск (без Docker)

```bash
# Создаём виртуальное окружение
python -m venv venv

# Активируем (Linux/macOS)
source venv/bin/activate

# Активируем (Windows)
venv\Scripts\activate

# Устанавливаем зависимости
pip install -r requirements.txt

# Запускаем
python main.py
```

### Запуск в Docker (рекомендуется для сервера)

**Требования:** Docker и Docker Compose

```bash
# Сборка и запуск
docker compose up -d --build

# Просмотр логов
docker compose logs -f

# Остановка
docker compose down

# Перезапуск
docker compose restart
```

---

## Развёртывание на Ubuntu 22.04

### 1. Установка Docker

```bash
# Обновляем систему
sudo apt update && sudo apt upgrade -y

# Устанавливаем Docker
sudo apt install -y docker.io docker-compose-v2

# Добавляем пользователя в группу docker
sudo usermod -aG docker $USER

# Применяем изменения (или перезайдите в систему)
newgrp docker
```

### 2. Загрузка и запуск бота

```bash
# Клонируем репозиторий
git clone https://github.com/jesusweb3/Python-Scripts.git
cd Python-Scripts/Telegram-Channel-Forwarder-Bot

# Создаём .env файл
cp env.example .env
nano .env  # Вводим BOT_TOKEN, SOURCE_CHANNEL_ID, TARGET_CHANNEL_ID

# Запускаем в Docker
docker compose up -d --build

# Проверяем статус
docker compose ps

# Смотрим логи
docker compose logs -f
```

### 3. Управление ботом

```bash
# Просмотр логов в реальном времени
docker compose logs -f

# Перезапуск бота
docker compose restart

# Остановка
docker compose down

# Обновление (после git pull)
docker compose up -d --build
```

---

## Структура проекта

```
Telegram-Channel-Forwarder-Bot/
├── main.py              # Точка входа
├── Dockerfile           # Сборка Docker-образа
├── docker-compose.yml   # Конфигурация Docker
├── .dockerignore        # Исключения для Docker
├── requirements.txt     # Python-зависимости
├── env.example          # Пример переменных окружения
├── .env                 # Ваши переменные (не в Git)
├── logs/                # Логи (создаётся автоматически)
└── src/
    ├── __init__.py
    ├── bot.py           # Обработчики сообщений
    └── utils/
        ├── __init__.py
        ├── config.py    # Конфигурация
        └── logger.py    # Логирование
```


### Контейнер падает
```bash
# Проверьте логи
docker compose logs --tail=50

# Проверьте переменные окружения
cat .env
```

---

## Лицензия

MIT
