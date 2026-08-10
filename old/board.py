import random
from pathlib import Path

from arrow import Arrow

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
EMPTY = "."


class Board:
  def __init__(self, rows, cols):
    self.rows: int = rows
    self.cols: int = cols
    self.tiles: dict = {(r, c): EMPTY for r in range(self.rows) for c in range(self.cols)}
    self.free: set = {p for p in self.tiles if self.tiles[p] == EMPTY}
    self.arrows: set = set()

  def display_board(self):
    # todo identify movable arrows and assign tails only temporarily to them
    for (r, c), s in self.tiles.items():
      print(s, end="")
      if c == self.cols - 1: print(end="\n")
    print()

  def fill(self) -> None:
    arrows: list = self._get_arrows_data()
    for i, data in enumerate(arrows):
      arrow = Arrow(list(data), i)
      self.arrows.add(arrow)
      for p in arrow.points: self.free.remove(p)
    self.update_tiles()

  def _get_arrows_data(self) -> list:
    CWD = Path(__file__).parent
    filename = f"solvable_{self.rows}x{self.cols}.txt"
    filepath = CWD / "generators" / "paths" / filename
    if filepath.exists():
      with (open(filepath, "r") as f):
        lines = f.readlines()
        arrows_data = eval(random.choice(lines))
        return arrows_data
    else:
      print("File not found")
      return []

  def can_move_step(self, a: Arrow) -> bool:
    np = a.points[0][0]+a.dr, a.points[0][1]+a.dc
    return np in self.free or np not in self.tiles

  def can_move_out(self, a: Arrow) -> bool:
    r, c = a.points[0]
    nr, nc = r+a.dr, c+a.dc
    while (nr, nc) in self.tiles:
      if (nr, nc) not in self.free: return False
      nr += a.dr
      nc += a.dc
    return True

  def update_tiles(self) -> None:
    self.tiles = {p: EMPTY for p in self.tiles}
    for a in self.arrows:
      for p in a.positions:
        if p not in self.tiles: continue
        self.tiles[p] = a.symbols[p]
    self.free = {p for p in self.tiles if self.tiles[p] == EMPTY}


if __name__ == '__main__':
  pass

