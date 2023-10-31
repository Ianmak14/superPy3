import sys
from components.console import console, err_console
from components.inputParser import create_parser
from components.buy import handleBuy
from components.sell import handleSell
from utils.advanceDate import advance
from components.revenue import handleRevenueRequest
from components.profit import handleProfitRequest
from components.inventory import displayCurrentInventory
from utils.setDate import set_date


def main():
    # Create the argument parser
    parser = create_parser()

    # Parse the command-line arguments
    parsed_args = parser.parse_args()

    # Execute the corresponding function based on the parsed arguments
    if parsed_args.buy:
        handleBuy(parsed_args)
    elif parsed_args.sell:
        handleSell(parsed_args)
    elif parsed_args.advance:
        advance(parsed_args.d)
    elif parsed_args.report:
        if parsed_args.inventory:
            displayCurrentInventory()
        elif parsed_args.revenue:
            handleRevenueRequest(parsed_args.date)
        elif parsed_args.profit:
            handleProfitRequest(parsed_args.date)
    elif parsed_args.set_date:
        set_date(parsed_args.set_date)
    else:
        # Print help message if no valid subcommand is provided
        parser.print_help()


if __name__ == "__main__":
    main()
