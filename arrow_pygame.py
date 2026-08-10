import pygame as pg


class Arrow:
  layer: pg.Surface = pg.Surface((200, 200), pg.SRCALPHA)
  thickness: int = 7
  colors = ["black", "blue4", "blue", "red2"]
  acceleration: float = 0.5
  max_speed: float = 15.0

  def __init__(self, positions: tuple[tuple[int, int]], tiles: dict):
    self.positions: tuple[tuple[int, int], ...] = positions  # rc positions of all points
    self.points: dict = {pos: tiles[pos].center for pos in self.positions}
    self.vertices: list = self._get_vertices()
    self.head_direction: tuple = self._get_head_direction()
    self.way_out: set = self._get_way_out(tiles)
    self.is_moving: bool = False
    self.gone: bool = False
    self.set_free: set = set()
    self.color_idx: int = 0
    self.speed: float = 0.0

  def _get_vertices(self) -> list:
    if len(self.points) == 2: return list(self.points.values())

    vertices = [self.points[self.positions[0]]]

    for i in range(1, len(self.positions) - 1):
      (lr, lc), (nr, nc) = self.positions[i - 1], self.positions[i + 1]
      if lr == nr or lc == nc: continue
      vertices.append(self.points[self.positions[i]])

    vertices.append(self.points[self.positions[-1]])
    return vertices

  def _get_head_direction(self) -> tuple:
    dy, dx = self.positions[0][0] - self.positions[1][0], self.positions[0][1] - self.positions[1][1]
    return dx, dy

  def _get_way_out(self, tiles: dict) -> set:
    way_out: set = set()
    r, c = self.positions[0]
    dc, dr = self.head_direction
    while (r := r + dr, c := c + dc) in tiles:
      way_out.add((r, c))
    return way_out

  @property
  def tail_direction(self):
    dx, dy = self.vertices[-2][0] - self.vertices[-1][0], self.vertices[-2][1] - self.vertices[-1][1]
    return (dx / abs(dx), 0) if dx else (0, dy / abs(dy))

  def is_blocked(self, free: set) -> bool:
    return bool(self.way_out - free)

  def update(self, free: set):

    if self.is_moving and self.is_blocked(free):
      self.color_idx = 3
      self.is_moving = False
      self.vertices = self._get_vertices()

    if self.is_moving:
      self.speed = min(self.speed + self.acceleration, self.max_speed)
      self.color_idx = 2
      self.update_vertices()

    self.draw()


  def draw(self):
    self.draw_head(self.vertices[0])
    for p0, p1 in zip(self.vertices[:-1], self.vertices[1:]):
      self.draw_line(p0, p1)

  def update_vertices(self):
    # move head to arrow layer surface
    x, y = self.vertices[0]
    dx, dy = self.head_direction
    nx, ny = x + dx * self.speed, y + dy * self.speed
    delta = 4 * self.thickness
    if -delta <= nx < self.layer.get_width() + delta and -delta <= ny < self.layer.get_height() + delta:
      self.vertices[0] = (nx, ny)

    # move tail to next segment or pop points
    x0, y0 = self.vertices[-1]
    x1, y1 = self.vertices[-2]
    dx, dy = self.tail_direction
    nx, ny = x0 + dx * self.speed, y0 + dy * self.speed

    if (dx, dy) == (0, 1) and ny < y1 or \
        (dx, dy) == (0, -1) and ny > y1 or \
        (dx, dy) == (1, 0) and nx < x1 or \
        (dx, dy) == (-1, 0) and nx > x1:
      self.vertices[-1] = (nx, ny)
    else:
      self.vertices.pop()

    # check which position can be set to free
    for pos, (x, y) in self.points.items():
      if x0 <= x <= nx or nx <= x <= x0 or y0 <= y <= ny or ny <= y <= y0:
        self.set_free.add(pos)

    self.is_moving = len(self.vertices) >= 2

    self.gone = len(self.vertices) < 2

  def draw_head(self, p: tuple[int, int]) -> None:
    x, y = p
    match self.head_direction:
      case (1, 0):
        p0 = x + self.thickness, y
        p1 = x - self.thickness, y - self.thickness
        p2 = x - self.thickness, y + self.thickness
      case (-1, 0):
        p0 = x - self.thickness, y
        p1 = x + self.thickness, y + self.thickness
        p2 = x + self.thickness, y - self.thickness
      case (0, -1):
        p0 = x, y - self.thickness
        p1 = x + self.thickness, y + self.thickness
        p2 = x - self.thickness, y + self.thickness
      case (0, 1):
        p0 = x, y + self.thickness
        p1 = x - self.thickness, y - self.thickness
        p2 = x + self.thickness, y - self.thickness
      case _:
        raise ValueError("Invalid direction index")

    pg.draw.polygon(self.layer, self.colors[self.color_idx], [p0, p1, p2], 0)

  def draw_line(self, p0: tuple[int, int], p1: tuple[int, int]):
    if p0[1] == p1[1]:
      self.draw_hline(p0, p1)
    else:
      self.draw_vline(p0, p1)

  def draw_hline(self, p0: tuple, p1: tuple):
    (x0, y0), (x1, y1) = p0, p1
    if x0 > x1: x0, x1 = x1, x0
    y_top = y0 - self.thickness // 2
    y_bot = y0 + self.thickness // 2
    rect = pg.Rect(x0, y_top, x1 - x0, y_bot - y_top)
    pg.draw.rect(self.layer, self.colors[self.color_idx], rect, 0)
    pg.draw.circle(self.layer, self.colors[self.color_idx], p1, self.thickness // 2)

  def draw_vline(self, p0: tuple, p1: tuple):
    (x0, y0), (x1, y1) = p0, p1
    if y0 > y1: y0, y1 = y1, y0
    x_left = x0 - self.thickness // 2
    x_right = x0 + self.thickness // 2
    rect = pg.Rect(x_left, y0, x_right - x_left, y1 - y0)
    pg.draw.rect(self.layer, self.colors[self.color_idx], rect, 0)
    pg.draw.circle(self.layer, self.colors[self.color_idx], p1, self.thickness // 2)


if __name__ == '__main__':
  pass
