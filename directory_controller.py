import sys


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
        print(f"Success! Current directories: {dirs['list']}")
    elif sys.argv[2].lower() == 'list':
        # Show existing list of directories
        try:
            print('Listing directories...')
            print(dirs['list'])
        except KeyError as error:
            print('No saved directories found!')
    elif sys.argv[2].lower() == 'clear' and len(sys.argv) == 3:
        # Clear total list of directories
        dirs.clear()
        print('Directory list cleared!')
    elif sys.argv[2].lower() == 'clear' and len(sys.argv) > 3:
        # Delete specified directories
        try:
            mod = dirs['list'].copy()
            for name in sys.argv[3:len(sys.argv)]:
                print(f"Removing {name}...")
                mod.remove(name)
            dirs['list'] = mod.copy()
        except KeyError as error:
            print('No saved directory is found!')
        except ValueError as error:
            print('Directory is not found in list!')
        print(f"Success! Current directories: {dirs['list']}")
    else:
        print('Invalid operation!')
