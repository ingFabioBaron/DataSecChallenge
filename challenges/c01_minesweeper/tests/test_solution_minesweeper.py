from challenges.c01_minesweeper.solution_minesweeper import count_neighbouring_mines
from common.logging_config import get_logger

logger = get_logger(__name__)


def test_basic_valid_grid():
    logger.info("[CH01] Running test test_basic_valid_grid()...")

    input_board = [[0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [0, 1, 0, 1],
                   [1, 1, 0, 0]]

    expected = [[1, 9, 2, 1],
                [2, 3, 9, 2],
                [3, 9, 4, 9],
                [9, 9, 3, 1]]

    assert count_neighbouring_mines(input_board) == expected
