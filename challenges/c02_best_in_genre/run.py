from common.logging_config import get_logger
from challenges.c02_best_in_genre.solution_best_in_genre import bestInGenre

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("[CH02] Manual execution of bestInGenre()")

    # Cambia el género que quieras probar aquí
    genre = "Action"

    try:
        result = bestInGenre(genre)
        print(f"\nBest TV series in genre '{genre}': {result}\n")
    except Exception as e:
        logger.error(f"Execution error: {e}")
