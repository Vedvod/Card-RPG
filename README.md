# Card-RPG
This is my SDD HSC Major project. As of now (26th December, 2021), I am unsure of the direction that I wish to take this project in. I will likely have a greater idea of this direction as the development of generic tools progresses.

# Changelog
## Pre-Alpha: Setting up files
### 2021/12/21
- I began work on my project. I created the project repository on Github, and began planning the contents of my project.
 
### 2021/12/22
- I added the [GameAssets](https://github.com/Vedvod/Card-RPG/tree/main/Contents/GameAssets) and [Scripts](https://github.com/Vedvod/Card-RPG/tree/main/Contents/Scripts) folders to the repository, which contain all the assets and code respectively that I have made while prototyping,

### 2021/12/23
- I made some slight changes to the project hierarchy. I created a main [Contents](https://github.com/Vedvod/Card-RPG/tree/main/Contents) directory, containing both [GameAssets](https://github.com/Vedvod/Card-RPG/tree/main/Contents/GameAssets) and [Scripts](https://github.com/Vedvod/Card-RPG/tree/main/Contents/Scripts).
- Implemented function to access a shortcut's target from the `.lnk` file directly. This will enable me to move directories and still preserve functionality, by using `.lnk` files instead of the directory itself.

## Alpha 1: Level file loader
### 2021/12/25
- I implemented a file loading system, which is able to load a file written in a certain format and then load every element in the file onto the screen. This is a major milestone as every level will likely use this mechanic to load screen elements. As understanding of the requirements of the game is enhanced, this system will be altered to meet these changing requirements.
  - The operation of this system is relatively simple, with the configuration file being a list of `Element` objects written in Pythonic format. The script then runs an `eval()` on the `open()`ed contents of the given file, thus loading the list into the script. 
  - This system was tested using three [different](https://pastebin.com/EQAPkYYE) config files, and was able to load all of them.
  - This system opens the possibility of a visual level editor and custom user-made levels. The viability of each will become more clear as the game is made.
- Moved to Github Desktop to more easily manage git tracking stuff. This does not alter much about the project, it simply makes it easier to quickly upload files to Github.

### 2021/12/26
- I updated the project documentation. I mainly went over the changelog and clarified some badly-worded entries, and I changed the date format to `YYYY/MM/DD` (rather than `DD/MM/YY`) to follow [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601).

