cmake_minimum_required(VERSION 3.16)
project(SudokuGame VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Build as DLL for Python integration
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)

# Source files - Core logic only (no Qt)
set(SOURCES
    src/Sudoku.cpp
    src/SudokuSolver.cpp
    src/PuzzleGenerator.cpp
    src/FileHandler.cpp
    src/Validator.cpp
    src/SudokuAPI.cpp
)

set(HEADERS
    src/FileHandler.h
    src/Sudoku.h
    src/SudokuSolver.h
    src/PuzzleGenerator.h
    src/Validator.h
    src/SudokuAPI.h
)

# Add shared library (DLL) instead of executable
add_library(SudokuGame SHARED ${SOURCES} ${HEADERS})

# Include directories
target_include_directories(SudokuGame PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)

