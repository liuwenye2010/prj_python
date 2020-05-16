#!usr/bin/env python
#import tkinter
from tkinter import *
from tkinter.scrolledtext import ScrolledText

def load():
    with open(filename.get()) as file: 
        contents.delete('1.0',END)
        contents.insert(INSERT,file.read())

def save(): 
    with open(filename.get(),'w') as file: 
        file.write(contents.get('1.0',END))


top = Tk()

contents = ScrolledText()
contents.pack(side=BOTTOM,expand=True, fill=BOTH)
filename = Entry()
filename.pack(side=LEFT,expand=True ,fill=X)
# label = Label(top, text='Simple Demo')
# label.pack(side=TOP)
quit = Button(top, text='Click me to quit!', command = top.quit)
quit.pack(side=BOTTOM)
button_open = Button(top, text='Open', command = load)
button_open.pack(side= LEFT)
button_save = Button(top, text='Save', command = save)
button_save.pack(side= LEFT)
top.iconbitmap('tclkit.ico')
top.title("quick_gui")
mainloop()

