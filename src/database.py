__DB__  = "database.txt"
__LOG__ = "logfile.txt"
__SET__ = "settings.json"
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
        return database

    except IOError as e:
        print("Cannot read from '%s'. Check if the file is within the root\
 directory or that this application has sufficient permissions\
 to access it." %path)
        print(e)

    finally:
        file.close()

def append(path, msg):

    """
    Adds a line of any String to the end of a file.

    Inputs:
        path (String) : path to a file
        msg  (String) : a message to append
    """

    try:
        file = open(str(path), "a")
        file.write(str(msg))
        file.write()
    except IOError as e:
        print("Cannot write to '%s'. Check if the file is within the root\
 directory or that this application has sufficient permissions\
 to access it." %path)
        print(e)
    finally:
        file.close()

def formatStr(strList, sym):
    """
    Joins a list with a separator, returns as a string.

    Inputs:
        strList ([String])  : List of Strings
        sym     (Char)      : Separator character

    Returns:
        (String) : String of joined list
    """
    return sym.join(strList)

print(read(__DB__))
