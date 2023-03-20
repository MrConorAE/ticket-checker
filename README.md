# Ticket Checker

This is a Python script to check a set of tickets at an entry point
against a provided list of tickets.

It includes a script to automatically generate double tickets from a single entry.

## Getting Started

Create a file called tickets.csv. (There's one included as an example.)

### Formatting Data

On each line, format the data as follows:
```
First name|Last name|Used|Invalid|Type
```
- Used should be 0
- Invalid should be 0, or set it to 1 to disallow entry with this ticket
- Type should be "S" for a single ticket or "D" to automatically generate a pair

Excel can help with this, but make sure to change the delimiter to a pipe (`|`) before
exporting or the script can't read it.

Then, run `double.py` to generate the tickets (including IDs). They'll be saved in the
SQLite database `tickets.db`.

**WARNING**: The ID numbers generated by double.py are *random*. Each time you
generate the ticket database, the old IDs are deleted and new ones created.
If you do this after printing and issuing tickets, all the IDs on the printed tickets
will become invalid and won't scan on entry. **Do not run double.py after printing tickets -
the database should not be modified after that point or you risk invalidating the ID set and
making everyone's tickets invalid.** It's worth making a copy of `tickets.db` to keep as a
backup in case the database does get overwritten.

### Making Tickets

You can see the list of tickets using SQL on the database. You can also import it into
a word processor (such as Microsoft Word or LibreOffice Writer) to use for a Mail Merge
to generate tickets for each entry automatically.

When making tickets to print, add the ID as a barcode on the ticket. This is what'll be
scanned on entry. It's also a good idea to add the name to the ticket, and the record
number in small text somewhere in a corner to help you check that they all printed and to
make them easier to sort (check the documentation for the word processor to find out how
to add the record number).

## At the Door

Finally, at the door, start running `ticket_checker.py`. Note that you'll need a color-
compatible terminal for this to work - the default Windows one isn't, so use Windows Terminal
from the Microsoft Store.

To start checking tickets, type `1` and press Enter. (The options are displayed on-screen.) To
go back to that main menu while checking tickets, don't type (or scan) anything and press Enter at the
"`Ready`" prompt.

### Checking Tickets

As people enter, point the barcode scanner at the barcode on the ticket. The scanner will type
in the ID and press Enter for you. Wait for it to look up the ticket data in the database,
and make sure it says "`TICKET OK`" in green before admitting.

Once a ticket has been scanned once, it will be marked "used" in the database to prevent re-entry
or sharing tickets. This also means that if the ticket is accidentally scanned twice, it will
show as used.

If the checker reports "`TICKET USED`", check you haven't scanned it twice (if you heard two beeps from
the scanner, it probably scanned twice). If not, then that ticket has been used already and you should
confirm they are allowed entry.

If the checker reports "`TICKET INVALID`", it means the `invalid` field was `1` in the database (it was
marked invalid).

If the checker reports "`TICKET NOT FOUND`", there's no ticket with that ID that exists.

### Generating Reports and Running Queries

During the program, you can also use options 2 and 3.

Choose option 2 to run an SQL query on the database. Be careful - there's no safety checks here
so you could easily destroy the database.

Choose option 3 to print a list of unused tickets (i.e. ones that have not been scanned). This is
handy for checking who didn't show up.

## License

Licensed under the GPLv2.

You may:
- modify this code
- distribute your modified versions
- use this code commercially or privately

You must:
- include this copyright and license notice with all modifications or derivatives
- summarise your changes in the notice
- give credit to the original
- distribute any copies or derivatives under the same license, with the same conditions

### Copyright Notice

Copyright (C) 2023 Conor Eager

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
