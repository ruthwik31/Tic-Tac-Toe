import numpy as np
import random

def empty_board():
    return np.zeros((3, 3), dtype=int)

def empty_places(board):
    return [(i, j) for i in range(len(board)) for j in range(len(board)) if board[i, j] == 0]

def player_place(board, p):
    while True:
        try:
            print(f"Player {p}, it's your turn!")
            #print(f"Current board:\n{board}")
            row, col = map(int, input("Enter row and column (e.g., '1 2'): ").split())
            if (row, col) in empty_places(board):
                board[row, col] = p
                return board
            else:
                print("It is already occupied. Try again.")
        except ValueError:
            print("Invalid input!")

def computer_place(board, player):
    _, move = minimax(board, player, True)
    if move:
        board[move] = player
    return board

def row_winner(board, player):
    for row in board:
        if np.all(row == player):
            return True
    return False

def col_winner(board, player):
    for col in board.T: #matrix transpose
        if np.all(col == player):
            return True
    return False

def diag_winner(board, player):
    if np.all(np.diag(board) == player) or np.all(np.diag(np.fliplr(board)) == player):
        return True
    return False

def evaluate_winner(board):
    for player in [1, 2]:
        if row_winner(board, player) or col_winner(board, player) or diag_winner(board, player):
            return player
    if np.all(board != 0):
        return -1  # Draw
    return 0  # No winner yet

def minimax(board, player, is_maximizing):
    opponent = 1 if player == 2 else 2
    winner = evaluate_winner(board)
    if winner == player:
        return 1, None
    elif winner == opponent:
        return -1, None
    elif winner == -1:  # Draw
        return 0, None

    best_move = None
    if is_maximizing:
        best_score = -float('inf')
        for move in empty_places(board):
            board[move] = player
            score, _ = minimax(board, player, False)
            board[move] = 0
            if score > best_score:
                best_score = score
                best_move = move
    else:
        best_score = float('inf')
        for move in empty_places(board):
            board[move] = opponent
            score, _ = minimax(board, player, True)
            board[move] = 0
            if score < best_score:
                best_score = score
                best_move = move

    return best_score, best_move

def tic_toc_toe():
    print("1: You vs Friend")
    print("2: You vs Computer")
    mode = input("Enter your choice (1 or 2): ")
    board = empty_board()
    winner = 0
    move_count = 1

    if mode == "1":
        print("You have selected 2-player mode.")
        while winner == 0:
            for player in [1, 2]:
                board = player_place(board, player)
                print(f"Board after move {move_count} by Player {player}:\n{board}\n")
                move_count += 1
                winner = evaluate_winner(board)
                if winner != 0:
                    break
    elif mode == "2":
        print("You have selected (You vs Computer).")
        while winner == 0:
            for player in [1, 2]:
                if player == 1:
                    board = player_place(board, player)
                else:
                    board = computer_place(board, player)
                print(f"Board after move {move_count} by {'Player' if player == 1 else 'Computer'}:\n{board}\n")
                move_count += 1
                winner = evaluate_winner(board)
                if winner != 0:
                    break
    else:
        print("Invalid choice. Exiting game.")
        return

    if winner == -1:
        print("The game is a draw!")
    else:
        print(f"Player {winner} wins!")

print("Welcome to Tic Tac Toe!")
tic_toc_toe()
