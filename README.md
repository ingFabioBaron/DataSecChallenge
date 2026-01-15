# 🚀 Solución al Mercado Libre DataSec Challenge

## 🌟 Descripción General del Proyecto

Este repositorio contiene la **implementación completa** de la prueba técnica solicitada para el **Mercado Libre DataSec Challenge**.

La solución está desarrollada principalmente en **Python 3.11.9**, con una sección en **GoLang (versión 1.25.5)** para el Challenge 4. Está organizada bajo una arquitectura de **monorepo**. Cada desafío reside en su propia carpeta bajo `challenges/`, lo que garantiza la **modularidad e independencia** de las soluciones.

El Challenge 4 (`c04_summarizer`) es el foco de la migración, con la versión Python en `c04_summarizer_py` y la versión Go en `c04_summarizer`.

## 🎯 Enfoque y Metodología

La solución se desarrolló priorizando la **calidad, la automatización y la mantenibilidad** del código:

- **Modularidad:** Cada reto está autocontenido y diseñado para ser ejecutable de forma independiente.
- **Gestión de Dependencias:** Utilización de **Poetry** (Python) y **Go Modules** (Go) para entornos aislados.
- **Automatización Nativa:** Makefile optimizado para entornos **Windows (PowerShell)** y Unix.

## 🛠️ Tecnologías y Herramientas de Desarrollo

| Categoría          | Tecnología/Librería | Versión        | Propósito                                                  |
|-------------------|---------------------|----------------|------------------------------------------------------------|
| **Lenguaje Base** | Python               | 3.11.9         | Plataforma de desarrollo principal.                        |
| **Lenguaje Go** | GoLang              | 1.25.5         | Utilizado para la migración del Challenge 4.              |
| **CLI Framework** | Cobra               | 1.10.2+        | Construcción de interfaces de línea de comandos en Go.     |
| **Env Vars** | godotenv            | 1.5.1+         | Carga de variables de entorno en Go.                      |
| **Gestión Env** | Poetry              | 2.x            | Gestión de dependencias de Python.                        |
| **Análisis** | Ruff / go fmt       | -              | Linting y formateo automático de código.                  |

## ⚙️ Instalación y Preparación

### 1. Requisitos Previos
* **Poetry 2.x**: Para la gestión de Python.
* **GoLang 1.25.5**: Para la ejecución y compilación de Go.
* **Make**: Recomendado para automatización.

### 2. Configuración
```bash
git clone https://github.com/ingFabioBaron/DataSecChallenge.git
cd DataSecChallenge
poetry install
go mod tidy
```

### 3. Configuración e Instalación de Dependencias

Ejecute los siguientes comandos para crear el entorno virtual de Python y resolver todas las dependencias:
```bash
poetry install
```

Para las dependencias de Go, una vez que haya configurado el módulo principal (ya hecho en este punto si está siguiendo la migración), Go gestionará automáticamente las dependencias. Sin embargo, puede ejecutar:
```bash
go mod tidy
```

### 4. Verificación y Ejecución Manual de Tareas

#### 4.1. Verificar si tiene Make instalado

En **Windows** (PowerShell o CMD):
```bash
make --version
```

Si ve un mensaje como: `'make' no se reconoce...`, entonces Make no está instalado.

En **Linux o macOS**:
```bash
make --version
```

Make suele venir preinstalado.

#### 4.2. Ejecutar sin Make (Comandos Manuales)

Si no tiene Make, puede utilizar los comandos nativos de **Poetry** (para Python) o **Go** directamente para ejecutar las tareas de desarrollo:

