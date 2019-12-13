import database as db
import booksearch as bs


def returnBook(bookID):
    """
    Marks a book with matching ID as available and logs the transaction

    Inputs:
        bookID (String) : Book ID number

    Returns:
        file   (String) : Formatted database to be written

    Raises:
        IndexError : "No such book with ID"
        Exception  : "Book is already available"
    """

    # Searches for a book that matches ID
    record = bs.bookID(bookID)

    # Database file to be modified, as 2D list.
    library = db.read(db.__DB__)

    # Checks if a book with given ID exists
    if record:
        # Since the 2D list only has one element,
        # the first element is extracted for ease of use
        record = record[0]

        # Checks if each book in library is borrowed
        # Available books always have memberID = "0"
        if record[4] != "0":
            for book in library:
                if book[0] == bookID:
                    book[4] = "0"

                    # Updates database and log transaction
                    file = db.formatStr(library)
                    db.write(db.__DB__, file)
                    db.log("0", bookID)

                    return file
        else:
            raise Exception("Book is already available")
    else:
        raise IndexError("No such book with ID")


if __name__ == "__main__":
    import argparse

    # Using argparse for testing purposes.
    # This takes arguments from terminal and parses it.
    p = argparse.ArgumentParser()

    # Adding arguments for each function above.
    # Usage: bookreturn.py [-h] [-r <BOOKID>]
    p.add_argument("-r", "--returnbook", help="returns a book that was borrowed",
                   metavar="<BOOKID>")

    # Parses Namespace into usable objects (Strings and lists)
    args = p.parse_args()

    # Checks if arguments are empty to avoid printing empty lists.
    if args.returnbook != None:
        print(returnBook(args.returnbook))
