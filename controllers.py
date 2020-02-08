"""
| ---------------------------------------------------------------------
| controllers.py
| ---------------------------------------------------------------------
| This control module holds all of the controllers. There are three
| controller classes defined in this file. The DirectoryController
| is responsible for performing all of the directory related tasks
| as its name suggests. The CommandController class runs the passed
| command throughout the saved directories using saved credentials.
| And the ProjectController class manipulates all project related
| tasks like setting active project and adding new projects.
|
| Version: 4.x
| License: GNU General Public License 3
"""

import os
from lcex import *
from pathlib import Path
from output import Output
from color_codes import ColorCodes


class DirectoryController:
    """
    Add, view, or delete directories/instances.
    """
    
    def __init__(self, instances):
        # instances is a list of module where all directory names are listed.
        self._instances = instances
    
    def add(self, *args):
        """
        Add directories/instances to the existing list or create a new list.
        :param args: Names of directories
        """
        try:
            if len(args) <= 0:
                raise ArgumentNotProvidedException(
                    "Aborting! No argument has been provided.")
            if self._instances is None:
                raise ActiveProjectNotSetException(
                    "May be no active project has been set. Please check.")
            
            # Process passed arguments
            directories = list((filter(lambda dir: isinstance(dir, str), args)))
            
            # Append new directories to the list, no redundant value will exist
            self._instances.extend([ins for ins in directories if ins not in self._instances])
        
        except ArgumentNotProvidedException as error:
            Output.write(error, ColorCodes.DANGER)
        except ActiveProjectNotSetException as error:
            Output.write(error, ColorCodes.DANGER)
        else:
            Output.write('Success!', ColorCodes.SUCCESS)
            self.view()
    
    def view(self, sort=False):
        """
        View list of added directories/instances in current active project.
        :param sort: Sort alphabetically, false by default (optional)
        """
        try:
            if self._instances is None:
                raise ActiveProjectNotSetException(
                    "May be no active project has been set. Please check.")
            
            Output.write('Listing directories...', ColorCodes.INFO)
            directories = self._instances.copy()
            Output.write("{}\n".format(
                '\n'.join(
                    ('- ' + ins for ins in sorted(directories)) if sort else ('- ' + ins for ins in directories))))
            Output.write("Total %d directories listed." % len(directories))
        except ActiveProjectNotSetException as error:
            Output.write(error, ColorCodes.DANGER)
    
    def clear(self, *args, full=False):
        """
        Clears entire list or specified directories/instances from the active project instance list.
        :param args: Names of directories/instances
        :param full: If true, clears entire list. False by default (optional)
        """
        try:
            if len(args) <= 0 and not full:
                raise ArgumentNotProvidedException(
                    "Aborting! No argument has been provided.")
            
            if self._instances is None:
                raise ActiveProjectNotSetException(
                    "May be no active project has been set. Please check.")
            
            # If flag full is true, remove entire list
            if full:
                # Ask for confirmation
                Output.write(
                    "This will clear the entire list, are you sure? (yes/no) [no]:", ColorCodes.WARNING)
                yes = {'yes', 'y'}
                decision = input(">> ")
                if decision not in yes:
                    raise KeyboardInterrupt("Aborted! Nothing is changed.")
                else:
                    self._instances.clear()
                    Output.write('Directory list cleared!', ColorCodes.SUCCESS)
                    return
            
            # Else remove specified keys only
            keys = set(filter(lambda dir: type(dir) is str, args))
            for key in keys:
                # Skip if a specified key is not in the list
                if key not in self._instances:
                    Output.write(f"{key} is not found in the list! Skipping...",
                                 ColorCodes.DANGER)
                    continue
                
                Output.write(f"Removing {key}...", ColorCodes.WARNING)
                self._instances.remove(key)
                Output.write('Success!', ColorCodes.SUCCESS)
            self.view()
        
        except ArgumentNotProvidedException as error:
            Output.write(error, ColorCodes.DANGER)
        except ActiveProjectNotSetException as error:
            Output.write(error, ColorCodes.DANGER)
        except KeyboardInterrupt as error:
            Output.write(error, ColorCodes.DANGER)


