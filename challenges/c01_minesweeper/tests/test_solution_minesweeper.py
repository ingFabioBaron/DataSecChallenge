"""
Test suite for the Minesweeper solution (challenge 01).

Organized in Gherkin style:
- Given: setup or input data
- When: the action being tested
- Then: assertions and expected outcomes
"""

import pytest
from challenges.c01_minesweeper.solution_minesweeper import count_neighbouring_mines
from common.logging_config import get_logger

logger = get_logger(__name__)


def test_count_neighbouring_mines_basic_grid():
    """
    Scenario: Validate Minesweeper neighbor counting on a standard 4x4 grid.

    Given a 4x4 Minesweeper board with mines indicated by 1
    When count_neighbouring_mines() is called
    Then the resulting board must correctly show counts and mines
    """
    logger.info("[CH01] Running test: count_neighbouring_mines_basic_grid")

    # Given
    input_board = [
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 1, 0, 0]
    ]

    expected_board = [
        [1, 9, 2, 1],
        [2, 3, 9, 2],
        [3, 9, 4, 9],
        [9, 9, 3, 1]
    ]

    # When
    result_board = count_neighbouring_mines(input_board)

    # Then
    assert result_board == expected_board


def test_count_neighbouring_mines_empty_board():
    """
    Scenario: Validate behavior with a board containing no mines.

    Given a 3x3 board with all cells empty (0)
    When count_neighbouring_mines() is called
    Then all cells should have a count of 0
    """
    logger.info("[CH01] Running test: count_neighbouring_mines_empty_board")

    # Given
    input_board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    expected_board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    # When
    result_board = count_neighbouring_mines(input_board)

    # Then
    assert result_board == expected_board


def test_count_neighbouring_mines_all_mines():
    """
    Scenario: Validate behavior with a board full of mines.

    Given a 2x2 board with all cells containing mines
    When count_neighbouring_mines() is called
    Then all cells should be marked as mines (9)
    """
    logger.info("[CH01] Running test: count_neighbouring_mines_all_mines")

    # Given
    input_board = [
        [1, 1],
        [1, 1]
    ]

    expected_board = [
        [9, 9],
        [9, 9]
    ]

    # When
    result_board = count_neighbouring_mines(input_board)

    # Then
    assert result_board == expected_board


def test_count_neighbouring_mines_single_cell():
    """
    Scenario: Validate behavior with a 1x1 board.

    Given a 1x1 board
    When count_neighbouring_mines() is called
    Then the result should match the input (mine=9, empty=0)
    """
    logger.info("[CH01] Running test: count_neighbouring_mines_single_cell")

    # Given - empty cell
    input_board_empty = [[0]]
    expected_board_empty = [[0]]

    # When
    result_empty = count_neighbouring_mines(input_board_empty)

    # Then
    assert result_empty == expected_board_empty

    # Given - mine cell
    input_board_mine = [[1]]
    expected_board_mine = [[9]]

    # When
    result_mine = count_neighbouring_mines(input_board_mine)

    # Then
    assert result_mine == expected_board_mine


def test_count_neighbouring_mines_rectangular_board():
    """
    Scenario: Validate behavior with non-square rectangular boards.

    Given a 2x4 rectangular board with some mines
    When count_neighbouring_mines() is called
    Then counts should be calculated correctly for all cells
    """
    logger.info("[CH01] Running test: count_neighbouring_mines_rectangular_board")

    # Given
    input_board = [
        [1, 0, 0, 1],
        [0, 1, 0, 0]
    ]

    expected_board = [
        [9, 2, 2, 9],
        [2, 9, 2, 1]
    ]

    # When
    result_board = count_neighbouring_mines(input_board)

    # Then
    assert result_board == expected_board


def test_count_neighbouring_mines_invalid_value():
    """
    Scenario: Validate error handling for invalid cell values.

    Given a board with invalid values (not 0 or 1)
    When count_neighbouring_mines() is called
    Then a ValueError should be raised
    """
    logger.info("[CH01] Running test: count_neighbouring_mines_invalid_value")

    # Given
    input_board = [
        [0, 2, 0],
        [0, 0, 0]
    ]

    # When/Then
    with pytest.raises(ValueError, match="Invalid value"):
        count_neighbouring_mines(input_board)


def test_count_neighbouring_mines_non_rectangular():
    """
    Scenario: Validate error handling for non-rectangular boards.

    Given a board with inconsistent row lengths
    When count_neighbouring_mines() is called
    Then a ValueError should be raised
    """
    logger.info("[CH01] Running test: count_neighbouring_mines_non_rectangular")

    # Given
    input_board = [
        [0, 0, 0],
        [1, 1]
    ]

    # When/Then
    with pytest.raises(ValueError, match="rectangular"):
        count_neighbouring_mines(input_board)


def test_count_neighbouring_mines_none_board():
    """
    Scenario: Validate error handling for None input.

    Given a None board
    When count_neighbouring_mines() is called
    Then a ValueError should be raised
    """
    logger.info("[CH01] Running test: count_neighbouring_mines_none_board")

    # Given
    input_board = None

    # When/Then
    with pytest.raises(ValueError, match="must not be None"):
        count_neighbouring_mines(input_board)


def test_count_neighbouring_mines_invalid_type():
    """
    Scenario: Validate error handling for invalid board type.

    Given a board that is not a list
    When count_neighbouring_mines() is called
    Then a TypeError should be raised
    """
    logger.info("[CH01] Running test: count_neighbouring_mines_invalid_type")

    # Given
    input_board = "not a list"

    # When/Then
    with pytest.raises(TypeError, match="must be a list"):
        count_neighbouring_mines(input_board)


def test_count_neighbouring_mines_corner_cases():
    """
    Scenario: Validate counting for mines in corners and edges.

    Given a board with mines only in corners
    When count_neighbouring_mines() is called
    Then center and edge cells should have correct counts
    """
    logger.info("[CH01] Running test: count_neighbouring_mines_corner_cases")

    # Given
    input_board = [
        [1, 0, 1],
        [0, 0, 0],
        [1, 0, 1]
    ]

    expected_board = [
        [9, 2, 9],
        [2, 4, 2],
        [9, 2, 9]
    ]

    # When
    result_board = count_neighbouring_mines(input_board)

    # Then
    assert result_board == expected_board