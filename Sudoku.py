import random
from enum import Enum
from typing import List, Optional, Union

class Cell:
    """
    A doubly linked cell for a sudoku board. Each cell contains references to every other
    Cell in its member row, column, and group.
    """

    class Membership(Enum):
        ROW = "row"
        COLUMN = "column"
        GROUP = "group"

    def __init__(self, value: Optional[int] = None):
        self.value: Union[int, None] = value
        self.column: List[Cell] = list()
        self.row: List[Cell] = list()
        self.group: List[Cell] = list()

    def __repr__(self):
        return f"Node(value: {self.value})"

    def add_memember_to(self, membership: Membership, member: Cell):
        """
        Mutually adds a member to a Cell's column, row, or group, and adds the current
        Cell to the member
        """
        if member not in getattr(self, str(membership)):
            getattr(self, str(membership)).append(member)
        if self not in getattr(member, str(membership)):
            getattr(member, str(membership)).append(self)

    def clear_value(self):
        self.value = None

    def set_possible_value(self):
        """
        Refers to all the member Cells linked to the current Cell, determines list of
        valid values, and randomly selects a one to set for the current Cell's value.
        """
        starting_set = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        for node in set(self.column + self.row + self.group):
            if node.value in starting_set:
                starting_set.remove(node.value)
        
        if len(starting_set) > 1:
            self.value = starting_set[random.randint(0, len(starting_set) - 1)]
        else:
            self.value = starting_set[0]
        

class Sudoku:
    """
    The Sudoku game. Initializes with no cells. Call method initialize_game to populate
    the instance with a valid, populated Sudoku grid.
    """

    class Difficulty(Enum):
        EASY = 'easy'
        MEDIUM = 'medium'
        HARD = 'hard'

    def __init__(self):
        self.cells: List[Cell] = list() 

    def create_raw_board(self) -> List[Cell]:
        """
        Generates a flat list of 81 cells with no values. Links all the cells with their
        column, group, and row memebers.
        """
        cells = [Cell() for _ in range(81)]

        offset = 0
        for i in range(0, 10):
            # set rows
            step = i * 9
            node_buff = cells[0 + step: 9 + step]
            for current_node in node_buff:
                for other_node in node_buff:
                    if current_node != other_node:
                        current_node.add_memember_to(Cell.Membership.ROW, other_node)

            # set columns
            node_buff = cells[0+ i: 73 + i: 9]
            for current_node in node_buff:
                for other_node in node_buff:
                    if current_node != other_node:
                        current_node.add_memember_to(Cell.Membership.COLUMN, other_node)

            # set groups
            if i % 3 == 0 and i > 0:
                offset += 6
            node_buff = (
                cells[3 * (i + offset): 3 * (i + offset) + 3] +
                cells[3 * (3 + i + offset): 3 * (3 + i + offset) + 3] + 
                cells[3 * (6 + i + offset): 3 * (6 + i + offset) + 3]
            )
            for current_node in node_buff:
                for other_node in node_buff:
                    if current_node != other_node:
                        current_node.add_memember_to(Cell.Membership.GROUP, other_node)
    
        return cells

    def set_values_for_cells(self, cells: List[Cell]):
        """
        Loops over the given list of cells, and sets the values for all of them using a 
        backtracking algorithm. The values are guaranteed to be valid.
        """
        backtrack = 2
        index = 0
        notch = 0

        while index < 81:
            try:
                cells[index].set_possible_value()
                if index > notch:
                    notch = index
                    backtrack = 2
                index += 1
            except IndexError:
                index -= backtrack
                for node in cells[index: notch+1]:
                    node.clear_value()
                backtrack += 1

    def initialize_game(self):
        """
        Initializes the Cells for the Sudoku instance.
        """
        cells = self.create_raw_board()
        self.set_values_for_cells(cells)
        self.cells = cells

    def get_grid(self, difficulty: Difficulty) -> List[int]:
        """
        Returns a flat list of integers representing the game. 0 is an empty cell
        """
        if difficulty == self.Difficulty.EASY:
            number_of_cells = 10
        elif difficulty == self.Difficulty.MEDIUM:
            number_of_cells = 7
        elif difficulty == self.Difficulty.HARD:
            number_of_cells = 5
        
        given_cells = random.choices(range(0, 81), k=number_of_cells)
        
        blah = []
        for i, cell in enumerate(self.cells):
            if i in given_cells:
                blah.append(cell.value or 0)
            else:
                blah.append(0)
        
        return blah

    def validate_solution(self, player_solution: List[int]) -> bool:
        """
        Takes a list of integers representing the user's solution of the game and
        compares to the values in the Sudoku instance.
        """
        return player_solution == [cell.value for cell in self.cells]

    def print_game(self, nodes):
        """
        prints the game grid to the console. For debugging purposes.
        """
        for i, x in enumerate(nodes):
            if i % 9 == 0:
                print("|")
                print('-------------------------------------')
            print(f'| {x.value} ', end = '')
        print("|")
        print('-------------------------------------')
