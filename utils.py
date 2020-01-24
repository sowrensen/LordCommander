"""
| ---------------------------------------------------------------------
| utils.py
| ---------------------------------------------------------------------
| This utils module holds some of the necessary functions that may
| require over time to time.
|
| Version: 3.0
| License: GNU General Public License 3
"""

from output import Output
from color_codes import ColorCodes


class Utils:
    """
    Some utilities that may come handy.
    """
    
    def __init__(self, dirs):
        self._dirs = dirs
    
    def search(self, key):
        """
        Search for a directory.
        :param key: Name of the directory to search
        :return: Name of the directory
        """
        return Output.write('Found!', ColorCodes.SUCCESS) if key in self._dirs['list'] else Output.write('Not found!',
                                                                                                         ColorCodes.DANGER)
    
    def total(self):
        """
        View total number of saved directories.
        :return: Number of directories.
        """
        return Output.write("Total %d directories listed." % len(self._dirs['list']), ColorCodes.INFO)
