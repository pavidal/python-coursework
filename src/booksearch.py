import database
from datetime import datetime

def title(bookTitle):
    """
    Searches for books with this title.

    Inputs:
        bookTitle (String) : Title of book
    
    Returns:
        filteredList ([[String]]) : 2D list of matching books
    """
    library = database.read(database.__DB__)
    filteredList = [books for books in library if bookTitle in books]
    return filteredList

def author(auth):
    """
    Searches for books written by this author.

    Inputs:
        auth (String) : Author of book
    
    Returns:
        filteredList ([[String]]) : 2D list of matching books
    """
    library = database.read(database.__DB__)
    filteredList = [books for books in library if auth in books]
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
        filteredList = [books for books in library if inDateRange(books[3], fromDate, toDate)]
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
    dateObj = datetime.strptime(date, "%d/%m/%Y")
    fromObj = datetime.strptime(minDate, "%d/%m/%Y")
    toObj = datetime.strptime(maxDate, "%d/%m/%Y")

    if dateObj >= fromObj and dateObj <= toObj:
        return True
    else:
        return False