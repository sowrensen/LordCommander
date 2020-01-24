"""
| ---------------------------------------------------------------------
| output.py
| ---------------------------------------------------------------------
| This module provides a fancy way to show output, errors, warnings,
| or info on CLI.
|
| Version: 3.0
| License: GNU General Public License 3
"""

from color_codes import ColorCodes
from colr import color


class Output:
    """Handles all output messages and formats them according to specified color code."""
    
    @staticmethod
    def write(message, code=ColorCodes.NORMAL):
        """
        Shows message according to color code in terminal. If message has several parts,
        you can pass a list of dictionaries as {text: 'Message', code: 'ffffff'} format.
        :param message: str | list
        :param code: str
        :return: None
        """
        if isinstance(message, list):
            for segment in message:
                print(color(f"{segment['text']}", fore=segment['code']), end=' ')
            print('\n')
            return
        
        print(color(f"{message}", fore=code))
