from termcolor import colored
from copy import deepcopy

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

def get_best_move(grid: list, player: str):
    moves = check_all_moves(grid, player)
    move_dict = dict()
    
    # print(moves)
    max = 0
    best_move = moves[0]
    for move in moves:
        r, c = move
        state = deepcopy(grid)
        pop_piece(state, player, r, c)
        score=0
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j][0] == player:
                    score += int(state[i][j][-1])
        
        if score > max: 
            best_move = move
            max = score

        move_dict[move] = score
    print(move_dict)
    return best_move

def play_game():
    grid = initialize_grid()
    players = ['b', 'r']
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
        print(f"Player {player.upper()}'s turn.")
        display_grid(grid)

        print(get_best_move(grid, player))
        # print(player)

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