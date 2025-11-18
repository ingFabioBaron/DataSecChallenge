import requests
from requests.exceptions import RequestException
from common.logging_config import get_logger

logger = get_logger(__name__)

# --- CONSTANTS ---
BASE_URL = "https://jsonmock.hackerrank.com/api/tvseries"
REQUEST_TIMEOUT = 5  # seconds


def _validate_genre(genre: str) -> None:
    if not isinstance(genre, str):
        raise TypeError("genre must be a string")
    if genre.strip() == "":
        raise ValueError("genre must not be empty")


def _normalize_genre_token(token: str) -> str:
    # Use casefold for robust case-insensitive comparison
    return token.strip().casefold()


def _get_json_page(page: int) -> dict:
    """
    Internal helper to fetch a single page from the API.
    Returns the JSON dict on success, or None on failure.
    """
    try:
        resp = requests.get(BASE_URL, params={"page": page}, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        return data
    except RequestException as e:
        logger.error("Network error when requesting page %d: %s", page, str(e))
        return {}
    except ValueError as e:
        logger.error("Invalid JSON on page %d: %s", page, str(e))
        return {}


def bestInGenre(genre: str) -> str:
    """
    Finds the highest-rated TV series in the given genre.

    Parameters:
        genre (str): The genre to search for (e.g., 'Action', 'Comedy', 'Drama').

    Returns:
        str: The name of the highest-rated show in the genre. If there is a tie,
             returns the alphabetically lower name. If no show found or on fatal
             API/network errors, returns an empty string "".

    Notes:
    - Genre matching is case-insensitive and splits the 'genre' field by commas.
    - The API is paginated; this function iterates all pages.
    - imdb_rating is parsed as float; missing or malformed ratings are treated as 0.0.
    """
    # Validate input
    _validate_genre(genre)
    search_token = genre.casefold().strip()

    logger.info("Searching best show for genre: '%s'", genre)

    page = 1
    best_name = ""
    best_rating = float("-inf")
    total_pages = None
    processed_items = 0

    while True:
        logger.debug("Fetching page %d", page)
        data = _get_json_page(page)
        if data is None:
            # Network or JSON error: decide to abort and return empty string
            logger.error("Aborting search due to API/network error on page %d", page)
            return ""

        # On first page, capture total_pages if present
        if total_pages is None:
            total_pages = data.get("total_pages", None)
            logger.debug("Total pages reported by API: %s", str(total_pages))

        items = data.get("data", [])
        for item in items:
            processed_items += 1
            # Extract fields safely
            name = item.get("name", "")
            genre_field = item.get("genre", "")
            # Parse imdb_rating robustly
            raw_rating = item.get("imdb_rating", 0)
            try:
                # Some responses may have rating as string or None
                rating = float(raw_rating or 0)
            except (ValueError, TypeError):
                logger.warning("Invalid imdb_rating for '%s': %s. Treating as 0.", name, raw_rating)
                rating = 0.0

            # Parse genres (comma separated)
            if not isinstance(genre_field, str):
                # skip if genres malformed
                logger.debug("Skipping item with malformed genre field: %r", genre_field)
                continue

            genre_tokens = [_normalize_genre_token(t) for t in genre_field.split(",") if t.strip() != ""]

            if search_token in genre_tokens:
                logger.debug("Candidate matched: %s (rating=%s)", name, rating)
                if rating > best_rating:
                    best_rating = rating
                    best_name = name or ""
                    logger.info("New best candidate: %s with rating %s", best_name, best_rating)
                elif rating == best_rating:
                    # tie-break: alphabetical order (case-insensitive)
                    # choose the alphabetically lower show name
                    # To make comparison stable, compare using casefold then fallback to original.
                    if best_name == "":
                        best_name = name or ""
                        logger.info("New best candidate (previous empty): %s (rating %s)", best_name, best_rating)
                    else:
                        # Use casefold for comparison to make it consistent with case-insensitive rules
                        if (name or "").casefold() < best_name.casefold():
                            logger.info("Tie on rating %s: choosing alphabetically lower name: %s over %s", rating, name, best_name)
                            best_name = name or ""

        # Paging logic: stop if we've processed all pages
        # If total_pages is None or not provided, break when no items returned
        if (total_pages is not None and page >= total_pages) or (total_pages is None and not items):
            logger.debug("Paging complete: page %d of %s", page, str(total_pages))
            break

        page += 1

    logger.info("Processed %d items. Best found: '%s' with rating %s", processed_items, best_name, best_rating if best_rating != float("-inf") else "N/A")

    # If best_name empty, return empty string per decision
    return best_name or ""
