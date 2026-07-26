import random
import re
from pathlib import Path


def _get_hamilton_path(rows:int, cols: int) -> list:
  CWD = Path(__file__).parent
  filename = f"hamilton_{rows}x{cols}.txt"
  filepath = CWD / "paths" / filename
  if filepath.exists():
    with open(filepath, "r") as f:
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
    if n_max > 62:
      raise ValueError("n_max > 62, not enough single character tails")

    base, rem = divmod(length, n_max)
    segments = []
    idx = 0
    for i in range(n_max):
      seg_len = base + (1 if i < rem else 0)
      segments.append(path[idx: idx + seg_len])
      idx += seg_len

    arrows_points = [list(reversed(seg)) for seg in segments]
    return arrows_points


def generate_arrows_list(rows: int, cols: int, n_max: int) -> list:
  path = _get_hamilton_path(rows, cols)
  return _path_to_arrows(path, n_max)


if __name__ == '__main__':

   print(generate_arrows_list(rows=6, cols=5, n_max=8))




