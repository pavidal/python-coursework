import database as db
import booksearch as bs


def checkout(memberID, bookID):
    """
    Marks a book with matching ID as borrowed by memberID

    Inputs:
        memberID (Int) : ID of a library member
        bookID   (Int) : ID of a book to borrow

    Returns:
        (String) : Database file to be written
    
    Raises:
        IndexError : "No such book with ID"
        Exception  : "Book is borrowed"
                     "IDs out of range"
    """

    library = db.read(db.__DB__)

    if not bs.bookID(bookID):
        raise IndexError("No such book with ID")
    else:
        if int(memberID) < 10000 and int(bookID) < 10000:
            for book in library:
                if book[0] == bookID:
                    if book[4] == "0":
                        book[4] = memberID
                        break
                    else:
                        raise Exception("Book is borrowed")
            return db.formatStr(library)
        else:
            raise Exception("IDs out of range")


if __name__ == "__main__":
    import argparse

    # Using argparse for testing purposes.
    # This takes arguments from terminal and parses it.
    p = argparse.ArgumentParser()

    # Adding arguments for each function above.
    # Usage:
    p.add_argument("-c", "--checkout", help="checkout a book to a member",
                   nargs=2, metavar=("<MEMBER>", "<BOOKID>"))

    # Parses Namespace into usable objects (Strings and lists)
    args = p.parse_args()

    # Checks if arguments are empty to avoid printing empty lists.
    if args.checkout != None:
        print(checkout(args.checkout[0], args.checkout[1]))
