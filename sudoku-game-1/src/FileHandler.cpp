#include "FileHandler.h"
#include <fstream>
#include <iostream>
using namespace std;

vector<vector<int>> FileHandler::loadPuzzle(const string& filename) {
    vector<vector<int>> board;
    ifstream file(filename);
    
    if (!file.is_open()) {
        cerr << "Error opening file: " << filename << endl;
        return board;
    }

    string line;
    while (getline(file, line)) {
        vector<int> row;
        for (char c : line) {
            if (c >= '0' && c <= '9') {
                row.push_back(c - '0');
            } else if (c == ' ') {
                continue; 
            }
        }
        if (row.size() == 9) {
            board.push_back(row);
        }
    }

    file.close();
    return board;
}

void FileHandler::savePuzzle(const string& filename, const vector<vector<int>>& board) {
    ofstream file(filename);
    
    if (!file.is_open()) {
        cerr << "Error opening file: " << filename << endl;
        return;
    }

    for (const auto& row : board) {
        for (size_t i = 0; i < row.size(); ++i) {
            file << row[i];
            if (i < row.size() - 1) file << " ";
        }
        file << endl;
    }

    file.close();
    cout << "Puzzle saved successfully to " << filename << endl;
}