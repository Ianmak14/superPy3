# Import necessary modules
from datetime import datetime
from components.console import console, err_console

# Function to set a custom date


def set_date(new_date):
    try:
        # Parse the input date string
        parsed_date = datetime.strptime(new_date, "%Y-%m-%d")

        # Format the parsed date for writing to the file
        formatted_date = parsed_date.strftime("%d-%m-%Y")

        # Write the new date to the file
        with open("./day/day.txt", "w") as file:
            file.write(formatted_date)

        # Print a success message
        console.print(f"[green]Current day set to: {formatted_date}")
        console.print("[blue bold]OK")

    except Exception as e:
        # Print an error message if there is a failure
        err_console.print("Failure!")
        err_console.print(f"Error: {e}")
