# python-trr
Python-trr is an terminal app for typing practice. It is written in Python with one of its standard libraries - Curses, which means no additional packages are required to run this app as long as you have python3 installed in your environment. Python-trr is inspired by ( or a remake of ) [emacs-trr](https://github.com/kawabata/emacs-trr) on GNU Emacs.

## What does it do?
<img src="https://github.com/kaiwinut/python-trr/blob/main/docs/sample.gif" alt="sample video of python-trr" width="500"/>

The current version of python-trr ( as in Dec 2021 ) supports the following features:

- [x] Has a stable graphics interface in a standard 80 x 24 terminal window
- [x] Highlights correct / incorrect inputs
- [x] Shows time, error rate, kpm ( keystrokes per minute ) in real-time
- [x] Stores results and histories in local files
- [x] Presents recent game results in scatter plot style
- [x] Provides a settings menu ( accessible with the TAB key ) for user settings

## Usage
First, install python-trr with pip. 

`pip install pythontrr`

Then, from the terminal, simply run

`python3 -m pythontrr`

and start typing!

## Configuration

#### Via settings menu
Press TAB during the game to pause and enter settings mode. There are currently 5 settings and several options for users to choose from. Here are some keys you will find useful:

`Up / Down arrow key`

Navigate through different settings

`Left / Right arrow key`

Navigate through different options

`TAB`

Save changes and let the game resume

`ESC`

**Save your changes beforehand, otherwise your current game status and changes to settings will be lost**. 

Press ESC to exit the game. After restarting the game, you will find the new settings applied.

---

#### Via connfiguration file ( not recommended )
In `config.py` you can tweak the configuration as you like. Here are some tips:

`READ_RESULT_FROM_HISTORY`, `READ_HISTORY`

If set to True, then the program will look for the stored history in your local files. If there is not one, it will be created. If set to False, it erases all existing histories stored in the file and overwrites them.

`HISTORY_ENTRIES`

Specifies how many entries will be shown in the History block. The maximum is 3.

`WORD_COUNT`

Specifies how many words ( or in fact keystrokes ) will be shown in the Text block. The maximum is 350.

## References
Sample texts are scraped from [Project Gutenberg's Website](https://www.gutenberg.org/).