# Этап сборки: создаем wheels
FROM python:3.13-slim AS builder

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "poetry" && poetry self add poetry-plugin-export

WORKDIR /app
RUN mkdir /wheels

COPY pyproject.toml poetry.lock* /app/

RUN poetry export -f requirements.txt --output /wheels/requirements.txt \
  && pip wheel --no-deps --wheel-dir=/wheels -r /wheels/requirements.txt \
  && pip wheel --no-deps --wheel-dir=/wheels uvicorn

FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /wheels /wheels

RUN pip install --no-cache-dir --no-index --find-links=/wheels uvicorn \
  && pip install --no-cache-dir --no-index --find-links=/wheels -r /wheels/requirements.txt \
  && rm -rf /wheels

COPY . /app/

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
