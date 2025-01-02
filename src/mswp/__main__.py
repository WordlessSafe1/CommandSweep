from random import sample

HEIGHT = 16
WIDTH = 16
FLAGS = 50


def main() -> int:
    """Entry Point"""
    grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    init_grid(grid, FLAGS)
    uncovered = [["▒" for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # First move
    print(format_grid(uncovered))
    x, y, flag = get_input()
    while grid[y][x] != 0:
        grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        init_grid(grid, FLAGS)
    uncover_cell(grid, uncovered, x, y)

    # Game Loop
    while True:
        print(format_grid(uncovered))
        if sum(row.count("▒") + row.count("!") for row in uncovered) == FLAGS:
            print("Success!")
            return 0
        x, y, flag = get_input()
        if flag:
            if str(uncovered[y][x]) not in "▒!":
                continue
            uncovered[y][x] = "▒" if uncovered[y][x] == "!" else "!"
            continue
        if uncovered[y][x] == "!":
            continue
        if grid[y][x] == "*":
            finish_grid(grid, uncovered)
            print(format_grid(uncovered))
            print("Fail")
            return 0
        uncover_cell(grid, uncovered, x, y)
    return 0


def finish_grid(grid, field):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if field[y][x] == "▒" or (
                field[y][x] == "!" and grid[y][x] != "*"
            ):
                field[y][x] = "\033[48;5;238m" + str(grid[y][x])


def get_input():
    flag = False
    t = input("X or X,Y: ")
    if len(t) > 0 and t[0] == "!":
        t = t[1:]
        flag = True
    if "," in t:
        try:
            t = [
                int(v.strip(), 10 if v.strip().isdigit() else 16)
                for v in t.split(",")
            ]
            if t[0] >= WIDTH or t[1] >= HEIGHT or t[0] < 0 or t[1] < 0:
                print("Invalid input.")
                return get_input()
            return t[0], t[1], flag
        except (ValueError, IndexError):
            print("Invalid input.")
            return get_input()
    y = input("Y: ")

    try:
        x = int(t.strip(), 10 if t.strip().isdigit() else 16)
        y = int(y.strip(), 10 if t.strip().isdigit() else 16)
        if x >= WIDTH or y >= HEIGHT or x < 0 or y < 0:
            print("Invalid input.")
            return get_input()
        return x, y, flag
    except ValueError:
        print("Invalid input.")
        return get_input()


def format_grid(grid) -> str:
    """
    Generate a string representation of the grid.
    """
    marks = 0
    content = ""
    y = 0
    for row in grid:
        content += f"{hex(y)[2:].upper()}┃ "
        for cell in row:
            if isinstance(cell, str) and len(cell) != 1:
                print()
            match (
                str(cell)
                if (not isinstance(cell, str)) or len(cell) == 1
                else cell[cell.find("m") + 1]
            ):
                case "!" | "*":
                    content += f"\033[91m{cell}\033[0m "
                    marks += 1
                case "1":
                    content += f"\033[92m{cell}\033[0m "
                case "2":
                    content += f"\033[96m{cell}\033[0m "
                case "3":
                    content += f"\033[94m{cell}\033[0m "
                case "4":
                    content += f"\033[93m{cell}\033[0m "
                case "5":
                    content += f"\033[93m{cell}\033[0m "
                case "6":
                    content += f"\033[93m{cell}\033[0m "
                case "7":
                    content += f"\033[93m{cell}\033[0m "
                case "8":
                    content += f"\033[91m{cell}\033[0m "
                case _:
                    content += str(cell) + "\033[49m" + " "
        content += f"┃{hex(y)[2:].upper()}\n"
        y += 1
    content += (
        " ┗"
        + ("━" * (WIDTH * 2 + 1))
        + "┛\n"
        + "   "
        + " ".join(hex(x)[2:].upper() for x in range(WIDTH))
        + "\n"
    )
    content = (
        "   "
        + " ".join(hex(x)[2:].upper() for x in range(WIDTH))
        + "   "
        + str(FLAGS - marks)
        + " / "
        + str(FLAGS)
        + "\n"
        + " ┏"
        + ("━" * (WIDTH * 2 + 1))
        + "┓\n"
        + content
    )
    return content


def init_grid(grid, flags):
    """
    Set *flags* amount of cells as occupied,
    and increase the count of all cells surrounding newly occupied cells.
    """
    tags = sample(range(HEIGHT * WIDTH), flags)
    for flag in tags:
        grid[flag // WIDTH][flag % WIDTH] = "*"
        for x, y in surrounding_cells(flag % WIDTH, flag // WIDTH):
            if isinstance(grid[y][x], int):
                grid[y][x] += 1


def surrounding_cells(x, y):
    """
    Get a list of x,y coordinates for all cells surrounding the provided
    x,y coordinate, excluding ones outside the bounds of the map.
    """
    xs = [x + v for v in range(-1, 2) if x + v < WIDTH and x + v >= 0]
    ys = [y + v for v in range(-1, 2) if y + v < HEIGHT and y + v >= 0]
    return [(x1, y1) for y1 in ys for x1 in xs]


def uncover_cell(grid, uncovered, x, y):
    value = grid[y][x]
    uncovered[y][x] = " " if value == 0 else value
    if value != 0:
        return
    for x1, y1 in surrounding_cells(x, y):
        if x1 == x and y1 == y:
            continue
        if uncovered[y1][x1] != "▒":
            continue
        uncover_cell(grid, uncovered, x1, y1)
    return
