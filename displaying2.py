from tkinter import *
from tkinter.ttk import *
import Pmw
import os, sys
from platform import system as platform


class DisplayingText():
    def __init__(self, root, canvas):
        self.canvas = canvas
        self.balloon = Pmw.Balloon(root)
    
    def drawText(self, sample_name, i, width, height):
        """ writes the sample number on canvas """
        item = self.canvas.create_text(width, height, font=("Purisa", 10), text=str(i+1))
        self.balloon.tagbind(self.canvas, item, sample_name)
        
    def drawHeight(self, coords, sample_name):
        """ draws a green bar """
        item = self.canvas.create_rectangle(coords, fill='forestgreen', tags=('renew', sample_name))
        self.balloon.tagbind(self.canvas, item, sample_name)
        
    def drawCircle(self, coords, sample_name, colour):
        """ creates an oval """
        item = self.canvas.create_oval(coords, width=3, outline=colour)
        self.balloon.tagbind(self.canvas, item, sample_name)
        

    