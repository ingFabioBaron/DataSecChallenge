# ===========================
#  DataSecChallenge – Makefile
#  Compatible con Windows + GNU Make (winget / ezwinports)
#  Compatible con Linux y macOS
# ===========================

# --- Variables globales ---
PYTHON = poetry run python
PYTEST = poetry run pytest --log-cli-level=INFO
RUFF   = poetry run ruff
BLACK  = poetry run black

# ===========================
# Instalación de dependencias
# ===========================
install:
	poetry install

# ===========================
# Linter y formateador
# ===========================
lint:
	$(RUFF) check .

fmt:
	$(BLACK) .

fmt-check:
	$(BLACK) --check .

# ===========================
# Tests
# ===========================
test:
	$(PYTEST)

# ===========================
# Ejecutar Challenges
# ===========================
run-ch1:
	$(PYTHON) challenges/c01_minesweeper/solution_minesweeper.py

# Aquí se agregarán comandos para los retos 2, 3 y 4 cuando los implementemos.
# Ejemplo (futuro):
# run-ch2:
# 	$(PYTHON) challenges/c02_best_in_genre/solution_best_in_genre.py

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
# Ayuda (mostrar comandos disponibles)
# ===========================
help:
	@echo "Comandos disponibles:"
	@echo ""
	@echo "  make install        -> Instala dependencias con Poetry"
	@echo "  make test           -> Ejecuta los tests con Pytest"
	@echo "  make lint           -> Ejecuta ruff"
	@echo "  make fmt            -> Formatea el código con Black"
	@echo "  make fmt-check      -> Verifica formato sin modificar archivos"
	@echo "  make run-ch1        -> Ejecuta el Challenge 1"
	@echo "  make clean          -> Limpia archivos temporales"
