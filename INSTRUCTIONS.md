# Sudoku Game - Instructions & Troubleshooting

## Quick Start

Run the game:
```powershell
cd D:\Kolya\Softwarecourse\SodukuCode
python sudoku_game.py
```

---

## Issue Fixed: Input Handling

### Problem
Board was rejecting keyboard input silently without feedback.

### Solution
Added clear feedback messages and console debugging. Now you'll see:
- Toast notifications explaining why moves are rejected
- Console `[Debug]` messages for troubleshooting
- Immediate visual feedback for valid placements

---

## How Input Works

### Input Validation Flow

When you press a number key (1-9):

```
User presses number key
       ↓
Is cell fixed (blue)?
├─ YES → Toast "Cannot modify fixed cell!" + Return
└─ NO → Continue
       ↓
Does cell already have a value?
├─ YES → Toast "Cell already has X! Clear first." + Return
└─ NO (empty) → Continue
       ↓
Does move violate Sudoku rules?
├─ YES → Toast "Invalid! N conflicts with row/column/box" + Return
└─ NO → Place number ✓
```

### Real-World Scenarios

**Scenario 1: Valid Move (SUCCESS)**
```
Click empty cell (2,3) → Press 5
Result: ✓ Number 5 appears in cell
Console: [Debug] Placed 5 at (2, 3)
```

**Scenario 2: Fixed Cell (PROTECTED)**
```
Click blue cell (0,0) with '8' → Press 3
Result: Toast "Cannot modify fixed cell!"
Console: [Debug] Cell (0, 0) is fixed - cannot modify
Reason: Pre-filled puzzle clues are protected
```

**Scenario 3: Cell Already Filled (MUST CLEAR)**
```
Cell (1,1) contains 7 (you placed it) → Press 2
Result: Toast "Cell already has 7! Clear first."
Console: [Debug] Cell (1, 1) already has 7
Action: Press Delete/Backspace → Then press 2
```

**Scenario 4: Sudoku Conflict (RULE VIOLATION)**
```
Cell (0,1) → Press 8 (but 8 already in row 0)
Result: Toast "Invalid! 8 conflicts with row/column/box"
Console: [Debug] Invalid move: 8 at (0, 1) - conflicts
Reason: Sudoku rules prevent duplicate numbers in same row/column/box
```

---

## Game Controls

| Input | Action |
|-------|--------|
| Click cell | Select cell (highlighted) |
| Arrow keys | Navigate grid |
| 1-9 | Place number (if valid) |
| Delete / Backspace / 0 | Clear cell |
| Escape | Deselect cell |
| Click Generate | New puzzle |
| Click Check | Verify solution |
| Click Solve | Auto-solve puzzle |
| Click Save | Save game state |
| Click Load | Load game state |
| Click Clear | Clear all user entries |
| Click Exit | Quit game |

---

## Interpreting Console Output

When playing, watch the Python console for debug messages:

| Console Output | Meaning | Action |
|---|---|---|
| `[Debug] Placed 5 at (0, 2)` | Success - number entered | Continue ✓ |
| `[Debug] Invalid move: 7 at (1, 3)` | Sudoku conflict | Try different number |
| `[Debug] Cell already has 8` | Cell not empty | Press Delete first |
| `[Debug] Cell (0, 0) is fixed` | Pre-filled cell | Select different cell |
| `[Debug] Cleared cell (2, 1)` | Number removed | Continue |

---

## Testing Checklist

Verify the game works correctly:

- [ ] Start new game (click "Generate")
- [ ] Select an empty cell (should highlight in green)
- [ ] Try entering 1-9: valid moves should work, invalid should show message
- [ ] Try entering a number in a blue (fixed) cell: should show "Cannot modify"
- [ ] Place a number, then try replacing it: should show "Clear first"
- [ ] Clear a number (Delete key) then enter new one: should work
- [ ] Use arrow keys: should navigate to adjacent cells
- [ ] Check console output matches expected behavior

---

## Technical Details

### Cell Colors
- **Blue (Light)** - Fixed cells (pre-filled puzzle clues) - CANNOT modify
- **Green** - User-entered cells - Can clear and replace

### Validation Rules (C++ Logic)

The game enforces standard Sudoku rules:
1. Each number 1-9 appears only once per row
2. Each number 1-9 appears only once per column
3. Each number 1-9 appears only once per 3x3 box
4. Cells cannot contain duplicate numbers

### Code Changes

File: `sudoku_game.py` (lines 520-560)

**Enhanced keyboard input handler with four feedback levels:**

1. **Fixed Cell Detection**
   ```python
   if fixed[r][c]:
       toast("Cannot modify fixed cell!")
       print(f"[Debug] Cell ({r}, {c}) is fixed - cannot modify")
   ```

2. **Already-Filled Cell Detection**
   ```python
   current_value = puzzle_board.get_value(r, c)
   if current_value != 0:
       toast(f"Cell already has {current_value}! Clear first.")
       print(f"[Debug] Cell ({r}, {c}) already has {current_value}")
   ```

3. **Sudoku Conflict Detection**
   ```python
   if puzzle_board.is_valid_move(r, c, num):
       puzzle_board.set_value(r, c, num)
       print(f"[Debug] Placed {num} at ({r}, {c})")
   else:
       toast(f"Invalid! {num} conflicts with row/column/box")
       print(f"[Debug] Invalid move: {num} at ({r}, {c})")
   ```

---

## Troubleshooting

### "Board doesn't take any input"

**Check:**
1. Is the game window in focus? (Click on it)
2. Is a cell selected? (Should be highlighted green)
3. Are you seeing `[Debug]` messages in console?

**Solution:**
- Click a cell first (should highlight)
- Press arrow keys (should move selection)
- Watch console for debug messages

### "Numbers won't place in specific cells"

**Check console output - one of these is happening:**

| Message | Reason | Fix |
|---------|--------|-----|
| "Cannot modify fixed cell" | Cell is blue (pre-filled) | Click different cell |
| "Cell already has X" | Cell not empty | Press Delete first |
| "Invalid! N conflicts" | Sudoku rule violation | Try different number |

### "Game crashes on startup"

**Check:**
1. Python 3.13+ installed? `python --version`
2. Pygame installed? `pip install pygame`
3. DLL built? Check `SudokuGame.dll` exists in root folder

**Solution:**
```powershell
# Install dependencies
pip install pygame

# Rebuild DLL
cd D:\Kolya\Softwarecourse\SodukuCode\sudoku-game-1\build
cmake --build . --config Debug
```

---

## Key Files

| File | Purpose |
|------|---------|
| `sudoku_game.py` | Main game GUI (pygame) |
| `sudoku_binding.py` | C++ to Python bridge |
| `SudokuGame.dll` | C++ logic library |
| `puzzles/` | Sample puzzle files |
| `saved/` | Save game files |
| `assets/` | Image files for UI |

---

## Quick Tips

- **Undo a move:** Press Delete/Backspace on the cell
- **See what's valid:** Console shows `[Debug]` messages
- **Speed up solving:** Click "Solve" button
- **Check your work:** Click "Check" button
- **Start over:** Click "Clear" button
- **Save progress:** Click "Save" button
- **Load saved game:** Click "Load" button

---

## Status

✅ Input handling - Fixed with clear feedback  
✅ Visual feedback - Toast notifications + console output  
✅ Sudoku validation - C++ rules enforced  
✅ Cell protection - Fixed cells cannot be modified  

**Ready to play!**
