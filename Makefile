VENV=.venv
UVICORN=$(VENV)\scripts\uvicorn


.PHONY: run
run:
	$(UVICORN) "src.main:app" --host localhost --port 8000 --reload
