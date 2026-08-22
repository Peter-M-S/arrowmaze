from operator import ifloordiv

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


class Grid:

  def __init__(self, rows: int, cols: int, mask: set | None = None) -> None:
    self.rows = rows
    self.cols = cols
    self.grid: dict = {(r, c): False for r in range(self.rows) for c in range(self.cols)}
    if mask is not None:
      for p in mask: del self.grid[p]
    self.neighbors: dict = self.get_neighbors()
    self.edges: set = {(r, c) for (r,c) in self.grid
                       if r == 0 or c == 0 or r == self.rows - 1 or c == self.cols - 1
                       }
    self.inwards: dict = self.get_inwards()

  def get_neighbors(self) -> dict:
    neighbors: dict = {}
    for r,c in self.grid:
      candidates = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
      neighbors[(r, c)]: set = {p for p in candidates if p in self.grid}
    return neighbors

  def get_inwards(self) -> dict:
    inwards = dict()
    for (r, c) in self.edges:
      inwards[(r, c)] = []
      for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
        if (nr, nc) not in self.grid: inwards[(r,c)].append((r-nr, c-nc))
    return inwards

  @property
  def full(self) -> set:
    return {k for k,v in self.grid.items() if v}

  @property
  def free(self) -> set:
    return self.grid.keys() - self.full

  def reset(self) -> None:
    for pos in self.grid:
      self.grid[pos] = False


if __name__ == '__main__':
  g = Grid(5, 5)
  print(len(g.edges) == 16)
  print(g.inwards[(4,4)])


