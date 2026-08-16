import random

from pathlib import Path
from dataclasses import dataclass

import networkx as nx
from generators.grid import Grid

CWD = Path(__file__).parent.parent


def _save(arrows: tuple):
  filepath = CWD / f"puzzles/solvable_{ROWS}x{COLS}.txt"
  with open(filepath, "a+") as f:
    f.write(str(arrows) + "\n")
  print("file saved")


@dataclass
class Cell:
  position: tuple
  arrow_idx: int
  head_idx: int
  direction: tuple  # direction towards head

  @property
  def next_position(self) -> tuple:
    return self.position[0] + self.direction[0], self.position[1] + self.direction[1]


def bump_arrows(g: Grid) -> tuple:
  arrows: list = []
  seen: set = set()

  while g.free - seen:
    pos = random.choice(list(g.free - seen))   # potential head
    for npos in g.neighbors[pos]:
      if npos in g.free:                # arrow with at least 2 points
        break  # for

    else:
      seen.add(pos)                     # pos cannot start an arrow
      continue  # while

    # add first 2 points
    arrow_idx: int = len(arrows)
    arrow: list = []

    head_idx: int = len(arrow)
    direction = pos[0]-npos[0], pos[1]-npos[1]
    g.grid[pos] = Cell(pos, arrow_idx, head_idx, direction)
    arrow.append(pos)

    head_idx = len(arrow)
    g.grid[npos] = Cell(npos, arrow_idx, head_idx, direction)
    arrow.append(npos)

    pos = npos

    while len(arrow) < MAX_LENGTH:

      for npos in g.neighbors[pos]:
        if npos in g.free:
          # found valid npos
          break  # for
      else:
        break  # while        # cannot grow arrow anymore

      head_idx = len(arrow)
      direction = pos[0]-npos[0], pos[1]-npos[1]
      g.grid[npos] = Cell(npos, arrow_idx, head_idx, direction)
      arrow.append(npos)
      pos = npos

    # print(arrow)
    arrows.append(tuple(arrow))
  return tuple(sorted(arrows))


def get_cycles(grid: Grid, arrows: tuple) -> list:
  """
    Betrachte jeden Pfeil als Knoten in einem gerichteten Graphen (Directed Acyclic Graph, DAG).
    Eine gerichtete Kante von Knoten $A$ zu Knoten $B$ bedeutet: „Pfeil A blockiert den Fluchtweg von Pfeil B“.
    Damit das Puzzle lösbar ist, darf der Graph absolut keine Zyklen enthalten
    (kein $A$ blockiert $B$ und $B$ blockiert $A$).
  """
  DiG = nx.DiGraph()

  for arrow_B, arrow in enumerate(arrows):
    pos, lpos = arrow[:2]
    dr, dc = pos[0]-lpos[0], pos[1]-lpos[1]
    pos = pos[0] + dr, pos[1] + dc
    while pos in grid.grid:
      if grid.grid[pos]:
        arrow_A = grid.grid[pos].arrow_idx
        DiG.add_edge(arrow_A, arrow_B)
        if len(list(nx.simple_cycles(DiG))) >= 5:
          return [0]*5
      pos = pos[0] + dr, pos[1] + dc

  cycles = nx.simple_cycles(DiG)

  return list(cycles)


if __name__ == '__main__':
  ROWS = COLS = 20
  MAX_LENGTH = 40
  MAX_TRIALS: int = 1_000_000

  max_solvables: int = 10
  solvables: int = 0
  grid: Grid = Grid(ROWS, COLS)
  seen: set = set()

  for i in range(MAX_TRIALS):
    if not i % 100: print(i, seen.__sizeof__()//1e3, "kByte")
    grid.reset()
    arrows = bump_arrows(grid)
    if arrows in seen: continue
    seen.add(arrows)
    cycles = get_cycles(grid, arrows)
    if 0 < len(cycles) < 5:
      print(f"found {len(cycles)} cycles")
      continue
    elif len(cycles) >= 5:
      continue

    print("found valid set of arrows:")
    print(arrows)
    _save(arrows)
    solvables += 1
    if solvables >= max_solvables:
      break

  # found 5 so far
  print(f"found {solvables} solvables")
