import sys
from colr import color
import colors2 as colors


def control(dirs) -> None:
    """Controls all operations regarding directory.
    :param dirs: Any
    :return: None
    """
    if sys.argv[2].lower() == 'add' and len(sys.argv) > 3:
        # Create new list of directories or append with the existing
        directories = sys.argv[3:len(sys.argv)]
        try:
            dirs['list'] += list(directories)
        except KeyError as error:
            dirs['list'] = directories.copy()
        print(color(f"Success! Current directories: {dirs['list']}", fore=colors.SUCCESS))
    elif sys.argv[2].lower() == 'list':
        # Show existing list of directories
        try:
            print(color('Listing directories...', fore=colors.INFO))
            dirs = dirs['list'].copy()
            
            if len(sys.argv) > 3 and sys.argv[3].lower() == 'alpha':
                dirs.sort()
            
            for dir in dirs:
                print(f"{dir}")
        except KeyError as error:
            print(color('No saved directories found!', fore=colors.DANGER))
    elif sys.argv[2].lower() == 'clear' and len(sys.argv) == 3:
        # Clear total list of directories
        dirs.clear()
        print(color('Directory list cleared!', fore=colors.SUCCESS))
    elif sys.argv[2].lower() == 'clear' and len(sys.argv) > 3:
        # Delete specified directories
        try:
            mod = dirs['list'].copy()
            for name in sys.argv[3:len(sys.argv)]:
                print(color(f"Removing {name}...", fore=colors.WARNING))
                mod.remove(name)
            dirs['list'] = mod.copy()
            print(color(f"Success! Current directories: {dirs['list']}", fore=colors.SUCCESS))
        except KeyError as error:
            print(color('No saved directory is found!', fore=colors.DANGER))
        except ValueError as error:
            print(color('Directory is not found in list!', fore=colors.DANGER))
    else:
        print(color('Invalid operation!', fore=colors.DANGER))
