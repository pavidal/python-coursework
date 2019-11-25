import database


def search(term):
    """
    Searches for books matching this title or author.

    Inputs:
        term (String) : Title or author  of book

    Returns:
        filteredList ([[String]]) : 2D list of matching books
    """
    library = database.read(database.__DB__)

    # Filters library to books that either matches the ID or Title field
    filteredList = [books for books in library if
                    term.lower() in [books[1].lower(), books[2].lower()]]
    return filteredList


def bookID(idNum):
    """
    Looks up a book with matching ID.

    Inputs:
        idNum (String) : Book ID number

    Returns:
        filteredList ([[String]]) : 2D list of matching books
    """
    library = database.read(database.__DB__)
    # The [0] at the end is used to convert
    # a 2D list (with 1 element) into 1D list
    # idNum is left as String because there is no int comparison involved
    filteredList = [books for books in library if books[0] == str(idNum)]
    return filteredList


def borrowed(isBorrowed):
    """
    Filter books based on if it is borrowed.

    Inputs:
        isBorrowed (Boolean) : Borrowed state

    Returns:
        filteredList ([[String]]) : 2D list of matching books
    """
    library = database.read(database.__DB__)

    # Borrowed books will always have ID > 0;
    # status can be filtered with this
    if isBorrowed:
        filteredList = [books for books in library if books[4] != "0"]
    else:
        filteredList = [books for books in library if books[4] == "0"]
    return filteredList


def dateRange(fromDate, toDate):
    """
    Searches for books published between two dates (inclusive).

    Inputs:
        fromDate (String) : Lower date limit
        toDate   (String) : Upper date limit

    Returns:
        filteredList ([[String]]) : 2D list of matching books
    """
    library = database.read(database.__DB__)
    try:
        filteredList = [books for books in library if inDateRange(
            books[3], fromDate, toDate)]
        return filteredList
    except ValueError as e:
        print(e)
        return []


def inDateRange(date, minDate, maxDate):
    """
    Checks if a given date is between two other dates.

    Inputs:
        date    (String) : Date to check
        minDate (String) : Lower date limit
        maxDate (String) : Upper date limit

    Returns:
        (Boolean) : If date is between min and max
    """
    from datetime import datetime

    # Parses inputs into datetime objects for comparison
    dateObj = datetime.strptime(date, "%d/%m/%Y")
    fromObj = datetime.strptime(minDate, "%d/%m/%Y")
    toObj = datetime.strptime(maxDate, "%d/%m/%Y")

    if dateObj >= fromObj and dateObj <= toObj:
        return True
    else:
        return False


if __name__ == "__main__":
    import argparse

    # Using argparse for testing purposes.
    # This takes arguments from terminal and parses it.
    p = argparse.ArgumentParser()

    # Adding arguments for each function above.
    # Usage: booksearch.py [-h] [-s <TITLE|AUTHOR>] [-i <ID>]
    #                      [-b <BORROWED>] [-d <FROMDATE> <TODATE>]
    p.add_argument("-s", "--search", help="searches for all books matching this term",
                   metavar="<String>")
    p.add_argument("-i", "--idsearch", help="searches for a book matching this id",
                   metavar="<Int>", type=int)
    p.add_argument("-b", "--borrow", help="shows list of books that are (or not) borrowed",
                   metavar="<Bool>")
    p.add_argument("-d", "--date", help="searches for all books between two dates",
                   nargs=2, metavar=("<Date>", "<Date>"))

    # Parses Namespace into usable objects (Strings and lists)
    args = p.parse_args()

    # Checks if arguments are empty to avoid printing empty lists.
    if args.search != None:
        print(search(args.search))
    if args.idsearch != None:
        print(bookID(args.idsearch))
    if args.borrow != None:

        # This additional if is required as bool("False") == True
        if args.borrow.lower() in ["true", "t", "y"]:
            print(borrowed(True))
        elif args.borrow.lower() in ["false", "f", "n"]:
            print(borrowed(False))
        else:
            print("booksearch.py: error: argument -b/\
                --borrow: invalid bool value: '%s'" % args.borrow)
    if args.date != None:
        print(dateRange(args.date[0], args.date[1]))
