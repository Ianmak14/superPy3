# Imports
import csv
import json
from datetime import datetime, timedelta
from rich.table import Table

from utils.getDateFromFile import getDateFromFile


def append_bought(inputId, name, day, price, amount, expiration):
    """Function to append a new row to bought.csv"""
    with open("./csv/bought.csv", "a", newline="") as inv:
        headers = ['id', 'name', 'buy_date', 'price', 'amount', 'expiration']
        writer = csv.DictWriter(inv, fieldnames=headers)
        writer.writeheader
        writer.writerow({'id': inputId, 'name': name, 'buy_date': day,
                        'price': price, 'amount': amount, 'expiration': expiration})


def append_inventory(inputId, name, amount):
    """Function to append a new row to inventory.csv"""
    with open("./csv/inventory.csv", "a", newline="") as inv:
        headers = ['id', 'name', 'amount']
        writer = csv.DictWriter(inv, fieldnames=headers)
        writer.writeheader
        writer.writerow({'id': inputId, 'name': name, 'amount': amount})


def adjust_inventory(inputId, amount):
    """Function to adjust the amount in inventory.csv for a specific item"""
    newLines = []
    with open("./csv/inventory.csv", "r+") as inv:
        lines = csv.DictReader(inv)
        for line in lines:
            if int(line["id"]) == inputId:
                newLines.append(
                    {
                        "id": line["id"],
                        "name": line["name"],
                        "amount": int(line["amount"]) - amount,
                    }
                )
            else:
                newLines.append(line)

    resetInventory()
    for line in newLines:
        append_inventory(line["id"], line["name"], line["amount"])


def remove_line(inputId):
    """Function to remove a line from inventory.csv"""
    newLines = []
    with open("./csv/inventory.csv", "r+") as inv:
        lines = csv.DictReader(inv)
        for line in lines:
            if int(line["id"]) != inputId:
                newLines.append(line)

    resetInventory()
    for line in newLines:
        append_inventory(line["id"], line["name"], line["amount"])


def append_sold(inputId, name, amount, date, price):
    """Function to append a new row to sold.csv"""
    with open("./csv/sold.csv", "a", newline="") as s:
        headers = ['id', 'name', 'amount', 'sell_date', 'sell_price']
        writer = csv.writer(s, fieldnames=headers)
        writer.writeheader
        writer.writerow({'id': inputId, 'name': name, 'amount': amount,
                        'sell_date': date, 'sell_price': price})


def resetInventory():
    """Function to reset inventory.csv"""
    with open("./csv/inventory.csv", "w") as inv:
        writer = csv.writer(inv, lineterminator="")
        writer.writerow(["id", "name", "amount"])


def resetBought():
    """Function to reset bought.csv"""
    with open("./csv/bought.csv", "w") as inv:
        writer = csv.writer(inv, lineterminator="")
        writer.writerow(["id", "name", "buy_date",
                        "price", "amount", "expiration"])


def resetSold():
    """Function to reset sold.csv"""
    with open("./csv/sold.csv", "w") as inv:
        writer = csv.writer(inv, lineterminator="")
        writer.writerow(["id", "name", "amount", "sell_date", "sell_price"])


def resetDay():
    """Function to reset day.txt"""
    with open(
        "./day/day.txt",
        "w",
    ) as day:
        writer = csv.writer(day, lineterminator="")
        writer.writerow(["01-01-2020"])


def resetAll():
    """Function to reset all CSV files"""
    resetBought()
    resetInventory()
    resetSold()
    resetDay()


def get_items_inventory(name) -> list:
    """Function to get all items with a specific name from inventory.csv"""
    inStock = []
    with open("./csv/inventory.csv") as inv:
        lines = csv.DictReader(inv)
        for line in lines:
            if line["name"] == name:
                inStock.append(
                    {
                        "id": int(line["id"]),
                        "name": line["name"],
                        "amount": int(line["amount"]),
                    }
                )
    return inStock


def item_bought_id(inputId):
    """Function to get an item from bought.csv by its ID"""
    with open("./csv/bought.csv") as inv:
        lines = csv.DictReader(inv)
        for line in lines:
            if int(line["id"]) == int(inputId):
                return line


def item_sold_date(inputDate):
    """Function to get all items from sold.csv by a specific date"""
    sold = []
    with open("./csv/sold.csv") as s:
        lines = csv.DictReader(s)
        for line in lines:
            if inputDate in line["sell_date"]:
                sold.append(line)
                continue
    return sold


def item_sold_array(inputDate):
    """Function to get all items from sold.csv by an array of dates"""
    sold = []
    with open("./csv/sold.csv") as s:
        lines = csv.DictReader(s)
        for line in lines:
            if line["sell_date"] in inputDate:
                sold.append(line)
                continue
    return sold


