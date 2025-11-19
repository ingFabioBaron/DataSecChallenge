from common.logging_config import get_logger

logger = get_logger(__name__)

# --- CONSTANTS ---
MINE_INDICATOR = 1
EMPTY_INDICATOR = 0
OUTPUT_MINE = 9

# Directions for the 8 neighbors (delta_row, delta_col)
_NEIGHBOR_DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1)
]


def count_neighbouring_mines(board: list) -> list:
    """
    Public function to calculate the number of neighboring mines for each cell
    in a Minesweeper board. The input board is expected to be validated.

    Each cell in the returned board contains either:
        - OUTPUT_MINE (9) if the cell is a mine.
        - The count of adjacent mines (0-8) if the cell is empty.

    Args:
        board (list): 2D list representing the Minesweeper board
                      where EMPTY_INDICATOR (0) is an empty cell and
                      MINE_INDICATOR (1) is a mine.

    Returns:
        list: 2D list of the same size with mine counts or OUTPUT_MINE.

    Raises:
        ValueError: If the board is invalid (non-rectangular, invalid values, etc.).
        TypeError: If the board or rows are not lists.
    """
    _validate_board(board)

    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    logger.info(f"Board dimensions: rows={rows}, cols={cols}")
    _log_board(board)

    # Initialize result board with zeros
    result_board = [[0 for _ in range(cols)] for _ in range(rows)]

    # --- Minesweeper logic ---
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == MINE_INDICATOR:
                result_board[row][col] = OUTPUT_MINE
            else:
                mine_count = 0
                for dr, dc in _NEIGHBOR_DIRECTIONS:
                    neighbor_row, neighbor_col = row + dr, col + dc
                    if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                        if board[neighbor_row][neighbor_col] == MINE_INDICATOR:
                            mine_count += 1
                result_board[row][col] = mine_count

    logger.info(f"Result board dimensions: rows={rows}, cols={cols}")
    _log_board(result_board)

    return result_board


def _log_board(board: list[list[int]]) -> None:
    """
    Private helper function to log the Minesweeper board row by row.

    Args:
        board (list[list[int]]): 2D list to log.
    """
    logger.info("--- Board ---")
    for row in board:
        logger.info(row)


def _validate_board(board: list[list[int]]) -> None:
    """
    Private helper function to validate the Minesweeper board.

    Ensures the board is:
        - Not None
        - A 2D rectangular list
        - Contains only EMPTY_INDICATOR (0) or MINE_INDICATOR (1) values

    Args:
        board (list[list[int]]): Board to validate.

    Raises:
        ValueError: If the board is None, non-rectangular, or contains invalid values.
        TypeError: If the board or its rows are not lists.
    """
    if board is None:
        raise ValueError("Board must not be None")

    if not isinstance(board, list):
        raise TypeError("Board must be a list of lists")

    if len(board) == 0:
        return  # Empty board is valid

    num_cols = len(board[0])

    for row_index, row in enumerate(board):
        if not isinstance(row, list):
            raise TypeError(f"Row {row_index} must be a list, got {type(row)}")
        if len(row) != num_cols:
            raise ValueError("All rows must have the same number of columns (rectangular board)")
        for col_index, value in enumerate(row):
            if value not in (EMPTY_INDICATOR, MINE_INDICATOR):
                raise ValueError(
                    f"Invalid value {value} at ({row_index},{col_index}). "
                    f"Expected {EMPTY_INDICATOR} or {MINE_INDICATOR}"
                )
