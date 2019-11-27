"""
    This control module holds all of the controllers. There are four Controller classes
    declared here. Three of them are subcontrollers, while the first one is primary.

    The Controller class has two functions. First, decide which subcontroller to initiate,
    and second, which method to call. The main program should only deal with this 
    controller and call the pilot method.

    The DirectoryController is responsible for performing all of the directory related 
    functions as its name suggests.

    The CredentialController accounts for credential related tasks as its name suggests.

    And finally, the CommandController class runs the passed command throughout the saved
    directories using saved credentials.
"""
import sys
import os
from output import Output
from color_codes import ColorCodes


class Controller:
    """
    Controller class decides which subcontroller class to be initiated and which method is
    to call. You should deal with this class only from outside to access the subclasses.
    Call the pilot method after initiating the Controller class.
    """

    def __init__(self, dirs, creds, cmd):
        self.dirs = dirs
        self.creds = creds
        self.cmd = cmd

    def pilot(self):
        """Decide which subcontroller to initiate."""
        if sys.argv[1].lower() == 'dirs':
            instance = DirectoryController(self.dirs)
        elif sys.argv[1].lower() == 'creds':
            instance = CredentialController(self.creds)
        elif sys.argv[1].lower() == 'run':
            instance = CommandController(self.cmd, self.dirs, self.creds)

        self.control(instance)

    def control(self, instance):
        """Decide which method to call."""
        if isinstance(instance, CommandController):
            instance.make()
        if sys.argv[2].lower() == 'add':
            instance.add()
        elif sys.argv[2].lower() == 'list':
            instance.list()
        elif sys.argv[2].lower() == 'clear':
            instance.clear()


class DirectoryController:
    """
    This class controls and performs all of the directory related 
    tasks according to the passed argument followed by dirs command.
    """

    def __init__(self, dirs):
        # dirs is a shelve module where all directory names are listed.
        self.dirs = dirs

    def add(self):
        """Create new list of directories or append to the existing list."""
        try:
            directories = sys.argv[3:len(sys.argv)]
            # Append new directories to existing list
            self.dirs['list'] += list(directories)
        except KeyError as error:
            # If there is no existing list, an error should raise,
            # hence create a new list of directories.
            self.dirs['list'] = directories.copy()
        Output.write('Success!', ColorCodes.SUCCESS)
        # Show new list
        self.list()

    def list(self):
        """Show existing list of directories."""
        sort = sys.argv[3].lower() if len(sys.argv) > 3 else None
        try:
            Output.write('Listing directories...', ColorCodes.INFO)
            directories = self.dirs['list'].copy()

            # Sort alphabetically if mentioned
            if sort == 'alpha':
                directories.sort()

            for directory in directories:
                Output.write(directory)
        except KeyError as error:
            Output.write('No saved directory has been found!',
                         ColorCodes.DANGER)

    def clear(self):
        """Clear specified key(s) or entire list of directory."""
        keys = sys.argv[3:len(sys.argv)].copy() if len(
            sys.argv) > 3 else None
        if keys is None:
            # If no key is specified, remove entire list
            self.dirs.clear()
            Output.write('Directory list cleared!', ColorCodes.SUCCESS)
            return

        # Else, try to remove specified keys
        try:
            # Copy the list into intermediate container
            mod = self.dirs['list'].copy()
            for key in keys:
                Output.write(f"Removing {key}...", ColorCodes.WARNING)
                mod.remove(key)
            # Restore directories after trimming
            self.dirs['list'] = mod.copy()
            Output.write('Success!', ColorCodes.SUCCESS)
            # Show new list
            self.list()
        except ValueError as error:
            # In case of missing key, expect ValueError
            Output.write('Directory is not found in list!', ColorCodes.DANGER)
        except KeyError as error:
            # In case of an empty list, expect KeyError
            Output.write('No saved directory has been found!',
                         ColorCodes.DANGER)


