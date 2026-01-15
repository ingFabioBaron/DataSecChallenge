# Challenge 4 · CLI Summarizer con GenAI (versión Python)

> El enunciado original pedía implementarlo en Go; en este repositorio se resolvió en **Python + Click** para mantener coherencia con el stack del resto de los desafíos.  
> Las funcionalidades, parámetros y comportamiento se respetan 1:1 respecto del requerimiento oficial.

## 📋 Resumen del problema
Construir un CLI que:
- Lea un archivo de texto plano.
- Permita elegir el tipo de resumen (`short`, `medium`, `bullet`).
- Forme un prompt acorde y consuma un modelo de Hugging Face vía API pública.
- Muestre el resumen junto con métricas de reducción.
- Maneje errores de entrada, credenciales y red.

## 🔐 Requisitos previos
| Variable | Obligatoria | Descripción |
|----------|-------------|-------------|
| `HF_API_TOKEN` | Sí | Token de Hugging Face para usar la API de inferencia. |
| `HF_MODEL` | No | Modelo alternativo; por defecto `Qwen/Qwen2.5-7B-Instruct`. |

El archivo `challenges/c04_summarizer/articles/article.txt` se usa como entrada por defecto cuando no se especifica otro.  
El requerimiento oficial pide enlazar la documentación del endpoint genAI utilizado; el código (`summarizer.py`) referencia explícitamente el modelo `Qwen/Qwen2.5-7B-Instruct` y su ficha técnica en Hugging Face: https://huggingface.co/Qwen/Qwen2.5-7B-Instruct.

## 🧠 Estrategia de la solución
1. **CLI con Click** (`solution_summarizer.py`):
   - Comando `summarize` con opciones `--input/-i`, `--type/-t`, `--model/-m`, `--api-token`.
   - Logging integrado (`common.logging_config`) para trazar parámetros y resultados.
2. **Módulo `summarizer.py`**:
   - Carga del texto (`_load_article`) resolviendo rutas relativas/absolutas.
   - Validación del token y modelo.
   - Cliente `huggingface_hub.InferenceClient` en modo chat-completion.
   - Prompts específicos por tipo de resumen (short, medium, bullet).
   - Post-procesamiento para bullets y cálculo de métricas (largo original vs resumen).
3. **Manejo de errores**:
   - Falta de archivo → `SystemExit(1)` con mensaje claro.
   - Token ausente o request fallida → salida controlada, logs con detalles.

Complejidad dominada por la llamada al modelo remoto; el resto del flujo es `O(n)` respecto a la longitud del texto.

## 🗂️ Organización
- `solution_summarizer.py`: CLI y parsing de flags.
- `summarizer.py`: lógica de negocio, prompts y formateo.
- `solution_summarizer_old.py`: versión previa conservada como referencia.
- `articles/article.txt`: entrada por defecto.
- `tests/test_summarizer.py`: fixtures de texto y mocks de la API.
- `run.py`: wrapper que ejecuta el comando con parámetros de ejemplo.

## ▶️ Ejecución
Desde la raíz del repo:

```bash
poetry run python challenges/c04_summarizer/solution_summarizer.py summarize \
  --type bullet \
  --input challenges/c04_summarizer/articles/article.txt
```

Atajos posibles:
```bash
poetry run python challenges/c04_summarizer/solution_summarizer.py summarize -t short
```
Si no se entrega `--input`, se usa el archivo por defecto.

## 🧪 Pruebas unitarias
```bash
poetry run pytest challenges/c04_summarizer/
```
Escenarios cubiertos:
- Rutas válidas e inválidas de archivos.
- Selección de tipo `short/medium/bullet`.
- Validación del token.
- Formateo de bullets y cálculo de métricas.

## 🧾 Ejemplo de salida (modo bullet)
```
=== SUMMARY RESULT ===

- Punto destacado 1
- Punto destacado 2
- Punto destacado 3

--- SUMMARY METRICS ---
Type           : bullet
Original length: 5421 chars
Summary length : 312 chars
Reduced        : 94%
```

## 🚧 Edge cases contemplados
- Archivos inexistentes o sin permisos → error claro y salida temprana.
- Tokens inválidos / rate limits → mensaje del API y código de salida `1`.
- Resumen vacío → se muestra igualmente junto a métricas (0 chars).
