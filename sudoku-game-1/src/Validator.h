#ifndef VALIDATOR_H
#define VALIDATOR_H

#include "Sudoku.h"
using namespace std;

class Validator {
public:
    static bool isValidBoard(const SudokuBoard& board);
    static bool isValidMove(const SudokuBoard& board, int row, int col, int num);
    static bool isValidRow(const SudokuBoard& board, int row);
    static bool isValidColumn(const SudokuBoard& board, int col);
    static bool isValidBox(const SudokuBoard& board, int boxRow, int boxCol);
    
private:
    // Helper methods
    static bool hasNoDuplicates(const vector<int>& values);
};

#endif 