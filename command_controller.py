import os


def control(cmd: str, dirs, creds) -> None:
    """Execute specified shell command for each of the saved directory.
    :param cmd: str
    :param dirs: Any
    :param creds: Any
    :return: None
    """
    try:
        directories = dirs['list'].copy()
        for directory in directories:
            if os.path.exists(f"../{directory}"):
                try:
                    print(f"Changed directory to {os.path.realpath('../' + directory)} and running '{cmd}'")
                    os.chdir(f"../{directory}")
                    os.system(cmd)
                except OSError as error:
                    print(error)
                finally:
                    os.chdir('../lordcommander')
    except KeyError as error:
        print('No saved directory is found!')
