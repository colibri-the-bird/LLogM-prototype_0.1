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

```
============

Автозапуск после старта Pod

Рекомендуемый вариант — настроить Start Script в шаблоне пода:
```bash
workspace/LLogM-prototype_0.1/scripts/onstart.sh
```
Скрипт создаст venv (если нет), поставит зависимости, прогонит быстрые проверки и подготовит кэш‑директории. Если не хотите трогать шаблон — можно вручную:

make onstart
Повседневная работа
# Под поднялся → onstart всё подготовил
```bash
cd /workspace/LLogM-prototype_0.1
source .venv/bin/activate
```

# Пример запуска скрипта обучения через Accelerate
```bash
accelerate launch \
  --config_file configs/accelerate.yaml \
  your_script.py --arg1 foo --arg2 bar
```

# Или torchrun (DDP позже):
```bash
 source configs/torch_distributed.env && \
 torchrun --nproc_per_node=1 your_script.py
```
Основные команды (Makefile)
```bash
make setup — создать venv, обновить pip, поставить зависимости, подключить pre‑commit

make onstart — идемпотентная инициализация: apt‑утилиты, venv, зависимости, sanity‑чек

make sanity — nvidia-smi и короткий src/check_cuda.py

make hf-login — вход в Hugging Face (использует HF_TOKEN из .env, если задан)

make fmt — автоформатирование (black/ruff)

make clean — удалить venv и кэши компиляции

make print-env — вывести ключевые переменные окружения
```
Конфигурация
```bash
.env и configs/runpod.env
```

Эти файлы настраивают кэши и поведение библиотек:
```bash
HF_HOME=/workspace/.cache/huggingface
TRANSFORMERS_CACHE=/workspace/.cache/huggingface
PIP_CACHE_DIR=/workspace/.cache/pip
TOKENIZERS_PARALLELISM=false
HF_HUB_ENABLE_HF_TRANSFER=1
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
NCCL_IB_DISABLE=1
RUNPOD_MOUNT_PATH=/workspace
```
Опционально добавьте HF_TOKEN в .env для неинтерактивного логина в HF Hub.
```bash
configs/docker.args
```
Аргументы контейнера, важные для производительности:
```bash
--shm-size 16g
configs/accelerate.yaml
```
Готовая конфигурация для одиночного GPU (A5000):
```bash
compute_environment: LOCAL_MACHINE
distributed_type: NO
device_placement: true
mixed_precision: bf16
num_processes: 1
rdzv_backend: static
same_network: true
use_cpu: false
configs/torch_distributed.env
```
Заготовка переменных для будущего torchrun/DDP:
```bash
MASTER_ADDR=127.0.0.1
MASTER_PORT=29500
WORLD_SIZE=1
RANK=0
```

