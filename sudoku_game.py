"""
Sudoku Game - Pygame GUI with C++ Logic Integration

This is the main game file that integrates:
- Pygame for the graphical interface
- C++ sudoku logic via ctypes bindings (sudoku_binding.py)

The C++ logic handles:
- Puzzle generation
- Validation and solving
- Error checking

The pygame GUI handles:
- Rendering and user interaction
- Visual effects and animations
- Game state management
"""

import pygame
import sys
import copy
import json
import os
import math
from pathlib import Path

# Import the C++ sudoku logic bindings
try:
    from sudoku_binding import SudokuBoard, generate_puzzle
except ImportError as e:
    print(f"Error: Could not import sudoku_binding module: {e}")
    print("Make sure the SudokuGame.dll is built and available.")
    sys.exit(1)

pygame.init()

# =====================================================
# WINDOW
# =====================================================
SW, SH = 1000, 950

screen = pygame.display.set_mode((SW, SH), pygame.NOFRAME)
pygame.display.set_caption("Sudoku Game")

clock = pygame.time.Clock()

# =====================================================
# COLORS
# =====================================================
BG = (10, 15, 30)

C_FIXED = (240, 240, 255)
C_USER = (90, 255, 160)

C_ERR_BG = (255, 70, 70)
C_ERR_NUM = (255, 255, 255)

TEXT = (255, 255, 255)

# =====================================================
# FONTS
# =====================================================
font_num = pygame.font.SysFont("Segoe UI", 32, bold=True)
font_toast = pygame.font.SysFont("Segoe UI", 20)

# =====================================================
# GRID
# =====================================================
GRID_X = 0
GRID_Y = 0
GRID_PADDING = 8
GRID_SIZE = 0
CELL = 0
GRID_TOP_OFFSET = 220
GRID_X_OFFSET = 0
GRID_OVERLAY_OFFSET_X = 0
GRID_OVERLAY_OFFSET_Y = 0
GRID_INSET_X = -2
GRID_INSET_Y = 6
NUM_OFFSET_X = -1
NUM_OFFSET_Y = -2

# =====================================================
# ASSETS
# =====================================================
ASSET_PATHS = {
    "background": "assets/maingamebg.png",
    "grid_bg": "assets/gridbackground.png",
    "grid_overlay": "assets/grid.png",
    "btn_generate": "assets/genratebutton.png",
    "btn_check": "assets/checkbutton.png",
    "btn_solve": "assets/solvebutton.png",
    "btn_save": "assets/savebutton.png",
    "btn_load": "assets/loadbutton.png",
    "btn_clear": "assets/clearbutton.png",
    "btn_exit": "assets/exit.png"
}

# =====================================================
# TOAST
# =====================================================
toast_msg = ""
toast_timer = 0

def toast(msg, frames=160):
    """Display a toast message on screen."""
    global toast_msg
    global toast_timer

    toast_msg = msg
    toast_timer = frames


