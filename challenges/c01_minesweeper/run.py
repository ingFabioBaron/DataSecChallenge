"""
Manual execution script for the Minesweeper challenge (CH01).

This script demonstrates how to call the `count_neighbouring_mines` function
from the solution module with a sample board and logs the resulting board.
"""

from challenges.c01_minesweeper.solution_minesweeper import count_neighbouring_mines
from common.logging_config import get_logger

logger = get_logger(__name__)


if __name__ == "__main__":
    logger.info("[CH01] Manual execution of count_neighbouring_mines()")

    # Sample Minesweeper board (0 = empty, 1 = mine)
    sample_board = [
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 1, 0, 0]
    ]

    try:
        # Compute the neighboring mine counts
        result_board = count_neighbouring_mines(sample_board)

        logger.info("Resulting board with mine counts:")
        for row in result_board:
            logger.info(row)

    except Exception as error:
        logger.error(f"Execution error: {error}")
