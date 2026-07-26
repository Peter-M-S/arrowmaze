import random

def hamiltonian_path_boustrophedon(rows, cols):
    """
    Schneller, deterministischer Hamiltonpfad im Schlangenlinien-Muster.
    n = Zeilen, m = Spalten. Gibt Liste von (row, col) Koordinaten zurück.
    """
    path = []
    for r in range(rows):
        cols = range(cols) if r % 2 == 0 else range(cols - 1, -1, -1)
        for c in cols:
            path.append((r, c))
    return path


def hamiltonian_path_random(rows, cols, max_attempts=200):
    """
    Randomisierter Backtracking-Hamiltonpfad mit mehr natürlichen Ecken.
    Für sehr große Raster kann das lange dauern - ggf. max_attempts erhöhen
    oder auf boustrophedon zurückfallen.
    """
    total_cells = rows * cols

    def neighbors(cell):
        r, c = cell
        candidates = [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
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
        print(f"attempt {i+1}/{max_attempts}")
        start = (random.randrange(rows), random.randrange(cols))
        visited = {start}
        result = backtrack([start], visited)
        if result:
            return result

    # Fallback, falls Backtracking nicht rechtzeitig konvergiert
    print("not converged")
    return hamiltonian_path_boustrophedon(rows, cols)


# def path_to_segments(path):
#     """
#     Zerlegt einen Pfad in seine 'Richtungssegmente' (für spätere Pfeil-Erkennung).
#     Gibt Liste von (start_index, end_index, direction) zurück.
#     """
#     if len(path) < 2:
#         return []
#
#     def direction(a, b):
#         dr, dc = b[0]-a[0], b[1]-a[1]
#         return (dr, dc)
#
#     segments = []
#     seg_start = 0
#     current_dir = direction(path[0], path[1])
#
#     for i in range(1, len(path) - 1):
#         d = direction(path[i], path[i+1])
#         if d != current_dir:
#             segments.append((seg_start, i, current_dir))
#             seg_start = i
#             current_dir = d
#     segments.append((seg_start, len(path) - 1, current_dir))
#     return segments


if __name__ == "__main__":
    rows, cols = 6, 10
    path = hamiltonian_path_random(rows, cols)
    print("Hamiltonpfad:", path)
    print("Anzahl Zellen:", len(path), "erwartet:", rows * cols)
    with open(f"paths/hamilton_{rows}x{cols}.txt", "a+") as f:
      f.write(str(path) + "\n")

