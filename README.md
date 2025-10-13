# 1) LLogM Prototype на RunPod

Краткое руководство по запуску и обслуживанию окружения на RunPod для проекта **LLogM-prototype_0.1**. Документ ориентирован на воспроизводимость и минимальное количество ручных действий. Добавлен модуль **hwr64** (распознавание рукописных символов 64×64) с автозагрузкой датасетов и базовой тренировкой.

## Требования
- Pod на базе образа с PyTorch и CUDA (например, *RunPod PyTorch 2.8.0, Ubuntu 22.04*).
- Постоянный том, примонтированный в `/workspace`.
- Доступ по SSH к Pod.
- Рекомендуется использовать виртуальное окружение Python (создаётся автоматически командой `make setup`).

## Быстрый старт (первый запуск на новом Pod)
```bash
cd /workspace
git clone https://github.com/colibri-the-bird/LLogM-prototype_0.1
cd LLogM-prototype_0.1

# (опционально) локальный .env на основе примера
cp .env.example .env

# установка окружения: venv, зависимости, pre-commit, editable‑install
make setup

# проверка работоспособности
. .venv/bin/activate
llogm sanity
# или альтернативно:
make sanity   # выведет nvidia-smi и выполнит короткий CUDA‑тест
```

## Автозапуск после старта Pod
Предпочтительный способ — задать **Start Script** в шаблоне Pod:
```bash
bash /workspace/LLogM-prototype_0.1/scripts/onstart.sh
```
Альтернатива вручную после запуска Pod:
```bash
make onstart
```

## Повседневная работа
```bash
cd /workspace/LLogM-prototype_0.1
. .venv/bin/activate

# пример: базовый прогон CLI
llogm extract --input README.md --output data/processed/sample.json

# пример: запуск пользовательского скрипта через Accelerate
accelerate launch   --config_file configs/accelerate.yaml   your_script.py --arg1 foo --arg2 bar

# пример: подготовка к torchrun (DDP на более позднем этапе)
# source configs/torch_distributed.env
# torchrun --nproc_per_node=1 your_script.py
```

## Основные команды (Makefile)
- `make setup` — создание venv, установка зависимостей, подключение pre‑commit, установка пакета в editable‑режиме.
- `make onstart` — идемпотентная подготовка Pod (apt‑утилиты, venv, зависимости, первичная проверка).
- `make sanity` — проверка GPU через `nvidia-smi` и короткий тест CUDA.
- `make hf-login` — вход в Hugging Face (использует `HF_TOKEN` из `.env`, если задан).
- `make fmt` — автоформатирование и линтинг (black/ruff).
- `make clean` — удаление venv и кэшей.
- `make print-env` — вывод ключевых переменных окружения для диагностики.

---

# 2) Модуль hwr64 (64×64 Handwriting)

Модуль расположен в `hwr64/` и включает:
- `configs/` — конфигурации модели и реестр датасетов `datasets.yaml`.
- `scripts/` — утилиты, включая автозагрузчик датасетов `fetch_datasets.py`.
- `src/` — код моделей и тренировки (скелет для smoke‑тестов).
- `data/` — каталоги данных (`raw/`, `processed/`).
- `runs/`, `out/` — логи, чекпоинты, экспорт.

## Полная инициализация hwr64 (с нуля)

1) Установка зависимостей для работы с данными
```bash
make hwr64-data-setup
```

2) (Опционально) Настройка Kaggle CLI для загрузки некоторых датасетов
```bash
pip install kaggle
mkdir -p ~/.kaggle
# скопируйте kaggle.json в ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
```

3) Автозагрузка датасетов (все публичные; «ручные» наборы будут пропущены с инструкциями)
```bash
make hwr64-data-all
```

Загрузка отдельного набора (пример: только MNIST):
```bash
make hwr64-data ONE=mnist
```

Проверка контрольных сумм и индексирование вручную добавленных наборов
```bash
make hwr64-data-verify
```

> Источник конфигурации: `hwr64/configs/datasets.yaml`.
> Папка назначения по умолчанию: `hwr64/data/raw/<dataset>`.
> Наборы, требующие регистрации (IAM, CASIA), имеют `method: manual`.

## Обучение и экспорт

Быстрый smoke‑тест обучения (1 эпоха, 5% данных):
```bash
python -m hwr64.src.train --cfg hwr64/configs/a2_cr_lite.yaml --epochs 1 --data-frac 0.05
```