| Tarea                      | Comando Manual                                            | Comando con Make        |
|----------------------------|-----------------------------------------------------------|-------------------------|
| **Instalar dependencias** | `poetry install`                                          | `make install`          |
| **Análisis Estático** | `poetry run ruff check .` && `go fmt ./challenges/...`    | `make lint`             |
| **Compilar Challenge 4** | `go build -o bin/summarizer ./challenges/c04_summarizer/solution_summarizer.go` | `make build-ch4`        |
| **Correr Tests (Python)** | `poetry run pytest`                                       | `make test`             |
| **Correr Tests (Go)** | `go test ./challenges/c04_summarizer/summarizer -v`      | `make test-ch4`         |
| **Ejecutar Challenge 1** | `poetry run python challenges/c01_minesweeper/run.py`     | `make run-ch1`          |
| **Ejecutar Challenge 2** | `poetry run python challenges/c02_best_in_genre/run.py`   | `make run-ch2`          |
| **Ejecutar Challenge 3** | `poetry run python challenges/c03_sql_failures/run.py`    | `make run-ch3`          |
| **Ejecutar Ch4 (Python)** | `poetry run python challenges/c04_summarizer_py/solution_summarizer.py summarize --type short` | `make run-ch4-py`       |
| **Ejecutar Ch4 (Go)** | `go run ./challenges/c04_summarizer --type short`         | `make run-ch4`          |
| **Limpiar Proyecto** | `powershell -Command "..."` (ver Makefile)                | `make clean`            |    |

#### 4.3. ⭐ Recomendación de Instalación (Windows)

Si está en Windows y desea usar Make (opción recomendada), puede instalarlo fácilmente mediante:

- **Git Bash:** (Viene incluido con la instalación estándar)
- **WSL (Ubuntu):** `sudo apt install make`
- **MSYS2:** `pacman -S make`
- **Windows (nativo):** `winget install ezwinports.make`

## 🧩 Variables de Entorno (Archivo `.env.example`)

El proyecto requiere la configuración de algunas variables de entorno para su correcta ejecución, especialmente en el **Challenge 4**. Se proporciona el archivo `.env.example` que debe ser copiado a un archivo **`.env`** y rellenado.

| Variable          | Challenge   | Descripción y Obligatoriedad                     |
|-------------------|-------------|--------------------------------------------------|
| **`LOG_LEVEL`**   | Transversal | Nivel de logging para todo el proyecto (ej: `INFO`, `DEBUG`). |
| **`DB_PATH`**     | Challenge 3 | Ruta local para el archivo de la base de datos SQLite.          |
| **`HF_API_TOKEN`**| Challenge 4 | **Obligatorio.** Token de API de HuggingFace necesario para el funcionamiento del Summarizer (Python y Go). |
| **`HF_MODEL`**    | Challenge 4 | Opcional. Permite especificar un modelo diferente para el Summarizer (Python y Go). |
| **`ARTICLE_PATH`**| Challenge 4 | Ruta al archivo de texto que se utilizará como artículo de entrada por defecto para la versión Go. Por defecto `articles/article.txt` si no se proporciona. |

## 🚀 Automatización de Tareas (Makefile)

El proyecto incluye un `Makefile` robusto, diseñado específicamente para ser **100% compatible con Windows PowerShell**, eliminando los errores comunes de comandos Unix (como `rm` o `mkdir -p`) en entornos Windows.

> **Nota:** Todos los comandos listados pueden ejecutarse manualmente utilizando `poetry run ...` para Python o comandos nativos de `go` si no dispone de la herramienta Make.

| Categoría | Tarea | Comando Make | Descripción |
| :--- | :--- | :--- | :--- |
| **Utilidades** | Instalación | `make install` | Instala dependencias de Python mediante Poetry. |
| | Calidad | `make lint` | Ejecuta `ruff` (Python) y `go fmt` (Go) para limpieza de código. |
| | Compilación | `make build-ch4` | Genera el binario ejecutable de Go en la carpeta `bin/`. |
| | Ayuda CLI | `make help-ch4` | Muestra la ayuda dinámica (flags y ejemplos) del summarizer en Go. |
| | Limpieza | `make clean` | Elimina caches de Python y borra la carpeta de binarios `bin/`. |
| **Tests** | Python | `make test` | Ejecuta la suite completa de pruebas unitarias con Pytest. |
| | Go | `make test-ch4` | Ejecuta los tests unitarios específicos del reto 4 en Go. |
| **Ejecución** | Challenges 1-3 | `make run-chX` | Ejecuta los desafíos 1, 2 o 3 desarrollados en Python. |
| | Challenge 4 (Py) | `make run-ch4-py` | Ejecuta la versión Python del Summarizer (3 modalidades). |
| | Challenge 4 (Go) | `make run-ch4` | Ejecuta la versión Go del Summarizer (3 modalidades). |
| | Ayuda General | `make help` | Muestra el menú de comandos disponibles en la terminal. |    |

