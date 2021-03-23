# Bongo Cat Crew
A program that dynamically displays a different assortment of cats to match the currently playing OSU! game mode.
OSU!standard and all OSU!Mania modes are supported. The program includes a talking cat which mimics your audio.

# Installation
Download the latest release.
Extract the folder somewhere convenient.
Run the `BongoCat.exe` file in the extracted folder.

# Installation: The Hard way
Download the repo and run the program using `python3`. The list of python dependencies include:
* sys
* keyboard
* pyqt5
* pyautogui
* pyaudio
* array
* os
* random

All of these packages can be installed using `pip3`.
Once installed, you can run the script from the terminal with a simple `python3 main.py`.


# Configuration
There are currently 11 supported layouts which can be set by the top row of the keyboard. The numbers `0` to `9` sets the
layout to a set of cats which controls that many number of keys. The `-` symbol displays a unique layout that displays
a two key cat with a cat that controls a mouse. In addition, every layout also displays a talking cat which plays a
talking animation to mimic talking when it detects audio input.

To change which keys activate the cats, modify the config.txt file.

# Caveats
This program has only been tested on Windows. It may work on Linux or MacOS but it has not been tested.

If you are installing the program the hard way on Windows you may have some difficulty installing `pyaudio`. I was able
to install `pyaudio` using [pipwin](https://stackoverflow.com/questions/52283840/i-cant-install-pyaudio-on-windows-how-to-solve-error-microsoft-visual-c-14).
