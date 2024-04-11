from tkinter import *
import time
from random import randint
from tkinter import ttk
import subprocess
import keyboard
window=Tk()
window.title('Maze')

window.geometry("1600x1000")

filename=PhotoImage(file=r"C:\IN104 Project\Untitled design.png")
filename1=PhotoImage(file=r"C:\IN104 Project\winn.png")
des=PhotoImage(file=r"C:\IN104 Project\label.png")
def clock(label1,label2):
    hour = time.strftime("%I")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    day = time.strftime("%A")
    am_pm = time.strftime("%p")

    label1.config(text=hour + ":" + minute + ":" + second + " " + am_pm)
    label1.after(1000,clock,label1,label2)

    label2.config(text=day)
# frontpage
def frontpage():
    #the game
    def pagegames():
        label1.destroy()
        label2.destroy()
        start.destroy()
        close.destroy()
        #return to frontpage
        def back():
            returns.destroy()
            frontpage()
        #win the game
        #read matrix
        def read_matrix(file_path):
            matrix = []
            with open(file_path, 'r') as file:
                for line in file:
                    row = [num for num in line.strip().split()]
                    matrix.append(row)
            return matrix

        cell_size = 12 #pixels
        global n,m,roow,cool
        roow=0
        cool=0
        n=0
        m=0

        #get the row
        def get_row():
            global n,m,roow,cool
            n=int(combos.get())
            roow+=1
            if (roow>0 and cool>0):
                games()
        #get the column
        def get_column():
            global n,m,roow,cool
            m=int(combo.get())
            cool+=1
            if (roow>0 and cool>0):
                games()
            
        combo=ttk.Combobox(window,font = ("Helvetica",20))
        combos=ttk.Combobox(window,font = ("Helvetica",20))
        lol=[]
        lols=[]
        for num in range(2, 36):
            lol.append(num)
        for num in range(2, 52):
            lols.append(num)
        combos["values"]=lol
        combos.set(20)
        combos.place(x = 1300, y = 550,width = 200)
        butt = Button(window,image=des,borderwidth=0, text='Rows', command=get_row)
        butt.place(x = 1350,y = 590)
        combo["values"]=lols
        combo.set(28)
        combo.place(x = 1300, y = 630,width = 200)
        butts = Button(window,borderwidth=0, text='Columns', command=get_column)
        butts.place(x = 1350,y = 670)

        returns = Button(window,text = "return",font = ("Helvetica",20),command = back,width = 20,fg="blue",bg="black")
        returns.place(x = 1300 , y = 700, width=200)
        def games():
            global n,m
            subprocess.call(["gcc", r"C:\IN104 Project\programme\main.c"])
            subprocess.call(["a.exe", str(n), str(m)])
            n = 2 * n + 1
            m = 2 * m + 1
            def win():
                returns.destroy()
                ffs.destroy()
                #return to the frontpage
                def backs():
                    bg1.destroy()
                    returnss.destroy()
                    frontpage()
                bg1=Label(window,image=filename1)
                bg1.place(x=0,y=0,relwidth=1,relheight=1)
                returnss = Button(window,text = "return",font = ("Helvetica",20),command = back,width = 20,fg="blue",bg="black")
                returnss.place(x = 650 , y = 603, width=200)
            file_path = "laby.txt"
            map= read_matrix(file_path)
            #create labyrinth
            def create():
                "Create a rectangle with draw function (below) with random color"
                for row in range(n):
                    for col in range(m):
                        if map[row][col] == 'P':
                            color = 'White'
                            draw(row, col, color)
                        elif map[row][col] == 'W':
                            color = 'black'
                            draw(row, col, color)
             
            #draw the current cell
            def draw(row, col, color):
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                ffs.create_rectangle(x1, y1, x2, y2, fill=color)
             
             

             
            #StartingPoint
             
            # starting color of row
            scr = randint(1, n-1)
            # starting random column
            scc = randint(1, m-1)
            while(map[scr][scc]=='W'):
                scr = randint(1, n-1)
                scc = randint(1, m-1)
            start_color = 'Green'
            # memorize row and column of the starting rectangle
            # current color row and current color column
            
            canvas_width = m*cell_size
            canvas_height = n*cell_size
            ffs = Canvas(window, width = canvas_width, height = canvas_height, bg = 'grey')
            ffs.place(x = 0,y = 0)
             
            global x,y,tari,tarj
            create()
            y = scr * cell_size 
            x = scc * cell_size
            draw(scr, scc, start_color)
            # ending color of row
            ccr = randint(1, n - 1)
            # ending random column
            ccc = randint(1, m - 1)
            while(map[ccr][ccc] == 'W' or(ccc==scc and ccr==scr)):
                ccr = randint(1, n - 1)
                ccc = randint(1, m - 1)
            end_color = 'red'
            # memorize row and column of the ending rectangle
            # current color row and current color column
            draw(ccr, ccc, end_color)
            # print(revisited_cells)
            tari = ccr * cell_size
            tarj = ccc * cell_size
             
             
            #draw new position
            def draw_rect():
                ffs.create_rectangle((x, y, x + cell_size, y + cell_size), fill="green")
            #remove old position
            def del_rect():
                ffs.create_rectangle((x, y, x + cell_size, y + cell_size), fill="white")
            #read the movements
            def move(event):
                global x, y
                # print(event.char)
                del_rect()
                col = w = x//cell_size
                row = h = y//cell_size
                if keyboard.is_pressed("left arrow"):
                    if map[row][col - 1] == "P":
                        x -= cell_size
                elif keyboard.is_pressed("right arrow"):
                    if map[row][col + 1] == "P":
                        x += cell_size
                elif keyboard.is_pressed("up arrow"):
                    if map[row - 1][col] == "P":
                        y -= cell_size
                elif keyboard.is_pressed("down arrow"):
                    if map[row + 1][col] == "P":
                        y += cell_size
             
                draw_rect()
                col = w = x//cell_size
                row = h = y//cell_size
                if (x==tarj and y==tari):
                    win()
                    
             
            window.bind("<Key>", move)

    bg=Label(window,image=filename)
    bg.place(x=0,y=0,relwidth=1,relheight=1)
    
    label1=Label(window,text="",font = ("Helvetica",60),fg="blue",bg="black")
    label1.place(x=450,y=50,width=600)

    label2=Label(window,text="",font = ("Helvetica",30),fg="red",bg="black")
    label2.place(x=620,y=128,width=250)
    
    clock(label1,label2)
    
    start = Button(window,borderwidth=0,image=des,text = "start",font = "Times 20 bold",command = pagegames)
    start.place(x=600,y=250)
    
    close = Button(window,text="close",font = ("Helvetica",20),command = lambda: window.destroy(),width=20,fg="blue",bg="black")
    close.place(x=600,y=317,width = 300)
    
    
window.overrideredirect(True)  # Hide the title bar
frontpage()
window.mainloop()
