"""
Test suite for the Best-in-Genre solution (challenge 02).

Organized in Gherkin style:
- Given: setup or mock API data
- When: the function call being tested
- Then: assertions and expected outcomes
"""

import responses

from challenges.c02_best_in_genre.solution_best_in_genre import BASE_URL, bestInGenre


# --- Helper Utilities (private) ---
def _make_page_payload(page: int, total_pages: int, items: list) -> dict:
    """Creates a mock API response payload for a given page."""
    return {
        "page": page,
        "per_page": len(items),
        "total": sum(len(items) for _ in range(total_pages)),
        "total_pages": total_pages,
        "data": items,
    }


# --- Tests ---
@responses.activate
def test_best_action_show_is_highest_rated():
    """Scenario: Find best 'Action' show among multiple pages."""
    # Given
    page1_items = [
        {"name": "Game of Thrones",
         "genre": "Action, Adventure, Drama", "imdb_rating": 9.3},
        {"name": "Avatar: The Last Airbender",
         "genre": "Action, Animation, Adventure", "imdb_rating": 9.2},
    ]
    page2_items = [
        {"name": "Hagane no renkinjutsushi",
         "genre": "Action, Fantasy", "imdb_rating": 9.1},
        {"name": "Shingeki no kyojin",
         "genre": "Action, Drama", "imdb_rating": 8.9},
    ]
    responses.add(
        responses.GET,
        BASE_URL,
        json=_make_page_payload(1, 2, page1_items),
        status=200,
        match=[responses.matchers.query_param_matcher({"page": "1"})],
    )
    responses.add(
        responses.GET,
        BASE_URL,
        json=_make_page_payload(2, 2, page2_items),
        status=200,
        match=[responses.matchers.query_param_matcher({"page": "2"})],
    )

    # When
    best_show = bestInGenre("Action")

    # Then
    assert best_show == "Game of Thrones"


@responses.activate
def test_genre_case_insensitive_and_spaces():
    """Scenario: Searching by genre should be case-insensitive and trim spaces."""
    # Given
    page_items = [
        {"name": "Show A", "genre": "comedy,Drama", "imdb_rating": 8.0},
        {"name": "Show B", "genre": "Drama , Romance", "imdb_rating": 8.5},
        {"name": "Show C", "genre": "romance, DRAMA", "imdb_rating": 8.7},
    ]
    responses.add(
        responses.GET,
        BASE_URL,
        json=_make_page_payload(1, 1, page_items),
        status=200,
        match=[responses.matchers.query_param_matcher({"page": "1"})],
    )

    # When
    best_show = bestInGenre("drama")

    # Then
    assert best_show == "Show C"


@responses.activate
def test_tie_break_alphabetical_order():
    """Scenario: Tie on rating should resolve alphabetically."""
    # Given
    page_items = [
        {"name": "Alpha Show", "genre": "Sci-Fi", "imdb_rating": 9.0},
        {"name": "Beta Show", "genre": "Sci-Fi", "imdb_rating": 9.0},
        {"name": "Gamma Show", "genre": "Sci-Fi", "imdb_rating": 8.5},
    ]
    responses.add(
        responses.GET,
        BASE_URL,
        json=_make_page_payload(1, 1, page_items),
        status=200,
        match=[responses.matchers.query_param_matcher({"page": "1"})],
    )

    # When
    best_show = bestInGenre("Sci-Fi")

    # Then
    assert best_show == "Alpha Show"


@responses.activate
def test_no_matching_genre_returns_empty():
    """Scenario: No show matches the requested genre → return empty string."""
    # Given
    page_items = [
        {"name": "Some Show", "genre": "Comedy", "imdb_rating": 7.0}
    ]
    responses.add(
        responses.GET,
        BASE_URL,
        json=_make_page_payload(1, 1, page_items),
        status=200,
        match=[responses.matchers.query_param_matcher({"page": "1"})],
    )

    # When
    best_show = bestInGenre("Action")

    # Then
    assert best_show == ""


@responses.activate
def test_api_failure_returns_empty():
    """Scenario: API/network failure → should return empty string."""
    # Given
    responses.add(
        responses.GET,
        BASE_URL,
        status=500,
        match=[responses.matchers.query_param_matcher({"page": "1"})],
    )

    # When
    best_show = bestInGenre("Action")

    # Then
    assert best_show == ""
