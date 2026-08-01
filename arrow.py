HEAD = {
  (0, 1): "→",
  (0, -1): "←",
  (1, 0): "↓",
  (-1, 0): "↑"
}
LINE = {
  (0, 1, 0, 1): "─",    # horiz
  (0,-1, 0,-1): "─",
  (1, 0, 1, 0): "│",    # verti
  (-1, 0, -1, 0): "│",
  (0, 1, 1, 0): "╮",    # right-down
  (-1, 0, 0, -1): "╮",  # up-left
  (0, -1, 1, 0): "╭",   # left-down
  (-1, 0, 0, 1): "╭",   # up-right
  (0, 1, -1, 0): "╯",   # right-up
  (1, 0, 0, -1): "╯",   # down-left
  (0,-1,-1,0): "╰",     # left-up
  (1, 0, 0, 1): "╰",    # down-right
}


class Arrow:
  TAILS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

  def __init__(self, points: list[tuple[int, int]], idx: int) -> None:
    self.points: list[tuple[int,int]] = points
    self.idx: int = idx
    if self.idx < len(self.TAILS):
      self.tail: str | None = self.TAILS[self.idx]
    else:
      self.tail = None
    self.dr: int = self.points[0][0]-self.points[1][0]
    self.dc: int = self.points[0][1]-self.points[1][1]
    self.symbols: dict = self.get_symbols()
    self.color: str = 'white'

  def get_symbols(self) -> dict:
    symbols: dict = {self.points[0]: HEAD[self.dr, self.dc]}
    ndr, ndc = -self.dr, -self.dc
    for i in range(1, len(self.points)-1):
      lr, lc = self.points[i-1]
      r, c = self.points[i]
      nr, nc = self.points[i+1]
      ldr, ldc = r-lr, c-lc
      ndr, ndc = nr-r, nc-c
      symbols[self.points[i]] = LINE[ldr,ldc, ndr, ndc]
    # symbols[self.points[-1]] = LINE[ndr, ndc, ndr, ndc]
    symbols[self.points[-1]] = self.tail
    return symbols

  def move(self) -> None:
    r,c = self.points[0]
    self.points = [(r+self.dr, c+self.dc)] + self.points
    self.symbols[self.points[0]] = self.symbols[self.points[1]]  # HEAD at front
    self.symbols[self.points[1]] = LINE[(self.dr, self.dc, self.dr, self.dc)]  # hori or verti at 2nd
    del self.symbols[self.points[-1]]
    self.points.pop()
    # todo rewrite to del self.symbols[self.points.pop()] ?
    self.symbols[self.points[-1]] = self.tail


if __name__ == '__main__':
  # test for Arrow class
    arrow = Arrow([(0,3), (0,2), (0,1), (0,0)], 0)
    print(arrow.dr, arrow.dc)
    print(arrow.points)
    arrow.move()
    print(arrow.points)


