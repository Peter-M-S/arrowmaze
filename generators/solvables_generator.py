import random

from pathlib import Path
from dataclasses import dataclass

from networkx import DiGraph, has_path
from generators.grid import Grid, DIRECTIONS

CWD = Path(__file__).parent.parent


@dataclass
class Cell:
  position: tuple
  arrow_idx: int
  head_idx: int
  direction: tuple  # direction towards head or head's direction


def _save(G, arrows: list):
  arrows: tuple = tuple(sorted(arrows))  # todo check for doubles
  filepath = CWD / f"puzzles/solvable_{G.rows}x{G.cols}.txt"
  with open(filepath, "a+") as f:
    f.write(str(arrows) + "\n")
  print("file saved")


def overwrite_grid(G: Grid, arrows: list) -> Grid:
  # arrow_idx based on current order of arrows
  G.reset()
  for arrow_idx, arrow in enumerate(arrows):
    G = add_arrow_to_grid(G, arrow, arrow_idx)
  return G


def add_arrow_to_grid(G: Grid, arrow: list, arrow_idx: int) -> Grid:
  for head_idx, pos in enumerate(arrow):
    (r0, c0), (r1, c1) = arrow[head_idx - 1:head_idx + 1] if head_idx else arrow[:2]
    drdc = r0-r1, c0-c1
    G.cells[pos] = Cell(pos, arrow_idx, head_idx, drdc)
  return G


def remove_arrow_from_grid(G, arrow) -> Grid:
  for pos in arrow:
    G.cells[pos] = False
  return G


def grid_to_DAG(G: Grid, arrows: list) -> DiGraph:

  DAG = DiGraph()

  for arrow_idx, arrow in enumerate(arrows):
    DAG = add_arrow_to_DAG(DAG, arrow, arrow_idx, G)

  return DAG


def add_arrow_to_DAG(DAG: DiGraph, arrow: list, arrow_idx: int, G: Grid) -> DiGraph:
  """
    Betrachte jeden Pfeil als Knoten in einem gerichteten Graphen (Directed Acyclic Graph, DAG).
    Eine gerichtete Kante von Knoten $A$ zu Knoten $B$ bedeutet: "Pfeil A blockiert den Fluchtweg von Pfeil B“.
    Damit das Puzzle lösbar ist, darf der Graph absolut keine Zyklen enthalten
    (kein $A$ blockiert $B$ und $B$ blockiert $A$).
  """
  DAG.add_node(arrow_idx)
  # new_arrow is already in G
  arrow_set: set = set(arrow)
  for cell in G.cells.values():
    if not cell or cell.head_idx: continue  # ignor empty cells or not-head-cells
    # found arrow head
    way_out = G.ways_out[cell.position][cell.direction]
    if arrow_set.intersection(way_out):  # new arrow is blocking an existing arrow
      DAG.add_edge(arrow_idx, cell.arrow_idx)

  head = arrow[0]
  for pos in G.ways_out[head][G.cells[head].direction]:
    cell = G.cells[pos]
    if cell and cell.arrow_idx != arrow_idx:
      DAG.add_edge(cell.arrow_idx, arrow_idx)   # existing arrow is block new arrow

  return DAG


def remove_arrow_from_DAG(DAG: DiGraph, arrow_idx: int) -> DiGraph:
  DAG.remove_node(arrow_idx)
  return DAG


def has_no_cycles(DAG: DiGraph, new_idx: int) -> bool:
  return not any(has_path(DAG, node, new_idx) for node in DAG.successors(new_idx))


def grow_arrow(arrow: list, G: Grid, free: set, way_out: list) -> tuple[list, set]:
  # grow arrow if possible
  pos = arrow[-1]
  while len(arrow) < int(G.rows*1.5):
    for n_pos in G.neighbors[pos] & free:
      if n_pos in way_out: continue  # avoid self blocking
      # found valid n_pos
      arrow.append(n_pos)
      free.remove(n_pos)
      pos = n_pos
      break  # for loop
    else:
      break  # while loop
  return arrow, free


def reverse_generator(G: Grid, arrows: list) -> tuple[Grid, list]:
  '''
  generates only arrows with free ways out
  :return:
  Grid holding cells of arrows
  list of arrows
  '''
  free: set = G.free_cells
  seen: set = set()

  while free - seen:

    pos = random.choice(list(free - seen))  # second point
    # way_out: list = []
    for d in set(DIRECTIONS):
      way_out = G.ways_out[pos][d]
      if way_out and all(p in free for p in way_out):
        # found head
        break  # for loop
    else:
      seen.add(pos)
      continue  # while loop

    # arrow head (way_out[0]) and second point
    arrow: list[tuple] = [way_out[0], pos]
    free = free.difference(arrow)

    arrow, free = grow_arrow(arrow, G, free, way_out)

    arrows.append(tuple(arrow))

  G = overwrite_grid(G, arrows)
  print(f"full ratio {G.full_ratio:4.1%}")
  print(f"{len(arrows)} arrows generated")
  return G, arrows


def fill_gaps(G: Grid, arrows: list) -> tuple[Grid, list]:

  seen: set = G.single_cells  # no arrow start possible in singles
  free: set = G.free_cells
  DAG: DiGraph = grid_to_DAG(G, arrows)

  while free - seen:

    pos: tuple = random.choice(list(free - seen))  # potential head, not a single

    for n_pos in G.neighbors[pos] & free:
      # head and 2nd point
      new_arrow: list[tuple] = [pos, n_pos]
      free = free.difference(new_arrow)
      direction: tuple = pos[0]-n_pos[0], pos[1]-n_pos[1]
      way_out = G.ways_out[pos][direction]

      new_arrow, free = grow_arrow(new_arrow, G, free, way_out)

      new_arrow_idx = len(arrows)  # order of existing arrows does not matter
      G = add_arrow_to_grid(G, new_arrow, new_arrow_idx)  # idx is consistent
      DAG = add_arrow_to_DAG(DAG, new_arrow, new_arrow_idx, G)  # idx is consistent

      success = has_no_cycles(DAG, new_arrow_idx)

      if success:
        arrows.append(tuple(new_arrow))
        seen = G.single_cells
        free = G.free_cells
        break  # for, no other neighbor of pos to check
      else:
        G = remove_arrow_from_grid(G, new_arrow)
        DAG = remove_arrow_from_DAG(DAG, new_arrow_idx)
        seen.add(new_arrow[0])  # starting position
        free = G.free_cells

  print(f"full ratio {G.full_ratio:4.1%}")
  print(f"{len(arrows)} arrows generated")
  return G, arrows


def main(levels: tuple):

  for size in levels:
    ROWS = COLS = size
    for _ in range(5):
      G: Grid = Grid(ROWS, COLS)
      arrows: list = []

      G, arrows = reverse_generator(G, arrows)
      print("first step done")

      G, arrows = fill_gaps(G, arrows)
      print("second step done")

      # todo try to join singles to adjacent arrow

      _save(G, arrows)


if __name__ == '__main__':
  levels = (10, 15, 20, 30, 40)
  # levels = (20,)
  main(levels)
