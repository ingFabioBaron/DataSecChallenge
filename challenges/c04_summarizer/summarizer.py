import os
from pathlib import Path
from huggingface_hub import InferenceClient
from common.logging_config import get_logger
from dotenv import load_dotenv

load_dotenv()
logger = get_logger(__name__)

# --- CONSTANTS ---
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_ARTICLE = BASE_DIR / "articles" / "article.txt"
DEFAULT_MODEL = "Qwen/Qwen2.5-7B-Instruct"

def load_article(path: str | None) -> str:
    """Carga el texto desde archivo, usando article.txt si no se proporciona ruta."""
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


def format_bullets(text: str) -> str:
    """Asegura que cada línea en modo bullet tenga prefijo '- '."""
    lines = [line.strip("• ").strip() for line in text.split("\n") if line.strip()]
    return "\n".join(f"{line}" for line in lines)


def summarize(text_path: str, summary_type: str, cli_model=None, cli_token=None) -> str:
    """
    Función principal usada por el CLI.
    """
    # Token obligatorio
    token = cli_token or os.getenv("HF_API_TOKEN")
    if not token:
        logger.error("""
            ❌ ERROR: No se detectó HF_API_TOKEN.
            
            Por favor configúralo antes de continuar:
                setx HF_API_TOKEN "tu_token_aquí"   (Windows)
                export HF_API_TOKEN="tu_token_aquí" (Linux/Mac)
            
            Obtén tu token en: https://huggingface.co/settings/tokens
        """)
        raise SystemExit(1)

    # Modelo
    model = cli_model or os.getenv("HF_MODEL") or DEFAULT_MODEL
    logger.info(f"[HF] Using model: {model}")

    # Cargar texto
    text = load_article(text_path)

    # Crear cliente HF
    client = InferenceClient(token=token)

    # System prompt según tipo
    system_prompts = {
        "short": "You create very concise summaries (1–2 sentences).",
        "medium": "You create paragraph-length summaries.",
        "bullet": "You create bullet-point summaries using dashes (-)."
    }

    # User prompts según tipo
    user_prompts = {
        "short": f"Summarize in 1–2 sentences:\n\n{text}",
        "medium": f"Summarize this text into one paragraph:\n\n{text}",
        "bullet": f"Summarize this text into bullet points using dashes (-):\n\n{text}"
    }

    system_prompt = system_prompts.get(summary_type, system_prompts["medium"])
    user_prompt = user_prompts.get(summary_type, user_prompts["medium"])

    logger.info("[HF] Sending summarization request...")

    try:
        response = client.chat_completion(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=300,
            temperature=0.0
        )

    except Exception as e:
        logger.error(f"[HF] API Error: {e}")
        raise SystemExit(1)

    summary = response.choices[0].message.content.strip()

    # Si es bullet → formatear
    if summary_type == "bullet":
        summary = format_bullets(summary)

    # Métricas
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
