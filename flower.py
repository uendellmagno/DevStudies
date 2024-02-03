from random import random
from turtle import *


def settings():
    window = Screen()
    window.bgcolor('black')
    window.title('My First Drawing')
    colors = ['red', 'green', 'blue', 'white']
    speed(0)

    return window, colors


def flower():
    window, colors = settings()
    for _ in range(36):
        for c0 in colors:
            color(c0)
            fd(200)
            lt(190)
            fd(200)
        lt(360 // len(colors))
    hideturtle()
    print('flower of flowers')
    pass


def startpoint():
    for i in range(50):
        for c in settings.colors:
            color(c)
            steps = (random() * 100)
            angle = (random() * 360)
            fd(steps)
            rt(angle)
            print(pos())

    home()


def on_click(x, y):
    settings.window.clearscreen()
    flower()


settings.window, settings.colors = settings()
startpoint()
settings.window.onclick(on_click)

mainloop()
done()