import os.path
import time
from tkinter import (Tk, messagebox, Frame, Label,
                     Button, Entry, OptionMenu, StringVar)
from tkinter.ttk import (Treeview)


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
    print("\nChecking for files:")
    #print("\t| Settings file: " + dict[settingsPath])
    print("\t| Database file: " + dict[dbPath])
    print("\t| Log file:      " + dict[logPath])

    # Checks if any of the previous files are missing
    if False in [dbPath, logPath]:
        while True:

            # Asks if user wants to create files
            createFiles = messagebox.askyesno("",
                                              "Required files are missing.\nCreate missing files?")

            # Creating files if user replies "y" (Yes)
            if createFiles:
                print("Creating files...")

                # List of all files required to function and their existence
                fileList = [["database.txt", dbPath], ["logfile.txt", logPath]]

                # List of files that doesn't exist, filtered from fileList.
                files = [f for f in fileList if f[1] == False]

                # Create each missing file
                for f in files:
                    try:
                        file = open(f[0], "w+")
                        print("Created", f[0])
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


def checkIfDate(event):
    if var.get() == "Date":
        dateBox.grid()
    else:
        dateBox.grid_remove()


if __name__ == "__main__":
    # TODO Add args
    print("Hello.")

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
options = ["Title", "Author", "Date"]
var = StringVar(toolbar)
searchOptn = OptionMenu(toolbar, var, *options, command=checkIfDate)
var.set("Title")
searchOptn.grid(column=3, row=0, padx=5, pady=5)

toolbar.grid(column=0, row=0)

### END OF FRAME BUILDING ###

### BUILDING TREEVIEW (TABLE) ###

table = Treeview(win)
table["columns"] = ("1", "2", "3", "4")     # Adding indexes

# Defining all columns and their width.
# Not iterated as each has a different width.
table.column("#0", width=50, minwidth=50)
table.heading("#0", text="ID")

table.column("1", width=452, minwidth=30)
table.heading("1", text="Title")

table.column("2", width=278, minwidth=30)
table.heading("2", text="Author")

table.column("3", width=150, minwidth=30)
table.heading("3", text="Date")

table.column("4", width=80, minwidth=30)
table.heading("4", text="Member")

# TODO: Populate table

table.grid(column=0, row=1, padx=5, pady=5)



win.deiconify()  # Shows window after all widgets are created


win.mainloop()
