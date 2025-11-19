# ===========================
#  DataSecChallenge – Makefile
# ===========================

# --- Variables globales ---
PYTHON = poetry run python
PYTEST = poetry run pytest --log-cli-level=INFO
RUFF   = poetry run ruff

# ===========================
# Instalación de dependencias
# ===========================
install:
	poetry install

# ===========================
# Linter
# ===========================
lint:
	$(RUFF) check .

# ===========================
# Tests
# ===========================
test:
	$(PYTEST)

# ===========================
# Ejecutar Challenges
# ===========================
run-ch1:
	$(PYTHON) challenges/c01_minesweeper/run.py

run-ch2:
	$(PYTHON) challenges/c02_best_in_genre/run.py

run-ch3:
	$(PYTHON) challenges/c03_sql_failures/run.py

run-ch4:
	@echo "Running Challenge 4 - Summarizer (bullet)"
	$(PYTHON) challenges/c04_summarizer/solution_summarizer.py summarize --type bullet
	@echo ""
	@echo "Running Challenge 4 - Summarizer (medium)"
	$(PYTHON) challenges/c04_summarizer/solution_summarizer.py summarize --type medium
	@echo ""
	@echo "Running Challenge 4 - Summarizer (short)"
	$(PYTHON) challenges/c04_summarizer/solution_summarizer.py summarize --type short

# ===========================
# Limpieza
# ===========================
clean:
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf .pytest_cache
	rm -rf */.pytest_cache
	rm -rf *.pyc *.pyo *.pyd || true

# ===========================
# Ayuda
# ===========================
help:
	@echo "Comandos disponibles:"
	@echo ""
	@echo "  make install        -> Instala dependencias con Poetry"
	@echo "  make test           -> Ejecuta los tests con Pytest"
	@echo "  make lint           -> Ejecuta ruff"
	@echo "  make run-ch1        -> Ejecuta el Challenge 1"
	@echo "  make run-ch2        -> Ejecuta el Challenge 2"
	@echo "  make run-ch3        -> Ejecuta el Challenge 3"
	@echo "  make run-ch4        -> Ejecuta el Challenge 4 (3 tipos de resumen)"
	@echo "  make clean          -> Limpia archivos temporales"
