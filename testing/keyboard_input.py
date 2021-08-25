# test script to get input from your keyboard.
# The text output for each keypress must match text in the input file.
# The program will exit once "esc" is pressed.
import keyboard


def keyboard_event(e):
    if e.event_type == "down":
        print(e.name)


def mouse_event(e):
    print(e)


def main():
    keyboard.hook(keyboard_event)
    keyboard.wait("esc")


if __name__ == '__main__':
    main()
