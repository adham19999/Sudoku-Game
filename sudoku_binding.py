"""
Python ctypes bindings for the Sudoku Game C++ DLL.

This module provides a Python interface to the compiled SudokuGame.dll,
allowing pygame GUI to interact with the C++ sudoku logic.

Usage:
    from sudoku_binding import SudokuBoard
    
    # Create a new board
    board = SudokuBoard()
    
    # Generate a puzzle
    puzzle, solution = SudokuBoard.generate_puzzle(35)
    
    # Manipulate the board
    board.set_value(0, 0, 5)
    value = board.get_value(0, 0)
    
    # Check validity
    if board.is_valid_move(0, 1, 3):
        board.set_value(0, 1, 3)
    
    # Solve
    board.solve()
"""

import ctypes
import os
import sys
from typing import Tuple, List, Optional
from pathlib import Path

# =====================================================
# DLL Loading with Dependency Resolution
# =====================================================

def _add_mingw_to_path():
    """Add MinGW library directory to DLL search path."""
    # Common MinGW installation paths
    mingw_paths = [
        "D:/programing lang/c++ setup/ucrt64/bin",
        "C:/MinGW/bin",
        "C:/MinGW64/bin",
        "C:/mingw64/bin",
        Path.cwd() / "sudoku-game-1" / "build",
    ]
    
    for path in mingw_paths:
        path_str = str(path).replace("/", "\\")
        if os.path.exists(path_str):
            try:
                if sys.version_info >= (3, 8):
                    # Python 3.8+ has os.add_dll_directory
                    os.add_dll_directory(path_str)
                    print(f"[Binding] Added DLL directory: {path_str}")
                break
            except Exception as e:
                continue

# =====================================================
# DLL Loading
# =====================================================

def _find_dll():
    """Find and load the SudokuGame DLL."""
    import glob
    
    # First, try to add MinGW paths to DLL search
    _add_mingw_to_path()
    
    # Possible DLL names (MinGW often prefixes with 'lib')
    dll_names = ["SudokuGame.dll", "libSudokuGame.dll"]
    
    # Check in current working directory first
    for dll_name in dll_names:
        if os.path.exists(dll_name):
            try:
                dll = ctypes.CDLL(dll_name)
                print(f"[Binding] Loaded DLL from current directory: {dll_name}")
                return dll
            except OSError as e:
                print(f"[Binding] Failed to load {dll_name} from current dir: {e}")
                continue
    
    # Check in the same directory as this script
    script_dir = Path(__file__).parent
    for dll_name in dll_names:
        dll_path = script_dir / dll_name
        if dll_path.exists():
            try:
                dll = ctypes.CDLL(str(dll_path))
                print(f"[Binding] Loaded DLL from script directory: {dll_path}")
                return dll
            except OSError as e:
                print(f"[Binding] Failed to load {dll_path}: {e}")
                continue
    
    # Check in build directories
    build_dirs = [
        script_dir / "build",
        script_dir / "sudoku-game-1" / "build",
        Path.cwd() / "build",
        Path.cwd() / "sudoku-game-1" / "build",
    ]
    
    for build_dir in build_dirs:
        if build_dir.exists():
            for dll_name in dll_names:
                dll_path = build_dir / dll_name
                if dll_path.exists():
                    try:
                        dll = ctypes.CDLL(str(dll_path))
                        print(f"[Binding] Loaded DLL from build directory: {dll_path}")
                        return dll
                    except OSError as e:
                        print(f"[Binding] Failed to load {dll_path}: {e}")
                        continue
    
    # Try using glob to find any matching DLL
    for pattern in ["*SudokuGame.dll", "Sudoku*.dll"]:
        for match in Path.cwd().glob(f"**/{pattern}"):
            try:
                dll = ctypes.CDLL(str(match))
                print(f"[Binding] Loaded DLL from glob search: {match}")
                return dll
            except OSError as e:
                print(f"[Binding] Failed to load {match}: {e}")
                continue
    
    # Last resort: try loading by name (system PATH)
    for dll_name in dll_names:
        try:
            dll = ctypes.CDLL(dll_name)
            print(f"[Binding] Loaded DLL from system PATH: {dll_name}")
            return dll
        except OSError as e:
            print(f"[Binding] Failed to load {dll_name} from PATH: {e}")
            continue
    
    raise RuntimeError(
        "Could not find SudokuGame.dll. "
        "Make sure the project is built and the DLL is in PATH or in the build directory."
    )


# Load the DLL
_dll = _find_dll()

# =====================================================
# C Type Definitions
# =====================================================

BoardHandle = ctypes.c_void_p

# =====================================================
# Function Prototypes
# =====================================================

