#Author:
#Date:
#Student ID:

# Task A:

def is_leap_year(year):
    """
    Determines if a given year is a leap year.
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def validate_day(month, year):
    """
    Validates the day input based on the month and year 
    """
    while True:
        day = input("Please enter the day of the survey in the format DD:: ")
        print("\n")
        if day.isdigit():
            day = int(day)
            
            # Check months with 31 days
            if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
                if day in range(1, 32):
                    return day
                else:
                    print("Out of range - day must be between 1 and 31 for the selected month.")

            # Check months with 30 days
            elif month == 4 or month == 6 or month == 9 or month == 11:
                if day in range(1, 31):
                    return day
                else:
                    print("Out of range - day must be between 1 and 30 for the selected month.")

            # Check February
            elif month == 2:
                if is_leap_year(year):
                    if day in range(1, 30):
                        return day
                    else:
                        print("Out of range - February in a leap year can only have 1–29 days.")
                else:
                    if day in range(1, 29):
                        return day
                    else:
                        print("Out of range - February can only have 1–28 days in a non-leap year.")

            else:
                print("Invalid month.")
        else:
            print("Digit Error: Day input must be a digit.")

def validate_month():
    """
    Validates the month input.
    """
    while True:
        month = input("Please enter the month of the survey in the format MM : ")
        if month.isdigit():
            month = int(month)
            if month in range(1, 13):
                return month
            else:
                print("Out of range - month must be between 1 and 12.")
        else:
            print("Digit Error: Month input must be a digit.")

def validate_year():
    """
    Validates the year input.
    """
    while True:
        year = input("Please enter the year of the survey in the format YYYY: ")
        if year.isdigit():
            year = int(year)
            if year in range(2000, 2025):
                return year
            else:
                print("Out of range - year must be between 2000 and 2024.")
        else:
            print("Digit Error: Year input must be a digit.")

def validate_date_input():
    """
    Combines day, month, and year validation to return the  file name.
    """
    year = validate_year()  # Validate the year
    month = validate_month()  # Validate the month
    day = validate_day(month, year)  # Validate the day with leap year and month checks

    return "traffic_data" + "{:02d}".format(day) + "{:02d}".format(month) + str(year) + ".csv"

def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    while True:
        response = input("\nWould you like to load another dataset? (Y/N): ").strip().upper()
        print("\n"*6)
        if response in {"Y", "N"}:
            return response
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")
            print("\n"*6)
            
# Task B:

def process_csv_data(file_path):
    """
    Processes a CSV file to analyze vehicle data.
    """
    try:
        with open(file_path, "r") as file:
            data = file.readlines()
    except FileNotFoundError:
        print("File not found. Please check the file path or date.")
        return None

    if len(data) < 2:
        print("The CSV file seems to be empty or invalid.")
        return None

    # Initializing counters and variables
    total_vehicles = 0
    trucks_total = 0
    electric_vehicles_total = 0
    two_wheeled_total = 0
    buses_head_north = 0  
    not_turned = 0  
    over_speed_limit = 0
    elm_rabbit_vehicles = 0
    hanley_westway_vehicles = 0
    scooters_elm_rabbit = 0
    bicycles = 0
    rainfall_hour = set()  
    peak_hour_counts = {}

    for line in data[1:]:
        fields = line.strip().split(",")
        if len(fields) < 10:
            continue

        # Extract fields from csv file
        junction = fields[0].strip()
        time_day = fields[2].strip()
        travel_in = fields[3].strip()
        travel_out = fields[4].strip()
        weather = fields[5].strip().lower()  
        speed_limit = int(fields[6].strip())
        vehicle_speed = int(fields[7].strip())
        vehicle_type = fields[8].strip().lower()
        electric = fields[9].strip().upper() == "TRUE"

        total_vehicles += 1

        # Classify vehicle type and add the total

        #Total number of Trucks
        if "truck" in vehicle_type:
            trucks_total += 1

        #Total number of Electric vehicles 
        if "electric" in vehicle_type or electric:
            electric_vehicles_total += 1

        #Total number of Bicycles 
        if "bicycle" in vehicle_type:
            bicycles += 1
            two_wheeled_total += 1

        #Total number of Two-wheeled vehicles
        if "motorcycle" in vehicle_type or "scooter" in vehicle_type:
            two_wheeled_total += 1

        # Elm Avenue/Rabbit Road specific calculations
        if junction == "Elm Avenue/Rabbit Road":
            elm_rabbit_vehicles += 1

            #Total number of Scooters 
            if "scooter" in vehicle_type:
                scooters_elm_rabbit += 1

            # Total number of  buses heading North
            if vehicle_type == "buss" and travel_out == "N":
                buses_head_north += 1

        # Hanley Highway/Westway specific calculations
        if junction == "Hanley Highway/Westway":
            hanley_westway_vehicles += 1
            hanley_time_components = time_day.split(":")
            hanley_hour_string = hanley_time_components[0]

            current_count = peak_hour_counts.get(hanley_hour_string, 0)
            new_count = current_count + 1
            peak_hour_counts[hanley_hour_string] = new_count 

        # Check if vehicle passed straight without turning
        if travel_in == travel_out:
            not_turned += 1  

        # Count vehicles over speed limit
        if vehicle_speed > speed_limit:
            over_speed_limit += 1

        # Track hours with rain
        if "rain" in weather:  # Matches "Heavy rain" or "Light rain"
            rain_time_components = time_day.split(":")
            rain_hour_string = rain_time_components[0]
            rainfall_hour.add(rain_hour_string)

    # Peak hour analysis for Hanley Highway/Westway
    if peak_hour_counts:
        peak_hour_count = max(peak_hour_counts.values())
    else:
        peak_hour_count = 0

    peak_hours = []
    for hour, count in peak_hour_counts.items():
        if count == peak_hour_count:
            hour_str = hour if len(hour) == 2 else '0' + hour
            next_hour = str(int(hour) + 1)
            next_hour_str = next_hour if len(next_hour) == 2 else '0' + next_hour
            formatted_hour = "Between " + hour_str + ":00 and " + next_hour_str + ":00"
            peak_hours.append(formatted_hour)

            
    peak_hours_string = ""
    for index in range(len(peak_hours)):
        if index > 0:
            peak_hours_string += ", " 
        peak_hours_string += peak_hours[index]
        
    
    # Calculate truck percentage
    if total_vehicles > 0:
        truck_percentage = (trucks_total / total_vehicles) * 100
    else:
        truck_percentage = 0

        
    # Calculate scooter percentage for Elm Avenue
    if elm_rabbit_vehicles > 0:
        scooter_percentage_elm = (scooters_elm_rabbit / elm_rabbit_vehicles) * 100
    else:
        scooter_percentage_elm = 0

    # Calculate average bicycles per hour
    avg_bicycles_per_hour = bicycles / 24
    avg_bicycles_per_hour = round(avg_bicycles_per_hour)

    return generate_results(file_path, total_vehicles, trucks_total, electric_vehicles_total, two_wheeled_total,
                            buses_head_north, not_turned, truck_percentage, avg_bicycles_per_hour, over_speed_limit,
                            elm_rabbit_vehicles, hanley_westway_vehicles, scooter_percentage_elm, peak_hour_count,
                            peak_hours, rainfall_hour)

def generate_results(file_path, total_vehicles, trucks_total, electric_vehicles_total, two_wheeled_total,
                     buses_head_north, not_turned, truck_percentage, avg_bicycles_per_hour, over_speed_limit,
                     elm_rabbit_vehicles, hanley_westway_vehicles, scooter_percentage_elm, peak_hour_count,
                     peak_hours, rainfall_hour):
    """
    Generates a dictionary containing the analysis results.
    """
    return {
        "Data file selected": file_path,
        "The total number of vehicles recorded for this date": total_vehicles,
        "The total number of trucks recorded for this date is": trucks_total,
        "The total number of electric vehicles for this date": electric_vehicles_total,
        "The total number of two-wheeled vehicles for this date": two_wheeled_total,
        "The total number of Buses leaving Elm Avenue/Rabbit Road heading North is": buses_head_north,
        "The total number of Vehicles through both junctions not turning left or right": not_turned,
        "The percentage of total vehicles recorded that are trucks for this date": f"{round(truck_percentage)}%",
        "The average number of Bicycles per hour for this date": avg_bicycles_per_hour,
        "The total number of Vehicles recorded as over the speed limit for this date": over_speed_limit,
        "The total number of vehicles recorded through Elm Avenue/Rabbit Road junction": elm_rabbit_vehicles,
        "The total number of vehicles recorded through Hanley Highway/Westway junction": hanley_westway_vehicles,
        "The percentage of total vehicles recorded through Elm Avenue/Rabbit Road that are scooters ": f"{int(scooter_percentage_elm)}%",
        "The highest number of vehicles in an hour on Hanley Highway/Westway": peak_hour_count,
        "The most vehicles through Hanley Highway/Westway were recorded": ", ".join(peak_hours),
        "The number of hours of rain for this date": len(rainfall_hour),
    }


#Task C

def save_results_to_file(results):
    """
    Save the outcomes list to a text file. This will append each run's data.
    """
    output_file = "results.txt"
    try:
        #  Open file in "write" mode to save all outcomes
        with open(output_file, "a") as file:  
            for outcome in results:  
                for key, value in outcome.items():
                    result_string = key + ": " + str(value)
                    file.write(result_string + "\n")
                file.write("\n")  

        print("Results saved in 'results.txt'.")

    except Exception as e:
        print("Error saving results: ", e)



#Task D


# Required imports
import graphics
from graphics import *
import os

class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data
        self.date = date
        self.hourly_data_elm = [0] * 24
        self.hourly_data_hanley = [0] * 24
        
        # Constants for window dimensions
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 500
        self.MARGIN = 60
        self.BAR_WIDTH = 15
        
        # Colors for histogram
        self.ELM_COLOR = "#98FB98"  # Lighter green to match Image 1
        self.HANLEY_COLOR = "#FFB6C1"  # Light pink

    def parse_traffic_data(self):
        """
        Reads and processes the traffic data to get hourly counts for each junction.
        """
        try:
            with open(self.traffic_data, 'r') as file:
                next(file)  # Skip the header
                for line in file:
                    fields = line.strip().split(',')
                    if len(fields) >= 3:
                        junction = fields[0].strip()
                        time = fields[2].strip()
                        hour = int(time.split(':')[0])

                        if junction == "Elm Avenue/Rabbit Road":
                            self.hourly_data_elm[hour] += 1
                        elif junction == "Hanley Highway/Westway":
                            self.hourly_data_hanley[hour] += 1
            return True
        except Exception as e:
            print(f"Error processing data: {e}")
            return False

    def display_histogram(self):
        """
        Displays the histogram using graphics.py.
        """
        if not self.parse_traffic_data():
            print("Failed to load traffic data.")
            return

        # Set up the graphics window
        win = GraphWin("Traffic Flow Histogram", self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        win.setCoords(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        win.setBackground("white")

        # Draw title
        title = Text(Point(self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT - 20), 
                     f"Histogram of Vehicle Frequency per Hour ({self.date})")
        title.setSize(14)
        title.setStyle("bold")
        title.draw(win)

        # Draw legend
        self.draw_legend(win)

        # Draw bars first (moved before axes)
        self.draw_bars(win)

        # Draw axes second
        self.draw_axes(win)

        try:
            win.getMouse()
        except graphics.GraphicsError:
            print("Window was closed")
        win.close()

    def draw_legend(self, win):
        """
        Draws the legend with small colored squares next to junction names.
        """
        # Constants for legend layout
        square_size = 15
        text_offset = 25
        legend_y = self.WINDOW_HEIGHT - 40
        
        # Draw Elm Avenue legend
        elm_x = 200
        # Draw small green square
        elm_square = Rectangle(Point(elm_x, legend_y - square_size/2),
                             Point(elm_x + square_size, legend_y + square_size/2))
        elm_square.setFill(self.ELM_COLOR)
        elm_square.setOutline("black")
        elm_square.draw(win)
        
        # Draw junction name
        elm_text = Text(Point(elm_x + text_offset + 100, legend_y), 
                       "Elm Avenue/Rabbit Road")
        elm_text.setSize(10)
        elm_text.draw(win)

        # Draw Hanley Highway legend
        hanley_x = elm_x + 300
        # Draw small pink square
        hanley_square = Rectangle(Point(hanley_x, legend_y - square_size/2),
                                Point(hanley_x + square_size, legend_y + square_size/2))
        hanley_square.setFill(self.HANLEY_COLOR)
        hanley_square.setOutline("black")
        hanley_square.draw(win)
        
        # Draw junction name
        hanley_text = Text(Point(hanley_x + text_offset + 100, legend_y),
                          "Hanley Highway/Westway")
        hanley_text.setSize(10)
        hanley_text.draw(win)

    def draw_axes(self, win):
        """
        Draws the axes and labels using graphics.py with 24-hour format.
        """
        # Draw only x-axis line (removed y-axis)
        x_axis = Line(Point(self.MARGIN, self.MARGIN), 
                     Point(self.WINDOW_WIDTH - self.MARGIN, self.MARGIN))
        x_axis.draw(win)

        # X-axis label
        x_label = Text(Point(self.WINDOW_WIDTH / 2, self.MARGIN - 30), 
                      "Hours 00:00 to 24:00")
        x_label.setSize(10)
        x_label.draw(win)

        # X-axis hour labels (in 24-hour format)
        for i in range(24):
            x = self.MARGIN + (i * ((self.WINDOW_WIDTH - 2 * self.MARGIN) / 23))
            # Format hour as two digits with :00
            hour_label = f"{i:02d}"
            label = Text(Point(x, self.MARGIN - 15), hour_label)
            label.setSize(10)
            label.draw(win)

    def draw_bars(self, win):
        """
        Draws the bars for the histogram using graphics.py.
        """
        max_value = max(max(self.hourly_data_elm), max(self.hourly_data_hanley))
        scale = (self.WINDOW_HEIGHT - 2 * self.MARGIN - 80) / max_value
        bar_spacing = (self.WINDOW_WIDTH - 2 * self.MARGIN) / 23

        for hour in range(24):
            x_base = self.MARGIN + (hour * bar_spacing)

            # Draw Elm Avenue bar (green)
            elm_height = self.hourly_data_elm[hour] * scale
            if elm_height > 0:
                elm_bar = Rectangle(Point(x_base, self.MARGIN), 
                                  Point(x_base + self.BAR_WIDTH, self.MARGIN + elm_height))
                elm_bar.setFill(self.ELM_COLOR)
                elm_bar.setOutline(self.ELM_COLOR)  # Set outline same as fill color
                elm_bar.draw(win)

                # Draw count above bar
                if self.hourly_data_elm[hour] > 0:
                    elm_count = Text(Point(x_base + self.BAR_WIDTH/2, 
                                         self.MARGIN + elm_height + 10),
                                   str(self.hourly_data_elm[hour]))
                    elm_count.setSize(10)
                    elm_count.setTextColor("green")
                    elm_count.draw(win)

            # Draw Hanley Highway bar (pink)
            hanley_height = self.hourly_data_hanley[hour] * scale
            if hanley_height > 0:
                hanley_bar = Rectangle(Point(x_base + self.BAR_WIDTH, self.MARGIN),
                                     Point(x_base + 2 * self.BAR_WIDTH, 
                                          self.MARGIN + hanley_height))
                hanley_bar.setFill(self.HANLEY_COLOR)
                hanley_bar.setOutline(self.HANLEY_COLOR)  # Set outline same as fill color
                hanley_bar.draw(win)

                # Draw count above bar
                if self.hourly_data_hanley[hour] > 0:
                    hanley_count = Text(Point(x_base + 1.5 * self.BAR_WIDTH,
                                            self.MARGIN + hanley_height + 10),
                                      str(self.hourly_data_hanley[hour]))
                    hanley_count.setSize(10)
                    hanley_count.setTextColor("red")
                    hanley_count.draw(win)



#Task E

                    
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.results = []
        print("Welcome to the Traffic Flow Analysis System")
        print("Your comprehensive solution for traffic data management\n")

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        while True:
            # Get validated date and construct filename
            file_name = validate_date_input()

            # Process the CSV file
            results = process_csv_data(file_name)

            if results:
                # Print results to console
                print("\nAnalysis Results:")
                for key, value in results.items():
                    print(f"{key}: {value}")

                # Store results for saving later
                self.results.append(results)

                # Display the histogram once after processing the file
                histogram = HistogramApp(file_name, file_name.split('.')[0][-8:])
                histogram.display_histogram()

                # Ask if user wants to continue after the histogram is displayed
                continue_response = validate_continue_input()

                if continue_response == 'N':
                    # Save all results before exiting
                    if self.results:
                        save_results_to_file(self.results)
                    print("Thank you for using the Traffic Flow Analysis System.")
                    break

            # Clear screen and previous data for next iteration
            self.clear_previous_data()


    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        # Clear the console with newlines
        print("\n" * 6)


# Directly calling the main function
processor = MultiCSVProcessor()
processor.process_files()

