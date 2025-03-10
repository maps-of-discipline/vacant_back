VENV=.venv
UVICORN=$(VENV)\bin\uvicorn
UNIX_UVICORN=$(VENV)/bin/uvicorn


.PHONY: run
run:
	$(UVICORN) "src.main:app" --host localhost --port 8000 --reload
	
	
.PHONY: urun
urun:
	$(UNIX_UVICORN) "src.main:app" --host localhost --port 8000 --reload
