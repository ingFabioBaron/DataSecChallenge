"""
Manual execution script for the Best-in-Genre challenge (CH02).

This script demonstrates how to call the `bestInGenre` function
from the solution module with a sample genre and logs the result.
"""

from challenges.c02_best_in_genre.solution_best_in_genre import bestInGenre
from common.logging_config import get_logger

logger = get_logger(__name__)


if __name__ == "__main__":
    logger.info("[CH02] Manual execution of bestInGenre()")

    # Genre to test
    genre = "Thriller"

    try:
        # Find the best TV series for the given genre
        result = bestInGenre(genre)
        logger.info(f"\nBest TV series in genre '{genre}': {result}\n")

    except Exception as error:
        logger.error(f"Execution error: {error}")