class CredentialController:
    """
    This class controls and performs all of the credentials related 
    tasks according to the passed argument followed by creds command.
    """

    def __init__(self, creds):
        self.creds = creds

    def add(self):
        """Appends new credentials in key - value pairs."""
        try:
            if len(sys.argv) != 5:
                raise SyntaxError(
                    'Invalid syntax! Please pass argument in <key> <value> format.')
            # Warn if key is already in list
            if sys.argv[3].lower() in self.creds:
                raise ValueError('Key already exists!')
            self.creds[sys.argv[3].lower()] = sys.argv[4]
            Output.write("Success!", ColorCodes.SUCCESS)
            # Show current list
            self.list()
        except SyntaxError as error:
            Output.write(error, ColorCodes.DANGER)
        except ValueError as error:
            Output.write(error, ColorCodes.DANGER)
            # TODO: Ask if user wish to replace it

    def list(self):
        """Show existing list of credentials."""
        try:
            Output.write('Listing credentials...', ColorCodes.INFO)
            if len(self.creds) <= 0:
                raise KeyError
            for key in self.creds:
                Output.write(f"{key} => {self.creds[key]}")
        except KeyError as error:
            Output.write('No saved credential has been found!',
                         ColorCodes.DANGER)

    def clear(self):
        """Clear specified key(s) or entire list of credentials."""
        keys = sys.argv[3:len(sys.argv)].copy() if len(
            sys.argv) > 3 else None
        if keys is None:
            # If no key is specified, remove entire list
            self.creds.clear()
            Output.write('Credential list cleared!', ColorCodes.SUCCESS)
            return

        # Else, try to remove specified keys
        try:
            # Copy the list into intermediate container
            for key in keys:
                Output.write(f"Removing {key}...", ColorCodes.WARNING)
                del self.creds[key]
            # Restore directories after trimming
            Output.write('Success!', ColorCodes.SUCCESS)
            # Show new list
            self.list()
        except ValueError as error:
            # In case of missing key, expect ValueError
            Output.write('Credential is not found in list!', ColorCodes.DANGER)
        except KeyError as error:
            # In case of an empty list, expect KeyError
            Output.write('No saved credential has been found!',
                         ColorCodes.DANGER)


class CommandController:
    """
    This class controls the running procedure of the command followed 
    by run keyword. It can be any shell command, anything!

    CAUTION: Definitely try at your home. If you do something like 
    "sudo rm -rf /" on your production server, your system may die.
    """

    def __init__(self, cmd, dirs, creds):
        self.cmd = cmd
        self.dirs = dirs
        self.creds = creds

    def make(self):
        """Process the ingredients to run."""
        try:
            if len(sys.argv) != 3:
                raise SyntaxError(
                    "Invalid syntax! The correct format is ./lc run '<command>'.")

            directories = self.dirs['list'].copy()
            # Sort directories alphabetically
            directories.sort()
            self.run(directories)
        except SyntaxError as error:
            # No time to deal with wrong syntax
            Output.write(error, ColorCodes.DANGER)
        except KeyError as error:
            # In case of an empty list, expect KeyError
            Output.write('No saved directory has been found!',
                         ColorCodes.DANGER)

    def run(self, directories):
        """Run the command through out each saved directory in dirs list."""
        for directory in directories:
            # If a directory is missing, tell the user
            if not os.path.exists(f"../{directory}"):
                print('\n')
                Output.write([
                    {'text': 'Directory', 'code': ColorCodes.DANGER},
                    {'text': f"'{directory}'", 'code': ColorCodes.WARNING},
                    {'text': 'not found! Skipping...',
                     'code': ColorCodes.DANGER}
                ])
            try:
                print('\n')
                Output.write([
                    {'text': 'Changed directory to',
                        'code': ColorCodes.INFO},
                    {'text': f"'{os.path.realpath('../' + directory)}'",
                        'code': ColorCodes.WARNING},
                    {'text': "and running", 'code': ColorCodes.INFO},
                    {'text': f"'{self.cmd}'", 'code': ColorCodes.WARNING}
                ])
                # Switch to the desired directory
                os.chdir(f"../{directory}")
                # Do the mischief
                os.system(self.cmd)
            except OSError as error:
                # If something goes wrong...
                Output.write(error, ColorCodes.DANGER)
            finally:
                # Return to home like a good animal
                os.chdir('../lordcommander')
