import os
import random

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
    for (r, c), s in self.tiles.items():
      print(s, end="")
      if c == self.cols - 1: print(end="\n")
    print()

  def fill(self, n_max):
    self.fill_by_random(n_max)

  def fill_by_random(self, n_max: int = 26) -> int:
    for i in range(n_max):
      r, c = random.choice(list(self.free))
      self.add_arrow(r, c, i)
    return len(self.arrows)

  def add_arrow(self, row: int, col: int, idx: int):
    n = random.randint(2, 5)
    points: list = [(row, col)]
    self.free.remove((row, col))
    for i in range(n):
      np = r, c = points[-1]
      while np not in self.free:
        dr, dc = random.choice(DIRECTIONS)
        np = r + dr, c + dc
      points.append(np)
      self.free.remove(np)
    self.arrows.add(Arrow(points, idx))
    self.update_tiles()

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

  def update_tiles(self):
    self.tiles = {p: EMPTY for p in self.tiles}
    for a in self.arrows:
      for p in a.points:
        if p not in self.tiles: continue
        self.tiles[p] = a.symbols[p]
    self.free = {p for p in self.tiles if self.tiles[p] == EMPTY}


if __name__ == '__main__':
  board = Board(6, 12)
  for i in range(3):
    r, c = random.choice(list(board.free))
    board.add_arrow(r, c, i)
  board.display_board()

  for i in range(6):
    for a in board.arrows:
      if not board.can_move_step(a):
        a.color = "red"
        continue
      a.move()
      board.update_tiles()
    print()
    board.display_board()
