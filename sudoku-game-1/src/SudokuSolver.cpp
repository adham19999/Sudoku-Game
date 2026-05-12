#include "SudokuSolver.h"
#include "Sudoku.h"

// Add constructor implementation
SudokuSolver::SudokuSolver() {
}

bool SudokuSolver::solve(SudokuBoard &board) {
    int row, col;
    if (!findEmptyCell(board, row, col)) {
        return true; 
    }
    
    return solveRecursive(board, row, col);
}

bool SudokuSolver::hasSolution(const SudokuBoard& board) {
    SudokuBoard tempBoard = board; 
    return solve(tempBoard);
}

bool SudokuSolver::solveRecursive(SudokuBoard& board, int row, int col) {
    if (!findEmptyCell(board, row, col)) {
        return true;
    }
    for (int num = 1; num <= 9; ++num) {
        if (board.isValidMove(row, col, num)) {
            board.setValue(row, col, num);
            int nextRow, nextCol;
            if (!findEmptyCell(board, nextRow, nextCol)) {
                return true; 
            }
            
            if (solveRecursive(board, nextRow, nextCol)) {
                return true;
            }
            board.setValue(row, col, SudokuBoard::EMPTY_CELL);
        }
    }
    
    return false;
}

bool SudokuSolver::findEmptyCell(const SudokuBoard& board, int& row, int& col) const {
    for (row = 0; row < SudokuBoard::BOARD_SIZE; ++row) {
        for (col = 0; col < SudokuBoard::BOARD_SIZE; ++col) {
            if (board.getValue(row, col) == SudokuBoard::EMPTY_CELL) {
                return true;
            }
        }
    }
    return false;
}