from common.logging_config import get_logger

logger = get_logger(__name__)

# --- CONSTANTS ---
INPUT_MINE_INDICATOR:  int = 1
INPUT_EMPTY_SPACE:     int = 0
OUTPUT_MINE_INDICATOR: int = 9

DIRECTIONS = [ # Directions for the 8 neighbors (dr=delta row, dc=delta column)
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1)
]

def count_neighbouring_mines(board: list) -> list:
    """
    Counts neighbouring mines for each cell in a Minesweeper board.
    All input validations are handled by the 'validate_input' function prior to execution.

    Parameters:
        board (list): A validated 2D list (matrix) where 0 represents an empty space
                      and 1 represents a mine.

    Returns:
        list: A 2D list (matrix) of the same dimensions where each cell contains:
              - 9 if the input cell contained a mine (1) (This value is commonly used
                to denote a mine in the resulting board).
              - otherwise the count of neighbouring mines (0-8).

    Raises:
        Exceptions raised by validate_input (ValueError, TypeError).
    """
    # Run all input validations first. An exception is raised if validation fails.
    _validate_input(board)

    rows = len(board)
    cols = len(board[0]) # input is guaranteed to be rectangular by the validation function.

    logger.info(f"Board dimensions: (rows, cols) = ({rows}, {cols})")
    _print_board(board)

    # Initialize the result matrix with zeros
    result = [[0 for _ in range(cols)] for _ in range(rows)]

    # --- Minesweeper Logic ---
    for r in range(rows):
        for c in range(cols):
            # If the cell is a mine (1), mark it as 9 in the result
            if board[r][c] == INPUT_MINE_INDICATOR:
                result[r][c] = OUTPUT_MINE_INDICATOR
            else:
                # If the cell is empty (0), calculate the neighbor mine count
                count = 0
                for dr, dc in DIRECTIONS:
                    nr, nc = r + dr, c + dc  # Neighbor coordinates (new row, new col)

                    # Boundary check: ensure the neighbor is within the grid limits
                    is_in_bounds = (0 <= nr < rows) and (0 <= nc < cols)

                    if is_in_bounds:
                        # If the neighbor is a mine (1), increment the count
                        if board[nr][nc] == INPUT_MINE_INDICATOR:
                            count += 1

                # Assign the final count to the empty cell
                result[r][c] = count

    logger.info(f"Result Board dimensions: (rows, cols) = ({rows}, {cols})")
    _print_board(result)

    return result

def _print_board(board: list) -> None:
    logger.info("--- Board ---")
    for row in board:
        logger.info(row)


def _validate_input(board: list) -> None:
    """
    Performs all necessary validations on the Minesweeper board.
    It ensures the input is a non-None, rectangular 2D list containing
    only integer values of 0 or 1.

    Args:
        board (list): The 2D list (matrix) to validate.

    Raises:
        ValueError: If board is None, non-rectangular, or contains invalid values (not 0 or 1).
        TypeError: If board or its rows are not lists.
    """
    # 1. Validation for None
    if board is None:
        raise ValueError("board must not be None")

    # 2. Top-level Type Validation
    if not isinstance(board, list):
        raise TypeError("board must be a list (2D list)")

    rows = len(board)
    if rows == 0:
        return  # Empty board is considered valid

    cols = None

    # 3. Row and Element Validation
    for i, row in enumerate(board):
        # 3.1. Row Type Validation
        if not isinstance(row, list):
            raise TypeError(f"Each row must be a list (row {i} is {type(row)})")

        # 3.2. Column Count and Rectangularity Validation
        if cols is None:
            # Set column count based on the first row
            cols = len(row)
        elif len(row) != cols:
            # Check if all subsequent rows match the first row's length
            raise ValueError("All rows must have the same number of columns (rectangular board)")

        # 3.3. Value Validation
        for j, val in enumerate(row):
            # Check if values are restricted to 0 or 1
            if val not in (INPUT_EMPTY_SPACE, INPUT_MINE_INDICATOR):
                raise ValueError(f"Board values must be {INPUT_EMPTY_SPACE}] "
                                 f"or {INPUT_MINE_INDICATOR}. "
                                 f"Found {val} at ({i},{j})")

    # if no error then return...
    return