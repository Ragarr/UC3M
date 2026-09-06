import turtle

speed = "fastest"
bg_color = "dark grey"
pen_color = "white"
screen_width = 1500
screen_height = 900
drawing_width= 1400
drawing_height = 800
pen_width = 1
fractal_depth = 10


def drawline(tur, pos1, pos2):
    tur.penup()
    tur.goto(pos1[0], pos1[1])
    tur.pendown()
    tur.goto(pos2[0], pos2[1])


def recursivedraw(tur, x, y, width, height, count):
    drawline(
        tur,
        [x + width * 0.25, height // 2 + y],
        [x + width * 0.75, height // 2 + y],
    )
    drawline(
        tur,
        [x + width * 0.25, (height * 0.5) // 2 + y],
        [x + width * 0.25, (height * 1.5) // 2 + y],
    )
    drawline(
        tur,
        [x + width * 0.75, (height * 0.5) // 2 + y],
        [x + width * 0.75, (height * 1.5) // 2 + y],
    )

    if count <= 0:  # The base case
        return
    else:  # The recursive step
        count -= 1
        
        recursivedraw(tur, x, y, width // 2, height // 2, count)
     
        recursivedraw(tur, x + width // 2, y, width // 2, height // 2, count)
       
        recursivedraw(tur, x, y + width // 2, width // 2, height // 2, count)
        
        recursivedraw(tur, x + width // 2, y + width // 2, width // 2, height // 2, count)


if __name__ == "__main__":
    
    screenset = turtle.Screen()
    screenset.setup(screen_width, screen_height)
    screenset.bgcolor(bg_color)

  
    artistpen = turtle.Turtle()
    artistpen.hideturtle()
    artistpen.pensize(pen_width)
    artistpen.color(pen_color)
    artistpen.speed(speed)

   
    recursivedraw(artistpen, - drawing_width / 2, - drawing_height / 2, drawing_width, drawing_height, fractal_depth)


    turtle.done()
