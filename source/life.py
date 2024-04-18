from time import sleep

import gc
import screennorm
import gc9a01

Grid = list[list[bool]]

ROWS = 40
COLS = 40
PIXELSIZE = 240 // ROWS
# ROWS = 5
# COLS = 80
grid1 = []
grid2 = []
BLACK = gc9a01.BLACK
WHITE = gc9a01.WHITE

# For 5x80
# INITIAL_GRID = """
# xxoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# xxoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# ooxxoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# ooxxoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# """

BEACON = """
xxoo
xxoo
ooxx
ooxx
"""

PULSAR = """
ooxxxoooxxxoo
ooooooooooooo
xooooxoxoooox
xooooxoxoooox
xooooxoxoooox
ooxxxoooxxxoo
ooooooooooooo
ooxxxoooxxxoo
xooooxoxoooox
xooooxoxoooox
xooooxoxoooox
ooooooooooooo
ooxxxoooxxxoo
"""

GLIDER = """
oox
xox
oxx
"""

GOSPER_GLIDER_GUN = """
.........................x............
.......................x.x............
.............xx......xx............xx.
............x...x....xx............xx.
.xx........x.....x...xx...............
.xx........x...x.xx....x.x............
...........x.....x.......x............
............x...x.....................
.............xx.......................
"""


R_PENTOMINO = """
.xx
xx.
.x.
"""

DIEHARD = """
......x.
xx......
.x...xxx
"""

ACORN = """
.x.....
...x...
xx..xxx
"""

def neighbour_at(grid: Grid, x: int, y: int) -> int:
    return int(grid[x][y]) if 0 <= x < COLS and 0 <= y < ROWS else 0


def count_neighbours(grid: Grid, x: int, y: int) -> int:
    res = 0
    if neighbour_at(grid, x - 1, y - 1):
        res += 1
    if neighbour_at(grid, x - 1, y):
        res += 1
    if neighbour_at(grid, x - 1, y + 1):
        res += 1

    if neighbour_at(grid, x, y - 1):
        res += 1
    if neighbour_at(grid, x, y + 1):
        res += 1

    if neighbour_at(grid, x + 1, y - 1):
        res += 1
    if neighbour_at(grid, x + 1, y):
        res += 1
    if neighbour_at(grid, x + 1, y + 1):
        res += 1
    return res


def calc_next_state(neighbours: int, prev_state: bool) -> bool:
    if neighbours < 2:
        return False

    if neighbours > 3:
        return False

    if neighbours == 3 and not prev_state:
        return True

    return prev_state

def update(dst: Grid, src: Grid):
    for x in range(COLS):
        for y in range(ROWS):
            neighbours = count_neighbours(grid=src, x=x, y=y)
            dst[x][y] = calc_next_state(
                neighbours=neighbours,
                prev_state=src[x][y],
            )

def show(grid: Grid):
    for y in range(ROWS):
        for x in range(COLS):
            print('x' if grid[x][y] else 'o', end='')
        print()

def show_tft(grid: Grid, screen):
    for x in range(ROWS):
        for y in range(COLS):
            screen.tft.fill_rect(
                x * PIXELSIZE,
                y * PIXELSIZE,
                PIXELSIZE,
                PIXELSIZE,
                WHITE if grid[x][y] else BLACK,
            )


def parse_grid(s: str, grid: Grid, offset = None):
    rows = s.strip().splitlines()
    dx, dy = offset or (
        COLS // 2 - len(rows[0]) // 2,
        ROWS // 2 - len(rows) // 2,
    )
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            grid[x + dx][y + dy] = c == 'x'


def initialize(grid: Grid):
    for _ in range(COLS):
        grid.append([False] * ROWS)


def vos_main(pattern):
    screen = screennorm.ScreenNorm()

    gc.collect()
    initialize(grid1)
    initialize(grid2)
    parse_grid({
        "pulsar": PULSAR,
        "beacon": BEACON,
        "glider": GLIDER,
        "gosper_glider_gun": GOSPER_GLIDER_GUN,
    }[pattern], grid1)

    while True:
        show_tft(grid1, screen)
        update(grid2, grid1)
        show_tft(grid2, screen)
        update(grid1, grid2)
