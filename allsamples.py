import os, sys
from tkinter import *
from tkinter.ttk import *
import pandas as pd
from random import randrange
from tkinter.colorchooser import askcolor


class AllSamples():
    def __init__(self, root, abundance_df, all_tax_levels, changed_filter_all_samples):
        self.root = root
        self.abundance_df_instance = abundance_df
        self.abundance_df = abundance_df.getDataframe()
        self.all_tax_levels = all_tax_levels
        self.samples = abundance_df.getSamplesList()
        self.changed_filter_all_samples = changed_filter_all_samples
        self.item_ids_set = set()
        self.item_ids_hidden_set = set()
        self.create_popup_window()
        self.create_table()
        self.create_filter_options()
    
    def cancel(self, event=None):
        """ destroys/closes pop upwindow """
        self.top.destroy()
        
    def create_popup_window(self):
        """ creates a popup window """
        self.top = Toplevel(self.root)
        self.top.protocol("WM_DELETE_WINDOW", self.cancel)
        self.top.attributes("-topmost", 1)
        self.top.attributes("-topmost", 0)
        self.top.columnconfigure(0, weight=1)
        self.top.rowconfigure(0, weight=1)
        self.top.title('Filtering options for analysis taking all samples')
        self.frame = Frame(self.top)
        self.frame.grid(row=0, column=0, sticky=N+S+W+E)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.colors_dict = {}
        self.top.focus_set()
    
    def create_table(self):
        """ creates table for filtering """
        self.tree_frame = ttk.Frame(self.frame)
        self.tree_frame.grid(row=0, column=0, columnspan=5)
        self.tax_tree = ttk.Treeview(self.tree_frame, height='26', columns=['max_abundance']+self.all_tax_levels + ['masked', 'colour'])#, show="headings", selectmode="extended")
        self.tax_tree.grid(row=1, column=0)
        treeScroll = Scrollbar(self.tree_frame, command=self.tax_tree.yview)
        treeScroll.grid(row=1, column=5, sticky='nsew')
        self.tax_tree.configure(yscrollcommand=treeScroll.set)

        #self.tax_tree.heading("#0", text='Id', anchor='w')
        self.tax_tree.column("#0", anchor="w", width=0)
        #self.tax_tree.heading('max_abundance', text='max_abundance')
        self.tax_tree.heading('max_abundance',text='Max_abundance',command=lambda each='max_abundance': self.treeview_sort_column(self.tax_tree, each, True))
        self.tax_tree.column('max_abundance', anchor='w', width=70)
        for col in self.all_tax_levels:
            #self.tax_tree.heading(col, text=col)
            self.tax_tree.heading(col,text=col.capitalize(),command=lambda each=col: self.treeview_sort_column(self.tax_tree, each, False))
            self.tax_tree.column(col, anchor='w', width=125)
        self.tax_tree.heading('masked', text='Hide', command=lambda each='masked': self.treeview_sort_column(self.tax_tree, each, False))
        self.tax_tree.column('masked', anchor='w', width=50)
        self.tax_tree.heading('colour', text='Colour', command=lambda each='colour': self.treeview_sort_column(self.tax_tree, each, False))
        self.tax_tree.column('colour', anchor='w', width=100)
        for idx in self.abundance_df.index:
            tax_list = list(self.abundance_df.loc[idx, self.all_tax_levels])
            max_abundance = self.abundance_df.loc[idx,self.samples].max()
            item = self.tax_tree.insert('', 'end', values=[round(max_abundance, 4)]+tax_list + [self.abundance_df.loc[idx,'masked'], self.abundance_df.loc[idx,'colour']])  
            if self.abundance_df.loc[idx,'masked'] == True or self.abundance_df.loc[idx,'masked'] == 'True':
                self.item_ids_hidden_set.add(item)
            else: 
                self.item_ids_set.add(item)
        self.tax_tree.bind("<Button-2>", self.create_popup_menu)
    
    def treeview_sort_column(self, tv, col, reverse):
        """ sorts the table by coloumn """
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

    def hide_show_items(self, event):
        """ hide or show the selected item or group of item depending on if the state of the selected item """
        item = self.tax_tree.identify_row(event.y) 
        col = int(self.tax_tree.identify_column(event.x).strip('#')) - 1
        hidden = self.tax_tree.item(item,'values')[-2]
        if hidden == 'False' or hidden == False:
            state='show'
        else:
            state='hide'
        if col == 1:
            if state == 'show':
                self.tax_tree.set(item,'masked', 'True')
                self.item_ids_set.discard(item)
                self.item_ids_hidden_set.add(item)
            elif state == 'hide':
                self.tax_tree.set(item,'masked', 'False')
                self.item_ids_set.add(item)
                self.item_ids_hidden_set.discard(item)
        elif 1 < col <= len(self.all_tax_levels):
            if state == 'show':
                group_to_delete = self.tax_tree.item(self.tax_tree.identify_row(event.y), 'values')[col]
                if group_to_delete != '-' and len(self.item_ids_set) > 0:
                    for item_id in self.item_ids_set.copy():
                        if self.tax_tree.item(item_id,'values')[col] == group_to_delete:
                            self.tax_tree.set(item_id,'masked', 'True')
                            self.item_ids_set.discard(item_id)
                            self.item_ids_hidden_set.add(item_id)
            elif state == 'hide':
                group_to_delete = self.tax_tree.item(self.tax_tree.identify_row(event.y), 'values')[col]
                if group_to_delete != '-' and len(self.item_ids_hidden_set) > 0:
                    for item_id in self.item_ids_hidden_set.copy():
                        if self.tax_tree.item(item_id,'values')[col] == group_to_delete:
                            self.tax_tree.set(item_id,'masked', 'False')
                            self.item_ids_set.add(item_id)
                            self.item_ids_hidden_set.discard(item)
        self.number_of_species_label.config(text='number of species: '+str(len(self.item_ids_set)) + ' / ' + str(len(self.abundance_df.index)))    

    
    def create_filter_options(self):
        """ creates options to filter the table """
        abundance_taxonomy_label = Label(self.frame, text='')
        abundance_taxonomy_label.grid(row=0, column=0)
        
        self.number_of_species_label = Label(self.frame, text='number of species: '+str(len(self.item_ids_set)) + ' / ' + str(len(self.abundance_df.index)))
        self.number_of_species_label.grid(row=2, column=0)
        m = self.abundance_df.max(numeric_only=True).max()
        self.threshold = StringVar()
        threshold_spinbox = Spinbox(self.frame, from_=0, to=m, increment=0.01, textvariable=self.threshold)
        threshold_spinbox.grid(row=2, column=2)
        self.threshold.set(0)
        self.threshold.trace('w', self.filter_abundances)
            
        save_changes_button = Button(self.frame, text='save changes', command=self.save_changes)
        save_changes_button.grid(row=2, column=3)    
        reset_button = Button(self.frame, text='reset', command=self.reset)
        reset_button.grid(row=2, column=4)
            
            
    def filter_abundances(self, a,b,c):
        """ filters the table for abundance """
        t = float(self.threshold.get())
        for item_id in self.item_ids_set.copy():
            if float(self.tax_tree.item(item_id,'values')[0]) < t:
                self.tax_tree.delete(item_id)
                self.item_ids_set.remove(item_id)
        self.number_of_species_label.config(text='number of species: '+str(len(self.item_ids_set)) + ' / ' + str(len(self.abundance_df.index)))
        
    def save_changes(self):
        """ saves changes so that they can be used in the rest of the program """
        indices = [self.tax_tree.item(item_id,'values')[1] for item_id in self.item_ids_set]
        colors_dict = dict((self.tax_tree.item(key,'text'),value) for (key,value) in self.colors_dict.items())
        self.abundance_df_instance.renewMasking(indices, colors_dict)
        self.change_filter_all_samples(self.changed_filter_all_samples)
        
    def reset(self):
        """ resets table (all shown) """
        self.item_ids_set.clear()
        self.item_ids_hidden_set.clear()
        self.threshold.set(0)
        self.abundance_df_instance.reset()
        self.abundance_df = self.abundance_df_instance.getDataframe()
        self.create_table()
        self.number_of_species_label.config(text='number of species: '+str(len(self.item_ids_set)) + ' / ' + str(len(self.abundance_df.index)))
    

    # def change_filter_all_samples(self, variable):
    #     """  """
    #     variable.set(randrange(0,1000))
        
    def select_colour(self, event):
        """ selects and sets the colour in the table """
        colour = askcolor()
        item = self.tax_tree.identify_row(event.y) 
        self.tax_tree.set(item,'colour', colour)
        self.tax_tree.item(item, tags=(colour,))
        color=colour[1]
        self.tax_tree.tag_configure(colour, foreground=color)
        self.colors_dict[item] = color

    def remove_colour(self, event):
        """ deletes the set colour in the table """
        item = self.tax_tree.identify_row(event.y) 
        self.tax_tree.item(item, tags=('black',))
        self.tax_tree.tag_configure('black', foreground='black')
        self.tax_tree.set(item,'colour', 'undefined')
        del self.colors_dict[item]
        
    def create_popup_menu(self, event):
        """ creates popup menu """
        if 1 <= int(self.tax_tree.identify_column(event.x).strip('#')) - 1 <= len(self.all_tax_levels):
            self.popup_menu = Menu(self.root, tearoff=0)
            self.popup_menu.add_command(label='hide/show', command=lambda event=event: self.hide_show_items(event))
            self.popup_menu.add_command(label='select colour', command=lambda event=event: self.select_colour(event))
            self.popup_menu.add_command(label='remove colour', command=lambda event=event: self.remove_colour(event))
            self.popup_menu.post(event.x_root, event.y_root)
        