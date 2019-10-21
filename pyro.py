#! python3
# pyro.py is a program which automatically run git pull for the
# defined directories. It helps you in situations like where you
# manually have to pull git commits on your several application
# instances at a time.
#
# Copyright (c) Sowren Sen

# things we need
# Shelve files (excluded from git)
#   - One to keep directory listings
#   - Another to keep credentials

# The algorithm
# -----------------
# 1. Read creds and dirs if exist
# 2. If not exist
#   a. Create two shelve files named creds and dirs
#   b. Ask for credentials first, hence directories
#   c. Go to 1
# 3. If exist,
#   a. If runs with "dirs" argument,
#       i. Append specified dirs to "dirs" file
#   b. If runs with "creds" argument,
#       i. Replace existing creds info with the given one
#   c. Else
#       i. For each directory read from dirs,
#           1. Determine current branch
#           2. Run git pull using credentials
#           3. Show if success or fail
# 4. Exit

import shelve
import os
import sys
import directory_controller
import credential_controller
import command_controller

if not os.path.exists('.files'):
    os.mkdir('.files')

creds = shelve.open('./.files/creds')
dirs = shelve.open('./.files/dirs')


def run():
    try:
        # read argument
        option = sys.argv[1]
        if option == 'dirs' and len(sys.argv) > 2:
            directory_controller.control(dirs)
        elif option == 'creds' and len(sys.argv) > 2:
            credential_controller.control(creds)
        elif option == 'run' and len(sys.argv) == 3:
            command_controller.control(sys.argv[2], dirs, creds)
        else:
            print('Invalid operation!')
    
    except IndexError as error:
        # no argument found
        print('Invalid operation!')

run()
