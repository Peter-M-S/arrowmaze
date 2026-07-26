import os
import random
import re


def _get_hamilton_path(rows:int, cols: int) -> list:
  filename = f"hamilton_{rows}x{cols}.txt"
  if filename in os.listdir("paths"):
    with open("paths/" + filename, "r") as f:
      line = random.choice(f.readlines())
      path = [tuple(map(int, s.split(","))) for s in re.findall(r"(\d+, \d+)", line)]
      return path
  else:
    print("File not found")
    return []


def _path_to_arrows(path, n_max) -> list:
    length = len(path)
    if n_max < 0:
      return []
    if n_max > length//2:
      raise ValueError("n_max > length//2, so some arrows will be too short")

    base, rem = divmod(length, n_max)
    segments = []
    idx = 0
    for i in range(n_max):
      seg_len = base + (1 if i < rem else 0)
      segments.append(path[idx: idx + seg_len])
      idx += seg_len

    arrows_points = [list(reversed(seg)) for seg in segments]
    return arrows_points


def generate_board(rows: int, cols: int, n_max: int) -> list:
  path = _get_hamilton_path(rows, cols)
  random_index = random.randint(0, len(path)-1)
  path = path[random_index:] + path[random_index:]
  return _path_to_arrows(path, n_max)


if __name__ == '__main__':

   print(generate_board(rows=6, cols=5, n_max=8))




