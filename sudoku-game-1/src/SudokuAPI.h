#ifndef SUDOKU_API_H
#define SUDOKU_API_H

#ifdef __cplusplus
extern "C" {
#endif

// Board handle (opaque pointer)
typedef void* BoardHandle;

// =====================================================
// Board Management
// =====================================================

/**
 * Create a new empty sudoku board
 * @return Handle to new board
 */
BoardHandle sudoku_create_board();

/**
 * Delete a sudoku board and free memory
 * @param board Handle to board to delete
 */
void sudoku_delete_board(BoardHandle board);

/**
 * Create a copy of a sudoku board
 * @param board Source board
 * @return Handle to new copied board
 */
BoardHandle sudoku_copy_board(BoardHandle board);

// =====================================================
// Board Operations
// =====================================================

/**
 * Get value at position
 * @param board Board handle
 * @param row Row (0-8)
 * @param col Column (0-8)
 * @return Value (0-9), -1 if invalid position
 */
int sudoku_get_value(BoardHandle board, int row, int col);

/**
 * Set value at position
 * @param board Board handle
 * @param row Row (0-8)
 * @param col Column (0-8)
 * @param value Value to set (0-9)
 */
void sudoku_set_value(BoardHandle board, int row, int col, int value);

/**
 * Check if a move is valid
 * @param board Board handle
 * @param row Row (0-8)
 * @param col Column (0-8)
 * @param num Number to check (1-9)
 * @return 1 if valid, 0 if invalid
 */
int sudoku_is_valid_move(BoardHandle board, int row, int col, int num);

/**
 * Clear all cells in the board
 * @param board Board handle
 */
void sudoku_clear_board(BoardHandle board);

/**
 * Get entire board data as flat array (81 integers)
 * @param board Board handle
 * @param output Array to store values (must be 81 integers)
 */
void sudoku_get_board_data(BoardHandle board, int* output);

/**
 * Set entire board from flat array (81 integers)
 * @param board Board handle
 * @param data Array of 81 integers
 */
void sudoku_set_board_data(BoardHandle board, const int* data);

/**
 * Check if board is solved
 * @param board Board handle
 * @return 1 if solved, 0 otherwise
 */
int sudoku_is_solved(BoardHandle board);

// =====================================================
// Puzzle Generation
// =====================================================

/**
 * Generate a new puzzle with given difficulty
 * Generates complete board then removes cells
 * @param difficulty Number of cells to keep (35=easy, 45=medium, 55=hard)
 * @param solution Output board handle for the solution (optional, can be NULL)
 * @return Handle to generated puzzle
 */
BoardHandle sudoku_generate_puzzle(int difficulty, BoardHandle* solution);

/**
 * Generate puzzle with specific number of clues
 * @param clues Number of cells to keep
 * @param solution Output board handle for the solution (optional, can be NULL)
 * @return Handle to generated puzzle
 */
BoardHandle sudoku_generate_puzzle_with_clues(int clues, BoardHandle* solution);

// =====================================================
// Solving
// =====================================================

/**
 * Solve a sudoku puzzle (modifies board in place)
 * @param board Board handle to solve
 * @return 1 if puzzle has solution, 0 otherwise
 */
int sudoku_solve(BoardHandle board);

/**
 * Check if puzzle has a solution without modifying it
 * @param board Board handle to check
 * @return 1 if puzzle has solution, 0 otherwise
 */
int sudoku_has_solution(BoardHandle board);

// =====================================================
// Validation & Error Checking
// =====================================================

/**
 * Check for errors by comparing with solution
 * Returns positions of cells that don't match solution
 * @param board User's board
 * @param solution Solution board
 * @param errors Output array for error positions (pairs of row, col)
 * @param max_errors Maximum errors to return
 * @return Number of errors found
 */
int sudoku_check_errors(BoardHandle board, BoardHandle solution, int* errors, int max_errors);

/**
 * Get number of errors
 * @param board User's board
 * @param solution Solution board
 * @return Number of errors
 */
int sudoku_count_errors(BoardHandle board, BoardHandle solution);

/**
 * Get number of filled cells
 * @param board Board handle
 * @return Number of filled cells (0-81)
 */
int sudoku_count_filled(BoardHandle board);

// =====================================================
// File Operations
// =====================================================

/**
 * Load puzzle from file
 * @param board Board handle to load into
 * @param filename Path to file
 * @return 1 if successful, 0 otherwise
 */
int sudoku_load_puzzle(BoardHandle board, const char* filename);

/**
 * Save puzzle to file
 * @param board Board handle to save
 * @param filename Path to file
 * @return 1 if successful, 0 otherwise
 */
int sudoku_save_puzzle(BoardHandle board, const char* filename);

// =====================================================
// Constants
// =====================================================
#define SUDOKU_BOARD_SIZE 9
#define SUDOKU_EMPTY_CELL 0
#define SUDOKU_DIFFICULTY_EASY 35
#define SUDOKU_DIFFICULTY_MEDIUM 45
#define SUDOKU_DIFFICULTY_HARD 55

#ifdef __cplusplus
}
#endif

#endif // SUDOKU_API_H
