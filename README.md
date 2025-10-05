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
git clone https://github.com/colibri-the-bird/LLogM-prototype_0.1


# 2) Установка окружения (venv + зависимости + pre-commit)
make setup


# 3) Проверка GPU и PyTorch
make sanity

# 4) После запуска:
make onstart
