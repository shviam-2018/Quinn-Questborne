# Code Explanation

## Classes

### Button (Line 47)
- Represents a button in the game interface.
- Attributes:
  - `x`: The x-coordinate of the button.
  - `y`: The y-coordinate of the button.
  - `image`: The image of the button.
  - `rect`: The rectangle boundary of the button.
  - `clicked`: Flag indicating if the button is clicked.
- Methods:
  - `draw()`: Draws the button on the screen and returns `True` if clicked.

### Player (Line 70)
- Represents the player character in the game.
- Attributes:
  - `x`: The x-coordinate of the player.
  - `y`: The y-coordinate of the player.
- Methods:
  - `update()`: Updates player position and actions based on game state.
  - `reset()`: Resets player to initial state.

### World (Line 116)
- Represents the game world.
- Attributes:
  - `tile_list`: List of tiles in the game world.
- Methods:
  - `draw()`: Draws the tiles on the screen.

### Enemy (Line 151)
- Represents an enemy in the game.
- Attributes:
  - `x`: The x-coordinate of the enemy.
  - `y`: The y-coordinate of the enemy.
- Methods:
  - `update()`: Updates enemy position.

### Lava (Line 175)
- Represents lava in the game.
- Attributes:
  - `x`: The x-coordinate of the lava.
  - `y`: The y-coordinate of the lava.

## Major Components

### Load Level (Line 186)
- Function to load level data from file.

### Game Loop (Line 206)
- Main game loop controlling the game flow.

### Main Menu (Line 212)
- Displayed when `main_menu` is `True`.
- Allows the player to start the game or exit.

### Game Screen (Line 221)
- Displayed when `main_menu` is `False`.
- Renders the game world, player, enemies, and lava.

### Event Handling (Line 234)
- Handles pygame events such as quitting the game.

### Display Update (Line 244)
- Updates the display to reflect changes in the game world.