## 📂 Estructura del Proyecto
```text
DataSecChallenge/
├── .github/               <- Configuración de flujos de trabajo GitHub
├── .idea/                 <- Configuración de entorno PyCharm/IntelliJ
├── bin/                   <- Binarios compilados de Go (ej. summarizer.exe)
├── challenges/            <- Directorio principal de desafíos
│   ├── c01_minesweeper/   <- Desafío 1: Lógica de Buscaminas (Python)
│   ├── c02_best_in_genre/ <- Desafío 2: Análisis de datos de películas (Python)
│   ├── c03_sql_failures/  <- Desafío 3: Reporte de fallas SQL (Python)
│   ├── c04_summarizer/    <- Desafío 4: Summarizer GenAI (Versión Go)
│   │   ├── articles/      <- Documentos de texto de entrada
│   │   ├── summarizer/    <- Lógica interna y paquetes de Go
│   │   └── solution_summarizer.go
│   └── c04_summarizer_py/ <- Desafío 4: Summarizer GenAI (Versión Python)
├── common/                <- Funcionalidades compartidas (Logging, etc.)
├── .env                   <- Variables de entorno locales
├── .env.example           <- Plantilla de configuración de entorno
├── .gitignore             <- Archivos excluidos del control de versiones
├── database.sqlite3       <- Base de datos local para Challenge 3
├── go.mod                 <- Definición del módulo de Go
├── go.sum                 <- Sumas de verificación de dependencias de Go
├── Makefile               <- Automatización de tareas (Multi-plataforma)
├── poetry.lock            <- Registro exacto de dependencias Python
├── pyproject.toml         <- Configuración de dependencias y herramientas Poetry
└── README.md              <- Documentación principal del proyecto
```

## 💡 Navegación a los Challenges Individuales

Para evaluar cada solución, diríjase a los directorios específicos. La documentación detallada para cada desafío se encuentra en su respectivo `README.md`.

| Challenge | Título del Challenge | Carpeta | Acceder a la Documentación |
|-----------|----------------------|---------|----------------------------|
| **Challenge 1** | Minesweeper | `c01_minesweeper/` | [Ver README Detallado](challenges/c01_minesweeper/README.md) |
| **Challenge 2** | Best In Genre | `c02_best_in_genre/` | [Ver README Detallado](challenges/c02_best_in_genre/README.md) |
| **Challenge 3** | SQL Failures | `c03_sql_failures/` | [Ver README Detallado](challenges/c03_sql_failures/README.md) |
| **Challenge 4 (Go)** | Summarizer | `c04_summarizer/` | [Ver README Detallado (Go)](challenges/c04_summarizer/README.md) |
| **Challenge 4 (Python)**| Summarizer | `c04_summarizer_py/` | [Ver README Detallado (Python)](challenges/c04_summarizer_py/README.md) |

## 👤 Autor y Contacto

Si tiene alguna pregunta sobre la implementación o las decisiones de diseño, no dude en contactarme.

- **Autor:** Fabio Barón
- **LinkedIn:** [www.linkedin.com/in/fabio-baron-barrera](https://www.linkedin.com/in/fabio-baron-barrera)
- **Email:** fabiaon@gmail.com

## 📄 Licencia

Este proyecto fue desarrollado únicamente con fines **académicos y de evaluación técnica** para el proceso de selección.
