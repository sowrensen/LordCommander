"""
| ---------------------------------------------------------------------
| lc.py
| ---------------------------------------------------------------------
| LordCommander (hence, lc) is a python program to run a shell
| command recursively through predefined directories.
|
| Version: 4.0
| License: GNU General Public License 3
"""

import os
import shelve
from utils import Utils
from output import Output
from color_codes import ColorCodes
from lcex import ActiveProjectNotSetException
from controllers import DirectoryController, CommandController, ProjectController


class LordCommander:
    """
    🐈 Run shell commands recursively throughout the predefined directories.
    """
    
    def __init__(self):
        try:
            self._lcdb = self._read_data()
            self._active = self._find_active()
            self.proj = ProjectController(self._lcdb)
            self.utils = Utils(self._lcdb, self._active)
            self.dirs = DirectoryController(self._active['instances'] if 'instances' in self._active else None)
        except IOError as error:
            Output.write(error)
    
    def __del__(self):
        # Close the shelve module
        self._lcdb.close()
    
    def _read_data(self):
        """
        Load the shelve module and create expected structure if necessary.
        :return: shelve
        """
        if not os.path.exists('.files'):
            os.mkdir('.files')
        
        # Setting writeback mode to True to persist changes.
        lcdb = shelve.open('.files/lcdb', writeback=True)
        if not all(key in lcdb.keys() for key in ['active', 'projects']):
            lcdb['active'] = ''
            lcdb['projects'] = {}
        
        return lcdb
    
    def _find_active(self):
        """
        Get the active project
        :return: dict
        """
        return self._lcdb['projects'][self._lcdb['active']] if self._lcdb['active'] != '' else {}
    
    def run(self, command, li=0, ui=None):
        """
        Run a command.
        :param command: The command to run
        :param li: Lower index (optional)
        :param ui: Upper index (optional)
        """
        try:
            if not self._active:
                raise ActiveProjectNotSetException(
                    "May be no active project has been set. Please check.")
            cc = CommandController()
            cc.run(self._active, command, li, ui)
        except ActiveProjectNotSetException as error:
            Output.write(error, ColorCodes.DANGER)
