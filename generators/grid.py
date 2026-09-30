from operator import ifloordiv

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


class Grid:

  def __init__(self, rows: int, cols: int) -> None:
    self.rows = rows
    self.cols = cols
    self.cells: dict = {(r, c): False for r in range(self.rows) for c in range(self.cols)}
    self.neighbors: dict = self.get_neighbors()
    # self.edges: set = {(r, c) for (r, c) in self.cells
    #                    if r == 0 or c == 0 or r == self.rows - 1 or c == self.cols - 1
    #                    }
    # self.inwards: dict = self.get_inwards()
    # self.blocking: dict = {p: self.get_blockings(p) for p in self.cells}
    self.ways_out: dict = {p: self.get_ways_out(p) for p in self.cells}

  def get_neighbors(self) -> dict:
    neighbors: dict = {}
    for r, c in self.cells:
      candidates = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
      neighbors[(r, c)]: set = {p for p in candidates if p in self.cells}
    return neighbors

  # def get_inwards(self) -> dict:
  #   inwards = dict()
  #   for (r, c) in self.edges:
  #     inwards[(r, c)] = []
  #     for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
  #       if (nr, nc) not in self.cells: inwards[(r, c)].append((r - nr, c - nc))
  #   return inwards

  # def get_blockings(self, pos) -> set:
  #   b = set()
  #   for dr, dc in DIRECTIONS:
  #     r, c = pos
  #     while (r + dr, c + dc) in self.cells:
  #       r += dr
  #       c += dc
  #       b.add((r, c))
  #   return b

  def get_ways_out(self, pos) -> dict:
    wo = {d: [] for d in DIRECTIONS}
    for dr, dc in DIRECTIONS:
      r, c = pos
      while (r + dr, c + dc) in self.cells:
        r += dr
        c += dc
        wo[(dr, dc)].append((r,c))
    return wo

  @property
  def full_cells(self) -> set:
    return {k for k, v in self.cells.items() if v}

  @property
  def free_cells(self) -> set:
    return self.cells.keys() - self.full_cells

  @property
  def single_cells(self) -> set:
    return {pos for pos in self.free_cells if not self.free_cells & self.neighbors[pos]}

  @property
  def free_ratio(self) -> float:
    return (len(self.free_cells) - len(self.single_cells)) / len(self.cells)

  @property
  def full_ratio(self) -> float:
    return len(self.full_cells)/len(self.cells)

  def reset(self) -> None:
    for pos in self.cells:
      self.cells[pos] = False


if __name__ == '__main__':
  g = Grid(5, 5)
  # print(len(g.edges) == 16)
  # print(g.inwards[(4, 4)])
  print(g.single_cells)
  # print(g.blocking[(0,0)])
  print(g.ways_out[(2,2)])
