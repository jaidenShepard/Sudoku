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