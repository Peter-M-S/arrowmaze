import os
import random
import re


def get_hamilton_path(rows:int , cols: int) -> list:
  filename = f"hamilton_{rows}x{cols}.txt"
  if filename in os.listdir("paths"):
    with open("paths/" + filename, "r") as f:
      line = random.choice(f.readlines())
      path = [tuple(map(int, s.split(","))) for s in re.findall(r"(\d+, \d+)", line)]
      return path
  else:
    print("File not found")
    return []


def path_to_segments(path):
  """
  Zerlegt einen Pfad in seine 'Richtungssegmente' (für spätere Pfeil-Erkennung).
  Gibt Liste von (start_index, end_index, direction) zurück.
  """
  if len(path) < 2:
    return []

  def direction(a, b):
    dr, dc = b[0] - a[0], b[1] - a[1]
    return (dr, dc)

  segments = []
  seg_start = 0
  current_dir = direction(path[0], path[1])

  for i in range(1, len(path) - 1):
    d = direction(path[i], path[i + 1])
    if d != current_dir:
      segments.append((seg_start, i, current_dir))
      seg_start = i
      current_dir = d
  segments.append((seg_start, len(path) - 1, current_dir))
  return segments


if __name__ == '__main__':
   path = get_hamilton_path(6,5)
   segments = path_to_segments(path)

   


