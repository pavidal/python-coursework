"""
This module performs IO operations for the other modules.
"""

__DB__ = "database.txt"
__LOG__ = "logfile.txt"
__SEP__ = "|"


def read(path):
    """
    Reads and returns a 2D list of records within a database file.

    Inputs:
        path (String) : path to a database file

    Returns:
        database ( [[String]] ) : List of records within the file.
    """

    try:
        file = open(str(path), "r")
        records = file.read().split("\n")
        database = [fields.split(__SEP__) for fields in records]

    except IOError as e:
        print("Cannot read from '%s'. Check if the file is within the root\
 directory or that this application has sufficient permissions\
 to access it." % path)
        print(e)

    finally:
        file.close()
        return database


def append(path, msg):

    """
    Adds a line of any String to the end of a file.

    Inputs:
        path (String) : path to a file
        msg  (String) : a message to append

    Returns:
        msg  (String) : appended line
    """

    try:
        file = open(str(path), "a")
        file.write(str(msg))
    except IOError as e:
        print("Cannot write to '%s'. Check if the file is within the root\
 directory or that this application has sufficient permissions\
 to access it." % path)
        print(e)
    finally:
        file.close()
        return msg


def write(path, msg):

    """
    Writes to a file, overwriting the previous contents.

    Inputs:
        path (String) : path to a file
        msg  (String) : a message to overwrite

    Returns:
        msg  (String) : appended line
    """

    try:
        file = open(path, "w")
        file.write(msg)

    except IOError as e:
        # TODO: Backups/error handling
        print("Cannot write to '%s'. Check if the file is within the root\
 directory or that this application has sufficient permissions\
 to access it." % path)
        print(e)

    finally:
        file.close()
        return msg


def log(memberID, bookID):
    """
    Logs checkout and appends to logfile

    Inputs:
        memberID (Int) : ID of a library member
        bookID   (Int) : ID of a book to borrow

    Returns:
        (String) : Log entry to append
    """

    import datetime as d
    import booksearch as bs

    # Reads logfile content
    log = read(__LOG__)

    # Gathering information for each field
    transID = str(len(log))
    date = d.date.today().strftime("%d/%m/%Y")
    status = "checkout" if int(memberID) > 0 else "return"
    bookName = bs.bookID(bookID)[0][1]

    # Building record/entry
    record = [transID, memberID, bookName, date, status]
    msg = __SEP__.join(record)

    append(__LOG__, msg + "\n")
    return msg


def formatStr(database):

    lines = [__SEP__.join(records) for records in database]
    file = "\n".join(lines)
    return file

if __name__ == "__main__":
    import argparse

    # Using argparse for testing purposes.
    # This takes arguments from terminal and parses it.
    p = argparse.ArgumentParser()

    # Adding arguments for each function above.
    # Usage: database.py [-h] [-l <MEMBER> <BOOKID>] [-r <PATH>] 
    #                   [-a <PATH> <STRING>] [-w <PATH> <STRING>]
    p.add_argument("-l", "--log", help="log checkout transaction",
                    nargs=2, metavar=("<MEMBER>", "<BOOKID>"))
    p.add_argument("-r", "--read", help="reads a database formatted text file",
                    metavar="<PATH>")
    p.add_argument("-a", "--append", help="appends a line to a file",
                    nargs=2, metavar=("<PATH>", "<STRING>"))
    p.add_argument("-w", "--write", help="Writes a string to a file",
                    nargs=2, metavar=("<PATH>", "<STRING>"))
    

    # Parses Namespace into usable objects (Strings and lists)
    args = p.parse_args()

    # Checks if arguments are empty to avoid printing empty lists.
    if args.log != None:
        print(log(args.log[0], args.log[1]))
    if args.read != None:
        for i in read(args.read):
            print(i)
    if args.append != None:
        optn = input("Are you sure you want to write to a file? [y/n]")
        if optn == "y":
            append(args.append[0], args.append[1])
    if args.write != None:
        optn = input("Are you sure you want to write to a file? [y/n]")
        if optn == "y":
            write(args.write[0], args.write[1])
