#include "Sudoku.h"
#include "FileHandler.h"
using namespace std;

SudokuBoard::SudokuBoard() 
    : board(BOARD_SIZE, vector<int>(BOARD_SIZE, EMPTY_CELL)) {
}

int SudokuBoard::getValue(int row, int col) const {
    if (!isValidPosition(row, col)) return -1;
    return board[row][col];
}

void SudokuBoard::setValue(int row, int col, int value) {
    if (isValidPosition(row, col) && value >= 0 && value <= 9) {
        board[row][col] = value;
    }
}

void SudokuBoard::clear() {
    for (auto& row : board) {
        fill(row.begin(), row.end(), EMPTY_CELL);
    }
}

bool SudokuBoard::isValidMove(int row, int col, int num) const {
    if (!isValidPosition(row, col) || num < 1 || num > 9) {
        return false;
    }
    
    // Cell must be empty or we're checking the same cell
    if (board[row][col] != EMPTY_CELL && board[row][col] != num) {
        return false;
    }
    
    return !isInRow(row, num) && 
           !isInCol(col, num) && 
           !isInBox(row - row % BOX_SIZE, col - col % BOX_SIZE, num);
}

bool SudokuBoard::isSolved() const {
    // Check if all cells are filled
    for (int i = 0; i < BOARD_SIZE; ++i) {
        for (int j = 0; j < BOARD_SIZE; ++j) {
            if (board[i][j] == EMPTY_CELL) {
                return false;
            }
        }
    }
    
    // Create a temporary copy to validate without modifying const board
    SudokuBoard tempBoard = *this;
    
    // Check if all values are valid
    for (int i = 0; i < BOARD_SIZE; ++i) {
        for (int j = 0; j < BOARD_SIZE; ++j) {
            int value = tempBoard.getValue(i, j);
            tempBoard.setValue(i, j, EMPTY_CELL); // Temporarily remove
            
            if (!tempBoard.isValidMove(i, j, value)) {
                return false;
            }
            
            tempBoard.setValue(i, j, value); // Restore
        }
    }
    
    return true;
}

bool SudokuBoard::isEmpty() const {
    for (const auto& row : board) {
        for (int cell : row) {
            if (cell != EMPTY_CELL) {
                return false;
            }
        }
    }
    return true;
}

const vector<vector<int>>& SudokuBoard::getBoard() const {
    return board;
}

void SudokuBoard::setBoard(const vector<vector<int>>& newBoard) {
    if (newBoard.size() == BOARD_SIZE && newBoard[0].size() == BOARD_SIZE) {
        board = newBoard;
    }
}

bool SudokuBoard::load(const string& filename) {
    auto loadedBoard = FileHandler::loadPuzzle(filename);
    if (loadedBoard.size() == BOARD_SIZE) {
        board = loadedBoard;
        return true;
    }
    return false;
}

bool SudokuBoard::save(const string& filename) const {
    FileHandler::savePuzzle(filename, board);
    return true;
}

// Private helper methods
bool SudokuBoard::isInRow(int row, int num) const {
    for (int col = 0; col < BOARD_SIZE; ++col) {
        if (board[row][col] == num) {
            return true;
        }
    }
    return false;
}

bool SudokuBoard::isInCol(int col, int num) const {
    for (int row = 0; row < BOARD_SIZE; ++row) {
        if (board[row][col] == num) {
            return true;
        }
    }
    return false;
}

bool SudokuBoard::isInBox(int startRow, int startCol, int num) const {
    for (int i = 0; i < BOX_SIZE; ++i) {
        for (int j = 0; j < BOX_SIZE; ++j) {
            if (board[i + startRow][j + startCol] == num) {
                return true;
            }
        }
    }
    return false;
}

bool SudokuBoard::isValidPosition(int row, int col) const {
    return row >= 0 && row < BOARD_SIZE && col >= 0 && col < BOARD_SIZE;
}