def checkForItemsExpired():
    """Function to check for items that have expired"""
    newLines = []
    day = getDateFromFile("date")
    with open("./csv/inventory.csv") as inv:
        lines = csv.DictReader(inv)
        for line in lines:
            item = item_bought_id(int(line["id"]))
            expirationDate = datetime.strptime(
                item["expiration"], "%d-%m-%Y").date()
            if day > expirationDate:
                # product expired (sell at price 0)
                adjust_inventory(int(line["id"]))
                append_sold(
                    line["id"],
                    line["name"],
                    line["amount"],
                    expirationDate.strftime("%d-%m-%Y"),
                    0,
                )
            else:
                newLines.append(line)

    resetInventory()
    """Update inventory"""
    for line in newLines:
        append_inventory(line["id"], line["name"], line["amount"])


def profit_sold(soldList):
    """Function to calculate the profit from a list of sold items"""
    totalSold = 0
    totalBought = 0

    for item in soldList:
        totalSold += float(item["amount"]) * float(item["sell_price"])
        buyPrice = item_bought_id(item["id"])["price"]
        totalBought += round(float(item["amount"]) * float(buyPrice), 2)

    totalProfit = totalSold - totalBought
    return totalProfit


def revenue_sold(soldList):
    """Function to calculate the revenue from a list of sold items"""
    totalSold = 0

    for item in soldList:
        totalSold += float(item["amount"]) * float(item["sell_price"])

    return totalSold


def check_date(inputDate):
    """Function to check the validity of an input date"""
    if len(inputDate) == 2:
        if int(inputDate) in range(0, 52):
            return {"status": True, "type": "week"}

    if len(inputDate) == 4:
        if int(inputDate) in range(2020, 2050):
            return {"status": True, "type": "year"}

    if len(inputDate) == 7:
        correctDate = None
        arrayDate = inputDate.split("-")

        try:
            newDate = (arrayDate[1], arrayDate[0])
            correctDate = True
        except ValueError:
            correctDate = False

        return {"status": correctDate, "type": "month"}

    if len(inputDate) == 10:
        correctDate = None
        arrayDate = inputDate.split("-")

        try:
            newDate = (arrayDate[2], arrayDate[1], arrayDate[0])
            correctDate = True
        except ValueError:
            correctDate = False

        return {"status": correctDate, "type": "date"}


def return_date(week):
    """Function to return a list of dates for a given week number"""
    day = getDateFromFile("str").split("-")
    startdate = datetime.strptime(f"1-{week}-{day[2]}", "%w-%W-%Y")
    dates = [startdate.strftime("%d-%m-%Y")]
    for i in range(1, 7):
        day = startdate + timedelta(days=i)
        dates.append(day.strftime("%d-%m-%Y"))
    return dates


def load_demo_data():
    """
    Function to load demo data into the program
    """
    # Set the date
    with open("./day/day.txt", "w") as day:
        day.write("22-01-2020")

    f = open("./demo/demodata.json")
    data = json.load(f)
    # Fill Bought.csv
    for item in data["bought"]:
        append_bought(
            item["id"],
            item["name"],
            item["buy_date"],
            item["price"],
            item["amount"],
            item["expiration"],
        )
    # Fill Sold.csv
    for item in data["sold"]:
        append_sold(
            item["id"],
            item["name"],
            item["amount"],
            item["sell_date"],
            item["sell_price"],
        )
    # Fill Inventory.csv
    for item in data["inventory"]:
        append_inventory(item["id"], item["name"], item["amount"])


def returnTableOfItems(data, type):
    """Function to create a rich Table of items for display"""
    table = Table(min_width=100)

    table.add_column("Product Name", style="magenta", no_wrap=True)
    table.add_column("Amount", justify="center", style="blue", no_wrap=True)
    if type != "revenue":
        table.add_column("Buy Price", justify="right",
                         style="green", no_wrap=True)
    table.add_column("Sell Price", justify="right",
                     style="green", no_wrap=True)
    table.add_column(
        "Date of Purchase/Expired", justify="center", style="yellow", no_wrap=True
    )
    for item in data:
        boughtItem = item_bought_id(int(item["id"]))
        if type != "revenue":
            table.add_row(
                item["name"],
                item["amount"],
                "\u20ac " + boughtItem["price"],
                "\u20ac " + item["sell_price"],
                item["sell_date"],
            )
        else:
            table.add_row(
                item["name"],
                item["amount"],
                "\u20ac " + item["sell_price"],
                item["sell_date"],
            )

    return table
