"""
CLI for text summarization using Click.

Allows summarizing a text file using Hugging Face models with options for:
- Summary type: short, medium, bullet
- Model override
- API token override
"""

import click
from summarizer import summarize

from common.logging_config import get_logger

logger = get_logger(__name__)


@click.group()
def cli() -> None:
    """Summarizer CLI group using Click."""
    pass


@cli.command(name="summarize")
@click.option(
    "--input",
    "-i",
    "input_file",
    type=click.Path(exists=False),
    required=False,
    help="Path to the article file. Defaults to article.txt if not provided.",
)
@click.option(
    "--type",
    "-t",
    "summary_type",
    required=True,
    type=click.Choice(["short", "medium", "bullet"]),
    help="Type of summary to generate.",
)
@click.option(
    "--model",
    "-m",
    help="Hugging Face model override (optional).",
)
@click.option(
    "--api-token",
    help="Hugging Face API token override (optional).",
)
def cli_summarize(input_file: str, summary_type: str, model: str, api_token: str) -> None:
    """
    Summarizes a text file using the Hugging Face model.

    Args:
        input_file (str): Path to input text file. Defaults to article.txt if None.
        summary_type (str): 'short', 'medium', or 'bullet'.
        model (str): Optional Hugging Face model override.
        api_token (str): Optional Hugging Face API token override.
    """
    if input_file:
        logger.info(f"[CLI] Using provided file: {input_file}")
        file_path = input_file
    else:
        logger.info("[CLI] No input provided → defaulting to article.txt")
        file_path = None  # summarizer handles default file

    # Run summarization
    result = summarize(
        text_path=file_path,
        summary_type=summary_type,
        cli_model=model,
        cli_token=api_token,
    )

    # Output result
    click.echo("\n=== SUMMARY RESULT ===\n")
    click.echo(result)


if __name__ == "__main__":
    cli()
