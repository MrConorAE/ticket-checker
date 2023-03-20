# Ticket Checker for NPBHS Ball
# By Conor Eager
# © (copyright) Conor Eager, 2022. All rights reserved.

# IMPORTS
# Import sqlite3 for databases
import sqlite3 as sql
# Import csv for importing
import csv
from time import sleep

# COLOURS


class ColoursOn:
    r = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class f:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        darkgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class b:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        darkgrey = '\033[47m'


# INITIALISATION
# Initialise the connection to the database.
db = sql.connect('tickets.db')
# Initialise the cursor.
cur = db.cursor()
# Save colours.
c = ColoursOn()


def reset_database(db, cur, c):
    print(f"{c.f.cyan}1/5{c.r} Dropping existing table...")
    cur.execute("DROP TABLE IF EXISTS tickets;")

    print(f"{c.f.cyan}2/5{c.r} Creating new table...")
    cur.execute(
        "CREATE TABLE tickets (id TEXT PRIMARY KEY UNIQUE NOT NULL, first TEXT NOT NULL, last TEXT NOT NULL, used INTEGER NOT NULL, invalid INTEGER NOT NULL, type CHAR NOT NULL, notes TEXT);")

    print(f"{c.f.cyan}3/5{c.r} Reading tickets.csv...")
    with open('tickets.csv', 'r') as fin:
        # csv.DictReader uses first line in file for column headings by default
        # comma is default delimiter
        tickets = csv.DictReader(fin, delimiter="|")
        data = [(ticket['id'], ticket['first'], ticket['last'], ticket['used'],
                ticket['invalid'], ticket['type'], ticket['notes']) for ticket in tickets]
        print(f"{c.f.cyan}4/5{c.r} Importing {len(data)} tickets...")
        cur.executemany(
            "INSERT INTO tickets (id, first, last, used, invalid, type, notes) VALUES (?, ?, ?, ?, ?, ?, ?);", data)

    print(f"{c.f.cyan}5/5{c.r} Committing changes...")
    db.commit()

    print(f"{c.f.green}Done!{c.r}")


import_data = input("Import data from tickets.csv? (y/N) ")
if (import_data.lower().startswith("y")):
    reset_database(db, cur, c)
else:
    print("Not importing.")

