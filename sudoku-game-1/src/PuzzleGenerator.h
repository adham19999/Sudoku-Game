#ifndef PUZZLEGENERATOR_H
#define PUZZLEGENERATOR_H

#include "Sudoku.h"
#include <random>
using namespace std;

class PuzzleGenerator {
public:
    enum Difficulty {
        EASY = 35,
        MEDIUM = 45,
        HARD = 55
    };
    
    PuzzleGenerator();
    
    // Generate puzzle with difficulty level
    SudokuBoard generate(Difficulty difficulty);
    SudokuBoard generate(int cellsToRemove);
    
private:
    mt19937 rng;
    
    // Generation steps
    void fillDiagonalBoxes(SudokuBoard& board);
    bool fillRemaining(SudokuBoard& board, int row, int col);
    void removeCells(SudokuBoard& board, int count);
    
    // Helper
    bool isValidPlacement(const SudokuBoard& board, int row, int col, int num);
};

#endif // PUZZLEGENERATOR_H