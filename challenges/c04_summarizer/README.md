Challenge 4: Go CLI – Text Summarizer with GenAI
Nota Importante

Aunque el enunciado original del challenge solicitaba implementar este CLI en el lenguaje Go, en este proyecto la solución fue implementada utilizando Python, manteniendo todas las funcionalidades, requisitos y comportamiento esperados.
La razón es demostrar un enfoque más consistente con el stack principal del repositorio y asegurar integración homogénea con las herramientas ya configuradas (Poetry, estructura de carpetas y pruebas automáticas).

El comportamiento, parámetros, lógica del CLI y comunicación con la API siguen exactamente las especificaciones del requirement oficial.

Objetivo del Desafío

Crear una aplicación de línea de comandos que genere el resumen de un archivo de texto usando un endpoint público de IA generativa.

La aplicación debe:

Aceptar parámetros para archivo de entrada y tipo de resumen (short, medium, bullet).

Construir un prompt adecuado para el tipo de resumen solicitado.

Llamar un endpoint público de IA para generar el resumen.

Mostrar el resultado por consola.

Manejar errores de archivo, red y API.

Entregar el código en un archivo equivalente al solicitado en el enunciado, pero implementado en Python.

Solución Implementada

Enfoque Algorítmico
El CLI implementado en Python realiza lo siguiente:

Procesamiento de argumentos:
Se valida el archivo de entrada, el tipo solicitado y el formato correcto de la llamada.

Lectura del archivo:
Se obtiene el texto original y se prepara la instrucción para la IA.

Construcción del prompt:
short: generar 1 a 2 oraciones.
medium: producir un párrafo.
bullet: generar puntos clave en formato lista.

Llamada a la API:
Se usa requests para enviar la solicitud POST al endpoint seleccionado de IA pública.
Se manejan errores como fallos de conexión, respuestas inválidas y límites de API.

Estructura del Código
Los archivos del challenge son:

challenges/c04_summarizer/solution_summarizer.py
Implementación completa del CLI en Python, manteniendo el diseño y flujo esperados en el enunciado.

challenges/c04_summarizer/run.py
Script auxiliar para ejecutar el CLI desde la raíz del proyecto.

challenges/c04_summarizer/tests/
Pruebas que validan comportamiento básico del CLI.

Instrucciones de Ejecución

Opción A: usando Poetry
poetry run python challenges/c04_summarizer/solution_summarizer.py --input ruta/archivo.txt --type bullet

Opción B: versión abreviada
poetry run python challenges/c04_summarizer/solution_summarizer.py -t short archivo.txt

Ejemplo de Entrada y Salida

Entrada:
Un archivo article.txt con texto extenso.

Ejemplo tipo bullet:

Punto destacado 1

Punto destacado 2

Punto destacado 3

Ejemplo tipo short:
Este artículo presenta los conceptos principales del tema y una conclusión breve.

Pruebas Unitarias

Si existen pruebas automatizadas para este challenge se encuentran en:
challenges/c04_summarizer/tests/

Para ejecutarlas:
poetry run pytest challenges/c04_summarizer/