# MAIN MENU
# Create the main menu.
while True:
    # Print the main menu.
    print(f"\n{c.bold}{c.f.cyan}{c.reverse}TICKET CHECKER{c.r}")

    print("""
Ticket Checker v1.1, Copyright (C) 2023 Conor Eager
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
For more information, see the included LICENSE file.
    """)

    print(f"Select an option:\n1. Start\n2. Run Query\n3. Print List of No-Shows\n0. Exit")
    menu_option = input(f"{c.bold}{c.f.cyan}Select: {c.r}")
    if (menu_option == "1"):
        while True:
            # Get the ticket number to check.
            print(f"\n{c.f.darkgrey}Processing, please wait a moment...{c.r}")
            sleep(1)
            barcode = input(
                f"\n\n\n\n\n{c.f.cyan}Ready. Scan a ticket barcode to check in.\n: {c.r}")
            if barcode == "":
                break
            else:
                # Search the database for the ticket and return it.
                print("\033c")
                result = cur.execute(
                    "SELECT * FROM tickets WHERE id = ?", (barcode,)).fetchone()
                if (result != None):
                    # Now show the ticket.
                    print(f"\n{c.bold}{c.f.green}* Ticket found{c.r}")

                    message = f"{c.f.cyan}ID:{c.r}\t{result[0]}\n{c.f.cyan}Name:{c.r}\t{result[1]} {result[2]}"

                    if result[6] != "":
                        message += f"\n{c.f.cyan}Note:{c.r}\t{result[6]}"
                    else:
                        message += f"\n{c.f.cyan}Note:{c.r}\t{c.f.darkgrey}None{c.r}"

                    if result[4] == 1:
                        message += f"\n{c.f.cyan}Status:{c.r}\t{c.f.red}{c.reverse}Invalidated{c.r}"
                        message += f"\n\n{c.f.red}{c.reverse} → TICKET INVALID - DO NOT ADMIT {c.r}"
                        print(message)

                        # input(
                        #     f"\n{c.f.cyan}Press ENTER to scan next ticket. {c.r}")

                    elif result[3] > 0:
                        message += f"\n{c.f.cyan}Status:{c.r}\t{c.f.yellow}{c.reverse}Used, {result[3]} times{c.r}"
                        message += f"\n\n{c.f.yellow}{c.reverse} → USED TICKET - CONFIRM DETAILS BEFORE ADMITTING {c.r}"
                        print(message)

                        # markunused = input(
                        #     f"\n{c.f.cyan}Press {c.f.green}ENTER to mark used again and continue{c.f.cyan}, or {c.f.red}type 'markunused' to mark unused.{c.f.cyan}\n: {c.r}")

                        # if (markunused.lower() == "markunused"):
                        #     confirm = input(
                        #         f"{c.f.red}Are you sure? About to reset ticket to UNUSED! Type 'confirm' to confirm. {c.f.cyan}\n: {c.r}")
                        #     if (confirm.lower() == "confirm"):
                        #         cur.execute(
                        #             "UPDATE tickets SET used = 0 WHERE id = ?", (barcode,))
                        #         db.commit()
                        #         print("Marked ticket as unused!")
                        #         continue
                        #     else:
                        #         print("Not marking ticket as unused.")
                        cur.execute(
                            "UPDATE tickets SET used = ? WHERE id = ?", (result[3]+1, barcode))
                        db.commit()
                        #         continue
                        # else:
                        #     print("Not marking ticket as unused.")
                        #     cur.execute(
                        #         "UPDATE tickets SET used = ? WHERE id = ?", (result[3]+1, barcode))
                        #     db.commit()
                        #     continue

                    else:
                        message += f"\n{c.f.cyan}Status:{c.r}\t{c.f.green}OK{c.r}"
                        message += f"\n\n{c.f.green}{c.reverse} → TICKET OK - CHECK DETAILS AND ADMIT {c.r}"
                        print(message)

                        # markused = input(
                        #     f"\n{c.f.cyan}Press {c.f.green}ENTER to mark used and continue{c.f.cyan}, or {c.f.red}type 'dontmarkused' to not mark used. {c.f.cyan}\n: {c.r}")
                        # if (markused.lower() == "dontmarkused"):
                        #     print("Not marking ticket as used!")
                        #     continue
                        # else:
                        cur.execute(
                            "UPDATE tickets SET used = ? WHERE id = ?", (result[3]+1, barcode))
                        db.commit()
                        # print("Marked ticket as used.")
                        # continue

                else:
                    print(f"\n{c.bold}{c.f.red}* Ticket not found{c.r}\n\n\n\n")
                    print(
                        f"\n{c.f.red}{c.reverse} → TICKET NOT FOUND - DO NOT ADMIT {c.r}")
                    # input(
                    #     f"\n{c.f.cyan}Press ENTER to continue.\n: {c.r}")
                    continue

    elif (menu_option == "2"):
        query = input(
            f"{c.f.cyan}Enter query: {c.r}")
        if query == "":
            break
        else:
            # Search the database for the ticket and return it.
            try:
                result = cur.execute(
                    query).fetchall()
                print(f"{c.f.green}Query OK{c.f.cyan}\nResults:{c.r}")
                print(result)
            except Exception as e:
                print(f"{c.f.red}Query error: {e}{c.f.cyan}\nResults:{c.r}")
                print(result)

    elif (menu_option == "3"):
        # Print list of non-attendees.
        data = cur.execute("SELECT * FROM tickets WHERE used = 0").fetchall()
        print(f"\n\n{c.f.cyan}{c.reverse}UNUSED TICKETS LIST{c.r}")

        for row in data:
            print(f"{row['id']}: {row['first']} {row['last']}")

        print("--- End of list ---")
        

    elif (menu_option == "R"):
        import_data = input(
            f"{c.f.red}Reset database and import data from tickets.csv? (y/N) {c.r}")
        if (import_data.lower().startswith("y")):
            reset_database(db, cur, c)
        else:
            print("Not importing.")

    elif (menu_option == "0"):
        print(f"{c.f.red}Exiting.{c.r}")
        exit()

    else:
        print(f"{c.bold}{c.f.red}Not an option. Please try again.{c.r}")
