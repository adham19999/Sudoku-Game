#include "SudokuAPI.h"
#include "Sudoku.h"
#include "SudokuSolver.h"
#include "PuzzleGenerator.h"
#include "FileHandler.h"

// =====================================================
// Board Management
// =====================================================

BoardHandle sudoku_create_board() {
    return new SudokuBoard();
}

void sudoku_delete_board(BoardHandle board) {
    delete static_cast<SudokuBoard*>(board);
}

BoardHandle sudoku_copy_board(BoardHandle board) {
    SudokuBoard* src = static_cast<SudokuBoard*>(board);
    SudokuBoard* copy = new SudokuBoard(*src);
    return copy;
}

// =====================================================
// Board Operations
// =====================================================

int sudoku_get_value(BoardHandle board, int row, int col) {
    SudokuBoard* b = static_cast<SudokuBoard*>(board);
    return b->getValue(row, col);
}

void sudoku_set_value(BoardHandle board, int row, int col, int value) {
    SudokuBoard* b = static_cast<SudokuBoard*>(board);
    b->setValue(row, col, value);
}

int sudoku_is_valid_move(BoardHandle board, int row, int col, int num) {
    SudokuBoard* b = static_cast<SudokuBoard*>(board);
    return b->isValidMove(row, col, num) ? 1 : 0;
}

void sudoku_clear_board(BoardHandle board) {
    SudokuBoard* b = static_cast<SudokuBoard*>(board);
    b->clear();
}

void sudoku_get_board_data(BoardHandle board, int* output) {
    SudokuBoard* b = static_cast<SudokuBoard*>(board);
    const auto& grid = b->getBoard();
    int idx = 0;
    for (int r = 0; r < 9; ++r) {
        for (int c = 0; c < 9; ++c) {
            output[idx++] = grid[r][c];
        }
    }
}

void sudoku_set_board_data(BoardHandle board, const int* data) {
    SudokuBoard* b = static_cast<SudokuBoard*>(board);
    vector<vector<int>> grid(9, vector<int>(9));
    int idx = 0;
    for (int r = 0; r < 9; ++r) {
        for (int c = 0; c < 9; ++c) {
            grid[r][c] = data[idx++];
        }
    }
    b->setBoard(grid);
}

int sudoku_is_solved(BoardHandle board) {
    SudokuBoard* b = static_cast<SudokuBoard*>(board);
    return b->isSolved() ? 1 : 0;
}

// =====================================================
// Puzzle Generation
// =====================================================

BoardHandle sudoku_generate_puzzle(int difficulty, BoardHandle* solution) {
    PuzzleGenerator gen;
    SudokuBoard puzzle = gen.generate(difficulty);
    
    if (solution) {
        // Create a copy for the solution and solve it
        SudokuBoard* sol = new SudokuBoard(puzzle);
        SudokuSolver solver;
        solver.solve(*sol);
        *solution = sol;
    }
    
    return new SudokuBoard(puzzle);
}

BoardHandle sudoku_generate_puzzle_with_clues(int clues, BoardHandle* solution) {
    PuzzleGenerator gen;
    SudokuBoard puzzle = gen.generate(clues);
    
    if (solution) {
        // Create a copy for the solution and solve it
        SudokuBoard* sol = new SudokuBoard(puzzle);
        SudokuSolver solver;
        solver.solve(*sol);
        *solution = sol;
    }
    
    return new SudokuBoard(puzzle);
}

// =====================================================
// Solving
// =====================================================

int sudoku_solve(BoardHandle board) {
    SudokuBoard* b = static_cast<SudokuBoard*>(board);
    SudokuSolver solver;
    return solver.solve(*b) ? 1 : 0;
}

int sudoku_has_solution(BoardHandle board) {
    SudokuBoard* b = static_cast<SudokuBoard*>(board);
    SudokuSolver solver;
    return solver.hasSolution(*b) ? 1 : 0;
}

// =====================================================
// Validation & Error Checking
// =====================================================

int sudoku_check_errors(BoardHandle board, BoardHandle solution, int* errors, int max_errors) {
    SudokuBoard* b = static_cast<SudokuBoard*>(board);
    SudokuBoard* sol = static_cast<SudokuBoard*>(solution);
    
    const auto& board_grid = b->getBoard();
    const auto& sol_grid = sol->getBoard();
    
    int error_count = 0;
    for (int r = 0; r < 9 && error_count < max_errors; ++r) {
        for (int c = 0; c < 9 && error_count < max_errors; ++c) {
            if (board_grid[r][c] != 0 && board_grid[r][c] != sol_grid[r][c]) {
                errors[error_count * 2] = r;
                errors[error_count * 2 + 1] = c;
                error_count++;
            }
        }
    }
    
    return error_count;
}

int sudoku_count_errors(BoardHandle board, BoardHandle solution) {
    SudokuBoard* b = static_cast<SudokuBoard*>(board);
    SudokuBoard* sol = static_cast<SudokuBoard*>(solution);
    
    const auto& board_grid = b->getBoard();
    const auto& sol_grid = sol->getBoard();
    
    int error_count = 0;
    for (int r = 0; r < 9; ++r) {
        for (int c = 0; c < 9; ++c) {
            if (board_grid[r][c] != 0 && board_grid[r][c] != sol_grid[r][c]) {
                error_count++;
            }
        }
    }
    
    return error_count;
}

int sudoku_count_filled(BoardHandle board) {
    SudokuBoard* b = static_cast<SudokuBoard*>(board);
    const auto& grid = b->getBoard();
    
    int filled = 0;
    for (int r = 0; r < 9; ++r) {
        for (int c = 0; c < 9; ++c) {
            if (grid[r][c] != 0) {
                filled++;
            }
        }
    }
    
    return filled;
}

// =====================================================
// File Operations
// =====================================================

int sudoku_load_puzzle(BoardHandle board, const char* filename) {
    SudokuBoard* b = static_cast<SudokuBoard*>(board);
    return b->load(filename) ? 1 : 0;
}

int sudoku_save_puzzle(BoardHandle board, const char* filename) {
    SudokuBoard* b = static_cast<SudokuBoard*>(board);
    return b->save(filename) ? 1 : 0;
}
