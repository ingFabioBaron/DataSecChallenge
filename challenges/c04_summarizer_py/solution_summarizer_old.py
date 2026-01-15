"""
Legacy CLI for text summarization using manual argument parsing.

Supports:
- Default article file
- Summary type: short, medium, bullet
- Optional model and API token overrides
"""

import sys
from typing import Optional, Tuple

from summarizer import summarize

from common.logging_config import get_logger

logger = get_logger(__name__)

DEFAULT_FILE = "challenges/c04_summarizer/articles/article.txt"
VALID_TYPES = ["short", "medium", "bullet"]


def print_usage() -> None:
    """Prints CLI usage instructions and examples."""
    print(
        "\nUsage:\n"
        "  python solution_summarizer_old.py <file?> <summary_type> [--model=...] "
        "[--api-token=...]\n\n"
        "Examples:\n"
        "  python solution_summarizer_old.py medium\n"
        "  python solution_summarizer_old.py article.txt medium\n"
        "  python solution_summarizer_old.py bullet --model=facebook/bart-large-cnn\n"
    )


def parse_arguments() -> Tuple[str, str, Optional[str], Optional[str]]:
    """
    Manually parses CLI arguments, supports default file and optional parameters.

    Returns:
        Tuple[str, str, Optional[str], Optional[str]]: (file, summary_type, model, api_token)

    Raises:
        SystemExit: On invalid arguments or missing required parameters.
    """
    args = sys.argv[1:]

    if not args:
        logger.error("No arguments provided.")
        print_usage()
        sys.exit(1)

    first_arg = args[0]
    file_path: str
    summary_type: str
    params = []

    # Determine if first argument is type or file
    if first_arg in VALID_TYPES:
        file_path = DEFAULT_FILE
        summary_type = first_arg
        params = args[1:]
        logger.info(f"[OLD CLI] No file provided → using default: {file_path}")
    else:
        file_path = first_arg
        if len(args) < 2:
            logger.error("No summary type specified.")
            print_usage()
            sys.exit(1)
        summary_type = args[1]
        params = args[2:]

    if summary_type not in VALID_TYPES:
        logger.error(f"Invalid summary type: {summary_type}")
        print_usage()
        sys.exit(1)

    # Parse optional parameters
    model: Optional[str] = None
    api_token: Optional[str] = None

    for p in params:
        if p.startswith("--model="):
            model = p.split("=", 1)[1]
        elif p.startswith("--api-token="):
            api_token = p.split("=", 1)[1]
        elif p.strip():
            logger.warning(f"Ignoring unknown parameter: {p}")

    return file_path, summary_type, model, api_token


def main() -> None:
    """Main function for the legacy CLI."""
    file_path, summary_type, model, api_token = parse_arguments()

    logger.info(f"[OLD CLI] File: {file_path}")
    logger.info(f"[OLD CLI] Summary type: {summary_type}")

    result = summarize(
        text_path=file_path,
        summary_type=summary_type,
        cli_model=model,
        cli_token=api_token,
    )

    print("\n=== SUMMARY RESULT (OLD API) ===\n")
    print(result)


if __name__ == "__main__":
    main()
