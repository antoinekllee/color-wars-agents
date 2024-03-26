from termcolor import colored
from copy import deepcopy
from time import sleep, time

def initialize_grid():
    return [['  ' for _ in range(5)] for _ in range(5)]

def display_grid(grid):
    print('    0    1    2    3    4')
    print('  ' + '-' * 26)
    for i, row in enumerate(grid):
        colored_row = []
        for cell in row:
            if cell.startswith('b'):
                colored_row.append(colored(cell, 'blue'))
            elif cell.startswith('r'):
                colored_row.append(colored(cell, 'red'))
            else:
                colored_row.append(cell)
        print(f'{i} | ' + ' | '.join(colored_row) + ' |')
        print('  ' + '-' * 26)

def validate_input(prompt, valid_range):
    while True:
        try:
            value = int(input(prompt))
            if value in valid_range:
                return value
            else:
                print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def place_piece(grid, player, row, col):
    grid[row][col] = player + '3'

def pop_piece(grid, player, row, col):
    if grid[row][col] == player + '3': 
        grid[row][col] = '  '
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + dx, col + dy
            if 0 <= new_row < 5 and 0 <= new_col < 5:
                if grid[new_row][new_col] == '  ': 
                    grid[new_row][new_col] = player + '1'
                elif grid[new_row][new_col][0] == player: 
                    value = int(grid[new_row][new_col][1]) + 1
                    if value == 4:
                        pop_piece(grid, player, new_row, new_col)
                    else:
                        grid[new_row][new_col] = player + str(value)
                else: 
                    grid[new_row][new_col] = player + grid[new_row][new_col][1]
                    value = int(grid[new_row][new_col][1]) + 1
                    if value == 4:
                        pop_piece(grid, player, new_row, new_col)
                    else:
                        grid[new_row][new_col] = player + str(value)
    else: 
        value = int(grid[row][col][1]) + 1
        if value == 4:
            pop_piece(grid, player, row, col)
        else:
            grid[row][col] = player + str(value)

def has_pieces(grid, player):
    for row in grid:
        for cell in row:
            if cell[0] == player:
                return True
    return False

def check_all_moves(grid, player):
    moves = []

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col][0] == player:
                moves.append((row, col))
    
    return moves

def evaluate_board(grid, player):
    # returns a score that is negatively proportional to the number of opponent dots
    # and proportional to the number of player dots
    opp = 'r' if player=='b' else 'b'
    p_score = 0
    opp_score = 0
    for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j][0] == opp:
                    opp_score += int(grid[i][j][-1])
                elif grid[i][j][0] == player:
                    p_score += int(grid[i][j][-1])
    return p_score - 3*opp_score

def minimax(grid, depth, is_maximizing, player):
    best_move = None

    if depth == 0 or not has_pieces(grid, 'r') or not has_pieces(grid, 'b'):
        # Base case: return the heuristic value of the board
        return evaluate_board(grid, player), None
    
    if is_maximizing:
        max_eval = float('-inf')
        for move in check_all_moves(grid, player):
            # Create a copy of the grid to simulate the move
            new_grid = deepcopy(grid)
            pop_piece(new_grid, player, move[0], move[1])
            eval, _ = minimax(new_grid, depth - 1, False, player)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    
    else:
        min_eval = float('inf')
        opponent = 'r' if player == 'b' else 'b'
        for move in check_all_moves(grid, opponent):
            # Create a copy of the grid to simulate the move
            new_grid = deepcopy(grid)
            pop_piece(new_grid, opponent, move[0], move[1])
            eval, _ = minimax(new_grid, depth - 1, True, player)
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move

def get_best_move(grid, player, depth=2):
    _, best_move = minimax(grid, depth, True, player)
    return best_move

def play_game():
    grid = initialize_grid()
    players = ['b', 'r']
    bots = []
    b_depth = 2
    r_depth = 2
    if 'Y' in input("Automote player B? (Y/N) ").upper():
        bots.append('b')
        b_depth = int(input("Player b depth:  "))
    if 'Y' in input("Automote player R? (Y/N) ").upper():
        bots.append('r')
        r_depth = int(input("Player r depth:  "))
    current_player = 0

    # First move
    for player in players:
        display_grid(grid)
        print(f"Player {player.upper()}'s turn.")
        row = validate_input("Enter the row (0-4): ", range(5))
        col = validate_input("Enter the column (0-4): ", range(5))
        while grid[row][col] != '  ':
            print("That position is already occupied. Please choose another position.")
            row = validate_input("Enter the row (0-4): ", range(5))
            col = validate_input("Enter the column (0-4): ", range(5))
        place_piece(grid, player, row, col)

    # Subsequent moves
    while True:
        player = players[current_player]
        display_grid(grid)
        print(f"Player {player.upper()}'s turn.")
        
        depth = b_depth if player=='b' else r_depth
        if player in bots:
            st = time()
            row, col = get_best_move(grid, player, depth)
            et = time()
            if et-st < 1: 
                sleep(1-(et-st))

        else:
            row = validate_input("Enter the row (0-4): ", range(5))
            col = validate_input("Enter the column (0-4): ", range(5))

            while grid[row][col][0] != player:
                print("You can only pop your own pieces. Please choose another position.")
                row = validate_input("Enter the row (0-4): ", range(5))
                col = validate_input("Enter the column (0-4): ", range(5))

        pop_piece(grid, player, row, col)

        if not has_pieces(grid, players[1 - current_player]):
            display_grid(grid)
            print(f"Player {player.upper()} wins!")
            break

        current_player = 1 - current_player


play_game()