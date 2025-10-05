# LLogM Prototype — репозиторий для RunPod (RU)


Готовый каркас, чтобы поднимать новый GPU‑Pod без ручной настройки.


## Требования
- Под на базе образа с PyTorch и CUDA (например, шаблон RunPod PyTorch 2.8.0, Ubuntu 22.04)
- Директория `/workspace` примонтирована как постоянный том
- Доступ по SSH в Pod


## Быстрый старт (первый запуск на новом Pod)


```bash
# 1) Клонируем репозиторий в постоянный том
cd /workspace
git clone <ваш-remote> llogm # или mkdir llogm && cd llogm && git init
cd llogm


# 2) Локальные переменные окружения
cp .env.example .env # при желании отредактируйте .env


# 3) Установка окружения (venv + зависимости + pre-commit)
make setup


# 4) Проверка GPU и PyTorch
make sanity
