from tkinter import *
import os, sys
import pickle
import subprocess
import numpy as np

from tkinter.filedialog import asksaveasfilename


def DumpParsed(file, what):
    """ saves (dump/pickle) 'what' to 'file' """
    fid = open(file, 'wb')
    pickle.dump(what, fid, protocol=pickle.HIGHEST_PROTOCOL)
    fid.close()

def UnDumpParsed(file, what):
    """ saves (undump/unpickle) file to what """
    try:
        fid = open(file, 'rb')
        tmpdict = pickle.load(fid)
        what.update(tmpdict)
        del(tmpdict)
    except ModuleNotFoundError:
        pass

def save_canvas_as_pdf(canvas, width=500, height=500):
    """ saves canvas as pdf """
    filename = asksaveasfilename()
    if filename is None: 
        return
    canvas.postscript(file=filename+'.ps', width=width, height=height)
    process = subprocess.call(["ps2pdf", filename+".ps", filename])
    os.remove(filename+'.ps')

def getColor(index, colors):
    """ returns the colour at the position of an array which contains colours """
    return colors[index%len(colors)]
    
def inverse(pattern):
    """ gets the inverse pattern of a pattern """
    new_pattern = ''
    for item in pattern:
        if item == '0':
            new_pattern += '1'
        elif item == '1':
            new_pattern += '0'
        else:
            new_pattern += item
    return new_pattern

def create_canvas(frame, row=0, col=0, height=400, width=800, yscroll=True, xscroll=True, colspan=1, rowspan=1, take_focus=False):
    """ creates a canvas """
    if xscroll and yscroll:
        xscrollbar = Scrollbar(frame, 
                                orient=HORIZONTAL)
        xscrollbar.grid(row=row+1+rowspan, column=col, sticky='NE'+'NW', columnspan=colspan)
        yscrollbar = Scrollbar(frame, 
                                orient=VERTICAL)
        yscrollbar.grid(row=row, column=col+colspan, sticky='NW'+'SW', rowspan=rowspan)
        canvas = Canvas(frame, 
                        bd=0,
                        xscrollcommand=xscrollbar.set, 
                        yscrollcommand=yscrollbar.set,
                        scrollregion=(0,
                                    0,
                                    width,
                                    height),
                        height=height, 
                        width=width)
        yscrollbar.config(command=canvas.yview)
        xscrollbar.config(command=canvas.xview)
    elif xscroll:
        xscrollbar = Scrollbar(frame, 
                                orient=HORIZONTAL)
        xscrollbar.grid(row=row+1+rowspan, column=col, sticky='NE'+'NW', columnspan=colspan)
        canvas = Canvas(frame, 
                        bd=0,
                        xscrollcommand=xscrollbar.set, 
                        scrollregion=(0,
                                    0,
                                    width,
                                    height),
                        height=height, 
                        width=width)
        xscrollbar.config(command=canvas.xview)
    elif yscroll:
        yscrollbar = Scrollbar(frame, 
                                orient=VERTICAL)
        yscrollbar.grid(row=row, column=col+colspan, sticky='NW'+'SW', rowspan=rowspan)
        canvas = Canvas(frame, 
                            bd=0,
                            yscrollcommand=yscrollbar.set)
        yscrollbar.config(command=canvas.yview)
    else:
        canvas = Canvas(frame, 
                        bd=0,
                        scrollregion=(0,
                                    0,
                                    width,
                                    height),
                        height=height, 
                        width=width)
    canvas.config(height=height)
    canvas.grid(row=row,column=col, sticky=N+W+E+S, columnspan=colspan, rowspan=rowspan)
    canvas.columnconfigure(col, weight=1)
    canvas.rowconfigure(row, weight=1)
    if take_focus:
        canvas.bind("<Button-1>", set_focus)
        canvas.bind("p", save_canvas)
    return canvas
    
def save_canvas(event):
    """ saves canvas """
    canvas = event.widget
    save_canvas_as_pdf(canvas)
    
def set_focus(event):
    """ sets focus to canvas """
    event.widget.focus_set()
    
def get_fonts():
    """ gets fonts """
    fonts_dict = {}
    fonts_dict['listbox_font'] = ('Courier', 14)#, 'roman bold')
    return fonts_dict
    
def set_window_to_front(root):
    """ sets windo to front"""
    root.lift()
    root.attributes('-topmost',True)
    root.after_idle(root.attributes,'-topmost',False)
    

def transform_to_another_scale(x,a,b,c,d):
    """ tranforms a value x from the scale [a,b] to the scale [c,d] """
    return (x-a)*((d-c)/(b-a))+c

def p_adjust_bh(p):
    """Benjamini-Hochberg p-value correction for multiple hypothesis testing"""
    p = np.asfarray(p)
    by_descend = p.argsort()[::-1]
    by_orig = by_descend.argsort()
    steps = float(len(p)) / np.arange(len(p), 0, -1)
    q = np.minimum(1, np.minimum.accumulate(steps * p[by_descend]))
    return q[by_orig]
    
def shannon_index(abundances, base=None): 
    abundances = abundances[abundances>0]
    abundances = abundances/sum(abundances)
    if base is None:
        return -sum(abundances*np.log(abundances))
    elif base == 2:
        return -sum(abundances*np.log2(abundances))