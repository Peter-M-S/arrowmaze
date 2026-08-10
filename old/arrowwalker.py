import random
from pathlib import Path

import board
from generators.grid import Grid

CWD = Path(__file__).parent

ROWS = COLS = 20
MAX_LENGTH = 10
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# todo check for more restrictions
#  ray from head to edge must be free
#  check all neighbors in shuffled order until suitable is found
#  cross check is number of arrows > 62 (if tail_id is active)
#  might be need to DFS
#  values in grid: (arrow_idx, point_idx_in this arrow)
#  after grow arrow: solvable puzzle, with isolated areas. Second step: fill only isolated areas with arrows


def creates_isolates(np: tuple, grid: Grid) -> bool:
  # todo find isolated areas up to size n
  return bool(grid.isolated_singles(np))


def head_is_blocked(np: tuple, lp: tuple, grid: Grid) -> bool:
  (nr, nc), (lr, lc) = np, lp
  dr, dc = nr-lr, nc-lc   # direction of head
  nnp = nr+dr, nc+dc
  while nnp in grid.grid:
    if nnp in grid.full: return True
    if (dr, dc) in grid.head_moves[nnp]: return True
    nnp = nnp[0]+dr, nnp[1]+dc
  return False


def get_next_start_point(g: Grid, excluded: set) -> tuple:
  return min(g.free-excluded, key=lambda p: g.distance(g.center, p))


def grow_primary_arrow(arrow: list, current_grid: Grid, max_length: int):

  if len(arrow) == max_length and not head_is_blocked(arrow[-1], arrow[-2], current_grid):
    return arrow

  if len(arrow) < max_length:
    candidates: list = current_grid.neighbors[arrow[-1]]
    random.shuffle(candidates)

    for np in candidates:
      if np in current_grid.full: continue

      if creates_isolates(np, current_grid): continue

      # if len(arrow) == max_length-1 and head_is_blocked(np, arrow[-1], current_grid): continue

      current_grid.grid[np] = True
      arrow.append(np)
      result = grow_primary_arrow(arrow, current_grid, max_length)
      if result is not None:
        return result
      else:
        current_grid.grid[np] = False
        arrow.pop()

  if len(arrow) >= 2 and not head_is_blocked(arrow[-1], arrow[-2], current_grid):
    return arrow

  return None


def primary_arrows(g: Grid) -> list:
  arrows: list = []
  impossibles: set = set()

  while g.free - impossibles:
    p = get_next_start_point(g, excluded=impossibles)
    arrow = [p]  # start of arrow
    g.grid[p] = True

    arrow = grow_primary_arrow(arrow, g, MAX_LENGTH)  # step into next recursion level

    if arrow is not None:
      arrows.append(arrow[::-1])
    else:
      g.grid[p] = False
      impossibles.add(p)

  return arrows


def get_paths(area: set):
  paths: list = []
  neighbors: dict = {p: {(p[0]+dr, p[1]+dc) for dr, dc in DIRECTIONS if (p[0]+dr, p[1]+dc) in area} for p in area}

  def _dfs(path: list):
    seen: set = set(path)
    p = path[-1]
    nps = neighbors[p] - seen
    if not nps:
      paths.append(path)
      return
    progress = False
    for np in nps:
      progress = True
      _dfs(path+[np])

    if not progress:
      paths.append(path)

  for start in area:
    _dfs([start])

  return paths


def secondary_arrows(g: Grid) -> list:
  arrows: list = []
  secondary_grid: Grid = Grid(g.rows, g.cols)
  secondary_grid.head_moves = g.head_moves

  for area in g.isolated_areas():
    # find list of longest path through this area
    all_paths = get_paths(area)
    max_path_length = max(len(path) for path in all_paths)
    long_paths = [path for path in all_paths if len(path) == max_path_length]
    # print(long_paths)

    # check if one or the other end as head has no blocking -> add to arrows
    for path in long_paths:
      if not head_is_blocked(path[0], path[1], secondary_grid):
        # todo must check for opposite head directions in primary arrows
        arrows.append(path)
        for p in path:
          secondary_grid.grid[p] = True
          g.grid[p] = True
        break

    # check if one or the other end can be connected to existing arrow (tail or head) -> modify arrow

  return arrows


def _save(arrows):
  filepath = CWD / f"paths/arrowwalker_{ROWS}x{COLS}.txt"
  with open(filepath, "a+") as f:
    f.write(str(arrows) + "\n")
  print("file saved")


def two_stage_arrows():
  g: Grid = Grid(ROWS, COLS)
  arrows: list = primary_arrows(g)
  print("primary ", len(arrows))
  g.update_head_moves(arrows)
  print("headmoves updated")
  _save(arrows)

  s_arrows = secondary_arrows(g)
  _save(s_arrows)
  arrows.extend(s_arrows)
  print("secondary", len(arrows))
  # todo check if single isolations can be grabbed by adjacent arrow, otherwise finally accept singles

  _save(arrows)


if __name__ == '__main__':
  two_stage_arrows()
  b = board.Board(ROWS, COLS)
  b.fill(62)
  b.display_board()

# start a new arrow line
#  find a point closest to the middle
#  get random length
#  as long as the length is not full and there are possible directions
#   get possible directions
#   choose out of possible directions
#   add to arrow line
#  if grid is not full: next arrow line


