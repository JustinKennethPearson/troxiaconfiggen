# Makefile
# Makefile magic taken form https://venthur.de/2021-03-31-python-makefiles.html

PY = python3
VENV = venv
BIN=$(VENV)/bin

$(VENV): requirments.txt
	$(PY) -m venv $(VENV)
	$(BIN)/python -m pip install --upgrade pip	
	$(BIN)/pip install --upgrade -r requirments.txt
standalone : experiments.py $(VENV)
	$(BIN)/pyinstaller --onefile experiments.py 

clean:
	rm -rf $(VENV)
	rm -rf build
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete	



