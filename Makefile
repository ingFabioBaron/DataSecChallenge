# ===========================
#  DataSecChallenge – Makefile
# ===========================

# --- Variables globales ---
PYTHON   = poetry run python
PYTEST   = poetry run pytest --log-cli-level=INFO
RUFF     = poetry run ruff

# --- Variables de Go ---
GO_CH4_DIR = ./challenges/c04_summarizer
GO_BINARY  = bin/summarizer
GO_FMT     = go fmt $(GO_CH4_DIR)/...

.PHONY: install lint build-ch4 clean test test-ch4 run-ch1 run-ch2 run-ch3 run-ch4-py run-ch4 help-ch4 help

# ===========================
# 1. Utilidades y Configuración
# ===========================

clean:
	@echo "Iniciando limpieza de temporales y binarios..."
	@powershell -Command "Get-ChildItem -Recurse -Include '__pycache__','.pytest_cache' | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue"
	@powershell -Command "if (Test-Path bin) { Remove-Item -Recurse -Force bin }"
	@echo "Limpieza completada con éxito."

install:
	@echo "Instalando dependencias de Python..."
	poetry install

lint:
	@echo "Ejecutando Linter (Python)..."
	$(RUFF) check .
	@echo "Ejecutando Formateo (Go)..."
	$(GO_FMT)

build-ch4:
	@echo "Compilando binario de Go..."
	@powershell -Command "if (!(Test-Path bin)) { New-Item -ItemType Directory -Path bin }"
	go build -o $(GO_BINARY) $(GO_CH4_DIR)/solution_summarizer.go
	@echo "Binario creado con éxito en: $(GO_BINARY)"

help-ch4:
	@echo "Mostrando ayuda del comando summarizer (Go)..."
	go run $(GO_CH4_DIR) --help

# ===========================
# 2. Tests
# ===========================

test:
	@echo "Ejecutando todos los tests de Python..."
	$(PYTEST)

test-ch4:
	@echo "Ejecutando tests unitarios del Challenge 4 (Go)..."
	go test ./challenges/c04_summarizer/summarizer -v

# ===========================
# 3. Ejecución de Challenges
# ===========================

run-ch1:
	@echo "Ejecutando Challenge 1: Minesweeper..."
	$(PYTHON) challenges/c01_minesweeper/run.py

run-ch2:
	@echo "Ejecutando Challenge 2: Best in Genre..."
	$(PYTHON) challenges/c02_best_in_genre/run.py

run-ch3:
	@echo "Ejecutando Challenge 3: SQL Failures..."
	$(PYTHON) challenges/c03_sql_failures/run.py

run-ch4-py:
	@echo "Ejecutando Challenge 4 (Python): Summarizer..."
	$(PYTHON) challenges/c04_summarizer_py/solution_summarizer.py summarize --type short

run-ch4:
	@echo "--- Ejecutando Challenge 4 (Go): 3 Tipos de Resumen ---"
	go run $(GO_CH4_DIR) --type bullet
	@echo ""
	go run $(GO_CH4_DIR) --type medium
	@echo ""
	go run $(GO_CH4_DIR) --type short
	@echo ""
	@echo "--- Ejecutando con Parámetros Completos ---"
	go run $(GO_CH4_DIR) --input $(GO_CH4_DIR)/articles/article.txt --type short --model "Qwen/Qwen2.5-7B-Instruct:together" --api-token ""

# ===========================
# Ayuda General
# ===========================

help:
	@echo ================================================================
	@echo              COMANDOS DISPONIBLES - DataSecChallenge            
	@echo ================================================================
	@echo.
	@echo UTILIDADES:
	@echo   make clean        -^> Borra caches de Python y binarios de Go
	@echo   make install      -^> Instala dependencias con Poetry
	@echo   make lint         -^> Ejecuta ruff (Py) y go fmt (Go)
	@echo   make build-ch4    -^> Compila el binario de Go en bin/	
	@echo   make help-ch4     -^> Ayuda interna del comando summarizer (Cobra)
	@echo.
	@echo TESTS:
	@echo   make test         -^> Ejecuta los tests de Python (Pytest)
	@echo   make test-ch4     -^> Ejecuta los tests unitarios de Go (Ch4)
	@echo.
	@echo EJECUCION DE CHALLENGES:
	@echo   make run-ch1      -^> Ejecuta Challenge 1 (Python)
	@echo   make run-ch2      -^> Ejecuta Challenge 2 (Python)
	@echo   make run-ch3      -^> Ejecuta Challenge 3 (Python)	
	@echo   make run-ch4      -^> Ejecuta Challenge 4 (Go)
	@echo   make run-ch4-py   -^> Ejecuta Challenge 4 (Python)
	@echo.