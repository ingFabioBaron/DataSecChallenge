import click
from summarizer import summarize

from common.logging_config import get_logger

logger = get_logger(__name__)


@click.group()
def cli():
    """Summarizer CLI using Click."""
    pass


@cli.command(name="summarize")
@click.option(
    "--input",
    "-i",
    "input_file",
    type=click.Path(exists=False),
    required=False,
    help="Ruta del archivo a resumir. Si no se indica se usará article.txt por defecto."
)
@click.option(
    "--type",
    "-t",
    "summary_type",
    required=True,
    type=click.Choice(["short", "medium", "bullet"]),
    help="Tipo de resumen."
)
@click.option(
    "--model",
    "-m",
    help="Modelo HF para override (opcional)."
)
@click.option(
    "--api-token",
    help="Token HF para override (opcional)."
)
def cli_summarize(input_file, summary_type, model, api_token):
    if input_file:
        logger.info(f"[CLI] Using provided file: {input_file}")
        file_path = input_file
    else:
        logger.info("[CLI] No input provided → defaulting to article.txt")
        file_path = None  # el summarizer se encarga de cargar el por defecto

    result = summarize(
        text_path=file_path,
        summary_type=summary_type,
        cli_model=model,
        cli_token=api_token
    )

    click.echo("\n=== SUMMARY RESULT ===\n")
    click.echo(result)


if __name__ == "__main__":
    cli()
