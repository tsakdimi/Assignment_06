#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (DTsakalos, 2021-Feb-21, Added code to complete program)
# DBiesinger, 2030-Jan-01, Created File
#------------------------------------------#

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of dicts to hold data
dicRow = {}  # dict of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object

# -- PROCESSING -- #
class DataProcessor:
    """Processing the data within memory"""

    @staticmethod
    def append_data(table):
        """Function to manage data addition within program memory

        Strips the data the user inputs and then appends them into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        # 3.3.1 Ask user for new ID, CD Title and Artist
        while True:
            try:
                intID = int(input('Enter an ID: ').strip())
                break
            except ValueError: #making sure the program does not crash with string as input
                print('Invalid Input! Try again.')
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        # 3.3.2 Add item to the table
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
        table.append(dicRow)
        IO.show_inventory(table)

    @staticmethod
    def delete_data(table):
        """ Function to manage data deletion within program memory

        Asks user for an ID number and checks to find the appropriate listing in a
        (list of dicts) table and removes the row (dict) that holds that ID number

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(table)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = int(input('Which ID would you like to delete? ').strip())
        # 3.5.2 search thru table and delete CD
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del table[intRowNr]
                blnCDRemoved = True
                break # Cannot remove more than one entry. When we have the same ID numbers only first is removed
        if blnCDRemoved:
            print('The CD was removed\n')
        else:
            print('Could not find this CD!\n')
        IO.show_inventory(table)

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        while True:
            try:
                objFile = open(file_name, 'r')
                break
            except FileNotFoundError:
                objFile = open(file_name, 'w')
        for line in objFile:
            data = line.strip().split(',')
            dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
            table.append(dicRow)
        objFile.close()

    @staticmethod
    def write_file(file_name, table):
        """Function to save data from a list of dictionaries to file in csv formating

        Saves the data from a 2D table in memory in current program 
        (list if dicts) and saves it to file, with each file line representing a row 
        of the 2D table, and each comma within a row separating the columns

        Args:
            file_name, (string): name of file used to save the data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(table)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            objFile = open(file_name, 'w')
            for row in table:
                lstValues = list(row.values())
                lstValues[0] = str(lstValues[0])
                objFile.write(','.join(lstValues) + '\n')
            objFile.close()
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')

# -- PRESENTATION (Input/Output) -- #
class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('\n------------Menu------------')
        print('[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case string of the users input out of the choices l, a, i, d, s or x
        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.
        """
        print('\n======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def load_choice(file_name, table):
        """Gets user input after selecting load on main menu

        Warns the user unsaved data will be lost if they type yes and runs FileProcessor.read_file

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """

        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(file_name, table)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break

    # 3.2 process load inventory
    if strChoice == 'l':
        IO.load_choice(strFileName, lstTbl)
        IO.show_inventory(lstTbl)

    # 3.3 process add a CD
    elif strChoice == 'a':
        DataProcessor.append_data(lstTbl)

    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)

    # 3.5 process delete a CD
    elif strChoice == 'd':
        DataProcessor.delete_data(lstTbl)

    # 3.6 process save inventory to file
    elif strChoice == 's':
        FileProcessor.write_file(strFileName, lstTbl)

    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')




