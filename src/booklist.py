"""
Filters the log file to calculate the popularity of a title.
"""


def monthly(dateRange):
    """
    Gets log entries in a date range from today.

    Inputs:
        dateRange (Int) : Number of days to today

    Returns:
        {String : Int}  : Dictionary of book titles and their tally. 
                          Sorted by count, descending. 
    """

    checkouts = filterMonth(dateRange)
    books = {}

    for entry in checkouts:
        try:
            # if the key already exists
            books[entry[2]] += 1
        except:
            # if the key doesn't exist, create it.
            books[entry[2]] = 1
    
    # sorting the dictionary.
    # sorted returns a tuple and needs to be converted.
    sortedBooks = {title: count for title, count in 
                    sorted(books.items(), key=lambda x:x[1], reverse=True)}

    return sortedBooks



def filterMonth(dateRange):
    """
    Filters the logs to checkouts at the specified date range to today.

    Inputs:
        dateRange (Int) : Number of days to today

    Returns:
        [[String]]      : List of transactions matching the filter
    """
    from datetime import date, timedelta
    from booksearch import inDateRange as dr
    import database as db

    # Calculating date range
    dt1 = date.today()
    dt2 = dt1 - timedelta(days=dateRange)
    lastMonth = dt2.strftime("%d/%m/%Y")
    today = dt1.strftime("%d/%m/%Y")

    # filtering logs
    log = db.read(db.__LOG__)
    checkouts = [entry for entry in log if 
                    entry[0] != "" and
                    entry[4] == "checkout" and 
                    dr(entry[3], lastMonth, today)]

    return checkouts



if __name__ == "__main__":
    import argparse

    # Using argparse for testing purposes.
    # This takes arguments from terminal and parses it.
    p = argparse.ArgumentParser()

    # Adding arguments for each function above.
    # Usage: booklist.py [-h] [-m <DAYS>] [-f <DAYS>]
    p.add_argument("-m", "--month", help="popularity for the past 30 days",
                    metavar="<DAYS>", type=int)
    p.add_argument("-f", "--filtermonth", help="popularity for the past 30 days",
                    metavar="<DAYS>", type=int)

    # Parses Namespace into usable objects (Strings and lists)
    args = p.parse_args()

    # Checks if arguments are empty to avoid printing empty lists.
    if args.month != None:
        m = monthly(args.month)
        for i in m:
            print(m[i], i)
    if args.filtermonth != None:
        for i in filterMonth(args.filtermonth):
            print(i)
