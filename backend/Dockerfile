# Используем официальный образ с предустановленным uv и Python 3.13
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

WORKDIR /app

# Копируем только файлы зависимостей
COPY pyproject.toml uv.lock ./

ENV UV_SYSTEM_PYTHON=1
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

COPY . .

CMD ["python", "main.py"]