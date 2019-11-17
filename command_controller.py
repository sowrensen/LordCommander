import os
from colr import color
import colors


def control(cmd: str, dirs, creds) -> None:
    """Execute specified shell command for each of the saved directory.
    :param cmd: str
    :param dirs: Any
    :param creds: Any
    :return: None
    """
    try:
        directories = dirs['list'].copy()
        # Sort directories alphabetically
        directories.sort()
        for directory in directories:
            if os.path.exists(f"../{directory}"):
                try:
                    print("\n\n")
                    print(
                        color("Changed directory to", fore=colors.INFO),
                        color(f"'{os.path.realpath('../' + directory)}'", fore=colors.WARNING),
                        color("and running", fore=colors.INFO),
                        color(f"'{cmd}'", fore=colors.WARNING)
                    )
                    os.chdir(f"../{directory}")
                    os.system(cmd)
                except OSError as error:
                    print(color(error, fore=colors.DANGER))
                finally:
                    os.chdir('../lordcommander')
    except KeyError as error:
        print('No saved directory is found!')
