import random

from pathlib import Path
from dataclasses import dataclass

from networkx import DiGraph, simple_cycles
from generators.grid import Grid, DIRECTIONS

CWD = Path(__file__).parent.parent


@dataclass
class Cell:
  position: tuple
  arrow_idx: int
  head_idx: int
  direction: tuple  # direction towards head or head's direction


def _save(arrows: list):
  arrows: tuple = tuple(arrows)  # todo check for doubles, then need to sort
  filepath = CWD / f"puzzles/solvable_{ROWS}x{COLS}.txt"
  with open(filepath, "a+") as f:
    f.write(str(arrows) + "\n")
  print("file saved")


def create_grid(arrows: list) -> Grid:
  # arrow_idx based on current order of arrows
  G = Grid(ROWS, COLS)
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

  for new_arrow_idx, new_arrow in enumerate(arrows):
    DAG = add_arrow_to_DAG(DAG, new_arrow, new_arrow_idx, G)

  return DAG


def add_arrow_to_DAG(DAG: DiGraph, arrow: list, arrow_idx: int, G: Grid) -> DiGraph:
  """
    Betrachte jeden Pfeil als Knoten in einem gerichteten Graphen (Directed Acyclic Graph, DAG).
    Eine gerichtete Kante von Knoten $A$ zu Knoten $B$ bedeutet: "Pfeil A blockiert den Fluchtweg von Pfeil B“.
    Damit das Puzzle lösbar ist, darf der Graph absolut keine Zyklen enthalten
    (kein $A$ blockiert $B$ und $B$ blockiert $A$).
  """
  # new_arrow is already in G
  arrow: set = set(arrow)
  for cell in G.cells.values():
    if not cell or cell.head_idx: continue  # ignor empty cells or not-head-cells
    # found arrow head
    way_out = G.ways_out[cell.position][cell.direction]
    if arrow.intersection(way_out):  # new_arrow is blocking this arrow
      DAG.add_edge(arrow_idx, cell.arrow_idx)

  return DAG


def remove_arrow_from_DAG(DAG: DiGraph, arrow_idx: int) -> DiGraph:
  DAG.remove_node(arrow_idx)
  return DAG


def has_no_cycles(DAG: DiGraph) -> bool:
  cycles = list(simple_cycles(DAG))
  return not bool(cycles)


def grow_arrow(arrow: list, G: Grid, free: set, way_out: list) -> tuple[list, set]:
  # grow arrow if possible
  pos = arrow[-1]
  while len(arrow) < MAX_LENGTH:
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

  # at this point arrows is solvable but grid is still empty
  G = create_grid(arrows)
  print(f"full ratio {G.full_ratio:4.1%}")
  print(f"{len(arrows)} arrows generated")
  return G, arrows


def fill_gaps(G: Grid, arrows: list) -> tuple[Grid, list]:
  # to fill remaining gaps bigger than 1
  # generate a new arrow head and second point
  # grow new arrow
  # add new arrow to Grid and DAG
  # check for solvable (no cycles in DAG)
  # if solvable add to arrows
  # else undo and mark as seen

  seen: set = G.single_cells  # no arrow start possible in singles
  free: set = G.free_cells
  DAG: DiGraph = grid_to_DAG(G, arrows)
  counter = 0
  while free - seen:
    counter += 1
    print(counter, len(free - seen))
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

      success = has_no_cycles(DAG)
      print(f"{success=}")
      if success:
        print(f" new arrow added {new_arrow}")
        arrows.append(tuple(new_arrow))
        seen = G.single_cells
        free = G.free_cells
        break  # for, no other neighbor of pos to check
      else:
        print(f" arrow not added")
        G = remove_arrow_from_grid(G, new_arrow)
        DAG = remove_arrow_from_DAG(DAG, new_arrow_idx)
        seen.add(new_arrow[0])  # starting position
        free = G.free_cells

  print(f"full ratio {G.full_ratio:4.1%}")
  print(f"{len(arrows)} arrows generated")
  return G, arrows


if __name__ == '__main__':
  ROWS = COLS = 11
  MAX_LENGTH = 10

  for seed in (1002, 1003):
    random.seed(seed)

    G: Grid = Grid(ROWS, COLS)
    arrows: list = []

    G, arrows = reverse_generator(G, arrows)
    print("first step done")

    G, arrows = fill_gaps(G, arrows)
    print("second step done")

    # todo fill singles by elongation of adjacent arrow

    DAG: DiGraph = grid_to_DAG(G, arrows)
    if has_no_cycles(DAG):
      print(seed, "has no cycles")
      # _save(arrows)
    else:
      print(seed, "cycles detected")


# def display_grid(grid: Grid) -> None:
#   for r in range(grid.rows):
#     for c in range(grid.cols):
#       cell: Cell | bool = grid.grid[r, c]
#       if not cell:
#         s = "."
#       elif cell.head_idx == 0:
#         s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ##########"[cell.arrow_idx]
#       else:
#         s = "abcdefghijklmnopqrstuvwxyz0123456789"[cell.arrow_idx]
#       print(s, end="")
#     print(end="\n")
#   print(f"{len(grid.free_cells) / len(grid.grid)}")
#   print()
#
#
# def get_way_out(free_edges: set, free: set, inwards: dict, max_inwards: int) -> tuple[list, int, int, int, int]:
#   r, c = random.choice(list(free_edges))
#   way = [(r, c)]
#   dr, dc = random.choice(inwards[(r, c)])
#   steps = 0
#   while (n_pos := (r + dr, c + dc)) in free and steps < max_inwards:
#     r, c = n_pos
#     steps += 1
#     way.append((r, c))
#   return way, r, c, dr, dc