from tkinter import *
import numpy as np
from popupwindow import PopUpWindow
from popupwindow import PopUpMenu

class Displaying():
    #"to display the abundance and taxonomy"
    def __init__(self, 
                color, 
                current_tax_level,
                x0=None, 
                y0=None, 
                x1=None, 
                y1=None, 
                name=None, 
                taxa=None, 
                taxa_level=None, 
                taxa_levels_list=None, 
                row_num=None, parent=None, 
                taxonomy_matrix=None, 
                abundance=None,
                samples_names=None,
                pop_ups=None,
                abundance_df=None,
                #threshold_slider=None,
                tax_list=None,
                meta_df=None,
                all_tax_levels=None):
        self.coords = (x0, y0, x1, y1)
        self.name = name
        self.color = color
        self.taxa = taxa
        self.taxa_level = taxa_level
        self.taxa_levels_list = taxa_levels_list
        self.row_num = row_num
        self.parent = parent
        self.taxonomy_matrix = taxonomy_matrix
        self.abundance = abundance
        self.col = ['orange red', 
                'maroon', 
                'red4', 
                'DarkOrange2', 
                'medium violet red', 
                'red', 
                'DeepPink4', 
                'magenta3', 
                'brown4', 
                'deep pink']
        self.pop_ups = pop_ups
        self.abundance_df = abundance_df
        self.popup_menu = PopUpMenu(self.parent, self.name, self.pop_ups, self.abundance_df, tax_list, meta_df, all_tax_levels=all_tax_levels, current_tax_level=current_tax_level)
        
        self.tax_levels_list = all_tax_levels
        
    def drawBar(self, canvas, root, balloon, os_windows):
        """ draws one bar of a bar graph """
        self.canvas = canvas
        self.root = root
        self.item = canvas.create_rectangle(self.coords, 
                                            outline=self.color, 
                                            fill=self.color, 
                                            tags=self.color)
        balloon.tagbind(canvas, self.item, str(self.name) + '\t' + '{0:.2f}'.format(round(self.abundance, 2)))
        if os_windows:  #windows
            canvas.tag_bind(self.item, '<Control-Button-3>', lambda event, new_bool=1: self.popup_menu.do_popup(event, new_bool))
            canvas.tag_bind(self.item, '<Button-3>', lambda event, new_bool=0: self.popup_menu.do_popup(event, new_bool))
        else:
            canvas.tag_bind(self.item, '<Command-Button-2>', lambda event, new_bool=1: self.popup_menu.do_popup(event, new_bool))
            canvas.tag_bind(self.item, '<Button-2>', lambda event, new_bool=0: self.popup_menu.do_popup(event, new_bool))
        return self.item
        
    def on_click(self, event):
        """ renews pop up window (if a pop up is open) """
        if len(self.pop_ups) > 0:
            self.pop_ups[-1][0].empty_graph(self.name)
            self.pop_ups[-1][0].create_graph(self.abundances, self.samples_names)
        else:
            self.on_ctrl_click()
        
    def on_enter(self, event):
        """ displays species name and abundance in label"""
        self.canvas.config(cursor='plus')

    def on_leave(self, event):
        """ empties species label """
        self.canvas.config(cursor='arrow')
        