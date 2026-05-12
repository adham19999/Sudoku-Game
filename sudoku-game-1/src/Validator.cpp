#include "Validator.h"
#include <unordered_set>
using namespace std;

bool Validator::isValidBoard(const SudokuBoard& board) {
    // Check all rows
    for (int row = 0; row < SudokuBoard::BOARD_SIZE; ++row) {
        if (!isValidRow(board, row)) {
            return false;
        }
    }
    
    // Check all columns
    for (int col = 0; col < SudokuBoard::BOARD_SIZE; ++col) {
        if (!isValidColumn(board, col)) {
            return false;
        }
    }
    
    // Check all 3x3 boxes
    for (int boxRow = 0; boxRow < 3; ++boxRow) {
        for (int boxCol = 0; boxCol < 3; ++boxCol) {
            if (!isValidBox(board, boxRow, boxCol)) {
                return false;
            }
        }
    }
    
    return true;
}

bool Validator::isValidMove(const SudokuBoard& board, int row, int col, int num) {
    return board.isValidMove(row, col, num);
}

bool Validator::isValidRow(const SudokuBoard& board, int row) {
    vector<int> values;
    for (int col = 0; col < SudokuBoard::BOARD_SIZE; ++col) {
        int val = board.getValue(row, col);
        if (val != SudokuBoard::EMPTY_CELL) {
            values.push_back(val);
        }
    }
    return hasNoDuplicates(values);
}

bool Validator::isValidColumn(const SudokuBoard& board, int col) {
    vector<int> values;
    for (int row = 0; row < SudokuBoard::BOARD_SIZE; ++row) {
        int val = board.getValue(row, col);
        if (val != SudokuBoard::EMPTY_CELL) {
            values.push_back(val);
        }
    }
    return hasNoDuplicates(values);
}

bool Validator::isValidBox(const SudokuBoard& board, int boxRow, int boxCol) {
    vector<int> values;
    int startRow = boxRow * SudokuBoard::BOX_SIZE;
    int startCol = boxCol * SudokuBoard::BOX_SIZE;
    
    for (int i = 0; i < SudokuBoard::BOX_SIZE; ++i) {
        for (int j = 0; j < SudokuBoard::BOX_SIZE; ++j) {
            int val = board.getValue(startRow + i, startCol + j);
            if (val != SudokuBoard::EMPTY_CELL) {
                values.push_back(val);
            }
        }
    }
    return hasNoDuplicates(values);
}

bool Validator::hasNoDuplicates(const vector<int>& values) {
    unordered_set<int> seen;
    for (int val : values) {
        if (seen.count(val)) {
            return false; // Duplicate found
        }
        seen.insert(val);
    }
    return true;
}