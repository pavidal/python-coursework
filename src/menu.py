from tkinter import (Tk, messagebox, Frame, Label,
                     Button, Entry, OptionMenu, StringVar)
from tkinter.ttk import (Treeview, Scrollbar)

import matplotlib.figure as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from database import (read, __DB__)


def pathChecker():
    '''
    Check for and create required additional files.

    Returns:
        exists (Boolean) : Wether all files exists

    Creates:
        settings.json : Settings file
        database.txt  : Database of all books, empty.
        logfile.txt   : Log of all transactions, empty.
    '''

    import os.path
    import time

    # Looks for the required files
    #settingsPath = os.path.exists("settings.json")
    dbPath = os.path.exists("database.txt")
    logPath = os.path.exists("logfile.txt")

    # Dict to convert "True" and "False" into something more understandable.
    dict = {}
    dict[True] = "Exists"
    dict[False] = "Missing"

    # Prints file status
    #print("\nChecking for files:")
    #print("\t| Settings file: " + dict[settingsPath])
    #print("\t| Database file: " + dict[dbPath])
    #print("\t| Log file:      " + dict[logPath])

    # Checks if any of the previous files are missing
    if False in [dbPath, logPath]:
        while True:

            # Asks if user wants to create files
            createFiles = messagebox.askyesno("",
                                              "Required files are missing.\nCreate missing files?")

            # Creating files if user replies "y" (Yes)
            if createFiles:
                #print("Creating files...")

                # List of all files required to function and their existence
                fileList = [["database.txt", dbPath], ["logfile.txt", logPath]]

                # List of files that doesn't exist, filtered from fileList.
                files = [f for f in fileList if f[1] == False]

                # Create each missing file
                for f in files:
                    try:
                        file = open(f[0], "w+")
                        #print("Created", f[0])
                        file.close()

                    except IOError:
                        messagebox.showerror("Error", "Unable to write files.")
                        # TODO Error Handling

                messagebox.showinfo("Done!", "All files successfully created.")

                time.sleep(2)
                os.system("cls")    # Clears output of cmd and PowerShell
                return True

            # If the user wishes not to create files, terminate.
            else:
                dialogue = ("This application will not work properly without these files.\
                    \nIf you have backups, please copy into the working directory \
                    \nbefore continuing.")

                messagebox.showwarning("Warning", dialogue)
                time.sleep(5)
                return False

    else:
        time.sleep(2)
        os.system("cls")
        return True


def search():
    """
    Searches for book matching entered value and field.
    Populates values onto the table.
    """
    import booksearch as bs

    opt     = var.get()
    term    = searchBox.get()
    term2   = dateBox.get()

    # Case statement (substitute) for different search areas
    # Each key is an option in the OptionMenu
    searchBy = {
        "Title & Author"    : bs.search(term),
        "ID"                : bs.bookID(term),
        "Date"              : bs.dateRange(term, term2),
        "Status"            : bs.borrowed(bool(term))
    }
    query = searchBy[opt]   # Make & stores a query (2D list)

    # Repopulates table
    if term != "":
        populate(query)


def checkIfDate(event):
    """
    Checks if the search option is set to date.
    If so, it shows a second search box, otherwise it's hidden.
    """
    if var.get() == "Date":
        dateBox.grid()
    else:
        dateBox.grid_remove()


def populate(library):
    """
    Takes a 2D list and inserts each row into the table

    Inputs:
        library ([[String]])    : a 2D list to populate the table with.
    """
    # Clears table
    table.delete(*table.get_children())

    # Inserts each book into the table
    # where text is the key field
    for book in library:
        table.insert("", int(book[0]), text=book[0], values=(book[1], book[2], book[3], book[4]))


