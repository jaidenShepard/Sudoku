# Sudoku
Core game logic for the game Sudoku. Initializing the game creates a list of 81 Cells that
are linked to each other by their column, group, and row. The game automatically generates a
solved grid that is guaranteed to be valid. The grid can then be retrieved with a difficulty level, which return a list of intergers representing the unsolved game board. 0 represents an
empty cell.
 - Easy shows 10 cells
 - Medium shows 7 cells
 - Hard shows 5 cells

The user's solution should be saves as a list of integers, and can be pass to the `validate_solution` method to see if the user got it correct.


Requires Python 3.5 +



## Usage
 ```python
# initilize game
sudoku = Sudoku()
sudoku.initialize_game()

# get's unsolved game grid
# Sudo class has Difficuly enum(EASY, MEDIUM, HARD)
grid = sudoku.get_grid(difficulty = Sudoku.Difficulty.EASY)

# present grid to user, play game, save user solution as flat list of integers
user_solution = [# user solution]

did_user_win = sudoku.validate_solution(user_solution)
```