import os.path, time
from os import path

def main():
    pathChecker()

def pathChecker():

    '''Checks if all additional files exists within the directory 
    and creates them as necessary.'''

    settingsPath = path.exists("settings.json")
    dbPath = path.exists("database.txt")
    logPath = path.exists("logfile.txt")

    # Dict to convert "True" and "False" into something more understandable.
    dict = {}
    dict["True"] = "Exists"
    dict["False"] = "Missing"

    print("\nChecking for files:")
    print("\t| Settings file: " + dict[str(settingsPath)])
    print("\t| Database file: " + dict[str(dbPath)])
    print("\t| Log file:      " + dict[str(logPath)])

    if False in [settingsPath, dbPath, logPath]:
        while True:
            createFiles = input("\nWould you like to create the missing files? [y/n]\n>>")

            if createFiles.lower() == "y":
                #TODO Create missing Files
                print("Creating files...")

                fileList = [["settings.json", settingsPath], 
                ["database.txt", dbPath], ["logfile.txt", logPath]]

                files = [f for f in fileList if f[1] == False]
                
                for f in files:
                    try:
                        file = open(f[0], "w+")
                        print("Created", f[0])
                        file.close
                    except IOError:
                        print("Unable to write files.")
                        #TODO Error Handling
                print("Done!")
                break

            elif createFiles.lower() == "n":
                print("This application will not work properly without these files.\
                    \nIf you have backups, please copy into the working directory \
                    \nbefore continuing.")
                os.system("pause")
                
            else:
                print("unrecognisable command. Please type again")
                continue
    
    time.sleep(2)
    os.system("cls")
    
if __name__== "__main__":
   main()