# LordCommander

LordCommander is a command line program to run shell commands recursively through predefined directories.

Requirements
-----

- ^Python 3.7.5
- [Python Fire](https://github.com/google/python-fire)

You also can use it using Pipenv, a `Pipfile` is provided along with the project.

For full changelog, please see [this file](changelog.md).

Initialization
-----

Run following commands to clone the repository and 
install dependencies:

```
git clone https://sowrensen@github.com/sowrensen/lordcommander.git
cd lordcommander
pipenv install
chmod +x lc
pipenv shell
./lc <command> <args> <flags>
```

Usage
-----

### How to run commands using LordCommander?

1. Add some projects to LordCommander.
2. Set a project as active.
3. Add some instances of that project.
4. Run a command.

You can append `--help` after each command always to see the manual.

### Project Handling

#### See project list

To see added projects to LordCommander, run:

```
./lc proj view
```

The active project will be check marked.

#### Add new project

To add a new project, you have to specify the path of the project directory. *Remember, 
this is not the location of individual project, i.e. directories where the command
will run are inside this location.* Run:

```
./lc proj add /home/sowrensen/test/project-a
```

This will create the following data structure in the shelve module:

```
'project-a': {
    'root': '/home/sowrensen/test/project-a',
    'instances': []
}
```

Later in the `instances` list, you will add your project instances using `dirs add` command.

#### Set or change active project

To set or change active project, you must have at least one project. After adding
projects, run:

```
./lc proj active project-a
```

#### Remove a project

To remote a project from LordCommander, run:

```
./lc proj clear project-a
```

The program will ask for your confirmation, if you allow it will remove entire project
along with it's added instances. If a project is set as active during removal, the
`active` key will set to null and you have to set an active project for further
operations.

-----

### Directory Handling

#### See directory list

```
./lc dirs view
```

This will show all saved directory names with the index as their insertion order. To sort directory names alphabetically,
append `sort`  or `--sort` after list.

```
./lc dirs view [sort|--sort]
```

#### Adding directories

```
./lc dirs add [dir1 dir2 dir3...]
```

All the directory names after `add` keyword will be appended to the directory list.

#### Removing directories

```
./lc dirs clear [dir1 dir2 dir3...]
```

Add desired directory names after `clear` to remove them from list. However, you can also clear the entire list
of directories if you specify `--full` after `clear`.

```
./lc dirs clear --full
```

It will ask for your confirmation, if you allow, it will remove the entire list of directories.

-----

### Running Commands

Running a command throughout the saved directories is easy. Here's an example:

```
./lc run pwd
```

That's it! It will recursively run for each saved directories and show the output. 
Afterwards, you will see the number of successful and failed runs. 

> **Note:** If your command is more than one word, you have to wrap it around with 
> single or double quote. An example can be `./lc run 'git status'`. 

#### Throttled execution

Now, if you have a huge list of directories and you don't want to run the command altogether, 
you can slice them by indices (I assume that you're familiar with how array or list index works). 
If you run `./lc run --help` you will see two flags `--li` and `--ui` respectively for 
**lower index** and **upper index**. So if you decide to run a command only to first 
50 directories, you can simply specify `--li=0` and `--ui=50`. Or even simpler, 
just mention `--ui=50`, it will run throughout index 0 to index 49 anyway.

```
./lc run <command> --li=0 --ui=50
```

or,

```
./lc run <command> 0 50
```

or,

```
./lc run <command> --ui=50
```

So for running the rest? I bet you already figured that out,

```
./lc run <command> --li=50
```

or,
```
./lc run <command> 50
```

Yes, you don't have to remember or know how any items are in your list. Just tell the program to 
run it from 50 and it will start right there and won't stop until it reaches the end of the list. 

#### Exclude directory/instance from execution

To exclude one or more particular directories/instances from execution, you can specify indices with `--ex` flag. e.g.:

```
./lc run <command> --ex=3,8
```

Thus, directories in index 3 and 8 will be excluded from the list during execution.

#### Run only for specified directories

Like exclusion, you only can run a command for desired instances. Add `--inc` flag with indices for that, e.g.:

```
./lc run <command> --inc=3,8
``` 

The command will run for index 3 and 8 only. 

> **NOTE**: The `--ex` and the `--inc` flag takes precedence over `li` and `ui`. That is to say, if you use `--ex` with `li` and `ui`, indices specified will be _excluded_. And in case of `--inc`, _only for instances within the indices_ the command will run. Also, you should not use `--ex` and `--inc` together.   

-----

### Utilities 

From version 3.0, a utility class has been added to run some handy tasks. Right now there are four 
commands, more will be introduced over time.

#### Searching for a directory

Forgot if a directory name has already been included or not? Just tell the program to look for it, 
it will tell you if it is there or not.

```
./lc utils search <directory_name>
```

> **Note**: It is case sensitive, so if you have a directory named `ABC` and your search string 
> is `abc`, you will get a negative result.

#### Seeing total number of directories

If you're wondering how many saved directories do you have, just tell LordCommander to count them for you:

```
./lc utils total
```

#### Dumping and restoring data using JSON file

With version 4.0, you can dump and restore data of LordCommander. To dump existing data in the 
shelve module, run:

```
./lc utils dump /home/sowrensen
```

The third argument is the location where you want to save the file. There you will find a file named
`lcdb_dump.json`. You can use that file later to restore data into shelve module. To restore from a 
JSON file, run following command with the file path as third argument.

>**Note:** Restoring data will replace existing data. It is a good idea to dump
before you restore.

```
./lc utils restore /home/sowrensen/lcdb_dump.json
```