def _setup_functions():
    """Setup all C function signatures."""
    dll = _dll
    
    # Board Management
    dll.sudoku_create_board.argtypes = []
    dll.sudoku_create_board.restype = BoardHandle
    
    dll.sudoku_delete_board.argtypes = [BoardHandle]
    dll.sudoku_delete_board.restype = None
    
    dll.sudoku_copy_board.argtypes = [BoardHandle]
    dll.sudoku_copy_board.restype = BoardHandle
    
    # Board Operations
    dll.sudoku_get_value.argtypes = [BoardHandle, ctypes.c_int, ctypes.c_int]
    dll.sudoku_get_value.restype = ctypes.c_int
    
    dll.sudoku_set_value.argtypes = [BoardHandle, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    dll.sudoku_set_value.restype = None
    
    dll.sudoku_is_valid_move.argtypes = [BoardHandle, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    dll.sudoku_is_valid_move.restype = ctypes.c_int
    
    dll.sudoku_clear_board.argtypes = [BoardHandle]
    dll.sudoku_clear_board.restype = None
    
    dll.sudoku_get_board_data.argtypes = [BoardHandle, ctypes.POINTER(ctypes.c_int)]
    dll.sudoku_get_board_data.restype = None
    
    dll.sudoku_set_board_data.argtypes = [BoardHandle, ctypes.POINTER(ctypes.c_int)]
    dll.sudoku_set_board_data.restype = None
    
    dll.sudoku_is_solved.argtypes = [BoardHandle]
    dll.sudoku_is_solved.restype = ctypes.c_int
    
    # Puzzle Generation
    dll.sudoku_generate_puzzle.argtypes = [ctypes.c_int, ctypes.POINTER(BoardHandle)]
    dll.sudoku_generate_puzzle.restype = BoardHandle
    
    dll.sudoku_generate_puzzle_with_clues.argtypes = [ctypes.c_int, ctypes.POINTER(BoardHandle)]
    dll.sudoku_generate_puzzle_with_clues.restype = BoardHandle
    
    # Solving
    dll.sudoku_solve.argtypes = [BoardHandle]
    dll.sudoku_solve.restype = ctypes.c_int
    
    dll.sudoku_has_solution.argtypes = [BoardHandle]
    dll.sudoku_has_solution.restype = ctypes.c_int
    
    # Validation & Error Checking
    dll.sudoku_check_errors.argtypes = [BoardHandle, BoardHandle, ctypes.POINTER(ctypes.c_int), ctypes.c_int]
    dll.sudoku_check_errors.restype = ctypes.c_int
    
    dll.sudoku_count_errors.argtypes = [BoardHandle, BoardHandle]
    dll.sudoku_count_errors.restype = ctypes.c_int
    
    dll.sudoku_count_filled.argtypes = [BoardHandle]
    dll.sudoku_count_filled.restype = ctypes.c_int
    
    # File Operations
    dll.sudoku_load_puzzle.argtypes = [BoardHandle, ctypes.c_char_p]
    dll.sudoku_load_puzzle.restype = ctypes.c_int
    
    dll.sudoku_save_puzzle.argtypes = [BoardHandle, ctypes.c_char_p]
    dll.sudoku_save_puzzle.restype = ctypes.c_int


_setup_functions()

# =====================================================
# Python Wrapper Classes
# =====================================================

class SudokuBoard:
    """Python wrapper for C++ SudokuBoard."""
    
    # Constants
    BOARD_SIZE = 9
    EMPTY_CELL = 0
    DIFFICULTY_EASY = 35
    DIFFICULTY_MEDIUM = 45
    DIFFICULTY_HARD = 55
    
    def __init__(self, handle: Optional[BoardHandle] = None):
        """
        Initialize a sudoku board.
        
        Args:
            handle: Optional C++ board handle. If None, creates a new board.
        """
        if handle is None:
            self._handle = _dll.sudoku_create_board()
        else:
            self._handle = handle
    
    def __del__(self):
        """Clean up C++ board when Python object is destroyed."""
        if self._handle:
            _dll.sudoku_delete_board(self._handle)
    
    def copy(self) -> 'SudokuBoard':
        """Create a deep copy of this board."""
        new_handle = _dll.sudoku_copy_board(self._handle)
        return SudokuBoard(new_handle)
    
    def get_value(self, row: int, col: int) -> int:
        """Get value at position (returns 0 for empty, -1 for invalid)."""
        return _dll.sudoku_get_value(self._handle, row, col)
    
    def set_value(self, row: int, col: int, value: int) -> None:
        """Set value at position (0 to clear, 1-9 to place number)."""
        _dll.sudoku_set_value(self._handle, row, col, value)
    
    def is_valid_move(self, row: int, col: int, num: int) -> bool:
        """Check if placing num at (row, col) is valid."""
        return bool(_dll.sudoku_is_valid_move(self._handle, row, col, num))
    
    def clear(self) -> None:
        """Clear all cells in the board."""
        _dll.sudoku_clear_board(self._handle)
    
    def get_board(self) -> List[List[int]]:
        """Get entire board as 2D list."""
        data = (ctypes.c_int * 81)()
        _dll.sudoku_get_board_data(self._handle, data)
        
        board = []
        for r in range(9):
            row = []
            for c in range(9):
                row.append(data[r * 9 + c])
            board.append(row)
        return board
    
    def set_board(self, board: List[List[int]]) -> None:
        """Set entire board from 2D list."""
        data = (ctypes.c_int * 81)()
        for r in range(9):
            for c in range(9):
                data[r * 9 + c] = board[r][c]
        _dll.sudoku_set_board_data(self._handle, data)
    
    def is_solved(self) -> bool:
        """Check if puzzle is completely and correctly solved."""
        return bool(_dll.sudoku_is_solved(self._handle))
    
    def solve(self) -> bool:
        """Solve the puzzle (modifies board in place)."""
        return bool(_dll.sudoku_solve(self._handle))
    
    def has_solution(self) -> bool:
        """Check if puzzle has a solution without solving it."""
        return bool(_dll.sudoku_has_solution(self._handle))
    
    def count_filled(self) -> int:
        """Count number of filled cells."""
        return _dll.sudoku_count_filled(self._handle)
    
    def check_errors(self, solution: 'SudokuBoard') -> List[Tuple[int, int]]:
        """
        Check for errors by comparing with solution.
        Returns list of (row, col) positions that are incorrect.
        """
        errors_array = (ctypes.c_int * 162)()  # Max 81 errors * 2
        error_count = _dll.sudoku_check_errors(
            self._handle, 
            solution._handle,
            errors_array,
            81
        )
        
        errors = []
        for i in range(error_count):
            row = errors_array[i * 2]
            col = errors_array[i * 2 + 1]
            errors.append((row, col))
        return errors
    
    def count_errors(self, solution: 'SudokuBoard') -> int:
        """Count number of errors compared to solution."""
        return _dll.sudoku_count_errors(self._handle, solution._handle)
    
    def load_puzzle(self, filename: str) -> bool:
        """Load puzzle from file."""
        return bool(_dll.sudoku_load_puzzle(
            self._handle,
            filename.encode('utf-8')
        ))
    
    def save_puzzle(self, filename: str) -> bool:
        """Save puzzle to file."""
        return bool(_dll.sudoku_save_puzzle(
            self._handle,
            filename.encode('utf-8')
        ))
    
    @staticmethod
    def generate_puzzle(difficulty: int = DIFFICULTY_EASY) -> Tuple['SudokuBoard', 'SudokuBoard']:
        """
        Generate a new puzzle with given difficulty.
        
        Args:
            difficulty: Number of cells to keep (35=easy, 45=medium, 55=hard)
        
        Returns:
            Tuple of (puzzle_board, solution_board)
        """
        solution_handle = BoardHandle()
        puzzle_handle = _dll.sudoku_generate_puzzle(
            difficulty,
            ctypes.byref(solution_handle)
        )
        
        puzzle = SudokuBoard(puzzle_handle)
        solution = SudokuBoard(solution_handle)
        return puzzle, solution
    
    @staticmethod
    def generate_puzzle_with_clues(clues: int) -> Tuple['SudokuBoard', 'SudokuBoard']:
        """
        Generate a new puzzle with specific number of clues.
        
        Args:
            clues: Number of cells to keep (typically 17-45)
        
        Returns:
            Tuple of (puzzle_board, solution_board)
        """
        solution_handle = BoardHandle()
        puzzle_handle = _dll.sudoku_generate_puzzle_with_clues(
            clues,
            ctypes.byref(solution_handle)
        )
        
        puzzle = SudokuBoard(puzzle_handle)
        solution = SudokuBoard(solution_handle)
        return puzzle, solution


# =====================================================
# Module-level functions for convenience
# =====================================================

def create_board() -> SudokuBoard:
    """Create a new empty sudoku board."""
    return SudokuBoard()


def generate_puzzle(difficulty: int = SudokuBoard.DIFFICULTY_EASY) -> Tuple[SudokuBoard, SudokuBoard]:
    """
    Generate a new puzzle with given difficulty.
    
    Args:
        difficulty: 35=easy, 45=medium, 55=hard
    
    Returns:
        Tuple of (puzzle, solution)
    """
    return SudokuBoard.generate_puzzle(difficulty)


# Test if module loads correctly
if __name__ == "__main__":
    print("Sudoku bindings module loaded successfully!")
    
    # Quick test
    board = create_board()
    print(f"Created new board with {board.count_filled()} filled cells")
    
    puzzle, solution = generate_puzzle(SudokuBoard.DIFFICULTY_EASY)
    print(f"Generated puzzle with {puzzle.count_filled()} clues")
    
    board.set_value(0, 0, 5)
    print(f"Set value at (0,0) to 5, is_valid: {board.is_valid_move(0, 0, 5)}")
    print("Module test passed!")
