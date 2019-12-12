import os.path
import time
from tkinter import (Tk, messagebox, Frame, Label,
                     Button, Entry, OptionMenu, StringVar,
                     Checkbutton, BooleanVar)
from tkinter.ttk import (Treeview, Scrollbar)
from database import (read, __DB__)
import booksearch as bs
import bookreturn as br
import bookcheckout as bc

# TODO: Remove CLI messages
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
    """
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
    populate(query)


def checkIfDate(event):
    if var.get() == "Date":
        dateBox.grid()
    else:
        dateBox.grid_remove()


def populate(library):
    """
    """
    # Clears table
    table.delete(*table.get_children())

    # Inserts each book into the table
    # where text is the key field
    for book in library:
        table.insert("", int(book[0]), text=book[0], values=(book[1], book[2], book[3], book[4]))


def checkinBook():
    """
    """

    try:
        # Gets book info from table selection
        selection   = table.focus()
        book        = table.item(selection)
        bookID      = book["text"]
        booktitle   = book["values"][0]

        checkoutBtn["state"]    = "disabled"
        returnBtn["state"]      = "disabled"

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
    finally:
        checkoutBtn["state"]    = "normal"
        returnBtn["state"]      = "normal"


def checkoutBook():
    """
    """

    try:
        # Gets book info from table selection
        selection   = table.focus()
        book        = table.item(selection)
        bookID      = book["text"]
        booktitle   = book["values"][0]

        if bookID != "":

            checkoutBtn["state"]    = "disabled"
            returnBtn["state"]      = "disabled"

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
                    checkoutBtn["state"]    = "normal"
                    returnBtn["state"]      = "normal"

            ### BUILDING INPUT DIALOGUE ###
            dialogue = Tk()
            dialogue.title("Borrow a Book")
            dialogue.geometry("300x80")
            dialogue.resizable(False, False)

            lbl         = Label(dialogue, text="Enter Member ID")
            txtbox      = Entry(dialogue)
            okBtn       = Button(dialogue, text="Okay",
                            command=checkout)
            cancelBtn   = Button(dialogue, text="Cancel",
                                    command=lambda:dialogue.destroy())

            lbl.pack(side="top", fill="x", padx=10)
            txtbox.pack(side="top", fill="x", padx=10)
            okBtn.pack(side="left", padx=50)
            cancelBtn.pack(side="right", padx=50)
            ### END OF DIALOGUE BUILDING ###

    except IndexError:
        # Flashes check-in button if nothing is selected
        checkoutBtn.flash()

if __name__ == "__main__":
    # TODO Add args
    #print("Hello.")
    pass


###########################
#                         #
# Creating GUI Components #
#                         #
###########################

# Creating main window
win = Tk()
win.withdraw()  # Hides root window when using messageboxes in pathChecker()
win.title("Vivlio - Library System")
win.geometry("1024x768")
win.resizable(False, False)

if not pathChecker():
    quit()

print("All files exists.")


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
var.set(options[0])
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

""" useSelection = BooleanVar()
returnCbtn = Checkbutton(win, text="Check-in with Selection",
                        variable=useSelection, onvalue=True, offvalue=False)
useSelection.set(True)
returnCbtn.grid(column=0, row=2, padx= 150, pady=5, sticky="e") """

popularBtn = Button(win, text="Monthly Charts")
popularBtn.grid(column=0, row=2, padx=5, pady=5, sticky="w")

### END OF FOOTER BUILDING ###

win.deiconify()  # Shows window after all widgets are created


win.mainloop()
