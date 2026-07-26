from board import Board
from arrow import Arrow

ROWS,COLS = 6, 10
ARROWS_MAX = int(ROWS*COLS/2)
LIVES = 3


def main():
  board = Board(ROWS, COLS)
  arrows_n = board.fill(ARROWS_MAX)
  lives = LIVES
  game_over = False

  board.display_board()
  while not game_over:
    s = input("enter your choice: ")
    if s not in Arrow.TAILS:
      print("Invalid choice")
      continue

    arrow = [a for a in board.arrows if a.tail == s][0]
    if arrow.color != 'white':
      print("arrow died")
      continue
    if arrow.points[-1] not in board.tiles:
      print("arrow is already out")
      continue

    if board.can_move_out(arrow):
      while arrow.points[-1] in board.tiles:
        arrow.move()
        board.update_tiles()
      board.display_board()

    elif board.can_move_step(arrow):
      arrow.move()
      board.update_tiles()
      board.display_board()

    else:
      arrow.color = 'red'
      lives -= 1
      print(f"arrow {arrow.tail} blocked. lives: {lives}")

    if lives == 0:
      print("Game Over")
      game_over = True

    if len(board.free) == len(board.tiles):
      print("Game solved!")
      game_over = True


if __name__ == '__main__':
    main()

# todo generate solvable puzzles (no blocking arrows)
# todo use all fields for generating arrows