def checkinBook():
    """
    Checks in a book that has been selected on the table.
    """
    import bookreturn as br

    try:
        # Gets book info from table selection
        selection   = table.focus()
        book        = table.item(selection)
        bookID      = book["text"]
        booktitle   = book["values"][0]

        msg = "Are you sure you want to check in \
            \nID: %s\
            \nTITLE: %s" % (bookID, booktitle)

        # Verifies action before checking in
        confirmed = messagebox.askquestion("Confirm check-in", msg)

        if confirmed == "yes":
            br.returnBook(bookID)
            populate(read(__DB__))

    except IndexError:
        # Flashes check-in button if nothing is selected
        returnBtn.flash()
    except Exception as e:
        # Displays warnings raised by bookreturn
        messagebox.showwarning("Watch out!", e)


def checkoutBook():
    """
    Checks out a book that's selected on the table.
    """
    import bookcheckout as bc

    try:
        # Gets book info from table selection
        selection   = table.focus()
        book        = table.item(selection)
        bookID      = book["text"]
        booktitle   = book["values"][0]

        # Checks if the user actually selects something from the table
        if bookID != "":

            # Sorry you have to see this function inception
            # I can't figure out a nicer way to do this considering
            # that tkinter doesn't have input dialogs
            def checkout():
                try:
                    memberID = txtbox.get()
                    int(memberID)           # Tests if input is integer

                    msg = "Are you sure you want to checkout \
                        \nID: %s\
                        \nTITLE: %s\
                        \nTO MEMBERID: %s" % (bookID, booktitle, memberID)

                    # Verifies action before checking in
                    confirmed = messagebox.askquestion("Confirm checkout", msg)

                    if confirmed == "yes":
                        bc.checkout(memberID, bookID)
                        populate(read(__DB__))
                        messagebox.showinfo("Success!",
                            "Book successfully lent to ID: " + memberID)
                except ValueError:
                    messagebox.showwarning("Watch out!", "Input is not a number")
                    dialogue.focus_force()
                except Exception as e:
                    # Displays warnings raised by bookreturn
                    messagebox.showwarning("Watch out!", e)
                    dialogue.focus_force()
                finally:
                    dialogue.destroy()

            ### BUILDING INPUT DIALOGUE ###
            # Creating window
            dialogue = Tk()
            dialogue.title("Borrow a Book")
            dialogue.geometry("300x80")
            dialogue.resizable(False, False)

            # Delcaring components
            lbl         = Label(dialogue, text="Enter Member ID")
            txtbox      = Entry(dialogue)
            okBtn       = Button(dialogue, text="Okay",
                                    command=checkout)
            cancelBtn   = Button(dialogue, text="Cancel",
                                    command=lambda:dialogue.destroy())

            # Placing components
            lbl.pack(side="top", fill="x", padx=10)
            txtbox.pack(side="top", fill="x", padx=10)
            okBtn.pack(side="left", padx=50)
            cancelBtn.pack(side="right", padx=50)
            ### END OF DIALOGUE BUILDING ###

    except IndexError:
        # Flashes checkout button if nothing is selected
        checkoutBtn.flash()


def showGraph():
    """
    Creates a window that shows a popularity graph.
    """
    from booklist import monthly

    # Creating a window
    statsWin = Tk()
    statsWin.title("Book Popularity")
    statsWin.geometry("1024x768")
    statsWin.resizable(False, False)

    # Creating the graph
    graphFrame = Frame(statsWin)
    fig = plt.Figure(figsize=(10.24, 7.68), dpi=100, tight_layout=True)
    area = fig.add_subplot(111)

    statsWin.withdraw()     # Hides window until done

    # translating options into respective values (days)
    optn = timeVar.get()
    tRange = {
        "Last Month": 30,
        "Last 3 Months": 90,
        "Last 6 Months": 180,
        "Last Year": 365,
    }

    # gets all transactions from log that is within selected time frame
    bookList = monthly(tRange[optn])

    x = list(bookList.keys())
    y = list(bookList.values())

    if len(x) < 5 or len(y) < 5:
        messagebox.showwarning("Feature Unavailable.",
            "This feature is not available as the log file is not populated enough.")
        return

    # Embeds graph into Tk
    graph = FigureCanvasTkAgg(fig, graphFrame)

    # Plotting graph
    area.bar(x, y)
    area.set_xlabel("Book Titles")
    area.set_ylabel("Copies on loan")

    # rotates label 90 degrees for readability
    [label.set_rotation(90) for label in area.get_xticklabels()]

    graph.draw()
    graph.get_tk_widget().pack()
    graphFrame.pack()

    statsWin.deiconify()        # show window
    statsWin.mainloop()


