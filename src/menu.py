import os.path, time
from os import path

def main():
    if pathChecker():
        print("yay")
        #TODO

def pathChecker():

    '''Checks if additional files exists within the directory 
    and creates them as necessary.'''

    # Looks for the required files
    settingsPath = path.exists("settings.json")
    dbPath = path.exists("database.txt")
    logPath = path.exists("logfile.txt")

    # Dict to convert "True" and "False" into something more understandable.
    # Using escape sequences to colour text output
    dict = {}
    dict["True"] = "\x1b[1;32;40m"+"Exists"+"\x1b[0m"
    dict["False"] = "\x1b[1;31;40m"+"Missing"+"\x1b[0m"

    # Prints file status
    print("\nChecking for files:")
    print("\t| Settings file: " + dict[str(settingsPath)])
    print("\t| Database file: " + dict[str(dbPath)])
    print("\t| Log file:      " + dict[str(logPath)])

    if False in [settingsPath, dbPath, logPath]:
        while True:
            createFiles = input("\nWould you like to create the missing files? [y/n]\n>>")

            if createFiles.lower() == "y":
                print("Creating files...")

                # List of all files required to function and their existence
                fileList = [["settings.json", settingsPath], 
                ["database.txt", dbPath], ["logfile.txt", logPath]]

                # List of files that doesn't exist, filtered from fileList.
                files = [f for f in fileList if f[1] == False]
                
                # Create each missing file
                for f in files:
                    try:
                        file = open(f[0], "w+")
                        print("Created", f[0])
                        file.close

                    except IOError:
                        print("Unable to write files.")
                        #TODO Error Handling

                print("Done!")

                time.sleep(2)
                os.system("cls")
                return True

            # If the user wishes not to create files: terminate.
            # Note: exit() may throw an exeption in some IDEs but will funtion
            # correctly in cmd and powershell.
            elif createFiles.lower() == "n":
                print("This application will not work properly without these files.\
                    \nIf you have backups, please copy into the working directory \
                    \nbefore continuing.")
                time.sleep(5)
                return False
            else:
                print("Unrecognisable command. Please type again")
                continue
    else:
        time.sleep(2)
        os.system("cls")
        return True
    
if __name__== "__main__":
   main()