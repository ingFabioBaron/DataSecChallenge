from unittest.mock import MagicMock, patch

import pytest

from challenges.c04_summarizer.summarizer import (
    format_bullets,
    load_article,
    summarize,
)


# -----------------------------
# FIXTURES
# -----------------------------
@pytest.fixture
def fake_article(tmp_path):
    """Crea un archivo temporal de texto."""
    file = tmp_path / "article.txt"
    file.write_text("Texto de prueba para el resumen.", encoding="utf-8")
    return file


@pytest.fixture
def mock_hf_response():
    """Mock del objeto retornado por HuggingFace."""
    mock_choice = MagicMock()
    mock_choice.message.content = "Resumen generado"

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    return mock_response


# -----------------------------
# TEST: load_article()
# -----------------------------
def test_load_article_custom(fake_article):
    """Debe cargar un archivo especificado por el usuario."""
    result = load_article(str(fake_article))
    assert result == "Texto de prueba para el resumen."


def test_load_article_default(monkeypatch, fake_article):
    """Debe cargar el artículo por defecto si no se especifica ruta."""
    monkeypatch.setattr(
        "challenges.c04_summarizer.summarizer.DEFAULT_ARTICLE",
        fake_article
    )

    result = load_article(None)
    assert result == "Texto de prueba para el resumen."


def test_load_article_not_found(tmp_path):
    """Debe fallar cuando el archivo no existe."""
    missing = tmp_path / "missing.txt"
    with pytest.raises(SystemExit):
        load_article(str(missing))


# -----------------------------
# TEST: format_bullets()
# -----------------------------
def test_format_bullets():
    text = """
    • item uno
    item dos
    """
    formatted = format_bullets(text)
    lines = formatted.split("\n")

    assert lines[0] == "item uno"
    assert lines[1] == "item dos"


# -----------------------------
# TEST: summarize()
# -----------------------------
@patch("challenges.c04_summarizer.summarizer.InferenceClient")
def test_summarize_ok(mock_client_cls, fake_article, mock_hf_response, monkeypatch):
    """Prueba completa del flujo de summarize() usando mock HF."""
    # Mock token obligatorio
    monkeypatch.setenv("HF_API_TOKEN", "fake-token")
    monkeypatch.setenv("HF_MODEL", "FakeModel")

    # Mock lectura de archivo
    monkeypatch.setattr(
        "challenges.c04_summarizer.summarizer.DEFAULT_ARTICLE",
        fake_article
    )

    # Mock del cliente HuggingFace
    mock_client = MagicMock()
    mock_client.chat_completion.return_value = mock_hf_response
    mock_client_cls.return_value = mock_client

    result = summarize(
        text_path=None,
        summary_type="medium"
    )

    assert "Resumen generado" in result
    assert "Summary length" in result


def test_summarize_missing_token(fake_article, monkeypatch):
    """Debe fallar si no existe HF_API_TOKEN."""
    monkeypatch.delenv("HF_API_TOKEN", raising=False)

    monkeypatch.setattr(
        "challenges.c04_summarizer.summarizer.DEFAULT_ARTICLE",
        fake_article
    )

    with pytest.raises(SystemExit):
        summarize(
            text_path=None,
            summary_type="medium"
        )
