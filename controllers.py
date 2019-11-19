#! /usr/bin/env python3.7
import sys
import os
from output import Output
from color_codes import ColorCodes


class DirectoryController:
    """
    This class controls and performs all of the directory related tasks according to the passed argument
    followed by dirs command. It automatically calls the control method and depending on the arguments, 
    the control method decides what to do with the input.
    """

    def __init__(self, dirs):
        # dirs is a shelve module where all directory names are listed.
        self.dirs = dirs
        self.control()

    def control(self):
        """Decide what to do with the user input."""
        if sys.argv[2].lower() == 'add' and len(sys.argv) > 3:
            directories = sys.argv[3:len(sys.argv)]
            self.add(directories)

        elif sys.argv[2].lower() == 'list':
            sort = sys.argv[3].lower() if len(sys.argv) > 3 else None
            self.list(sort)

        elif sys.argv[2].lower() == 'clear':
            keys = sys.argv[3:len(sys.argv)].copy() if len(
                sys.argv) > 3 else None
            self.clear(keys)
        else:
            Output.write('Invalid operation!', ColorCodes.DANGER)

    def add(self, directories):
        """Create new list of directories or append to the existing list."""
        try:
            # Append new directories to existing list
            self.dirs['list'] += list(directories)
        except KeyError as error:
            # If there is no existing list, an error should raise,
            # hence create a new list of directories.
            self.dirs['list'] = directories.copy()
        Output.write('Success!', ColorCodes.SUCCESS)
        # Show new list
        self.list()

    def list(self, sort=None):
        """Show existing list of directories."""
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

    def clear(self, keys=None):
        """Clear specified key(s) or entire list of directory."""
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

    def __init__(self, creds):
        self.creds = creds

    def control(self):
        """
        Control credentials related operations
        :return:
        """


class CommandController:
    """
    This class controls the running procedure of the command followed by run keyword. It can be
    any shell command, anything!

    CAUTION: Definitely try at your home. If you do something like "sudo rm -rf /" on your 
    production server, your system may die.
    """

    def __init__(self, cmd, dirs, creds):
        self.cmd = cmd
        self.dirs = dirs
        self.creds = creds

    def run(self):
        """Run the command through out each saved directory in dirs list."""
        try:
            directories = self.dirs['list'].copy()
            # Sort directories alphabetically
            directories.sort()
            for directory in directories:
                # Check if there is really a directory exists
                if os.path.exists(f"../{directory}"):
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
                else:
                    # If a directory is missing, tell the user
                    print('\n')
                    Output.write([
                        {'text': 'Directory', 'code': ColorCodes.DANGER},
                        {'text': f"'{directory}'", 'code': ColorCodes.WARNING},
                        {'text': 'not found! Skipping...',
                            'code': ColorCodes.DANGER}
                    ])
        except KeyError as error:
            # In case of an empty list, expect KeyError
            Output.write('No saved directory has been found!',
                         ColorCodes.DANGER)
