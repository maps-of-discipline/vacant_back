VENV ?= .venv

# Определение пути к uvicorn в зависимости от ОС
ifeq ($(OS),Windows_NT)
    UVICORN := $(VENV)\Scripts\uvicorn.exe
else
    UVICORN := $(VENV)/bin/uvicorn
endif

UNIX_UVICORN := $(VENV)/bin/uvicorn

UVICORN_ARGS := "src.main:app" --host localhost --port 8000 --reload

.PHONY: run urun

## Запуск с учетом текущей ОС
run:
	$(UVICORN) $(UVICORN_ARGS)

## Явный запуск Unix-версии (например, в WSL или CI)
urun:
	$(UNIX_UVICORN) $(UVICORN_ARGS)
