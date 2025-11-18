import responses
from challenges.c02_best_in_genre.solution_best_in_genre import bestInGenre, BASE_URL

# Utility: build a page payload
def make_page_payload(page: int, total_pages: int, items: list):
    return {
        "page": page,
        "per_page": len(items),
        "total": sum(len(items) for _ in range(total_pages)),  # not used heavily
        "total_pages": total_pages,
        "data": items,
    }


@responses.activate
def test_basic_action_example():
    # Build two pages; only some items contain 'Action'
    page1_items = [
        {"name": "Game of Thrones", "genre": "Action, Adventure, Drama", "imdb_rating": 9.3},
        {"name": "Avatar: The Last Airbender", "genre": "Action, Animation, Adventure", "imdb_rating": 9.2},
    ]
    page2_items = [
        {"name": "Hagane no renkinjutsushi", "genre": "Action, Fantasy", "imdb_rating": 9.1},
        {"name": "Shingeki no kyojin", "genre": "Action, Drama", "imdb_rating": 8.9},
    ]

    responses.add(
        responses.GET,
        BASE_URL,
        json=make_page_payload(1, 2, page1_items),
        status=200,
        match=[responses.matchers.query_param_matcher({"page": "1"})],
    )
    responses.add(
        responses.GET,
        BASE_URL,
        json=make_page_payload(2, 2, page2_items),
        status=200,
        match=[responses.matchers.query_param_matcher({"page": "2"})],
    )

    assert bestInGenre("Action") == "Game of Thrones"


@responses.activate
def test_genre_case_insensitive_and_spaces():
    # Genres have different cases and spaces
    page_items = [
        {"name": "Show A", "genre": "comedy,Drama", "imdb_rating": 8.0},
        {"name": "Show B", "genre": "Drama , Romance", "imdb_rating": 8.5},
        {"name": "Show C", "genre": "romance, DRAMA", "imdb_rating": 8.7},
    ]

    responses.add(
        responses.GET,
        BASE_URL,
        json=make_page_payload(1, 1, page_items),
        status=200,
        match=[responses.matchers.query_param_matcher({"page": "1"})],
    )

    # Searching for 'drama' lower-case should match
    assert bestInGenre("drama") == "Show C"  # highest rating 8.7


@responses.activate
def test_tie_break_alphabetical():
    page_items = [
        {"name": "Alpha Show", "genre": "Sci-Fi", "imdb_rating": 9.0},
        {"name": "Beta Show", "genre": "Sci-Fi", "imdb_rating": 9.0},
        {"name": "Gamma Show", "genre": "Sci-Fi", "imdb_rating": 8.5},
    ]

    responses.add(
        responses.GET,
        BASE_URL,
        json=make_page_payload(1, 1, page_items),
        status=200,
        match=[responses.matchers.query_param_matcher({"page": "1"})],
    )

    # Alpha Show and Beta Show tie on rating 9.0 -> alphabetically 'Alpha Show' < 'Beta Show'
    assert bestInGenre("Sci-Fi") == "Alpha Show"


@responses.activate
def test_no_results_returns_empty_string():
    page_items = [
        {"name": "Some Show", "genre": "Comedy", "imdb_rating": 7.0}
    ]

    responses.add(
        responses.GET,
        BASE_URL,
        json=make_page_payload(1, 1, page_items),
        status=200,
        match=[responses.matchers.query_param_matcher({"page": "1"})],
    )

    # Searching for genre that doesn't exist in payload -> empty string
    assert bestInGenre("Action") == ""


@responses.activate
def test_api_failure_returns_empty_string():
    # Simulate server error on first page
    responses.add(
        responses.GET,
        BASE_URL,
        status=500,
        match=[responses.matchers.query_param_matcher({"page": "1"})],
    )

    # On API failure, function returns empty string (and logs error)
    assert bestInGenre("Action") == ""
