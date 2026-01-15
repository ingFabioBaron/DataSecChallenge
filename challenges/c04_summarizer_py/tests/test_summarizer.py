"""
Test suite for the Summarizer solution (challenge 04).

Organized in Gherkin style:
- Given: setup data, article files, environment variables, and mocks
- When: summarizer functions are called
- Then: assertions on expected outputs
"""

from unittest.mock import MagicMock, patch

import pytest

from challenges.c04_summarizer_py.summarizer import (
    _format_bullets,
    _load_article,
    summarize,
)


# -----------------------------
# Fixtures / Private Utilities
# -----------------------------
@pytest.fixture
def _fake_article(tmp_path):
    """Crea un archivo temporal de texto para pruebas."""
    file = tmp_path / "article.txt"
    file.write_text("Texto de prueba para el resumen.", encoding="utf-8")
    return file


@pytest.fixture
def _mock_hf_response():
    """Mock del objeto retornado por HuggingFace."""
    mock_choice = MagicMock()
    mock_choice.message.content = "Resumen generado"

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    return mock_response


# -----------------------------
# Tests: load_article()
# -----------------------------
def test_load_article_loads_custom_file(_fake_article):
    """Given a user-provided file, load_article() should return its contents."""
    # Given

    # When
    result = _load_article(str(_fake_article))

    # Then
    assert result == "Texto de prueba para el resumen."


def test_load_article_loads_default_file(monkeypatch, _fake_article):
    """Given no file provided, load_article() should use the default article."""
    # Given
    monkeypatch.setattr(
        "challenges.c04_summarizer_py.summarizer.DEFAULT_ARTICLE",
        _fake_article
    )

    # When
    result = _load_article(None)

    # Then
    assert result == "Texto de prueba para el resumen."


def test_load_article_raises_on_missing_file(tmp_path):
    """Given a non-existent file, load_article() should raise SystemExit."""
    # Given
    missing = tmp_path / "missing.txt"

    # When / Then
    with pytest.raises(SystemExit):
        _load_article(str(missing))


# -----------------------------
# Tests: format_bullets()
# -----------------------------
def test_format_bullets_removes_prefixes_and_spaces():
    """Given text with bullets, format_bullets() should clean lines."""
    # Given
    text = """
    • item uno
    item dos
    """

    # When
    formatted = _format_bullets(text)
    lines = formatted.split("\n")

    # Then
    assert lines[0] == "- item uno"
    assert lines[1] == "- item dos"


# -----------------------------
# Tests: summarize()
# -----------------------------
@patch("challenges.c04_summarizer_py.summarizer.InferenceClient")
def test_summarize_returns_summary(mock_client_cls, _fake_article, _mock_hf_response, monkeypatch):
    """Given a valid article and HF token, summarize()
    should return formatted summary with metrics."""
    # Given
    monkeypatch.setenv("HF_API_TOKEN", "fake-token")
    monkeypatch.setenv("HF_MODEL", "FakeModel")
    monkeypatch.setattr(
        "challenges.c04_summarizer_py.summarizer.DEFAULT_ARTICLE",
        _fake_article
    )

    mock_client = MagicMock()
    mock_client.chat_completion.return_value = _mock_hf_response
    mock_client_cls.return_value = mock_client

    # When
    result = summarize(
        text_path=None,
        summary_type="medium"
    )

    # Then
    assert "Resumen generado" in result
    assert "Summary length" in result


def test_summarize_raises_without_token(_fake_article, monkeypatch):
    """Given no HF_API_TOKEN, summarize() should raise SystemExit."""
    # Given
    monkeypatch.delenv("HF_API_TOKEN", raising=False)
    monkeypatch.setattr(
        "challenges.c04_summarizer_py.summarizer.DEFAULT_ARTICLE",
        _fake_article
    )

    # When / Then
    with pytest.raises(SystemExit):
        summarize(
            text_path=None,
            summary_type="medium"
        )
