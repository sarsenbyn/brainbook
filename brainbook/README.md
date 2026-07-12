# Brainbook AI

Brainbook — интеллектуальный инструмент для анализа документов, использующий возможности Google Gemini для глубокого разбора текста.

## 🚀 Основные возможности
* **AI-анализ:** Ответы на вопросы на основе содержания ваших файлов.
* **Минималистичный UI:** Удобный и чистый интерфейс.
* **Docker Ready:** Простой запуск всего стека одной командой.

## 🛠 Технологии
* **Frontend:** React, Vite, TypeScript, Tailwind CSS
* **Backend:** FastAPI, Python 3.12
* **Database:** PostgreSQL
* **AI:** Google Gemini API

## 🏗 Быстрый запуск
```bash
git clone [https://github.com/sarsenbyn/brainbook.git](https://github.com/sarsenbyn/brainbook.git)
cd brainbook

Создайте файл .env на основе примера:
cp .env.example .env

docker compose up --build

⚙️ Переменные окружения

Необходимые переменные в .env:

    SECRET_KEY — ключ для безопасности.

    DATABASE_URL — строка подключения к БД.

    API_KEY — ключ для Gemini API.

    API_KEY_EMBEDDING — ключ для эмбеддингов.

