#ifndef SUDOKU_H
#define SUDOKU_H

#include <vector>
#include <string>
using namespace std;
class SudokuBoard {
public:
    static constexpr int BOARD_SIZE = 9;
    static constexpr int BOX_SIZE = 3;
    static constexpr int EMPTY_CELL = 0;
    
    // Constructor
    SudokuBoard();
    
    // Core operations
    int getValue(int row, int col) const;
    void setValue(int row, int col, int value);
    void clear();
    
    // Validation
    bool isValidMove(int row, int col, int num) const;
    bool isSolved() const;
    bool isEmpty() const;
    
    // Board access
    const vector<vector<int>>& getBoard() const;
    void setBoard(const vector<vector<int>>& newBoard);
    
    // File operations
    bool load(const string& filename);
    bool save(const string& filename) const;

private:
    vector<vector<int>> board;
    
    // Helper validation methods
    bool isInRow(int row, int num) const;
    bool isInCol(int col, int num) const;
    bool isInBox(int startRow, int startCol, int num) const;
    
    // Bounds checking
    bool isValidPosition(int row, int col) const;
};

#endif // SUDOKU_H