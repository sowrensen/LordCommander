"""
| ---------------------------------------------------------------------
| controllers.py
| ---------------------------------------------------------------------
| This control module holds all of the controllers. There are two
| controller classes defined in this file. The DirectoryController
| is responsible for performing all of the directory related tasks
| as its name suggests. The CommandController class runs the passed
| command throughout the saved directories using saved credentials.
|
| Version: 3.0
| License: GNU General Public License 3
"""

import os
from output import Output
from color_codes import ColorCodes
from pathlib import Path


class DirectoryController:
    """
    Controls everything related to directories.
    """
    
    def __init__(self, dirs):
        # dirs is a shelve module where all directory names are listed.
        self._dirs = dirs
    
    def add(self, *args):
        """
        Add directories to the existing list or create a new list.
        :param args: Names of directories
        """
        if len(args) <= 0:
            Output.write(
                "Aborting! No argument has been provided.", ColorCodes.DANGER)
            return
        try:
            directories = list(set(filter(lambda dir: type(dir) is str, args)))
            # Append new directories to existing list
            self._dirs['list'] += directories.copy()
        except KeyError as error:
            # If there is no existing list, an error should raise,
            # hence create a new list of directories.
            self._dirs['list'] = directories.copy()
        finally:
            Output.write('Success!', ColorCodes.SUCCESS)
            self.view()
    
    def view(self, sort=False):
        """
        View list of added directories.
        :param sort: Sort alphabetically, false by default (optional)
        """
        try:
            Output.write('Listing directories...', ColorCodes.INFO)
            directories = self._dirs['list'].copy()
            Output.write("{}\n".format('\n'.join(sorted(directories) if sort else directories)))
            Output.write("Total %d directories listed." % len(directories))
        except KeyError as error:
            Output.write('No saved directory has been found!',
                         ColorCodes.DANGER)
    
    def clear(self, *args, full=False):
        """
        Clears entire list or specified directories from the list.
        :param args: Names of directories
        :param full: If true, clears entire list. False by default (optional)
        """
        if len(args) <= 0 and not full:
            Output.write(
                "Aborting! No argument has been provided.", ColorCodes.DANGER)
            return
        # If flag full is true, remove entire list
        if full:
            # Ask for confirmation
            Output.write("This will clear the entire list, are you sure? (yes/no) [no]:", ColorCodes.WARNING)
            yes = {'yes', 'y'}
            ans = input(">> ")
            if ans in yes:
                self._dirs.clear()
                Output.write('Directory list cleared!', ColorCodes.SUCCESS)
            else:
                Output.write('Action aborted.', ColorCodes.INFO)
            return
        # Else remove specified keys only
        try:
            keys = set(filter(lambda dir: type(dir) is str, args))
            # Copy the list into an intermediate container
            mod = self._dirs['list'].copy()
            for key in keys:
                if key not in mod:
                    Output.write(f"{key} is not found in the list! Skiping...",
                                 ColorCodes.DANGER)
                    continue
                Output.write(f"Removing {key}...", ColorCodes.WARNING)
                mod.remove(key)
                Output.write('Success!', ColorCodes.SUCCESS)
            # Restore directories after trimming
            self._dirs['list'] = mod.copy()
            self.view()
        except KeyError as error:
            # In case of an empty list, expect KeyError
            Output.write('No saved directory has been found!',
                         ColorCodes.DANGER)


class CommandController:
    """
    Controls everything related to the command.
    """
    
    def run(self, dirs, cmd, li=0, ui=None):
        """
        Run the command.
        :param dirs: The shelve module where the list is saved
        :param cmd: The command to run
        :param li: Lower index (optional)
        :param ui: Upper index (optional)
        """
        try:
            directories = dirs['list'][li:ui].copy()
            cwd = Path(os.getcwd())
            succeed = 0
            failed = 0
            for directory in directories:
                # If a directory is missing, tell the user
                if not os.path.exists(cwd.parent.joinpath(directory)):
                    print("\n")
                    Output.write([
                        {'text': 'Directory', 'code': ColorCodes.DANGER},
                        {'text': f"'{directory}'", 'code': ColorCodes.WARNING},
                        {'text': 'is not found! Skipping...',
                         'code': ColorCodes.DANGER}
                    ])
                    failed += 1
                    continue
                # Omit if not a directory
                if not os.path.isdir(cwd.parent.joinpath(directory)):
                    print("\n")
                    Output.write([
                        {'text': f"'{directory}'", 'code': ColorCodes.WARNING},
                        {'text': 'is not a directory. Skipping...',
                         'code': ColorCodes.INFO}
                    ])
                    failed += 1
                    continue
                self.execute(directory, cmd, cwd)
                succeed += 1
        except TypeError:
            Output.write("Please provide valid integers!", ColorCodes.DANGER)
        except KeyError:
            # In case of an empty list, expect KeyError
            Output.write('No saved directory has been found!',
                         ColorCodes.DANGER)
        finally:
            # Return to home like a good cat 🐈
            os.chdir(cwd)
            Output.write([
                {'text': f"\nSuccessful run:", 'code': ColorCodes.NORMAL},
                {'text': succeed, 'code': ColorCodes.SUCCESS},
                {'text': f"\nFailed run:", 'code': ColorCodes.NORMAL},
                {'text': failed, 'code': ColorCodes.DANGER}
            ])
    
    def execute(self, directory, cmd, cwd):
        """
        Execute the command to the specified directory.
        :param directory: The directory where the command will run
        :param cmd: The command to run
        :param cwd: Location of the lordcommander program
        """
        try:
            print('\n')
            Output.write([
                {'text': 'Changed directory to',
                 'code': ColorCodes.INFO},
                {'text': f"'{cwd.parent.joinpath(directory)}'",
                 'code': ColorCodes.WARNING},
                {'text': "and running", 'code': ColorCodes.INFO},
                {'text': f"'{cmd}'", 'code': ColorCodes.WARNING}
            ])
            # Switch to the desired directory
            os.chdir(cwd.parent.joinpath(directory))
            # Do the mischief
            os.system(cmd)
        except OSError as error:
            # If something goes wrong...
            Output.write(error, ColorCodes.DANGER)
