"""
| ---------------------------------------------------------------------
| utils.py
| ---------------------------------------------------------------------
| This utils module holds some of the necessary functions that may
| require over time to time.
|
| Version: 4.x
| License: GNU General Public License 3
"""
import os
import json
from pathlib import Path
from output import Output
from color_codes import ColorCodes
from lcex import ActiveProjectNotSetException


class Utils:
    """
    Some utilities that may come handy.
    """
    
    def __init__(self, lcdb, active):
        self._lcdb = lcdb
        self._project = active
    
    def search(self, key):
        """
        Search for a directory/instance of active project.
        :param key: Name of the directory to search
        :return: Name of the directory
        """
        try:
            if not self._project:
                raise ActiveProjectNotSetException(
                    "May be no active project has been set. Please check.")
            if key in self._project['instances']:
                Output.write('Found! Index: {}'.format(
                    self._project['instances'].index(key)), ColorCodes.SUCCESS)
            else:
                Output.write(
                    'Not found!',
                    ColorCodes.DANGER)
        except ActiveProjectNotSetException as error:
            Output.write(error, ColorCodes.DANGER)
    
    def total(self):
        """
        View total number of saved directories/instances of active project.
        :return: Number of directories.
        """
        try:
            if not self._project:
                raise ActiveProjectNotSetException(
                    "May be no active project has been set. Please check.")
            return Output.write("Total %d directories listed." % len(self._project['instances']), ColorCodes.INFO)
        except ActiveProjectNotSetException as error:
            Output.write(error, ColorCodes.DANGER)
    
    def dump(self, strpath):
        """
        Dump shelve module data to a JSON file.
        :param strpath: The output file directory
        """
        try:
            if not os.path.exists(strpath) or not os.path.isdir(strpath):
                raise FileNotFoundError(
                    "Invalid path, please provide a valid path.")
            path = Path(strpath)
            filename = path.joinpath('lcdb_dump.json')
            with open(filename, 'w') as output:
                json.dump(dict(self._lcdb), output, indent=4)
            Output.write("Data dumping successful. Output file: %s" %
                         filename, ColorCodes.SUCCESS)
        except FileNotFoundError as error:
            Output.write(error, ColorCodes.DANGER)
    
    def restore(self, strpath):
        """
        Restore data to shelve module from a dumped JSON file.
        :param strpath: The path of the JSON file
        """
        try:
            if not os.path.exists(strpath) or not os.path.isfile(strpath):
                raise FileNotFoundError(
                    "Invalid path, please provide a valid path.")
            
            # Load JSON file
            with open(strpath) as backup_file:
                data = json.load(backup_file)
            
            # Check content of the file and report if invalid
            if not all(key in data for key in ['active', 'projects']) or len(data.keys()) > 2:
                raise ValueError(
                    "Failed! Not a valid LordCommander supported file.")
            
            # Ask for confirmation to restore
            Output.write(
                "This will remove existing data completely. Are you sure? (yes/no)[no]:")
            yes = {'yes', 'y'}
            if input(">> ") not in yes:
                raise KeyboardInterrupt("Aborted! Nothing is changed.")
            
            # Clear existing and restore imported data
            self._lcdb.clear()
            for key, value in data.items():
                self._lcdb[key] = value
            Output.write("Data has been imported successfully.",
                         ColorCodes.SUCCESS)
        
        except FileNotFoundError as error:
            Output.write(error, ColorCodes.DANGER)
        except json.decoder.JSONDecodeError as error:
            Output.write(error, ColorCodes.DANGER)
        except ValueError as error:
            Output.write(error, ColorCodes.DANGER)
        except KeyboardInterrupt as error:
            Output.write(error, ColorCodes.DANGER)
