import sqlite3 as sql
# Import csv for importing
import csv
import random
db = sql.connect('tickets.db')
# Initialise the cursor.
cur = db.cursor()

cur.execute(
    "CREATE TABLE tickets (id TEXT PRIMARY KEY UNIQUE NOT NULL, first TEXT NOT NULL, last TEXT NOT NULL, used INTEGER NOT NULL, invalid INTEGER NOT NULL, type CHAR NOT NULL);")

with open('tickets.csv', 'r') as fin:
    # csv.DictReader uses first line in file for column headings by default
    tickets = csv.DictReader(fin, delimiter="|")  # comma is default delimiter
    for ticket in tickets:
        # generate a 5-digit random number for the ID
        id = ''.join(random.choice(
            ['1', '2', '3', '4', '5', '6', '7', '8', '9']) for i in range(5))
        # insert the ticket into the database
        data = (id, ticket['first'], ticket['last'], ticket['used'],
                ticket['invalid'], ticket['type'])
        print(
            f"Ticket ({ticket['type']}) {id} for {ticket['first']} {ticket['last']}")
        cur.execute(
            "INSERT INTO tickets (id, first, last, used, invalid, type) VALUES (?, ?, ?, ?, ?, ?);", data)
        db.commit()

        if (ticket['type'] == "d"):
            # generate a 5-digit random number for the ID
            id = ''.join(random.choice(
                ['1', '2', '3', '4', '5', '6', '7', '8', '9']) for i in range(5))
            # insert the ticket into the database
            ticket['last'] += "'s +1"

            data = (id, ticket['first'], ticket['last'], ticket['used'],
                    ticket['invalid'], ticket['type'])

            print('Generating second ticket for double')
            print(
                f"Ticket ({ticket['type']}) {id} for {ticket['first']} {ticket['last']}")
            cur.execute(
                "INSERT INTO tickets (id, first, last, used, invalid, type) VALUES (?, ?, ?, ?, ?, ?);", data)
            db.commit()