class CommandController:
    """
    Stirs the command executor.
    """
    
    def run(self, project, cmd, li=0, ui=None, ex=()):
        """
        Run the command.
        :param project: The active project dictionary
        :param cmd: The command to run
        :param li: Lower index (optional)
        :param ui: Upper index (optional)
        :param ex: Tuple of indices to exclude during execution (optional)
        """
        try:
            succeeded = 0
            failed = 0
            # First, apply li and ui to slice instances/directories,
            # then filter out by excluding according to ex
            instances = [proj for proj in project['instances'][li:ui] if project['instances'].index(proj) not in ex]
            instance_root = Path(project['root'])
            
            if len(instances) <= 0:
                Output.write("No instances has been found in the list.", ColorCodes.DANGER)
            
            for instance in instances:
                # If a directory is missing, tell the user
                if not os.path.exists(instance_root.joinpath(instance)):
                    print("\n")
                    Output.write([
                        {'text': 'Directory', 'code': ColorCodes.DANGER},
                        {'text': f"'{instance}'", 'code': ColorCodes.WARNING},
                        {'text': 'is not found! Skipping...',
                         'code': ColorCodes.DANGER}
                    ])
                    failed += 1
                    continue
                
                # Omit if not a directory
                if not os.path.isdir(instance_root.joinpath(instance)):
                    print("\n")
                    Output.write([
                        {'text': f"'{instance}'", 'code': ColorCodes.WARNING},
                        {'text': 'is not a instance. Skipping...',
                         'code': ColorCodes.INFO}
                    ])
                    failed += 1
                    continue
                
                self.execute(cmd, instance_root.joinpath(instance))
                succeeded += 1
        
        except TypeError:
            Output.write("Please provide valid integers!", ColorCodes.DANGER)
        finally:
            # Show the statistics
            Output.write([
                {'text': f"\nSuccessful run:", 'code': ColorCodes.NORMAL},
                {'text': succeeded, 'code': ColorCodes.SUCCESS},
                {'text': f"\nFailed run:", 'code': ColorCodes.NORMAL},
                {'text': failed, 'code': ColorCodes.DANGER}
            ])
    
    def execute(self, cmd, instance_path):
        """
        Execute the command to the specified directory.
        :param cmd: The command to run
        :param instance_path: Path where the command should execute
        """
        try:
            print('\n')
            Output.write([
                {'text': 'Changed directory to',
                 'code': ColorCodes.INFO},
                {'text': f"'{instance_path}'",
                 'code': ColorCodes.WARNING},
                {'text': "and running", 'code': ColorCodes.INFO},
                {'text': f"'{cmd}'", 'code': ColorCodes.WARNING}
            ])
            # Switch to the desired directory
            os.chdir(instance_path)
            # Do the mischief
            os.system(cmd)
        except OSError as error:
            # If something goes wrong...
            Output.write(error, ColorCodes.DANGER)


class ProjectController:
    """
    Add, view, or delete projects and set active project.
    """
    
    def __init__(self, lcdb):
        self._lcdb = lcdb
    
    def active(self, project):
        """
        Set active project.
        :param project: Name of the project
        """
        try:
            if project not in self._lcdb['projects'].keys() or len(self._lcdb['projects']) <= 0:
                raise ProjectNotFoundException(
                    "Project %s is not found in the list, to see available projects run 'proj view'." % project)
            
            self._lcdb['active'] = project
            Output.write("%s is set as active project." %
                         project, ColorCodes.SUCCESS)
        except ProjectNotFoundException as error:
            Output.write(error, ColorCodes.DANGER)
    
    def add(self, strpath):
        """
        Add new project.
        :param strpath: The absolute path to the project.
        """
        try:
            if not os.path.isabs(strpath):
                raise NotAnAbsolutePathException(
                    "Invalid path, it should be absolute.")
            
            if not os.path.exists(strpath):
                raise FileNotFoundError(
                    "Provided path does not exist, please enter a valid path.")
            
            path = Path(strpath)
            # Exit if already exists
            if path.stem in self._lcdb['projects'].keys():
                Output.write("Project already exists!", ColorCodes.DANGER)
                return
            
            # Add project with default structure
            data = {
                'root': str(path),
                'instances': []
            }
            self._lcdb['projects'][path.stem] = data
            Output.write("%s is added to project list." %
                         path.stem, ColorCodes.SUCCESS)
        
        except NotAnAbsolutePathException as error:
            Output.write(error, ColorCodes.DANGER)
        except FileNotFoundError as error:
            Output.write(error, ColorCodes.DANGER)
    
    def view(self):
        """
        View list of added projects. Active project will be star marked.
        """
        try:
            projects = list(self._lcdb['projects'].keys())
            
            if len(projects) <= 0:
                raise ProjectNotFoundException(
                    "No project has been found in the list.")
            
            Output.write('Listing projects...', ColorCodes.INFO)
            for project in projects:
                Output.write("- %s%s" %
                             (project, '*' if project == self._lcdb['active'] else ''))
            Output.write("\nTotal %d projects listed." % len(projects))
        
        except ProjectNotFoundException as error:
            Output.write(error, ColorCodes.WARNING)
    
    def clear(self, key):
        """
        Remove a project along with it's instances from the list.
        :param key: The name of the project
        """
        try:
            if key not in self._lcdb['projects'].keys():
                raise ProjectNotFoundException(
                    'Project is not found in the list.')
            
            # Ask for confirmation
            Output.write(
                "Caution! This cannot be undone. Do you want to proceed? (yes/no)[no]:", ColorCodes.DANGER)
            yes = {'yes', 'y'}
            decision = input(">> ")
            if decision not in yes:
                raise KeyboardInterrupt("Aborted! Nothing is changed.")
            
            # If the key is the active project, set active project empty
            if key == self._lcdb['active']:
                self._lcdb['active'] = ''
            
            del self._lcdb['projects'][key]
            Output.write("%s is removed from LordCommander." %
                         key, ColorCodes.SUCCESS)
        
        except ProjectNotFoundException as error:
            Output.write(error, ColorCodes.DANGER)
        except KeyboardInterrupt as error:
            Output.write(error, ColorCodes.DANGER)