Базовое обучение CR‑Lite (классификация символа):
```bash
make hwr64-train-a2
```

Экспорт в ONNX и квантизация int8:
```bash
make hwr64-export
make hwr64-quant
```

Выгрузка артефактов на локальную машину (пример):
```bash
# модель (ONNX int8)
scp -i "$HOME/.ssh/id_ed25519" \
  USERNAME@ssh.runpod.io:/workspace/LLogM-prototype_0.1/hwr64/out/model_int8.onnx \
  ./model_int8.onnx

# синхронизация чекпоинтов
rsync -avz -e "ssh -i $HOME/.ssh/id_ed25519" \
  USERNAME@ssh.runpod.io:/workspace/LLogM-prototype_0.1/hwr64/runs/checkpoints/ \
  ./checkpoints/
```

## Дополнительные цели Makefile (hwr64)
- `hwr64-data-setup` — установка зависимостей для работы с данными.
- `hwr64-data-all` — загрузка всех поддерживаемых публичных датасетов.
- `hwr64-data ONE=<имя>` — выборочная загрузка датасета (см. `hwr64/configs/datasets.yaml`).
- `hwr64-data-verify` — проверка контрольных сумм и индексирование «ручных» наборов.
- `hwr64-train-a2` — обучение базовой модели CR‑Lite.
- `hwr64-export` — экспорт модели в ONNX.
- `hwr64-quant` — динамическая квантизация в int8 (ONNX Runtime).
- `hwr64-hpo-bo` — каркас для BO‑поиска гиперпараметров (qMES; требует доработки).
- `hwr64-hpo-refine` — локальная доводка гиперпараметров методом имитации отжига.

---

# 3) Конфигурация окружения

**`.env` и `configs/runpod.env`** — базовые переменные окружения:
```ini
HF_HOME=/workspace/.cache/huggingface
TRANSFORMERS_CACHE=/workspace/.cache/huggingface
PIP_CACHE_DIR=/workspace/.cache/pip
TOKENIZERS_PARALLELISM=false
HF_HUB_ENABLE_HF_TRANSFER=1
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
NCCL_IB_DISABLE=1
RUNPOD_MOUNT_PATH=/workspace
# опционально: токен для неинтерактивного входа в HF Hub
# HF_TOKEN=
```

**`configs/docker.args`** — аргументы контейнера, влияющие на стабильность и производительность:
```text
--shm-size 16g
```

**`configs/accelerate.yaml`** — типовая конфигурация для 1×GPU (A5000), `bf16`, без DDP:
```yaml
compute_environment: LOCAL_MACHINE
distributed_type: NO
device_placement: true
mixed_precision: bf16
num_processes: 1
rdzv_backend: static
same_network: true
use_cpu: false
```

**`configs/torch_distributed.env`** — заготовка переменных окружения для `torchrun`/DDP:
```ini
MASTER_ADDR=127.0.0.1
MASTER_PORT=29500
WORLD_SIZE=1
RANK=0
```

---

# 4) Отладка (кратко)
- **`llogm: command not found`** — активируйте venv: `. .venv/bin/activate`; при необходимости выполните `make setup`.
- **`No module named llogm`** — пакет не установлен в editable‑режиме; повторите `make setup`.
- **Ошибки при записи файлов** — CLI создаёт директории вывода автоматически; проверьте корректность аргумента `--output`.
- **CUDA не распознаётся** — убедитесь в корректности образа Pod; выполните `make sanity`.
- **Папка с именем `"$VOL"`** — признак ошибок кавычек в пользовательских скриптах; удалите папку `rm -rf '"$VOL"'` и проверьте, что переменные не заключены в одинарные кавычки.

# 5) Обновление
```bash
git pull
make setup
```

# 6) Зависимости (краткая сводка)
- `transformers`, `datasets` — базовый стек моделей и датасетов.
- `accelerate` — упрощённый запуск и масштабирование обучения.
- `bitsandbytes` — квантование 8/4‑бит на GPU.
- `peft` — адаптеры LoRA и похожие методы без полного дообучения.
- `sentencepiece` — токенизация.
- `trl` — методы обучения с подкреплением (RLHF и др.).
- `huggingface_hub` — загрузка/публикация моделей и весов.
- **Дополнительно для hwr64**: `PyYAML`, `requests`, `opencv-python-headless`, `einops`, `torchmetrics`, `onnx`, `onnxruntime`, `botorch`, `gpytorch`, `optuna`.
