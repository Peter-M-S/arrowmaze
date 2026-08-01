
class Grid:

  def __init__(self, rows: int, cols: int) -> None:
    self.rows = rows
    self.cols = cols
    self.grid: dict = {(r, c): False for r in range(self.rows) for c in range(self.cols)}
    self.neighbors: dict = self.get_neighbors()
    self.center: tuple = self.rows//2, self.cols//2

  def get_neighbors(self) -> dict:
    neighbors: dict = {}
    for r,c in self.grid:
      candidates = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
      neighbors[(r, c)] = [p for p in candidates if p in self.grid]
    return neighbors

  @property
  def full(self) -> set:
    return {k for k,v in self.grid.items() if v}

  @property
  def free(self) -> set:
    return self.grid.keys() - self.full

  @property
  def isolated(self) -> set:
    isolated: set = set()
    for p in self.grid:
      if not self.grid[p] and all(self.grid[np] for np in self.neighbors[p]):
        isolated.add(p)
    return isolated

  @staticmethod
  def distance(p1: tuple, p2: tuple) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


if __name__ == '__main__':
  # test class Grid
  g = Grid(rows=5, cols=5)
  for k, v in g.grid.items():
    print(k, v, g.neighbors[k])
  print(g.full)
  print(g.free)
  print(g.center)
  print(g.distance(g.center, (0, 0)))
  g.grid[(1, 0)] = True
  g.grid[(0, 1)] = True
  print(g.isolated)

