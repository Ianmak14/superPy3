import sys
import random
from datetime import timedelta, datetime
from components.console import console
from utils.getDateFromFile import getDateFromFile
from utils.utils import appendRowToBoughtCsv, appendRowToInventoryCsv

sys.path.insert(0, "../csv")
sys.path.insert(0, "../utils")


def handleBuy(parserInfo):
    # Generate a random ID for the new product
    newId = random.randint(10000000, 99999999)

    # Extract information from the argument parser
    name = parserInfo.name.lower()
    price = parserInfo.price
    amount = parserInfo.amount
    inputExpiration = parserInfo.expiration

    # Get the current day from file to set the expiration date
    day = getDateFromFile("datetime")
    euDay = day.strftime("%d-%m-%Y")
    expiration = (day + timedelta(days=inputExpiration)).strftime("%d-%m-%Y")

    try:
        # Write new product to the inventory
        # Append line to bought.csv
        appendRowToBoughtCsv(newId, name, euDay, price, amount, expiration)

        # Append line to inventory.csv
        appendRowToInventoryCsv(newId, name, amount)

        console.print("[blue bold]OK")
    except Exception as e:
        # Handle exceptions
        console.print(f"[red bold]Error: {e}")
