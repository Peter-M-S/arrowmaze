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


def hamiltonian_path_random(rows: int, cols: int, max_attempts=200):
  """
    Randomisierter Backtracking-Hamiltonpfad mit mehr natürlichen Ecken.
    Für sehr große Raster kann das lange dauern - ggf. max_attempts erhöhen
    oder auf boustrophedon zurückfallen.
    Erzeugt nicht zwangsläufig Hamilton-KREIS!
    """
  total_cells = rows * cols

  def neighbors(cell):
    r, c = cell
    candidates = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
    random.shuffle(candidates)
    return [(rr, cc) for rr, cc in candidates if 0 <= rr < rows and 0 <= cc < cols]

  def backtrack(path, visited):
    if len(path) == total_cells:
      return path
    current = path[-1]
    for nxt in neighbors(current):
      if nxt not in visited:
        visited.add(nxt)
        path.append(nxt)
        result = backtrack(path, visited)
        if result:
          return result
        path.pop()
        visited.remove(nxt)
    return None

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
  filepath = CWD / f"paths/hamilton_{rows}x{cols}.txt"
  with open(filepath, "a+") as f:
    f.write(str(ham_path) + "\n")
