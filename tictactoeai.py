import math
import random
from typing import List, Optional, Tuple

player_symbol: str = ""
comp_symbol: str = ""


def create_board() -> List[str]:
    """Initialize a 3x3 tic-tac-toe board"""
    return [" " for _ in range(9)]


def display(board: List[str]) -> None:
    """Print the board in a neat format"""
    print("\n")
    for r in range(3):
        row = " | ".join(board[r * 3 : (r + 1) * 3])
        print(" " + row)
        if r < 2:
            print("---+---+---")
    print("\n")


def display_positions() -> None:
    """Show player the numbering of cells (1-9)"""
    positions = [str(i + 1) for i in range(9)]
    print("Cell numbers:")
    display(positions)


def free_slots(board: List[str]) -> List[int]:
    """Return indices of empty spaces"""
    return [idx for idx, val in enumerate(board) if val == " "]


def check_winner(board: List[str]) -> Optional[str]:
    """Return the winner symbol ('X'/'O'), 'Tie' or None"""
    lines = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),  # rows
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),  # cols
        (0, 4, 8),
        (2, 4, 6),  # diagonals
    ]
    for a, b, c in lines:
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    if " " not in board:
        return "Tie"
    return None


def place_move(board: List[str], index: int, symbol: str) -> None:
    """Put symbol on board"""
    board[index] = symbol


def minimax_algo(
    board: List[str], turn: str, alpha: float = -math.inf, beta: float = math.inf
) -> Tuple[int, Optional[int]]:
    """
    Minimax with alpha-beta pruning.
    Returns (score, best_index)
    score: +1 (computer win), -1 (player win), 0 (tie)
    """
    outcome = check_winner(board)
    if outcome == comp_symbol:
        return 1, None
    elif outcome == player_symbol:
        return -1, None
    elif outcome == "Tie":
        return 0, None

    if turn == comp_symbol:
        best_val = -math.inf
        best_idx: Optional[int] = None
        for mv in free_slots(board):
            board[mv] = comp_symbol
            score, _ = minimax_algo(board, player_symbol, alpha, beta)
            board[mv] = " "
            if score > best_val:
                best_val = score
                best_idx = mv
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break
        return best_val, best_idx
    else:
        worst_val = math.inf
        best_idx: Optional[int] = None
        for mv in free_slots(board):
            board[mv] = player_symbol
            score, _ = minimax_algo(board, comp_symbol, alpha, beta)
            board[mv] = " "
            if score < worst_val:
                worst_val = score
                best_idx = mv
            beta = min(beta, worst_val)
            if beta <= alpha:
                break
        return worst_val, best_idx


def comp_turn(board: List[str], level: str = "hard") -> int:
    """Computer chooses a move (index 0-8)"""
    moves = free_slots(board)
    if not moves:
        raise RuntimeError("No moves available")

    if level == "easy":
        return random.choice(moves)

    if level == "medium":
        # evaluate each move and choose among top-scoring moves randomly
        scored_moves: List[Tuple[int, int]] = []
        for mv in moves:
            board[mv] = comp_symbol
            score, _ = minimax_algo(board, player_symbol)
            board[mv] = " "
            scored_moves.append((score, mv))
        top_score = max(scored_moves, key=lambda x: x[0])[0]
        top_choices = [mv for sc, mv in scored_moves if sc == top_score]
        return random.choice(top_choices)

    # hard (minimax)
    _, best = minimax_algo(board, comp_symbol)
    if best is None:
        # fallback (shouldn't normally happen)
        return random.choice(moves)
    return best


def player_input(board: List[str]) -> int:
    """Get valid input from player (1-9) and return index 0-8"""
    options = free_slots(board)
    while True:
        try:
            raw = input("Pick a cell (1-9): ").strip()
            val = int(raw) - 1
            if val in options:
                return val
            print("Cell taken or invalid, try again.")
        except ValueError:
            print("Enter a number from 1 to 9.")
        except KeyboardInterrupt:
            print("\nInput cancelled. Exiting.")
            raise


def choose_side() -> str:
    """Ask player to pick X or O"""
    while True:
        s = input("Do you want X or O? (X starts): ").strip().upper()
        if s in ("X", "O"):
            return s
        print("Please choose X or O.")


def choose_level() -> str:
    """Select difficulty"""
    while True:
        d = input("Difficulty (easy/medium/hard) [hard]: ").strip().lower()
        if d == "":
            return "hard"
        if d in ("easy", "medium", "hard"):
            return d
        print("Enter easy, medium or hard.")


def play() -> None:
    """Main game loop"""
    global player_symbol, comp_symbol
    print("Welcome to Tic Tac Toe AI!")
    player_symbol = choose_side()
    comp_symbol = "O" if player_symbol == "X" else "X"
    difficulty = choose_level()

    board = create_board()
    current = "X"  # X always starts
    display_positions()
    display(board)

    while True:
        if current == player_symbol:
            print("Your move:")
            mv = player_input(board)
            place_move(board, mv, player_symbol)
        else:
            print("Computer thinking...")
            mv = comp_turn(board, difficulty)
            place_move(board, mv, comp_symbol)
            print(f"Computer placed at {mv + 1}")

        display(board)
        result = check_winner(board)
        if result:
            if result == "Tie":
                print("It's a tie!")
            elif result == player_symbol:
                print("You win!")
            else:
                print("Computer wins!")
            break

        # toggle turn
        current = comp_symbol if current == player_symbol else player_symbol


if __name__ == "__main__":
    try:
        play()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
