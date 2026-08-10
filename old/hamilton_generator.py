import random
from pathlib import Path

CWD = Path(__file__).parent


def hamiltonian_path_boustrophedon(rows, cols):
  """
    Schneller, deterministischer Hamiltonpfad im Schlangenlinien-Muster.
    n = Zeilen, m = Spalten. Gibt Liste von (row, col) Koordinaten zurück.
    """
  path = []
  for r in range(rows):
    columns = range(cols) if r % 2 == 0 else range(cols - 1, -1, -1)
    for c in columns:
      path.append((r, c))
  return path


def hamiltonian_path_random(rows: int, cols: int, max_attempts=200) -> list:
  """
    Randomisierter Backtracking-Hamiltonpfad mit mehr natürlichen Ecken.
    Für sehr große Raster kann das lange dauern - ggf. max_attempts erhöhen
    oder auf boustrophedon zurückfallen.
    Erzeugt nicht zwangsläufig Hamilton-KREIS!
    """
  total_cells = rows * cols
  cells = {(r, c) for r in range(rows) for c in range(cols)}

  neighbors: dict = {}
  for r in range(rows):
    for c in range(cols):
      candidates = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
      random.shuffle(candidates)
      neighbors[(r,c)] = [(rr, cc) for rr, cc in candidates if 0 <= rr < rows and 0 <= cc < cols]

  def backtrack(path: list[tuple], visited):
    if len(path) == total_cells:
      return path
    current = path[-1]
    for nxt in neighbors[current]:
      if nxt not in visited:
        visited.add(nxt)
        # todo check for >2 isolated free points (last-but-one step will see 1 free point)
        if two_isolated_points(visited): return []
        path.append(nxt)
        result = backtrack(path, visited)
        if result:
          return result
        path.pop()
        visited.remove(nxt)
    return None

  def two_isolated_points(points: set) -> bool:
    counter = 0
    for c in cells:
      if c in points: continue
      # c is empty cell / not visited
      counter += all(np in points for np in neighbors[c])
      if counter >= 2: return True
    return False

  for i in range(max_attempts):
    print(f"attempt {i + 1}/{max_attempts}")
    start = (random.randrange(rows), random.randrange(cols))
    visited = {start}
    result = backtrack([start], visited)
    if result:
      return result

  # Fallback, falls Backtracking nicht rechtzeitig konvergiert
  print("not converged")
  # return hamiltonian_path_boustrophedon(rows, cols)
  return None


if __name__ == "__main__":
  rows, cols = 6, 10
  ham_path = hamiltonian_path_random(rows, cols)
  print("Hamiltonpfad:", ham_path)
  print("Anzahl Zellen:", len(ham_path), "erwartet:", rows * cols)
  if len(ham_path) == rows * cols:
    filepath = CWD / f"paths/hamilton_{rows}x{cols}.txt"
    with open(filepath, "a+") as f:
      f.write(str(ham_path) + "\n")
