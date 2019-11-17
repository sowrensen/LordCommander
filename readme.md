# LordCommander

LordCommander is a command line program to run a shell command recursively through predefined
directories.

## Changelog

#### Version 1.1
- Added alphabetical sorting for directory list.
- Added colored output to distinguish between errors, infos, warnings, and success messages.
- Polished and more clear output.

## Running

```
git clone https://sowrensen@github.com/sowrensen/lordcommander.git
cd lordcommander
chmod +x lc.py
./lc <key> <value>
```

## Usage

### Directory Controller

#### See directory list

```
./lc dirs list
```

This will show all saved directory names as there insertion order. To sort directory names alphabetically,
append `alpha` after list.

```
./lc dirs list alpha
```

#### Adding directories

```
./lc dirs add dir1, dir2, dir3...
```

All the directory names after `add` keyword will be appended to the directory list.

#### Removing directories

```
./lc dirs clear <directory_name>
```

Add desired directory name to remove it from list after `clear`. However, you can also clear entire list
of directories if you do not specify any name.

```
./lc dirs clear
```

The above command will remove the entire list of directories.
<hr>

**Note:** Usage documentation is unfinished yet. You can safely use Directory Controller though.
