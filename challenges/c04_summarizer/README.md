# Challenge 4 · Go CLI Summarizer con GenAI

Este directorio contiene la solución al Challenge 4, implementado en **GoLang**.

## 📋 Resumen del problema
Construir un CLI que:
- Lea un archivo de texto plano.
- Permita elegir el tipo de resumen (`short`, `medium`, `bullet`).
- Forme un prompt acorde y consuma un modelo de Hugging Face vía API pública (`router.huggingface.co`).
- Muestre el resumen junto con métricas de reducción.
- Maneje errores de entrada, credenciales y red.

## 🔐 Requisitos previos
| Variable | Obligatoria | Descripción |
|----------|-------------|-------------|
| `HF_API_TOKEN` | Sí | Token de Hugging Face para usar la API de inferencia. Se puede cargar desde un archivo `.env` en la raíz del proyecto (`../../.env`) o desde las variables de entorno del sistema. |
| `HF_MODEL` | No | Modelo alternativo; por defecto `Qwen/Qwen2.5-7B-Instruct:together`. |
| `ARTICLE_PATH` | No | Ruta al archivo de texto que se utilizará como artículo de entrada por defecto. Por defecto `articles/article.txt` si no se proporciona. |

El archivo `articles/article.txt` se usa como entrada por defecto cuando no se especifica otro.
El requerimiento oficial pide enlazar la documentación del endpoint genAI utilizado; el código (`summarizer/summarizer.go`) utiliza el modelo `Qwen/Qwen2.5-7B-Instruct` a través del `router.huggingface.co`. Puedes encontrar más detalles sobre este modelo en Hugging Face: https://huggingface.co/Qwen/Qwen2.5-7B-Instruct

## 🧠 Estrategia de la solución (GoLang)
1.  **CLI con Cobra** (`solution_summarizer.go`):
    *   Comando `summarize` con opciones `--input/-i`, `--type/-t`, `--model/-m`, `--api-token`.
    *   Manejo de argumentos posicionales para `--input`.
    *   Integración con el paquete `summarizer` para la lógica de negocio.
2.  **Módulo `summarizer/summarizer.go`**:
    *   Carga del texto (`LoadArticle`) resolviendo rutas relativas/absolutas y usando el archivo por defecto.
    *   Carga de variables de entorno desde `.env` (usando `godotenv`).
    *   Validación del token y selección del modelo.
    *   Cliente HTTP (`net/http`) para interactuar con la API de Hugging Face (`https://router.huggingface.co/v1/chat/completions`).
    *   Prompts específicos por tipo de resumen (`short`, `medium`, `bullet`).
    *   Post-procesamiento para bullets y cálculo de métricas (largo original vs resumen).
3.  **Manejo de errores**:
    *   Errores de archivo no encontrado, token ausente o fallos de la API se manejan con mensajes claros y salida temprana.

## 🗂️ Organización
- `solution_summarizer.go`: CLI y parsing de flags.
- `summarizer/summarizer.go`: Lógica de negocio, prompts, formateo y llamada a la API.
- `articles/article.txt`: Entrada por defecto.
- `go.mod`, `go.sum`: Archivos de módulo de Go.
- `summarizer/summarizer_test.go`: Pruebas unitarias para el paquete `summarizer`.

## ▶️ Ejecución
Desde el directorio `challenges/c04_summarizer`:

```bash
go run . --type bullet --input articles/article.txt
```

Atajos posibles:
```bash
go run . -t short
```
Si no se entrega `--input`, se usa el archivo por defecto (`articles/article.txt`).

## 🧪 Pruebas unitarias
Desde el directorio `challenges/c04_summarizer`:

```bash
go test ./summarizer
```
Se cubrirán escenarios como carga de archivos, validación de token y formateo de summaries (usando mocks para la API).

## 🧾 Ejemplo de salida (modo short)
```
[CLI] No input provided → defaulting to article.txt
[summarizer] No file provided → using default: articles/article.txt
[summarizer] Loading article from: articles/article.txt
[HF] Using model: Qwen/Qwen2.5-7B-Instruct:together
[HF] Sending summarization request to Hugging Face API...

=== SUMMARY RESULT ===

Albert Einstein, nacido en 1879 en Alemania, revolucionó la física del siglo XX con sus teorías, incluyendo la relatividad especial y general, y la ecuación \(E = mc^2\), transformando nuestra comprensión del espacio, el tiempo, la materia y la energía. Su vida y obra continuaron influyendo en la ciencia y la cultura popular hasta su muerte en 1955.   

--- SUMMARY METRICS ---
Type           : short
Original length: 5365 chars
Summary length : 357 chars
Reduced        : 94%
```
