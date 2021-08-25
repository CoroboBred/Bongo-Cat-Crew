# test script to get input from your mouse.
# The text output for each keypress must match text in the input file.
# The program will exit once "esc" is pressed.
import keyboard
import mouse


def mouse_event(e):
    print(e)


def main():
    mouse.hook(mouse_event)
    keyboard.wait("esc")


if __name__ == '__main__':
    main()