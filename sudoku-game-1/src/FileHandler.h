#ifndef FILEHANDLER_H
#define FILEHANDLER_H

#include <string>
#include <vector>
using namespace std;

class FileHandler {
public:
    static vector<vector<int>> loadPuzzle(const string& filename);
    static void savePuzzle(const string& filename, const vector<vector<int>>& puzzle);
};

#endif 