"""
Summarizer module for Hugging Face LLM.

Provides functionality to:
- Load text from a file (default or user-provided).
- Summarize text using a Hugging Face model.
- Format bullet-point summaries.
- Validate API token and model usage.
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from common.logging_config import get_logger

load_dotenv()
logger = get_logger(__name__)

# --- CONSTANTS ---
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_ARTICLE = BASE_DIR / "articles" / "article.txt"
DEFAULT_MODEL = "Qwen/Qwen2.5-7B-Instruct"
# API docs requirement: https://huggingface.co/Qwen/Qwen2.5-7B-Instruct


def _load_article(path: Optional[str]) -> str:
    """
    Loads the text from a file.
    Uses DEFAULT_ARTICLE if path is not provided.

    Args:
        path (Optional[str]): Path to the article file.

    Returns:
        str: Content of the article.

    Raises:
        SystemExit: If file does not exist.
    """
    if path:
        file_path = Path(path)
        if not file_path.is_absolute():
            file_path = (Path.cwd() / file_path).resolve()
    else:
        file_path = DEFAULT_ARTICLE
        logger.info(f"[summarizer] No file provided → using default: {file_path}")

    if not file_path.exists():
        logger.error(f"[summarizer] ERROR: File not found → {file_path}")
        raise SystemExit(1)

    logger.info(f"[summarizer] Loading article from: {file_path}")
    return file_path.read_text(encoding="utf-8")


def _format_bullets(text: str) -> str:
    """
    Ensures each line is formatted as a bullet point prefixed with '- '.

    Args:
        text (str): Input text.

    Returns:
        str: Bullet-point formatted text.
    """
    lines = [line.strip("• ").strip() for line in text.split("\n") if line.strip()]
    return "\n".join(f"- {line}" for line in lines)


def summarize(
    text_path: Optional[str],
    summary_type: str,
    cli_model: Optional[str] = None,
    cli_token: Optional[str] = None,
) -> str:
    """
    Main function for summarization. Can be called from CLI.

    Args:
        text_path (Optional[str]): Path to the text file.
        summary_type (str): 'short', 'medium', or 'bullet'.
        cli_model (Optional[str]): Hugging Face model override.
        cli_token (Optional[str]): Hugging Face API token override.

    Returns:
        str: Generated summary with metrics appended.

    Raises:
        SystemExit: If token is missing or API fails.
    """
    # Token validation
    token = cli_token or os.getenv("HF_API_TOKEN")
    if not token:
        logger.error(
            "\n❌ ERROR: No HF_API_TOKEN detected.\n\n"
            "Please set it before continuing:\n"
            "    setx HF_API_TOKEN \"your_token_here\"   (Windows)\n"
            "    export HF_API_TOKEN=\"your_token_here\" (Linux/Mac)\n\n"
            "Obtain your token at: https://huggingface.co/settings/tokens"
        )
        raise SystemExit(1)

    # Model selection
    model = cli_model or os.getenv("HF_MODEL") or DEFAULT_MODEL
    logger.info(f"[HF] Using model: {model}")

    # Load text
    text = _load_article(text_path)

    # Create Hugging Face client (requirement: include API docs link)
    # Docs: https://huggingface.co/Qwen/Qwen2.5-7B-Instruct
    client = InferenceClient(token=token)

    # System prompts
    system_prompts = {
        "short": "You create very concise summaries (1–2 sentences).",
        "medium": "You create paragraph-length summaries.",
        "bullet": "You create bullet-point summaries using dashes (-).",
    }

    # User prompts
    user_prompts = {
        "short": f"Summarize in 1–2 sentences:\n\n{text}",
        "medium": f"Summarize this text into one paragraph:\n\n{text}",
        "bullet": f"Summarize this text into bullet points using dashes (-):\n\n{text}",
    }

    system_prompt = system_prompts.get(summary_type, system_prompts["medium"])
    user_prompt = user_prompts.get(summary_type, user_prompts["medium"])

    logger.info("[HF] Sending summarization request...")

    # Request summarization
    try:
        response = client.chat_completion(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=300,
            temperature=0.0,
        )
    except Exception as error:
        logger.error(f"[HF] API Error: {error}")
        raise SystemExit(1)

    summary = response.choices[0].message.content.strip()

    # Format bullets if requested
    if summary_type == "bullet":
        summary = _format_bullets(summary)

    # Metrics calculation
    original_chars = len(text)
    summary_chars = len(summary)
    reduction = 100 - int((summary_chars / original_chars) * 100)

    metrics_msg = (
        "\n\n--- SUMMARY METRICS ---\n"
        f"Type           : {summary_type}\n"
        f"Original length: {original_chars} chars\n"
        f"Summary length : {summary_chars} chars\n"
        f"Reduced        : {reduction}%\n"
    )

    return summary + metrics_msg
