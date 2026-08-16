import re
import time

import pygame as pg
import random
from pathlib import Path

from arrow_pygame import Arrow


def get_puzzle(rows, cols) -> list:
  CWD = Path(__file__).parent
  filename = f"solvable_{rows}x{cols}.txt"
  filepath = CWD / "puzzles" / filename
  if filepath.exists():
    with (open(filepath, "r") as f):
      lines = f.readlines()
      puzzle = eval(random.choice(lines))
    return puzzle
  else:
    print("File not found")
    return []


def get_grid_sizes() -> list:
  sizes = []
  CWD = Path(__file__).parent
  check_path = CWD / "puzzles"
  for filename in check_path.glob("solvable_*.txt"):
    sizes.append(tuple(map(int, re.findall(r"\d+", str(filename)))))
  return sizes


def init_puzzle() -> tuple[set, dict, list, set, pg.Surface]:
  ROWS, COLS = random.choice(get_grid_sizes())  # number of tiles
  TILE_SIZE = min(30, int(height / ROWS), int(width / COLS))
  THICK = TILE_SIZE // 4
  BOARD_SIZE = ((COLS * TILE_SIZE), (ROWS * TILE_SIZE))  # number of pixel
  X_OFFSET, Y_OFFSET = (width - BOARD_SIZE[0]) // 2, (height - BOARD_SIZE[1]) // 2

  free: set = set()
  tiles: dict = {}
  lost_lives: set = set()
  background = pg.Surface(size)
  background.fill(BG_COLOR)
  for r in range(ROWS):
    for c in range(COLS):
      free.add((r, c))
      x = X_OFFSET + TILE_SIZE // 2 + c * TILE_SIZE
      y = Y_OFFSET + TILE_SIZE // 2 + r * TILE_SIZE
      pg.draw.line(background, "black", (x - 1, y), (x + 1, y), 1)
      pg.draw.line(background, "black", (x, y - 1), (x, y + 1), 1)
      tile_rect = pg.Rect(0, 0, TILE_SIZE, TILE_SIZE)
      tile_rect.center = (x, y)
      tiles[(r, c)] = tile_rect

  # general Arrow settings
  Arrow.thickness = THICK
  Arrow.layer = pg.Surface(size, pg.SRCALPHA)
  puzzle = get_puzzle(ROWS, COLS)  # list or tuple of tuples of all points in arrow
  arrows = [Arrow(arrow, tiles) for arrow in puzzle]
  for a in arrows:
    free -= set(a.positions)
  return free, tiles, arrows, lost_lives, background


def main() -> None:

  free, tiles, arrows, lost_lives, background = init_puzzle()
  selected_arrow = []

  while True:
    clock.tick(FPS)
    for event in pg.event.get():
      if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE: quit()
      if event.type == pg.KEYDOWN and event.key == pg.K_SPACE: pass

    pg.display.set_caption("ArrowMaze  " + " live " * (3-len(lost_lives)))

    if len(lost_lives) >= 3 or not arrows:
      free, tiles, arrows, lost_lives, background = init_puzzle()
      time.sleep(3)
      continue

    m_pos = pg.mouse.get_pos()
    tile = [pos for pos, rect in tiles.items() if rect.collidepoint(m_pos)]
    hover_tile = tile[0] if tile else False

    if pg.mouse.get_pressed()[0] and hover_tile:
      selected_arrow = [a for a in arrows if hover_tile in a.positions]
      if selected_arrow:
        selected_arrow[0].is_moving = True
        if selected_arrow[0].is_blocked(free):
          lost_lives.add(selected_arrow[0])

    window.blit(background, (0, 0))

    Arrow.layer.fill(pg.SRCALPHA)
    for arrow in arrows[::-1]:
      arrow.update(free)
      free.update(arrow.set_free)
      if arrow.gone: arrows.remove(arrow)
    window.blit(Arrow.layer, (0, 0))

    pg.display.flip()


if __name__ == '__main__':
  pg.init()
  size = width, height = 800, 800
  window = pg.display.set_mode(size)
  clock = pg.time.Clock()
  FPS = 100
  BG_COLOR = "grey90"

  main()
