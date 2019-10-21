import sys


def control(creds) -> None:
    """Controls all operations regarding credentials.
    :param creds: Any
    :return: None
    """
    if sys.argv[2].lower() == 'add':
        # Append new keyword: key
        try:
            # Check if a key is already exists
            if sys.argv[3].lower() in creds:
                print(f"Error! Key already exists. Run 'creds clear {sys.argv[3].lower()}' first.")
                # TODO: check if user wants to replace it
                return
            creds[sys.argv[3].lower()] = sys.argv[4]
            print(f"Success! {sys.argv[3].lower()}: {creds[sys.argv[3]].lower()} saved.")
        except IndexError as error:
            print('Please provide as <keyword> <key> pair.')
    elif sys.argv[2].lower() == 'list':
        # Show existing list of keys
        if len(creds.keys()) <= 0:
            print('No saved keys found!')
            return
        print('Listing credentials...')
        for key in creds:
            print(f"{key} => {creds[key]}")
    elif sys.argv[2].lower() == 'clear' and len(sys.argv) == 3:
        # Clear total list of keys
        creds.clear()
        print('Credential list cleared!')
    elif sys.argv[2].lower() == 'clear' and len(sys.argv) == 4:
        # Delete specified key
        try:
            del creds[sys.argv[3].lower()]
            print(f"Success! Removed {sys.argv[3]} from key list.")
        except KeyError as error:
            print('Key is not found in the list!')
    else:
        print('Invalid operation!')
