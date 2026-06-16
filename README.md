# Sudoku Game

![Current Design](predesign.png)

![Final Design](desgin.png)

A software engineering course project built as a full two-layer application. The frontend is written in Python using Pygame, and the backend logic is written in C++ and exposed to Python as a compiled DLL. The project practices clean separation of concerns, language interoperability, and algorithm design.

---

## Requirements

- Python 3.7 or higher
- Pygame
- Windows (compiled C++ DLL included)

```
pip install pygame
```

---

## How to run

```
python sudoku_game.py
```

---

## Controls

| Input | Action |
|---|---|
| Click cell | Select a cell |
| Arrow keys | Move between cells |
| 1 - 9 | Place a number |
| Delete / Backspace | Clear a cell |
| Escape | Deselect |
| Generate | New puzzle |
| Check | Validate your solution |
| Solve | Auto-solve the puzzle |
| Save / Load | Save or restore progress |
| Clear | Remove all your entries |

---

## Architecture

The game is split into two layers. Python handles the interface and C++ handles all the logic — solving, generating, and validating — compiled as a DLL and called from Python via ctypes.

---

## Author

Adham Ayman Mohamed
