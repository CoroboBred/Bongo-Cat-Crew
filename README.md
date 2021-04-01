# Bongo Cat Crew
An overlay program that can swap to a different assortment of cats to match the currently playing OSU! game mode.
There are 10 keyboard layouts, a mouse layout, a controller layout, and talking cat layout suitable for streams.
OSU!standard and all OSU!Mania modes are supported.

## Installation
Download the latest release shown on the right-hand side of this page.
Extract the folder somewhere convenient.

## Usage
Run the `BongoCat.exe` file to start the program.
I recommend creating a shortcut to the `BongoCat.exe` file to easily run the program from anywhere.
The program will configure the application as described in the [Configuration](#configuration) section.
The program will automatically respond to keyboard, mouse, and audio input.
Swap between different layouts by pressing `esc` + the layout's activation key.
View the list of layouts and activation keys in [Layouts](#layouts).


### Layouts 
The program supports 13 different layouts. You can swap to each layout by pressing the `esc` + the activation key. Each layout and its activation key is described in the table below.

**Layout** | **Default Activation Key** | **Cats** | **Description** |
-----------|:----------------|:---------|:----------------|
`mouse` | `-` | `2-key` , `mouse` | A special cat with a mouse. |
`controller` | `` ` ``| `1-key`, `4-button`, `1-key`, `joystick` | A set of cats that represents a controller. There are two optional one key cats that represent the bumpers, a four button cat, and a joystick cat. |
`keyboard` | `=` | 3 `4-key` | A row of 4-Key cats that responds to most keyboard input. |
`talk` | `0` | `talk` | A special talking cat that mimics audio input. |
`1-key` | `1` | `1-key` | Just a single cat with a single key. |
`2-key` | `2` | `2-key` | Just a single cat with two keys. |
`3-key` | `3` | `3-key` | Three cats with a single key each. |
`4-key` | `4` | `4-key` | A single cat with four keys. |
`5-key` | `5` | `2-key`, `1-key`, `2-key` | Three cats with two keys, one key, and two keys in that order. |
`6-key` | `6` | `4-key`, `4-key` | Two cats wth 4 keys each. I'm too lazy to make a unique layout for this. |
`7-key` | `7` | `4-key`, `1-key`, `4-key` | Three cats with four keys, one key, and four keys in that order. |
`8-key` | `8` | `4-key`, `4-key` | Two cats wth 4 keys each. |
`9-key` | `9` | `4-key`, `1-key`, `4-key` | Three cats with four keys, one key, and four keys in that order. |

The activation keys for each layout can be changed by modifying the `config.txt` file as described in [Input Configuration](#input-configuration).
By default, every layout also has a talking cat attached to it. Learn how to remove the talking in cat in [Startup Configuration](#startup-configuration).

## Configuration

### Input Configuration
The `input.txt` file contains the data for which keys on the keyboard corresponds to which keys in the program.
View the table below for a description of each key.

Every value in `input.txt` can be replaced by any keyboard character.
Regular alphanumeric characters and printable characters are represented as their single printable character.
Special characters are represented using specific keywords.
View the [keyboard](https://github.com/boppreh/keyboard/blob/master/keyboard/_winkeyboard.py#L170) to view how each special character is represented.

**Key** | **Mode** | **Character** | **Description** |
--------|:-----------|:--------------|:--------------|
key1 | Mouse | `z` | Left Key |
key2 | Mouse | `x` | Right Key |
key1 | Mania | `a` | Left Pinky Finger |
key2 | Mania | `s` | Left Index Finger |
key3 | Mania | `d` | Left Middle Finger |
key4 | Mania | `f` | Left Pointer Finger |
key5 | Mania | `space` | Thumbs |
key6 | Mania | `j` | Right Pointer Finger |
key7 | Mania | `k` | Right Middle Finger |
key8 | Mania | `l` | Right Index Finger |
key9 | Mania | `;` | Right Pinky Finger |
down_button | Controller | `page up` | Lowest Button, `X' on pro controller |
right_button | Controller | `page down` | Rightmost Button, 'A' on pro controller |
up_button | Controller | `enter` | Topmost Button, 'B' on pro controller |
left_button | Controller | `space` | Leftmost Button, 'Y' on pro controller |
stick_left | Controller | `left` | Left Joystick Movement |
stick_up | Controller | `up` | Up Joystick Movement |
stick_right | Controller | `right` | Right Joystick Movement |
stick_down | Controller | `down` | Down Joystick Movement |
left_bumper | Controller | `ctrl` | Left Bumper |
right_bumper | Controller | `end` | Right Bumper |

### Startup Configuration
The `config.txt` lists a set of options that modify how the program starts and runs.
View the table for info on each available option.

**Field** | **Description** | **Default Value** | **Possible Values** |
----------|:----------------|:------------------|:--------------------|
default_layout | The initial layout that the program will start with. This can be any layout described in [Layouts](#layouts). | `mouse` | `mouse`, `controller`, `keyboard`, `talk`, `1-key`, `2-key`, `3-key`, `4-key`, `5-key`, `6-key`, `7-key`, `8-key`, `9-key` |
enable_dynamic_layout | Whether the Layout still stay fixed to a single layout. If set  to `false` then the default layout will be the only layout available. | `true` | `true`, `false` |
enable_talking | Whether to enable the talking cat for all layouts. | `true` | `true`, `false`|
enable_bumpers | Whether to enable to bumper cats for the Controller layout. | `false` | `true`, `false` |
fps | The maximum FPS that the program will run at. Increasing this number will make some animations smoother but may increase CPU utilization.| 40 | Positive numbers |

Each field in `config.txt` can be replaced with any of the values listed under `Possible Values`.


## Custom Images
To add your own images replace the pngs in the `images` folder. Every set of cat PNGs needs to be the same size.

## Installation: The Hard way
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

## Caveats
### pyaudio
This program has only been tested on Windows. It may work on Linux or macOS but it has not been tested.

If you are installing the program the hard way on Windows you may have some difficulty installing `pyaudio`. I was able
to install `pyaudio` using [pipwin](https://stackoverflow.com/questions/52283840/i-cant-install-pyaudio-on-windows-how-to-solve-error-microsoft-visual-c-14).
