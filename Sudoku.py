import random

from cell import Cell
from enum import Enum
from typing import List

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
