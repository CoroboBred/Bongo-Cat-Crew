import pygame

pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 700))
screen.fill(pygame.Color('white'))
pygame.display.flip()
while True:
    for i in range(pygame.joystick.get_count()):
        js = pygame.joystick.Joystick(i)
        js.init()
        for j in range(js.get_numaxes()):
            axis = js.get_axis(j)
            print(axis)
    clock.tick(20)