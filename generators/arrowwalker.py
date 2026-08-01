import random
from pathlib import Path

from grid import Grid

CWD = Path(__file__).parent

ROWS = 15
COLS = 15
MAX_LENGTH = 10
# DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# todo check for more restrictions
#  ray from head to edge must be free
#  check all neighbors in shuffled order until suitable is found
#  cross check is number of arrows > 62 (if tail_id is active)
#  might be need to DFS
#  values in grid: (arrow_idx, point_idx_in this arrow)


def has_isolates(np: tuple, grid: Grid) -> bool:
  # todo find isolated areas up to size n
  grid.grid[np] = True
  result = bool(grid.isolated)
  grid.grid[np] = False
  return result


def head_is_blocked(np: tuple, lp: tuple, grid: Grid) -> bool:
  result = False
  grid.grid[np] = True    # set test point
  (nr, nc), (lr, lc) = np, lp
  dr, dc = nr-lr, nc-lc   # direction of head
  nnp = nr+dr, nc+dc
  while nnp in grid.grid:
    if nnp in grid.full:
      result = True
      break
    nnp = nnp[0]+dr, nnp[1]+dc

  grid.grid[np] = False   # undo test point
  return result


def grow_arrow(arrow: list, current_grid: Grid, max_length: int):

  if len(arrow) == max_length:
    return arrow

  candidates: list = current_grid.neighbors[arrow[-1]]
  random.shuffle(candidates)

  for np in candidates:
    if np in current_grid.full: continue

    if has_isolates(np, current_grid): continue  # todo this is property of grid(np)?

    if head_is_blocked(np, arrow[-1], current_grid): continue

    current_grid.grid[np] = True
    arrow.append(np)
    result = grow_arrow(arrow, current_grid, max_length)
    if result is not None:
      return result
    else:
      current_grid.grid[np] = False
      arrow.pop()

  return None


def main():
  g = Grid(ROWS, COLS)
  impossibles: set = set()

  while g.free - impossibles:
    # find next start point  todo use sorting by key lambda
    p, d_min = g.center, ROWS + COLS
    for np in g.free - impossibles:
      if (d := g.distance(g.center, np)) < d_min:
        d_min, p = d, np

    arrow = [p]  # start of arrow
    g.grid[p] = True

    arrow = grow_arrow(arrow, g, MAX_LENGTH)    # step into next recursion level

    if arrow is not None:
      arrows.append(arrow[::-1])
    else:
      g.grid[p] = False
      impossibles.add(p)

  for a in arrows:
    print(a)

  filepath = CWD / f"paths/arrowwalker_{ROWS}x{COLS}.txt"
  with open(filepath, "a+") as f:
    f.write(str(arrows) + "\n")


if __name__ == '__main__':
  arrows = []
  main()


# start a new arrow line
#  find a point closest to the middle
#  get random length
#  as long as the length is not full and there are possible directions
#   get possible directions
#   choose out of possible directions
#   add to arrow line
#  if grid is not full: next arrow line


