# solution_summarizer_old.py
import sys
import os
from common.logging_config import get_logger
from summarizer import summarize

logger = get_logger(__name__)

DEFAULT_FILE = "challenges/c04_summarizer/articles/article.txt"


def print_usage():
    print(
        "\nUso:\n"
        "  python solution_summarizer_old.py <file?> <summary_type> [--model=...] [--api-token=...]\n\n"
        "Ejemplos:\n"
        "  python solution_summarizer_old.py medium\n"
        "  python solution_summarizer_old.py article.txt medium\n"
        "  python solution_summarizer_old.py bullet --model=facebook/bart-large-cnn\n"
    )


def parse_arguments():
    """Procesamiento manual de argumentos CLI con archivo por defecto."""
    args = sys.argv[1:]

    if len(args) == 0:
        logger.error("No se recibió ningún argumento.")
        print_usage()
        sys.exit(1)

    # Detectar si primer argumento es tipo o archivo
    first = args[0]
    file = None
    summary_type = None

    valid_types = ["short", "medium", "bullet"]

    if first in valid_types:
        # Caso: user escribió solo el tipo → usar archivo por defecto
        file = DEFAULT_FILE
        summary_type = first
        params = args[1:]

        logger.info("[OLD CLI] No file provided → using default article.txt")

    else:
        # Caso: usuario sí pasó archivo
        file = first

        if len(args) < 2:
            logger.error("No se especificó el tipo de resumen.")
            print_usage()
            sys.exit(1)

        summary_type = args[1]
        params = args[2:]

    if summary_type not in valid_types:
        logger.error(f"Tipo inválido: {summary_type}")
        print_usage()
        sys.exit(1)

    # Parámetros opcionales
    model = None
    api_token = None

    for p in params:
        if p.startswith("--model="):
            model = p.split("=", 1)[1]
        elif p.startswith("--api-token="):
            api_token = p.split("=", 1)[1]
        elif p.strip():
            logger.warning(f"Parámetro desconocido ignorado: {p}")

    return file, summary_type, model, api_token


def main():
    file, summary_type, model, api_token = parse_arguments()

    logger.info(f"[OLD CLI] Archivo: {file}")
    logger.info(f"[OLD CLI] Tipo: {summary_type}")

    result = summarize(
        text_path=file,
        summary_type=summary_type,
        cli_model=model,
        cli_token=api_token
    )

    print("\n=== SUMMARY RESULT (OLD API) ===\n")
    print(result)


if __name__ == "__main__":
    main()
