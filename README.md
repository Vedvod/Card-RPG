﻿# Card-RPG
This is my SDD HSC Major project. As of now (26th December, 2021), I am unsure of the direction that I wish to take this project in. I will likely have a greater idea of this direction as the development of generic tools progresses.

# Changelog
## Pre-Alpha: Setting up files
### 2021/12/21
- I began work on my project. I created the project repository on Github, and began planning the contents of my project.
 
### 2021/12/22
- I added the [GameAssets](https://github.com/Vedvod/Card-RPG/tree/main/Contents/GameAssets) and [Scripts](https://github.com/Vedvod/Card-RPG/tree/main/Contents/Scripts) folders to the repository, which contain all the assets and code respectively that I have made while prototyping,

### 2021/12/23
- I made some slight changes to the project hierarchy. I created a main [Contents](https://github.com/Vedvod/Card-RPG/tree/main/Contents) directory, containing both [GameAssets](https://github.com/Vedvod/Card-RPG/tree/main/Contents/GameAssets) and [Scripts](https://github.com/Vedvod/Card-RPG/tree/main/Contents/Scripts).
- Made and implemented a function to access a shortcut's target from the `.lnk` file directly. This will enable me to move directories and still preserve functionality, by using `.lnk` files instead of the directory itself.
	- The function uses the 'read binary' functionality of `open()` and linearly searches until it finds the beginning and end of the target file path, saving the string found between these two.

## Alpha 1: Level file loader
### 2021/12/25
- I implemented a file loading system, which is able to load a file written in a certain format and then load every element in the file onto the screen. This is a major milestone as every level will likely use this mechanic to load screen elements. As understanding of the requirements of the game is enhanced, this system will be altered to meet these changing requirements.
  - The operation of this system is relatively simple, with the configuration file being a list of `Element` objects written in Pythonic format. The script then runs an `eval()` on the `open()`ed contents of the given file, thus loading the list into the script. 
  - This system was tested using three [different](https://pastebin.com/EQAPkYYE) config files, and was able to load all of them.
  - This system opens the possibility of a visual level editor and custom user-made levels. The viability of each will become more clear as the game is made.
- Moved to Github Desktop to more easily manage git tracking stuff. This does not alter much about the project, it simply makes it easier to quickly upload files to Github.

### 2021/12/26
- I updated the project documentation. I mainly went over the changelog and clarified some badly-worded entries, and I changed the date format to `YYYY/MM/DD` (rather than `DD/MM/YY`) to follow [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601).

### 2022/01/31
Though not directly related to this project, I have made several concepts that may be used in the game.
- Firstly, I made a ~gambling~

### 2022/02/02
- I revised some incomplete scripts, such as a button concept, which will likely be used as the basis of the GUI menus.
- I updated some commenting on the [classes and functions script](https://github.com/Vedvod/Card-RPG/tree/main/Contents/Scripts/PyGameTemplate.py), and added in a `Timer` class, which can track the time since its creation, and be reset to a new start time
  - This class will likely be used to set the activation cooldown of `Button()`, preventing rapid feedback from a single click.
- I started work on a new version of the `Player(Element)` class, which will utilise the updated set of `Element` class functions and allow the user to move around.