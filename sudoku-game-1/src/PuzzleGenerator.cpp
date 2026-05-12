#include "PuzzleGenerator.h"
#include <algorithm>
#include <ctime>
using namespace std;

PuzzleGenerator::PuzzleGenerator() 
    : rng(static_cast<unsigned int>(time(nullptr))) {
}

SudokuBoard PuzzleGenerator::generate(Difficulty difficulty) {
    return generate(static_cast<int>(difficulty));
}

SudokuBoard PuzzleGenerator::generate(int cellsToRemove) {
    SudokuBoard board;
    fillDiagonalBoxes(board);
    fillRemaining(board, 0, 0);
    removeCells(board, cellsToRemove);
    
    return board;
}

void PuzzleGenerator::fillDiagonalBoxes(SudokuBoard& board) {
    for (int box = 0; box < 3; ++box) {
        int startRow = box * SudokuBoard::BOX_SIZE;
        int startCol = box * SudokuBoard::BOX_SIZE;
        
        vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9};
        shuffle(numbers.begin(), numbers.end(), rng);
        
        int idx = 0;
        for (int i = 0; i < SudokuBoard::BOX_SIZE; ++i) {
            for (int j = 0; j < SudokuBoard::BOX_SIZE; ++j) {
                board.setValue(startRow + i, startCol + j, numbers[idx++]);
            }
        }
    }
}

bool PuzzleGenerator::fillRemaining(SudokuBoard& board, int row, int col) {
    // Move to next column/row
    if (col >= SudokuBoard::BOARD_SIZE) {
        col = 0;
        row++;
    }
    
    // Base case: All cells filled
    if (row >= SudokuBoard::BOARD_SIZE) {
        return true;
    }
    
    // Skip already filled cells (diagonal boxes)
    if (board.getValue(row, col) != SudokuBoard::EMPTY_CELL) {
        return fillRemaining(board, row, col + 1);
    }
    
    // Try random numbers
    vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    shuffle(numbers.begin(), numbers.end(), rng);
    
    for (int num : numbers) {
        if (board.isValidMove(row, col, num)) {
            board.setValue(row, col, num);
            
            if (fillRemaining(board, row, col + 1)) {
                return true;
            }
            
            // Backtrack
            board.setValue(row, col, SudokuBoard::EMPTY_CELL);
        }
    }
    
    return false;
}

void PuzzleGenerator::removeCells(SudokuBoard& board, int count) {
    vector<pair<int, int>> positions;
    
    // Create list of all positions
    for (int i = 0; i < SudokuBoard::BOARD_SIZE; ++i) {
        for (int j = 0; j < SudokuBoard::BOARD_SIZE; ++j) {
            positions.push_back({i, j});
        }
    }
    
    // Shuffle and remove
    shuffle(positions.begin(), positions.end(), rng);
    
    int removed = 0;
    for (const auto& pos : positions) {
        if (removed >= count) break;
        
        int row = pos.first;
        int col = pos.second;
        
        board.setValue(row, col, SudokuBoard::EMPTY_CELL);
        removed++;
    }
}