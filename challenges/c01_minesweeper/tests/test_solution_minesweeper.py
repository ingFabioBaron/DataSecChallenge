"""
Test suite for the Minesweeper solution (challenge 01).

Organized in Gherkin style:
- Given: setup or input data
- When: the action being tested
- Then: assertions and expected outcomes
"""

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