def draw_toast(target):
    """Draw toast message."""
    global toast_timer

    if toast_timer <= 0:
        return

    alpha = min(220, toast_timer * 2)

    surf = pygame.Surface((420, 55), pygame.SRCALPHA)

    pygame.draw.rect(
        surf,
        (0, 0, 0, alpha),
        surf.get_rect(),
        border_radius=18
    )

    txt = font_toast.render(toast_msg, True, TEXT)

    surf.blit(
        txt,
        txt.get_rect(center=surf.get_rect().center)
    )

    target.blit(
        surf,
        ((SW - surf.get_width()) // 2, SH - 90)
    )

    toast_timer -= 1


def load_images():
    """Load all image assets. Create placeholders if images don't exist."""
    images = {}

    for key, path in ASSET_PATHS.items():
        try:
            images[key] = pygame.image.load(path).convert_alpha()
            print(f"[Game] Loaded image: {path}")
        except (pygame.error, FileNotFoundError):
            # Create placeholder surface if image not found
            print(f"[Game] Warning: Could not load image '{path}', using placeholder")
            
            # Create placeholder surfaces with appropriate sizes
            if key == "background":
                images[key] = pygame.Surface((SW, SH))
                images[key].fill(BG)
            elif key == "grid_bg":
                images[key] = pygame.Surface((450, 450))
                images[key].fill((40, 40, 60))
            elif key == "grid_overlay":
                images[key] = pygame.Surface((450, 450))
                # Draw grid lines
                grid_line_color = (100, 100, 120)
                for i in range(10):
                    x = i * 50
                    y = i * 50
                    thick = 2 if i % 3 == 0 else 1
                    pygame.draw.line(images[key], grid_line_color, (x, 0), (x, 450), thick)
                    pygame.draw.line(images[key], grid_line_color, (0, y), (450, y), thick)
            elif "btn_" in key:
                # Button placeholder
                if key == "btn_exit":
                    images[key] = pygame.Surface((60, 60))
                else:
                    images[key] = pygame.Surface((120, 50))
                images[key].fill((100, 150, 255))
                font = pygame.font.SysFont("Arial", 14)
                label = key.replace("btn_", "").title()
                text = font.render(label, True, (255, 255, 255))
                images[key].blit(text, (5, 5))

    if images["background"].get_size() != (SW, SH):
        images["background"] = pygame.transform.smoothscale(
            images["background"],
            (SW, SH)
        )

    return images


def layout_scene(images):
    """Calculate layout positions for all UI elements."""
    grid_bg = images["grid_bg"]
    grid_overlay = images["grid_overlay"]

    grid_bg_rect = grid_bg.get_rect()
    grid_bg_rect.centerx = SW // 2 + GRID_X_OFFSET
    grid_bg_rect.top = GRID_TOP_OFFSET

    grid_overlay_rect = grid_overlay.get_rect()
    grid_overlay_rect.center = grid_bg_rect.center
    grid_overlay_rect.x += GRID_OVERLAY_OFFSET_X
    grid_overlay_rect.y += GRID_OVERLAY_OFFSET_Y

    clear_img = images["btn_clear"]
    if grid_bg_rect.bottom + clear_img.get_height() + 24 > SH:
        grid_bg_rect.top = SH - clear_img.get_height() - grid_bg_rect.height - 24
        grid_overlay_rect.center = grid_bg_rect.center
        grid_overlay_rect.x += GRID_OVERLAY_OFFSET_X
        grid_overlay_rect.y += GRID_OVERLAY_OFFSET_Y

    left_keys = ["btn_generate", "btn_check", "btn_solve"]
    right_keys = ["btn_save", "btn_load"]

    left_w = max(images[key].get_width() for key in left_keys)
    right_w = max(images[key].get_width() for key in right_keys)

    left_gap = 28
    right_gap = 36

    left_total = sum(images[key].get_height() for key in left_keys) + left_gap * (len(left_keys) - 1)
    right_total = sum(images[key].get_height() for key in right_keys) + right_gap * (len(right_keys) - 1)

    left_x = grid_bg_rect.left - left_w - 40
    if left_x < 20:
        left_x = 20

    right_x = grid_bg_rect.right + 40
    if right_x + right_w > SW - 20:
        right_x = SW - 20 - right_w

    left_y = int(grid_bg_rect.centery - left_total / 2)
    right_y = int(grid_bg_rect.centery - right_total / 2)

    button_rects = {}

    for key in left_keys:
        img = images[key]
        rect = img.get_rect()
        rect.topleft = (left_x + (left_w - rect.width) // 2, left_y)
        button_rects[key] = rect
        left_y += rect.height + left_gap

    for key in right_keys:
        img = images[key]
        rect = img.get_rect()
        rect.topleft = (right_x + (right_w - rect.width) // 2, right_y)
        button_rects[key] = rect
        right_y += rect.height + right_gap

    clear_rect = images["btn_clear"].get_rect()
    clear_rect.centerx = grid_bg_rect.centerx
    clear_rect.top = grid_bg_rect.bottom + 24
    button_rects["btn_clear"] = clear_rect

    exit_img = pygame.transform.scale(images["btn_exit"], (70, 70))
    exit_rect = exit_img.get_rect()
    exit_rect.topright = (SW - 8, 8)
    button_rects["btn_exit"] = exit_rect
    images["btn_exit"] = exit_img

    return grid_bg_rect, grid_overlay_rect, button_rects


# =====================================================
# GRID HELPERS
# =====================================================
def cell_rect(r, c):
    """Get the rectangle for a cell at (row, col)."""
    x = GRID_X + c * CELL
    y = GRID_Y + r * CELL

    return pygame.Rect(x, y, CELL, CELL)


# =====================================================
# DRAW GRID
# =====================================================
def draw_grid(target, board_obj, fixed_board, selected, errors):
    """Draw the sudoku grid with numbers and effects."""
    # Get board data from C++ object
    board = board_obj.get_board()

    # Selected Cell
    if selected:
        sr, sc = selected

        rect = cell_rect(sr, sc)

        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005))

        alpha = 80 + int(pulse * 100)

        glow = pygame.Surface((CELL, CELL), pygame.SRCALPHA)

        glow.fill((124, 58, 237, alpha))

        target.blit(glow, rect)

    # Error Cells
    for r, c in errors:
        rect = cell_rect(r, c)

        err = pygame.Surface((CELL, CELL), pygame.SRCALPHA)

        err.fill((255, 60, 60, 150))

        target.blit(err, rect)

    # Numbers
    for r in range(9):
        for c in range(9):
            value = board[r][c]

            if value != 0:
                if (r, c) in errors:
                    color = C_ERR_NUM

                elif fixed_board[r][c]:
                    color = C_FIXED

                else:
                    color = C_USER

                txt = font_num.render(str(value), True, color)

                base_center = cell_rect(r, c).center
                target.blit(
                    txt,
                    txt.get_rect(
                        center=(
                            base_center[0] + NUM_OFFSET_X,
                            base_center[1] + NUM_OFFSET_Y
                        )
                    )
                )


# =====================================================
# MAIN
# =====================================================
def main():
    """Main game loop."""
    SAVE_FILE = "sudoku_save.json"

    images = load_images()

    grid_bg_rect, grid_overlay_rect, button_rects = layout_scene(images)

    global GRID_X, GRID_Y, GRID_SIZE, CELL
    GRID_SIZE = grid_overlay_rect.width - GRID_INSET_X * 2
    CELL = GRID_SIZE // 9
    used_grid = CELL * 9
    grid_center_offset = (GRID_SIZE - used_grid) // 2
    GRID_X = grid_overlay_rect.left + GRID_INSET_X + grid_center_offset
    GRID_Y = grid_overlay_rect.top + GRID_INSET_Y + grid_center_offset

    # Use C++ logic to generate puzzle
    puzzle_board, solution_board = generate_puzzle(SudokuBoard.DIFFICULTY_EASY)

    # Create fixed board (which cells are given/fixed)
    puzzle_data = puzzle_board.get_board()
    fixed = [
        [puzzle_data[r][c] != 0 for c in range(9)]
        for r in range(9)
    ]

    selected = None
    errors = set()

    start_time = pygame.time.get_ticks()

    mistakes = 0

    while True:
        mouse = pygame.mouse.get_pos()

        # =================================================
        # EVENTS
        # =================================================
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # =============================================
            # MOUSE
            # =============================================
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    clicked = None

                    for name, rect in button_rects.items():
                        if rect.collidepoint(event.pos):
                            clicked = name

                    if clicked == "btn_generate":
                        # Generate new puzzle using C++ logic
                        puzzle_board, solution_board = generate_puzzle(SudokuBoard.DIFFICULTY_EASY)

                        puzzle_data = puzzle_board.get_board()
                        fixed = [
                            [puzzle_data[r][c] != 0 for c in range(9)]
                            for r in range(9)
                        ]

                        selected = None
                        errors.clear()

                        start_time = pygame.time.get_ticks()
                        mistakes = 0

                        toast("New Puzzle Generated!")

                    elif clicked == "btn_solve":
                        # Solve using C++ logic
                        puzzle_board.solve()
                        errors.clear()

                        toast("Puzzle Solved!")

                    elif clicked == "btn_check":
                        # Check errors using C++ logic
                        errors_list = puzzle_board.check_errors(solution_board)
                        errors = set(errors_list)

                        mistakes = len(errors)

                        filled = puzzle_board.count_filled()

                        if not errors and filled == 81:
                            toast("Congratulations! Puzzle Complete!")

                        elif not errors:
                            toast("No Mistakes!")

                        else:
                            toast(f"{mistakes} Mistakes Found!")

                    elif clicked == "btn_clear":
                        # Clear user entries (keep fixed cells)
                        board_data = puzzle_board.get_board()
                        for r in range(9):
                            for c in range(9):
                                if not fixed[r][c]:
                                    puzzle_board.set_value(r, c, 0)

                        errors.clear()

                        toast("Board Cleared!")

                    elif clicked == "btn_save":
                        # Save game state
                        board_data = puzzle_board.get_board()
                        solution_data = solution_board.get_board()
                        
                        save_data = {
                            "board": board_data,
                            "fixed": fixed,
                            "solution": solution_data
                        }

                        with open(SAVE_FILE, "w") as f:
                            json.dump(save_data, f)

                        toast("Game Saved!")

                    elif clicked == "btn_load":
                        # Load game state
                        if os.path.exists(SAVE_FILE):
                            with open(SAVE_FILE) as f:
                                save_data = json.load(f)

                            puzzle_board = SudokuBoard()
                            puzzle_board.set_board(save_data["board"])
                            
                            solution_board = SudokuBoard()
                            solution_board.set_board(save_data["solution"])
                            
                            fixed = save_data["fixed"]

                            errors.clear()

                            toast("Game Loaded!")

                        else:
                            toast("No Save File Found!")

                    elif clicked == "btn_exit":
                        pygame.quit()
                        sys.exit()

                    else:
                        # Click on grid cell
                        mx, my = event.pos

                        if (
                            GRID_X <= mx < GRID_X + GRID_SIZE and
                            GRID_Y <= my < GRID_Y + GRID_SIZE
                        ):

                            row = int((my - GRID_Y) / CELL)
                            col = int((mx - GRID_X) / CELL)

                            if 0 <= row < 9 and 0 <= col < 9:
                                selected = (row, col)

            # =============================================
            # KEYBOARD
            # =============================================
            if event.type == pygame.KEYDOWN and selected:

                r, c = selected

                if event.key == pygame.K_ESCAPE:
                    selected = None

                elif event.key in (
                    pygame.K_BACKSPACE,
                    pygame.K_DELETE,
                    pygame.K_0
                ):

                    if not fixed[r][c]:
                        puzzle_board.set_value(r, c, 0)
                        print(f"[Debug] Cleared cell ({r}, {c})")
                    else:
                        toast("Cannot clear fixed cell!")

                elif pygame.K_1 <= event.key <= pygame.K_9:

                    if fixed[r][c]:
                        print(f"[Debug] Cell ({r}, {c}) is fixed - cannot modify")
                        toast("Cannot modify fixed cell!")
                    else:
                        num = event.key - pygame.K_0
                        current_value = puzzle_board.get_value(r, c)
                        
                        if current_value != 0:
                            print(f"[Debug] Cell ({r}, {c}) already has {current_value}, trying to place {num}")
                            toast(f"Cell already has {current_value}! Clear first.")
                        elif puzzle_board.is_valid_move(r, c, num):
                            puzzle_board.set_value(r, c, num)
                            print(f"[Debug] Placed {num} at ({r}, {c})")
                        else:
                            print(f"[Debug] Invalid move: {num} at ({r}, {c}) - conflicts with row/col/box")
                            toast(f"Invalid! {num} conflicts with row/column/box")

                elif event.key == pygame.K_UP and r > 0:
                    selected = (r - 1, c)

                elif event.key == pygame.K_DOWN and r < 8:
                    selected = (r + 1, c)

                elif event.key == pygame.K_LEFT and c > 0:
                    selected = (r, c - 1)

                elif event.key == pygame.K_RIGHT and c < 8:
                    selected = (r, c + 1)

        # =================================================
        # DRAW
        # =================================================
        scene = pygame.Surface((SW, SH), pygame.SRCALPHA)
        scene.blit(images["background"], (0, 0))
        scene.blit(images["grid_bg"], grid_bg_rect.topleft)

        # Grid
        draw_grid(scene, puzzle_board, fixed, selected, errors)

        scene.blit(images["grid_overlay"], grid_overlay_rect.topleft)

        # Buttons with hover
        for key, rect in button_rects.items():
            hovered = rect.collidepoint(mouse)
            
            if hovered:
                pulse = abs(math.sin(pygame.time.get_ticks() * 0.004))
                glow_alpha = 60 + int(pulse * 80)
                
                # Red glow for clear and exit buttons, green for others
                if key in ("btn_clear", "btn_exit"):
                    glow_color = (255, 100, 100, glow_alpha)
                else:
                    glow_color = (100, 255, 100, glow_alpha)
                
                glow = pygame.Surface((rect.w + 20, rect.h + 20), pygame.SRCALPHA)
                pygame.draw.rect(
                    glow,
                    glow_color,
                    glow.get_rect(),
                    border_radius=15
                )
                scene.blit(glow, (rect.x - 10, rect.y - 10))
                
                scaled = pygame.transform.scale(images[key], (int(rect.w * 1.08), int(rect.h * 1.08)))
                scene.blit(scaled, (int(rect.x - (scaled.get_width() - rect.w) / 2), int(rect.y - (scaled.get_height() - rect.h) / 2)))
            else:
                scene.blit(images[key], rect.topleft)

        draw_toast(scene)

        mask = pygame.Surface((SW, SH), pygame.SRCALPHA)
        pygame.draw.rect(
            mask,
            (255, 255, 255, 255),
            mask.get_rect(),
            border_radius=32
        )
        scene.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        screen.fill(BG)
        screen.blit(scene, (0, 0))

        pygame.display.flip()

        clock.tick(60)


# =====================================================
# START
# =====================================================
if __name__ == "__main__":
    main()
