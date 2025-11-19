import requests
from requests.exceptions import RequestException

from common.logging_config import get_logger

logger = get_logger(__name__)

# --- CONSTANTS ---
BASE_URL = "https://jsonmock.hackerrank.com/api/tvseries"
REQUEST_TIMEOUT = 5  # seconds


def _validate_genre(genre: str) -> None:
    """
    Validates the genre input.

    Args:
        genre (str): The genre string to validate.

    Raises:
        TypeError: If genre is not a string.
        ValueError: If genre is empty or only whitespace.
    """
    if not isinstance(genre, str):
        raise TypeError("genre must be a string")
    if genre.strip() == "":
        raise ValueError("genre must not be empty")


def _normalize_genre_token(token: str) -> str:
    """
    Normalizes a genre token for robust, case-insensitive comparison.

    Args:
        token (str): Genre token to normalize.

    Returns:
        str: Normalized token (casefolded and stripped).
    """
    return token.strip().casefold()


def _get_json_page(page: int) -> dict:
    """
    Internal helper to fetch a single page from the TV series API.

    Args:
        page (int): Page number to fetch.

    Returns:
        dict: JSON response as dictionary on success, empty dict on failure.
    """
    try:
        response = requests.get(BASE_URL, params={"page": page}, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        logger.error(f"Network error when requesting page {page}: {e}")
        return {}
    except ValueError as e:
        logger.error(f"Invalid JSON on page {page}: {e}")
        return {}


def bestInGenre(genre: str) -> str:
    """
    Finds the highest-rated TV series in the given genre.

    Genre matching is case-insensitive. In case of ties, the alphabetically
    lower name is returned. Iterates through all API pages.

    Args:
        genre (str): Genre to search for (e.g., 'Action', 'Comedy').

    Returns:
        str: Name of the highest-rated TV series. Returns empty string if no match
        or fatal API/network errors.
    """
    # Validate input
    _validate_genre(genre)
    search_token = genre.casefold().strip()

    logger.info(f"Searching best show for genre: '{genre}'")

    page = 1
    best_name = ""
    best_rating = float("-inf")
    total_pages = None
    processed_items = 0

    while True:
        logger.debug(f"Fetching page {page}")
        data = _get_json_page(page)
        if data is None:
            logger.error(f"Aborting search due to API/network error on page {page}")
            return ""

        # Capture total pages on first page
        if total_pages is None:
            total_pages = data.get("total_pages")
            logger.debug(f"Total pages reported by API: {total_pages}")

        items = data.get("data", [])
        for item in items:
            processed_items += 1

            # Extract fields safely
            name = item.get("name", "")
            genre_field = item.get("genre", "")
            raw_rating = item.get("imdb_rating", 0)

            # Parse IMDb rating robustly
            try:
                rating = float(raw_rating or 0)
            except (ValueError, TypeError):
                logger.warning(f"Invalid imdb_rating for '{name}': {raw_rating}. Treating as 0.")
                rating = 0.0

            # Parse and normalize genres
            if not isinstance(genre_field, str):
                logger.debug(f"Skipping item with malformed genre field: {genre_field!r}")
                continue

            genre_tokens = [_normalize_genre_token(t)
                            for t in genre_field.split(",") if t.strip() != ""]

            if search_token in genre_tokens:
                logger.debug(f"Candidate matched: {name} (rating={rating})")
                if rating > best_rating:
                    best_rating = rating
                    best_name = name or ""
                    logger.info(f"New best candidate: {best_name} with rating {best_rating}")
                elif rating == best_rating:
                    if best_name == "" or (name or "").casefold() < best_name.casefold():
                        logger.info(f"Tie on rating {rating}: "
                                    f"choosing alphabetically lower name: {name}")
                        best_name = name or ""

        # Paging logic
        if (total_pages is not None and page >= total_pages) or (total_pages is None and not items):
            logger.debug(f"Paging complete: page {page} of {total_pages}")
            break

        page += 1

    # --- Final logging using f-string ---
    rating_info = best_rating if best_rating != float("-inf") else "N/A"
    logger.info(f"Processed {processed_items} items. "
                f"Best found: '{best_name}' with rating {rating_info}")

    return best_name or ""
