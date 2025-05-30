# AIogram Telegram Bot (v3.16.0)

Этот проект — телеграм-бот, реализованный с использованием библиотеки [aiogram](https://docs.aiogram.dev/en/latest/), предназначенный для автоматизации различных задач и взаимодействия с пользователями.

## Описание

Бот включает в себя:

- Обработку команд и сообщений
- Регистрацию новых пользователей
- Административные функции
- Планировщик задач (cron) для автоматических сообщений
- Модульную структуру с роутерами

## Особенности

- Использование `aiogram` версии 3.16.0
- Конфигурация через отдельный модуль `config_data`
- Планировщик задач с помощью `apscheduler`
- Логирование работы бота

## Установка и запуск

1. **Клонируйте репозиторий**

```bash
git clone https://github.com/MaminAmetist/aiogram-3.16.0.git
cd aiogram-3.16.0
```

2. **Создайте виртуальное окружение и активируйте его**

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

3. **Установите зависимости**

```bash
pip install -r requirements.txt
```

*Обратите внимание:* В файле `requirements.txt` должны быть указаны все необходимые библиотеки, например:

```
aiogram==3.16.0
apscheduler
```

4. **Настройте конфигурацию**

В файле `config_data/config.py` должен быть реализован модуль `load_config()`, который загружает токен бота и другие параметры.

Пример файла конфигурации (`config.py`):

```python
from dataclasses import dataclass

@dataclass
class TgBot:
    token: str

@dataclass
class Config:
    tg_bot: TgBot

def load_config() -> Config:
    return Config(tg_bot=TgBot(token='ВАШ_ТОКЕН_ТЕЛЕГРАММ_БОТА'))
```

Замените `'ВАШ_ТОКЕН_ТЕЛЕГРАММ_БОТА'` на ваш реальный токен.

5. **Запустите бота**

```bash
python main.py
```

6. **Бот запустится и начнет работу, автоматически отправляя запланированные сообщения по расписанию**

## Структура проекта

- `main.py` — основной файл запуска бота и настройки планировщика.
- `handlers/` — папка с обработчиками команд и сообщений.
  - `admin.py` — административные команды.
  - `registration_user.py` — обработка регистрации пользователей.
  - `other_handlers.py` — дополнительные обработчики.
- `time_messages.py` — функции для отправки запланированных сообщений.
- `config_data/` — конфигурационные файлы.

## Использование

После запуска бот готов к взаимодействию через Telegram:

- Отправляйте команды, определенные в обработчиках.
- Пользователи могут регистрироваться, получать уведомления или выполнять другие действия, реализованные в обработчиках.
