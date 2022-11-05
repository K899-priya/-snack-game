from tkinter import *
from random import randrange

root = Tk()
root.geometry('650x604+300+100')
root.title('Snake')

c = Canvas(root,bg='black', width=1350, height=680, highlightthickness=0)
c.pack()
c.create_text(502, 250, font='Terminal 30 bold', text="Press space to start", fill='white')

s = []
directions = [[-30,0],[0,-30],[30,0],[0,30]]
which_direction = randrange(0,4)
ap = []
run = True
score = 0
speed = 50
score_board = ''
pause_text = ''
sp = ''


def create_s_square(x, y):
    square = c.create_rectangle(x, y, x+30, y+30, fill='red', outline='white')
    s.insert(0,square)


def create_s():
    for x in range(4):
        create_s_square(x=400,y=400)


def s_move():
    iswall()
    if run:
        for part in range(len(s)-1):
            c.coords(s[part],c.coords(s[part+1]))
        c.move(s[len(s)-1],directions[which_direction][0],directions[which_direction][1])
    is_snake()
    if run:
        aple()  
        c.after(speed*3+70,s_move)


def is_snake():
    for part in range(len(s)-1):
        if c.coords(s[part]) == c.coords(s[len(s)-1]):
            game_over()


def iswall():
    if (c.coords(s[len(s)-1])[0]+directions[which_direction][0]>=1000 or \
       c.coords(s[len(s)-1])[1]+directions[which_direction][1]>=1000 or \
       c.coords(s[len(s)-1])[0]+directions[which_direction][0]<=-80 or \
       c.coords(s[len(s)-1])[1]+directions[which_direction][1]<=-80) and run:
        game_over()


def aple():
    global score
    x, y = randrange(0,600,30), randrange(0,600,30)
    if not ap:
        apple = c.create_rectangle(x+7,y+7,x+23,y+23, fill='', outline='white')
        ap.append(apple)
    ap_co = [c.coords(ap[0])[0]-7,c.coords(ap[0])[1]-7]
    if c.coords(s[len(s)-1])[:2] == ap_co:
        create_s_square(c.coords(s[0])[0],c.coords(s[0])[1])
        c.delete(ap[0])
        del ap[0]
        score += 1
        score_counter()


def score_counter():
    global score_board
    c.delete(score_board)
    score_board = c.create_text(5, 80, font='Terminal 50 bold', text=str(score), fill='light blue', anchor=W)


def game_over():
    global run
    run = False
    c.create_text(355, 200, font='Terminal 50 bold', text='GAME OVER', fill='white')
    c.create_text(502, 260, font ='Terminal 25', text="Press space to restart", fill='white')
    root.bind('<space>', restart)


def restart(_):
    global s, ap, run, which_direction, score
    root.bind('<space>', pause)
    c.delete(ALL)
    score = 0
    score_counter()
    show_speed()
    s = []
    
    ap = []
    which_direction = randrange(0,4)
    create_s()
    run = True
    s_move()


def pause(_):
    global run, pause_text
    if run == False:
        run = True
        c.delete(pause_text)
        c.after(speed*3+70,s_move)
    else:
        run = False
        pause_text = c.create_text(502, 250, font='Terminal 30 bold', text="Press <space> to resume", fill='white')


def rotate_left(_):
    global which_direction
    if run: which_direction += 1
    if which_direction == 4: which_direction = 0


def rotate_right(_):
    global which_direction
    if run: which_direction -= 1
    if which_direction == -1: which_direction = 3   


def show_speed():
    global sp
    c.delete(sp)
    sp = c.create_text(10, 585, font='TimesNewRoman 10', text=f'speed: {100-speed}', fill='white', anchor=W)


def increase_speed(_):
    global speed
    if speed > 0:
        speed -= 1
        show_speed()

def decrease_speed(_):
    global speed
    if speed < 100:
        speed += 1
        show_speed()


def start(_):
    global score_board
    root.bind('<space>', pause)
    root.bind('k',decrease_speed)
    root.bind('l',increase_speed)
    c.delete(ALL)
    score_counter()
    show_speed()
    root.bind('a',rotate_right)
    root.bind('d',rotate_left)
    create_s()
    s_move()

root.bind('<space>',start)

root.mainloop()
