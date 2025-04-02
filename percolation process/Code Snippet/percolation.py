import random
import sub.function
import sys
from prettytable import PrettyTable
import datetime

while True:
    grid_size = input("\n\nEnter Size (eg:3x3): ")
    print(grid_size)

    if not grid_size.strip():
        rows, columns = 5, 5  # default size
    else:
        rows, columns = map(int, grid_size.split("x"))

    try:
        if not (3 <= rows <= 9 and 3 <= columns <= 9):
            raise ValueError("ERROR")

        grid = sub.function.create_grid(rows, columns)  # Corrected function import

        # Create pretty table
        table = PrettyTable()

        # Add columns to pretty table with alignment
        for i in range(columns):
            table.add_column(f"Column {i + 1}", [grid[j][i] for j in range(rows)], align="c")

        # Print the table
        print(table)

        # Create a list to store the status of each column (Ok or No)
        column_status = []
        for i in range(columns):
            column_width = max(len(str(row[i])) for row in grid)
            if any(row[i] == ' ' for row in grid):
                column_status.append("No")
                print(" " * column_width + "    No  ", end=" ")
            else:
                column_status.append("Ok")
                print(" " * column_width + "    Ok  ", end=" ")

        # Add the column status row to the table
        table.add_row(column_status)

        # Generating File Name
        current_date = datetime.datetime.now().strftime("%Y_%m_%d")
        rand_num = random.randint(1000, 9999)
        filename = f"{current_date}_{rand_num}.txt"

        # Save table to file
        with open(filename, "w") as file:
            file.write(str(table))
            print("\n\nTable saved as file")

        # Save table to html
        table.border = True
        htmlfile = f"{current_date}_{rand_num}.html"
        with open(htmlfile, "w") as file:
            file.write(table.get_html_string())
            print("Table saved as html")

        while True:
            Run = str(input("\n\nTo continue press 'C' and to end the program press 'E': "))
            if Run.lower() == 'c':
                break  # Breaks out of the inner loop and continues to the outer loop
            elif Run.lower() == 'e':
                sys.exit()  # Exits system
            else:
                print("Invalid Input... Try again !!!")
                continue

    except ValueError:
        print("Error Occurred...")

 
