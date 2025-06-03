import random

def ConstBoard(board):
  print("\nCurrent State of the board:\n")
  for i in range(3):
      row = []
      for j in range(3):
          cell = board[i * 3 + j]
          if cell == 0:
              row.append(" ")   
          elif cell == -1:
              row.append("X")
          elif cell == 1:
              row.append("O")
      print(" " + " | ".join(row))  
      if i < 2:
          print("---+---+---")  # Print horizontal separator between rows
  print()



def User1Turn(board):
    while True:
        try:
            pos = int(input("Enter X's position [1-9]: "))
            if 1 <= pos <= 9 and board[pos - 1] == 0:
                board[pos - 1] = -1
                break
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Please enter a number.")


def User2Turn(board):
    while True:
        try:
            pos = int(input("Enter O's position [1-9]: "))
            if 1 <= pos <= 9 and board[pos - 1] == 0:
                board[pos - 1] = 1
                break
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Please enter a number.")


def CompTurn(board, difficulty):

    def random_move():
        available_positions = [i for i in range(9) if board[i] == 0]
        if available_positions:
            board[random.choice(available_positions)] = 1

    if difficulty == "easy":
        random_move()
    elif difficulty == "medium":
        if random.random() < 0.5:
            random_move()
        else:
            best_move_minimax(board)
    else:  
        best_move_minimax(board)


def best_move_minimax(board):
    best_score = -float('inf')
    best_move = -1
    for i in range(9):
        if board[i] == 0:
            board[i] = 1  
            score = minimax(board, 0, False)
            board[i] = 0
            if score > best_score:
                best_score = score
                best_move = i
    board[best_move] = 1


def minimax(board, depth, is_maximizing):
    winner = analyzeboard(board)
    if winner != 0:
        return winner
    if 0 not in board:
        return 0  

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == 0:
                board[i] = 1
                score = minimax(board, depth + 1, False)
                board[i] = 0
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == 0:
                board[i] = -1
                score = minimax(board, depth + 1, True)
                board[i] = 0
                best_score = min(score, best_score)
        return best_score

def analyzeboard(board):
    win_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                        [0, 3, 6], [1, 4, 7], [2, 5, 8],
                        [0, 4, 8], [2, 4, 6]]
    for combo in win_combinations:
        a, b, c = combo
        if board[a] != 0 and board[a] == board[b] == board[c]:
            return board[a]
    return 0


def show_scores(player_x_wins_sp, player_o_wins_sp, draws_sp,
                player_x_wins_mp, player_o_wins_mp, draws_mp):
    print("\nDo you want to check scores?")
    choice = input("Enter 'y' to check or any other key to continue: ").lower()
    if choice == 'y':
        print("1. Single Player Scores")
        print("2. Multiplayer Scores")
        opt = input("Choose option (1 or 2): ")
        if opt == '1':
            print("\n--- Single Player Scores ---")
            print(f"Player X (You): {player_x_wins_sp}")
            print(f"Computer O: {player_o_wins_sp}")
            print(f"Draws: {draws_sp}")
        elif opt == '2':
            print("\n--- Multiplayer Scores ---")
            print(f"Player X: {player_x_wins_mp}")
            print(f"Player O: {player_o_wins_mp}")
            print(f"Draws: {draws_mp}")
        else:
            print("Invalid option. Skipping scores.")
    print("\n")


def show_instructions():
    print("\n HOW TO PLAY TIC-TAC-TOE")
    print("-" * 40)
    print(" Objective: Get 3 of your marks (X or O) in a row—")
    print("   horizontally, vertically, or diagonally.")
    print("\n Controls:")
    print("   - Each cell in the 3x3 board is numbered 1 to 9.")
    print("   - To place your move, enter the number of the cell.\n")
    print("   Cell positions:")
    print("     1 | 2 | 3")
    print("     ---------")
    print("     4 | 5 | 6")
    print("     ---------")
    print("     7 | 8 | 9\n")
    print("   - Single Player:")
    print("     - You are 'X'. The computer is 'O'.")
    print("     - You can choose difficulty (easy, medium, hard).\n")
    print("   - Multiplayer:")
    print("     - Player 1 is 'X'. Player 2 is 'O'.")
    print("     - Take turns to enter your moves.\n")
    print("   - Win Conditions:")
    print("     - First player to align three marks wins.")
    print("     - If the board is full without a winner, it is a draw.")
    print("-" * 40)


def main():
    # Initialize score counters
    player_x_wins_sp = 0
    player_o_wins_sp = 0
    draws_sp = 0

    player_x_wins_mp = 0
    player_o_wins_mp = 0
    draws_mp = 0

    while True:
        board = [0] * 9
        print("\n MAIN MENU")
        print("1. Single Player")
        print("2. Multiplayer")
        print("3. Check Scores")
        print("4. View Instructions")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '0':
            print("\nThanks for playing!")
            break

        elif choice == '1':
            print("\nSingle Player Mode: You (X) versus Computer (O)")
            try:
                player = int(input("Enter 1 to play first, 2 to play second: "))
            except ValueError:
                print("Invalid input. Defaulting to first player.")
                player = 1

            difficulty = input("Choose difficulty (easy, medium, hard): ").lower()
            if difficulty not in ['easy', 'medium', 'hard']:
                print("Invalid difficulty. Defaulting to hard.")
                difficulty = "hard"

            for i in range(9):
                if analyzeboard(board) != 0:
                    break
                if (i + player) % 2 == 0:
                    CompTurn(board, difficulty)
                else:
                    ConstBoard(board)
                    User1Turn(board)

            ConstBoard(board)
            result = analyzeboard(board)
            if result == 0:
                print("It is a draw!")
                draws_sp += 1
            elif result == -1:
                print("You Win!")
                player_x_wins_sp += 1
            elif result == 1:
                print("Computer Wins!")
                player_o_wins_sp += 1

        elif choice == '2':
            print("\nMultiplayer Mode: Player X versus Player O")
            for i in range(9):
                if analyzeboard(board) != 0:
                    break
                ConstBoard(board)
                if i % 2 == 0:
                    User1Turn(board)
                else:
                    User2Turn(board)

            ConstBoard(board)
            result = analyzeboard(board)
            if result == 0:
                print("It is a draw!")
                draws_mp += 1
            elif result == -1:
                print("Player X Wins!")
                player_x_wins_mp += 1
            elif result == 1:
                print("Player O Wins!")
                player_o_wins_mp += 1

        elif choice == '3':
            show_scores(player_x_wins_sp, player_o_wins_sp, draws_sp,
                        player_x_wins_mp, player_o_wins_mp, draws_mp)

        elif choice == '4':
            show_instructions()

        else:
            print("Invalid option. Please enter 0, 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
