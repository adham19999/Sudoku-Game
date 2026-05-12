#ifndef SUDOKUSOLVER_H
#define SUDOKUSOLVER_H

#include "Sudoku.h"

class SudokuSolver {
public:
    SudokuSolver();
    
    // Method to solve the Sudoku puzzle using backtracking
    bool solve(SudokuBoard& board);
    
    // Method to check if the Sudoku puzzle has a solution
    bool hasSolution(const SudokuBoard& board);
    
private:
    // Backtracking algorithm
    bool solveRecursive(SudokuBoard& board, int row, int col);
    
    // Helper method to find the next empty cell
    bool findEmptyCell(const SudokuBoard& board, int& row, int& col) const;
};

#endif // SUDOKUSOLVER_H