###########################
#                         #
# Creating GUI Components #
#                         #
###########################

### CREATING MAIN WINDOW ###
win = Tk()
win.withdraw()  # Hides root window when using messageboxes in pathChecker()
win.title("Vivlio - Library System")
win.geometry("1024x768")
win.resizable(False, False)

# Checks for database.txt and logfile.txt
# If these aren't created or doesn't exist: quit.
if not pathChecker():
    quit()


### BUILDING FRAME (TOOLBAR) ###

# A frame is used to prevent
toolbar = Frame(win)

# General search entry box
searchBox = Entry(toolbar)
searchBox.grid(column=0, row=0, padx=5, pady=5)

# Second entry box for date range
dateBox = Entry(toolbar)
dateBox.grid(column=1, row=0, padx=5, pady=5)
dateBox.grid_remove()   # Hidden by default, only used when searching by dates.

searchBtn = Button(toolbar, text="Search", command=search)
searchBtn.grid(column=2, row=0, padx=5, pady=5)

# Search options drop list. Chooses which field to search.
# Every time the option is changed, checkIfDate() is called.
options = ["Title & Author", "ID", "Date", "Status"]
var = StringVar(toolbar)
searchOptn = OptionMenu(toolbar, var, *options, command=checkIfDate)
var.set(options[0])         # Sets default option
searchOptn.grid(column=3, row=0, padx=5, pady=5)

toolbar.grid(column=0, row=0)

resetBtn = Button(toolbar, text="Reset Table",
                    command=lambda:populate(read(__DB__)))
resetBtn.grid(column=4, row=0, padx=5, pady=5)

### END OF FRAME BUILDING ###


### BUILDING TREEVIEW (TABLE) ###

table = Treeview(win, height=32)
table["columns"] = ("1", "2", "3", "4")     # Adding indexes

# Defining all columns and their width.
# Not iterated as each has a different width.
table.column("#0", width=50, minwidth=50)
table.heading("#0", text="ID")

table.column("1", width=452, minwidth=30)
table.heading("1", text="Title")

table.column("2", width=270, minwidth=30)
table.heading("2", text="Author")

table.column("3", width=150, minwidth=30)
table.heading("3", text="Date")

table.column("4", width=80, minwidth=30)
table.heading("4", text="Member")

# Populates the table with the entire database
populate(read(__DB__))

table.grid(column=0, row=1, padx=1, pady=5, sticky="ns")

# Creating a vertical scrollbar for the table
scroll = Scrollbar(win, orient="vertical", command=table.yview)
scroll.grid(column=1, row=1, sticky="ns")   # Sticky is for resizing

# adds another option for communication with scrollbar
table.configure(yscrollcommand=scroll.set)

### END OF TREEVIEW BUILDING ###


### BUILDING FOOTER ###

checkoutBtn = Button(win, text="Checkout", command=checkoutBook)
checkoutBtn.grid(column=0, row=2, padx=5, pady=5, sticky="e")

returnBtn = Button(win, text="Check-in", command=checkinBook)
returnBtn.grid(column=0, row=2, padx=80, pady=5, sticky="e")    # too lazy to use a frame

popularBtn = Button(win, text="Monthly Charts", command=showGraph)
popularBtn.grid(column=0, row=2, padx=5, pady=5, sticky="w")

# Option menu used with the popularity function. Denotes time range.
timeRange = ["Last Month", "Last 3 Months", "Last 6 Months", "Last Year"]
timeVar = StringVar(win)
timeRangeOptn = OptionMenu(win, timeVar, *timeRange)
timeVar.set(timeRange[0])
timeRangeOptn.grid(column=0, row=2, padx=110, pady=5, sticky="w")

### END OF FOOTER BUILDING ###

win.deiconify()  # Shows window after all widgets are created
win.mainloop()

### END OF MAIN WINDOW CREATION ###
