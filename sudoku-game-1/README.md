# Sudoku Game

## Overview
This project is a console-based Sudoku game implemented in C++. It allows users to load Sudoku puzzles from files, place values on the board, check the validity of the puzzle, and solve it automatically using a backtracking algorithm. The game also supports saving current puzzles and includes optional features such as puzzle generation and advanced solving techniques.
## Current Design
![Current Working Design](PreDesign.png)

## Upcoming Design
![Upcoming Enhanced Design](Design.png)

## Features
- Load Sudoku puzzles from text files.
- Place values on the Sudoku board.
- Check the validity of the current puzzle state.
- Automatically solve puzzles using backtracking.
- Save the current state of the puzzle to a file.
- Generate new Sudoku puzzles of varying difficulty levels (easy, medium, hard).
- Unit tests for the solver and validator classes.

## Project Structure
```
sudoku-game
├── src
│   ├── main.cpp
│   ├── Sudoku.cpp
│   ├── Sudoku.h
│   ├── SudokuSolver.cpp
│   ├── SudokuSolver.h
│   ├── PuzzleGenerator.cpp
│   ├── PuzzleGenerator.h
│   ├── FileHandler.cpp
│   ├── FileHandler.h
│   ├── Validator.cpp
│   └── Validator.h
├── puzzles
│   ├── easy.txt
│   ├── medium.txt
│   └── hard.txt
├── saved
│   └── .gitkeep
├── tests
│   ├── test_solver.cpp
│   └── test_validator.cpp
├── CMakeLists.txt
├── Makefile
└── README.md
```

## Setup Instructions
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Build the project using either CMake or Makefile:
   - For CMake:
    mkdir build
    cd build
    cmake ..
    cmake --build . --config Release
    cd Release
    .\SudokuGame.exe

4. Run the executable generated in the build directory.

## Usage
- Launch the game from the console.
- Follow the on-screen menu to load a puzzle, place values, check validity, solve the puzzle, or save your progress.
- You can also generate new puzzles by selecting the appropriate option in the menu.

