# challenges/c01_minesweeper/run.py

from common.logging_config import get_logger
from challenges.c01_minesweeper.solution_minesweeper import count_neighbouring_mines

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("[CH01] Manual execution of count_neighbouring_mines()")

    board = [
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 1, 0, 0]
    ]

    try:
        result = count_neighbouring_mines(board)
        logger.info("Result:")
        for row in result:
            logger.info(row)
    except Exception as e:
        logger.error(f"Execution error: {e}")
