#!/usr/bin/env python3

from os.path import basename, splitext
import tkinter as tk
from tkinter import Scale, Label, Entry, Frame, HORIZONTAL, LEFT, S


# from tkinter import ttk


class Application(tk.Tk):
    name = "ColorMishMash"

    def __init__(self):
        super().__init__(className=self.name)

        self.title(self.name)
        self.bind("<Escape>", self.quit)
        self.lblHlavni = tk.Label(self, text="ColoMishMash")
        self.lblHlavni.pack()

        self.btnQuit = tk.Button(self, text="Quit", command=self.quit)
        self.btnQuit.pack()

        self.varR = tk.IntVar()
        self.varG = tk.IntVar()
        self.varB = tk.IntVar()
        self.varR.trace('w', self.color_change)
        self.varG.trace('w', self.color_change)
        self.varB.trace('w', self.color_change)

        self.frameR = Frame(self)
        self.frameG = Frame(self)
        self.frameB = Frame(self)
        self.frameR.pack()
        self.frameG.pack()
        self.frameB.pack()

        # R složka
        self.lblR = Label(self.frameR, text="R", fg="#ff0000")
        self.lblR.pack(side=LEFT, anchor=S)
        self.scaleR = Scale(
            self.frameR,
            from_=0,
            to=0xFF,
            orient=HORIZONTAL,
            length=333,
            variable=self.varR,
        )
        self.scaleR.pack(side=LEFT, anchor=S)
        self.entryR = Entry(self.frameR, width=4, textvariable=self.varR)
        self.entryR.pack(side=LEFT, anchor=S)
        
        self.entryR.bind('<Key>', self.update)
        


        # G složka
        self.lblG = Label(self.frameG, text="G", fg="#00ff00")
        self.lblG.pack(side=LEFT, anchor=S)
        self.scaleG = Scale(
            self.frameG,
            from_=0,
            to=0xFF,
            orient=HORIZONTAL,
            length=333,
            variable=self.varG,
        )
        self.scaleG.pack(side=LEFT, anchor=S)
        self.entryG = Entry(self.frameG, width=4, textvariable=self.varG)
        self.entryG.pack(side='left', anchor='s')
        # B složka
        self.lblB = Label(self.frameB, text="B", fg="#0000ff")
        self.lblB.pack(side=LEFT, anchor=S)
        self.scaleB = Scale(
            self.frameB,
            from_=0,
            to=0xFF,
            orient=HORIZONTAL,
            length=333,
            variable=self.varB,
        )
        self.scaleB.pack(side=LEFT, anchor=S)
        self.entryB = Entry(self.frameB, width=4, textvariable=self.varB)
        self.entryB.pack(side=LEFT, anchor=S)

        self.canvasMain = tk.Canvas(self, width=300, height=200, bg="#123456")
        self.canvasMain.pack()
        self.canvasMain.bind('<Button-1>', self.clickHandler)
        
        self.entryHex = tk.Entry(self, width=8)
        self.entryHex.pack(anchor='e')

        self.frameMem = Frame(self)
        self.frameMem.pack()
        self.canvasMem = []
        for row in range(3):
            for column in range(7):
                canvas = tk.Canvas(self.frameMem, width=50, height=50, bg='#654321')
                canvas.grid(row=row, column=column)
                canvas.bind('<Button-1>', self.clickHandler)
                self.canvasMem.append(canvas)


    def clickHandler(self, event):
        if self.cget('cursor') != 'pencil':      # kliknu poprve
            self.config(cursor='pencil')
            self.color = event.widget.cget('bg')
        else:                                    # kliknu podruhe
            self.config(cursor='')
            if event.widget is self.canvasMain:
                self.canvasColor2Slids()
            event.widget.config(bg=self.color)

    def canvasColor2Slids(self):
        print(self.color)
        r = int( self.color[1:3] , 16)
        g = int( self.color[3:5] , 16)
        b = int( self.color[5:] , 16)
        self.varR.set(r)
        self.varG.set(g)
        self.varB.set(b)

    def color_change(self, var=None, index=None, mode=None):
        print(var, index, mode)
        r = self.varR.get()
        g = self.varG.get()
        b = self.varB.get()
        colorstring = f"#{r:02X}{g:02X}{b:02X}"
        print(colorstring)
        self.canvasMain.config(bg=colorstring)

        self.entryHex.delete(0, 'end')
        self.entryHex.insert(0, colorstring)

    def colorSave(self):
        with open("colors.txt", "w") as f:
            f.write(self.canvasMain.cget("background") + "\n")
            for canvas in self.canvasMem:
                f.write(canvas.cget("background") + "\n")

    def quit(self, event=None):
        self.colorSave()
        super().quit()

    def update(self, event=None):
        print(event.keycode, event.keysym, event.x, event.y)


app = Application()
app.mainloop()
