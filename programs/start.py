import turtle

def draw_star():
    t = turtle.Turtle()
    t.speed(5)
    t.color("blue")
    t.pensize(3)

    for i in range(5):
        t.forward(150)
        t.right(144)

    turtle.done()

draw_star()
