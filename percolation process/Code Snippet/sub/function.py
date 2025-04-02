import random
from prettytable import PrettyTable
import datetime

#takes two parameters (rows and columns) 
def create_grid(rows, columns):
    grid = []
    for i in range(rows):
        row = []
        for j in range(columns):
            if random.random() < 0.20:  # Changed threshold to 20%
                row.append(" ")
            else:
                value = random.randint(10, 99)#integer between 10 and 99 (2digit integer)
                row.append(value)
        grid.append(row)
    return grid

#assigning the value to pretty table by calling it
def display_grid(grid):
    table = PrettyTable()
    for row in grid:
        table.add_row(row)
    print(table)#assigned into pretty table 
    

def display_grid(grid):
    for row in grid:#display the grid row by row
        for value in row:
            print(value, end=" ")
        print()
    for j in range(len(grid[0])):#Provide column information
        empty = any(row[j] == ' ' for row in grid)
        if empty:
            print("    No  ", end=" ")  # Adjusted spacing for "No"
        else:
            print("    Ok  ", end=" ")  # Adjusted spacing for "Ok"
    print()

