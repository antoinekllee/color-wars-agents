import numpy as np
import torch

# This file defines the game environment, including initialization, resetting,
# executing actions (steps), and rendering the current game state.
class GameEnv:
    def __init__(self):
        self.grid = np.full((5, 5), '  ', dtype='<U2')  # Initialize 5x5 grid
        self.reset()  # Reset the game to start state

    def reset(self):
        # Reset the grid
        self.grid[:, :] = '  '
        # Place initial pieces for blue and red
        self.grid[1, 1] = 'b3'
        self.grid[3, 3] = 'r3'
        self.moves_made = 0  # Keep track of the number of moves made
        return self._get_state()

    def step(self, action):
        # Decode the action (assumed to be a linear index for simplicity)
        row, col = divmod(action, 5)
        player = 'b' if self.moves_made % 2 == 0 else 'r'  # Determine whose turn it is

        reward = 0
        done = False

        if self._validate_action(row, col, player):
            self._pop_piece(row, col, player)
            self.moves_made += 1
            reward = 1  # Simple reward for a valid move
        else:
            reward = -1  # Penalty for an invalid move

        if self._check_game_over():
            done = True
            reward = 10  # Large reward for winning the game

        return self._get_state(), reward, done, {}

    def render(self):
        for row in self.grid:
            print('|'.join(row))
        print()

    def _validate_action(self, row, col, player):
        # Validate if the action can be performed
        return self.grid[row, col].startswith(player)

    def _pop_piece(self, row, col, player):
        # Implement the logic to pop a piece and update the grid
        if self.grid[row, col] == player + '3':
            self.grid[row, col] = '  '
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_row, new_col = row + dx, col + dy
                if 0 <= new_row < 5 and 0 <= new_col < 5:
                    if self.grid[new_row, new_col] == '  ':
                        self.grid[new_row, new_col] = player + '1'
                    elif self.grid[new_row, new_col][0] == player:
                        value = int(self.grid[new_row, new_col][1]) + 1
                        if value == 4:
                            self._pop_piece(new_row, new_col, player)
                        else:
                            self.grid[new_row, new_col] = player + str(value)
                    else:
                        self.grid[new_row, new_col] = player + self.grid[new_row, new_col][1]
                        value = int(self.grid[new_row, new_col][1]) + 1
                        if value == 4:
                            self._pop_piece(new_row, new_col, player)
                        else:
                            self.grid[new_row, new_col] = player + str(value)
        else:
            value = int(self.grid[row, col][1]) + 1
            if value == 4:
                self._pop_piece(row, col, player)
            else:
                self.grid[row, col] = player + str(value)


    def _get_state(self):
        # Convert the grid to a tensor for the neural network
        state = np.zeros((5, 5, 2))  # Two channels: one for each player
        for r in range(5):
            for c in range(5):
                if self.grid[r, c].startswith('b'):
                    state[r, c, 0] = int(self.grid[r, c][1])
                elif self.grid[r, c].startswith('r'):
                    state[r, c, 1] = int(self.grid[r, c][1])
        return torch.tensor(state, dtype=torch.float32).unsqueeze(0)  # Add batch dimension

    def _check_game_over(self):
        # Check if the game is over
        return not np.any(self.grid == '  ')  # Simplified check
    