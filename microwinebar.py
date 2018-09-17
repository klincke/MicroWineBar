### python3

#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import os.path
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilenames, askopenfilename, asksaveasfilename
import tkinter.messagebox as tmb
import pandas as pd
import itertools

from os import system
from platform import system as platform

import Pmw
import numpy as np

from data import Abundances
from data import MetaData
from displaying import Displaying
from popupwindow import PopUpWindow
from popupwindow import PopUpGraph
from popupwindow import PopUpMenu
from general_functions import *
from allsamples import AllSamples
from popupwindow_matplotlib import PopUpIncludingMatplotlib

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

class Interaction(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.protocol('WM_DELETE_WINDOW', self.QuitProgram)  #dump also when closed
        
        #self.parent.rowconfigure('all', minsize = 200)
        #self.parent.columnconfigure('all', minsize = 200)
        self.initGUI()


    def initGUI(self):
        """ initialises the GUI """
        self.canvas_width = 1000
        self.canvas_height = 400
        #self.canvas_orig_width = 1000
        #self.canvas_orig_height = 400
        self.COLOR_SCHEME = ['#0000df', '#007a15', '#a35a00', '#0096b6']
        self.COLOR_SCHEME2 = ['#000078', '#006912', '#784300', '#01758d']
        self.toggle_color_scheme = itertools.cycle([self.COLOR_SCHEME, self.COLOR_SCHEME2])
        self.change_tax_level_bool = False
        self.balloon = Pmw.Balloon(self.parent)
        self.pop_ups = []
        self.pop_ups2 = []
        self.bar_ids = []
        self.presets_list = [('-', [], [])]
        #self.all_tax_levels = ['species', 'genus', 'family', 'order', 'class', 'phylum', 'superfamily']
        self.all_tax_levels = None
        self.corr_matrix, self.corr_signature = None, None
        self.abundance_df = None
        self.meta_df = None
        self.sample_names = None
        self.working_sample = None
        if platform() == 'Darwin':
            self.os = True
        else:
            self.os = False
        self.always_together_id = None
        
        self.changed_filter_all_samples = IntVar()
        self.changed_filter_all_samples.set(2)
        
        self.createGraphFrame()
        self.createTaxonomyFrame()
        self.createFeaturesFrame()
        self.createMenu()
        
        self.changed_filter_all_samples.trace("w", self.change_filter_all_samples)

    def change_filter_all_samples(self, *args):
        """ change filter options """
        self.abundance_df.getSample(self.getSampleName())
        self.working_sample = self.abundance_df.getWorkingSample(self.get_current_tax_level())
        self.min_abundance.delete(0, END)
        self.min_abundance.insert(0, '{0:.2f}'.format(self.getMinAbundance(self.working_sample)))
        self.max_abundance.delete(0, END)
        self.max_abundance.insert(0, '{0:.2f}'.format(self.getMaxAbundance(self.working_sample)))
        self.update()


    def createGraphFrame(self):
        """ creates the frame and canvas for displaying the graph """
        self.graph_frame = Frame(self.parent, height=self.canvas_height+5)
        self.graph_frame.rowconfigure(0, weight=1)
        self.graph_frame.columnconfigure(0, weight=1)
        self.graph_frame.grid(column=0,row=0,sticky=N+W+E+S, columnspan=3)
        
        self.canvas = create_canvas(self.graph_frame, col=1, height=self.canvas_height, width=self.canvas_width, take_focus=True)
        self.canvas.config(scrollregion=(0,0,self.canvas_width*2, self.canvas_height))
        self.canvas.rowconfigure(0, weight=1)
        self.canvas.columnconfigure(0, weight=1)

        self.graph_frame.grid_columnconfigure(0, weight=0)
        self.graph_frame.grid_columnconfigure(1, weight=1, minsize=100)
        self.graph_frame.grid_rowconfigure(0, weight=1, minsize=100)

    def createTaxonomyFrame(self):
        """ creates the frame for the taxonomy and species lists """
        self.taxa_frame = ttk.Frame(self.parent, 
                                height=180, 
                                width=250, 
                                padding=(5,5))
        self.taxa_frame.rowconfigure(1, weight=1)
        self.taxa_frame.columnconfigure(0, weight=1)
        self.taxa_frame.grid(row=1,column=0,sticky='NSEW')#rowspan=2)#, )
        taxa_label = ttk.Label(self.taxa_frame,
                                text='taxonomic levels:')
        taxa_label.grid(row=0, column=0)
        self.tax_lbox = Listbox(self.taxa_frame, 
                                listvariable=[],
                                height=10,
                                width=15,
                                selectmode='browse',
                                exportselection=0)
        self.tax_lbox.grid(row=1, column=0, sticky = N+S+E+W)
        
        species_label = ttk.Label(self.taxa_frame, 
                            text='select to display:')
        species_label.grid(row=0, column=2)
        
        self.sbary = Scrollbar(self.taxa_frame, orient=VERTICAL)
        self.sbary.grid(row=1, column=3, sticky = 'NW' + 'SW')
        self.lbox = Listbox(self.taxa_frame, 
                            listvariable=[], 
                            height=10, 
                            width=50, 
                            selectmode='extended', 
                            yscrollcommand=self.sbary.set,
                            exportselection=0)
        self.lbox.grid(row=1, column=2, sticky='NSEW')
        self.sbary.config(command=self.lbox.yview)
        
    def createFeaturesFrame(self):
        """ creates frame for the features (buttons etc.) """
        self.features_frame = ttk.Frame(self.parent, 
                                    height=180, 
                                    width=150, 
                                    padding=(5,5))
        self.features_frame.grid(row=1, column=1, sticky=N+S+E+W)
        
        filter_frame = Labelframe(self.features_frame, 
                                        text='filter:')
        filter_frame.grid(rowspan=2, 
                            columnspan=2, 
                            row=0, 
                            column=1, 
                            sticky=N+S+E+W)
        
        filter_minlabel = ttk.Label(filter_frame, 
                                text='min abundance', 
                                background='white')
        filter_minlabel.grid(row=0,column=1)
        
        filter_maxlabel = ttk.Label(filter_frame, 
                                    text='max abundance', 
                                    background='white')
        filter_maxlabel.grid(row=1,column=1)
        
        self.min_abundance = ttk.Entry(filter_frame, width=8)
        self.min_abundance.insert(0, '{0:.2f}'.format(float(0)))
        self.min_abundance.grid(row=0, column=2)
        
        self.max_abundance = ttk.Entry(filter_frame, width=8)
        self.max_abundance.insert(0, '{0:.2f}'.format(float(0)))
        self.max_abundance.grid(row=1, column=2)
        self.number_of_bars_label = ttk.Label(self.features_frame,
                                            text='number of bars: ',
                                            background='white')
        self.number_of_bars_label.grid(row=4, column=2)
        
        update_button = ttk.Button(self.features_frame, 
                                text='update', 
                                command=self.update)
        update_button.grid(row=2, column=2)
        self.balloon.bind(update_button, 'update graph')
        
        reset_button = ttk.Button(self.features_frame, 
                                text='reset', 
                                command=self.reset)
        reset_button.grid(row=3, column=2)
        
        scale_label = ttk.Label(self.features_frame, 
                                text='scale:', 
                                background='white')
        scale_label.grid(row=0, column=3)
        self.scale_slider = Scale(self.features_frame, 
                                from_=20, 
                                to=1, 
                                orient=VERTICAL,
                                length=150)
        self.scale_slider.set(1)
        self.scale_slider.grid(row=1, column=3, rowspan=3)
        
        #scale_corr_label = ttk.Label(self.features_frame,
        #                            text='correlation threshold:',
        #                            background='white')
        #scale_corr_label.grid(row=2, column=0)
        #self.threshold = DoubleVar()
        #self.threshold.set(0.95)
        #self.scale_corr_slider = Spinbox(self.features_frame, 
        #                                    from_=0, 
        #                                    to=1, 
        #                                    increment=0.01, 
        #                                    textvariable=self.threshold)
        #self.scale_corr_slider.grid(row=3, column=0)
        
        search_frame = ttk.Labelframe(self.features_frame, text='search taxonomic name:')
        search_frame.grid(rowspan=2, row=3, column=0, sticky=N+S+E+W)
        self.species_to_search = StringVar()
        self.species_to_search.trace("w", 
                                    lambda name, index, mode, sv=self.species_to_search: self.searchTaxName(self.species_to_search))
        search_species = Entry(search_frame, 
                                textvariable=self.species_to_search)
        search_species.grid(row=0, column=0)
        self.tax_name_hits_count = ttk.Label(search_frame, 
                                                text='number of hits: 0')
        self.tax_name_hits_count.grid(row=1, column=0)  
    
    
    def reset(self):
        """ resets the diplaying options """
        self.abundance_df.reset()
        self.min_abundance.delete(0, END)
        self.min_abundance.insert(0, '{0:.2f}'.format(float(0)))
        self.max_abundance.delete(0, END)
        self.max_abundance.insert(0, '{0:.2f}'.format(self.abundance_df.getMaxAbundanceOfSample()+0.01))
        self.scale_slider.set(1)
        self.update()
    
    def createMenu(self):
        """ creates the menu """
        self.parent.option_add('*tearOff', FALSE)
        self.menu = Menu(self.parent)#, background='#000099', foreground='white', activebackground='#004c99', activeforeground='white')
        self.filemenu = Menu(self.menu, tearoff=0)
        self.sortmenu = Menu(self.menu, tearoff=0)
        self.highlightmenu = Menu(self.menu, tearoff=0)
        self.corrmenu = Menu(self.menu, tearoff=0)
        self.aboutmenu = Menu(self.menu, tearoff=0)
        self.samplemenu = Menu(self.menu, tearoff=0)
        self.overviewmenu = Menu(self.menu, tearoff=0)
        
        self.sort_list=[]
        # self.sort_list=['superkingdom, abundance', 'family, abundance', 'abundance', 'species', 'genus', 'family', 'order', 'class', 'phylum', 'superkingdom']
        self.sort_ind = IntVar()
        self.sort_ind.set(0)
        self.sample_index = IntVar()
        self.sample_index.set(0)
        self.preset_ind = IntVar()
        self.preset_ind.set(0)
        self.checkDumped()
        self.menu.add_cascade(label="File", menu=self.filemenu)
        if not self.os:
            self.filemenu.add_command(label="Open sample(s)", command=self.OpenFiles, accelerator="Ctrl+o")
            self.bind_all("<Control-o>", self.OpenFiles)
            self.filemenu.add_command(label='Open MetsPhlan file(s)', command=self.OpenMetaPhlanFiles)
            #self.filemenu.add_command(label="Open sample(s) - MGmapper classify", command=self.OpenMGmapperClassifyFiles)
            self.filemenu.add_command(label="Open metadata", command=self.OpenMetadata, accelerator="Ctrl+m")
            self.filemenu.add_separator()
            self.filemenu.add_command(label='add preset', command=self.addPreset, accelerator="Ctrl+p")
        else:
            self.filemenu.add_command(label="Open", command=self.OpenFiles, accelerator="Cmd+o")
            #self.filemenu.add_command(label="Open MGmapper classify", command=self.OpenMGmapperClassifyFiles)
            self.filemenu.add_command(label="Open MGmapper", command=self.OpenMGmapper)
            self.bind_all("<Command-o>", self.OpenFiles)
            self.filemenu.add_command(label='Open MetsPhlan file(s)', command=self.OpenMetaPhlanFiles)
            self.filemenu.add_command(label="Open metadata", command=self.OpenMetadata, accelerator="Cmd+m")
            self.filemenu.add_separator()
            self.filemenu.add_command(label='add preset', command=self.addPreset, accelerator="Cmd+p")
        self.filemenu.add_separator()
        #write samples to table
        self.filemenu.add_command(label='write csv', command=self.writeCsv)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Quit (dump)', command=self.QuitProgram, accelerator="Ctrl+q")
        self.bind_all("<Control-q>", self.QuitProgram)
        #self.filemenu.add_separator()
        self.filemenu.add_command(label='Quit and remove dump file', command=self.removeDump)
        self.menu.add_cascade(label="Sort by", menu=self.sortmenu)
        for ind in range(len(self.sort_list)):
            self.sortmenu.add_radiobutton(label=self.sort_list[ind], 
                                        variable=self.sort_ind, 
                                        value=ind, 
                                        command=self.update)   
        self.menu.add_cascade(label="Display sample", menu=self.samplemenu)
        self.menu.add_cascade(label="Highlight", menu=self.highlightmenu)
        for ind in range(len(self.presets_list)):
            self.highlightmenu.add_radiobutton(label=self.presets_list[ind][0],
                                                variable=self.preset_ind,
                                                value=ind,
                                                command=self.HighlightPresets)
        self.menu.add_cascade(label='overview', menu=self.overviewmenu)
        self.overviewmenu.add_command(label='stacked bar graph', command=self.overview_bar)
        self.overviewmenu.add_command(label='line graph', command=self.overview_line)
        self.overviewmenu.add_command(label='richness', command=self.richness_all_samples)
        self.overviewmenu.add_command(label='Shannon diversity', command=self.shannon_diversity_all_samples)
        self.overviewmenu.add_command(label='save beta diversity heatmap', command=self.beta_diversity_heatmap)

        self.overviewmenu.add_command(label='compare two groups of samples', command=self.compare_groups)
        self.overviewmenu.add_command(label='correlation', command=self.correlate)
        self.overviewmenu.add_command(label='scatter plot', command=self.scatter_plot)
        self.overviewmenu.add_command(label='filter', command=self.filter_all_samples)
        with open('path.txt', 'r') as path_file:
            r_path = path_file.readline().split('=')[1].strip().strip("'")
        if r_path != '' and r_path is not None:
            self.overviewmenu.add_command(label='rarafaction curve', command=self.r_rarefactioncurve)
        self.menu.add_cascade(label="About", menu=self.aboutmenu)
        self.aboutmenu.add_command(label="About", command=self.ShowAbout)
        self.aboutmenu.add_command(label="Help")
        
        self.parent.config(menu=self.menu)
    
    def update(self):
        """ updates the graph """
        #self.species_to_search.set(self.species_to_search.get()+' ')
        #old_string = self.species_to_search.get()
        #self.species_to_search.set('')
        #self.species_to_search.set(old_string)
        
        #self.searchTaxName(self.species_to_search.get())
        indexes = self.lbox.curselection()
        if len(indexes) > 0:
            self.abundance_df.selectOfSample(indexes)
        sort_key_list = self.sort_list[self.sort_ind.get()].split(', ')
        if self.abundance_df is not None:
            self.working_sample = self.abundance_df.getWorkingSample(self.get_current_tax_level())
            if self.sort_ind.get() < 3:
                self.abundance_df.sortSample(sort_key_list, False)
                self.working_sample = self.sortBy(self.working_sample, sort_key_list, False)
            else:
                self.abundance_df.sortSample(sort_key_list, True)
                self.working_sample = self.sortBy(self.working_sample, sort_key_list, True)
            
            if not self.change_tax_level_bool:
                self.working_sample = self.filterAbundance(self.working_sample)
            self.change_tax_level_bool = False
            self.min_abundance.delete(0, END)
            self.min_abundance.insert(0, '{0:.2f}'.format(self.getMinAbundance(self.working_sample)))
            self.max_abundance.delete(0, END)
            self.max_abundance.insert(0, '{0:.2f}'.format(self.getMaxAbundance(self.working_sample)))
            #self.searchTaxName(self.species_to_search)
            self.barGraph()
            self.HighlightPresets()
            
            self.createTaxLevelList()
            self.createSpeciesList()
            self.lbox.selection_clear(0, END)
            self.number_of_bars_label.config(text='number of bars: '+str(len(self.bar_ids)))
    
    def sortBy(self, dataframe, key, ascending):
        """ sorts the dataframe with the species of a sample by the given key """
        flag = True
        for element in key:
            if element not in dataframe.columns:
                flag = False
        if flag: return dataframe.sort_values(by=key, ascending=ascending)
        else: return dataframe
    
    def filterAbundance(self, sample):
        """ filters for abundance """
        for ind in sample.index:
            if float(sample.loc[ind,'abundance']) < float(self.min_abundance.get()) or float(sample.loc[ind,'abundance']) > float(self.max_abundance.get()):
                sample.at[ind,'masked'] = True
            else:
                sample.at[ind,'masked'] = False
        return sample[sample['masked'] == False]
    
    def getMinAbundance(self, sample):
        """ gets the minimum abundance of a sample """
        try: minimum = min(sample[sample['masked'] == False]['abundance'])
        except: minimum = 0.0
        return float(minimum)
        
    def getMaxAbundance(self, sample):
        """ gets the mamimum abaundance of a sample """
        try: maximum = max(sample[sample['masked'] == False]['abundance'])
        except: maximum = 0
        return float(maximum+0.01)
    
    def HighlightPresets(self):
        """  hightlights presets of species in the bar graph"""
        for idx in self.canvas.find_withtag('orange'):
            self.canvas.dtag(idx, 'orange')
            tag = self.canvas.gettags(idx)[0]
            self.canvas.itemconfig(idx, outline=tag, width=1)
        if self.working_sample is not None:
            if 'species' in self.working_sample.columns:
                for species in self.presets_list[self.preset_ind.get()][1]:
                    if species in list(self.working_sample['species']):
                        idx = self.working_sample[self.working_sample['species'] == species].index.tolist()[0]
                        idx = self.working_sample.index.tolist().index(idx)
                        self.canvas.addtag_withtag('orange', self.bar_ids[idx])
                        #self.lbox.itemconfig(index, foreground='orange')
                        self.canvas.itemconfigure(self.bar_ids[idx], outline='orange', width=3)
                for genus in self.presets_list[self.preset_ind.get()][2]:
                    if genus in list(self.working_sample['genus']):
                        idx = self.working_sample[self.working_sample['genus'] == genus].index.tolist()[0]
                        idx = self.working_sample.index.tolist().index(idx)
                        self.canvas.addtag_withtag('orange', self.bar_ids[idx])
                        self.canvas.itemconfigure(self.bar_ids[idx], outline='orange', width=3)
            if 'genus' in self.working_sample.columns:
                for genus in self.presets_list[self.preset_ind.get()][2]:
                    if genus in list(self.working_sample['genus']):
                        idx = self.working_sample[self.working_sample['genus'] == genus].index.tolist()[0]
                        idx = self.working_sample.index.tolist().index(idx)
                        self.canvas.addtag_withtag('orange', self.bar_ids[idx])
                        self.canvas.itemconfigure(self.bar_ids[idx], outline='orange', width=3)
    
    def barGraph(self):
        """ creates the bar graph """
        self.canvas.delete('all')
        self.bar_ids = []
        width = self.canvas_width/len(self.working_sample.index)
        if width > 30:
            width = 30
        elif width < 7:
            width = 7
        canvas_scroll_width = width * len(self.working_sample.index) + 75
        self.canvas.config(scrollregion=(0, 
                                        0, 
                                        canvas_scroll_width, 
                                        self.canvas_height+50))
        sample_name = self.getSampleName()
        max_abundance = max(self.working_sample['abundance']+0.01)
        self.max_abundance.delete(0, END)
        self.max_abundance.insert(0, '{0:.2f}'.format(max_abundance))
        scale_value = self.scale_slider.get()
        current_tax_level = self.get_current_tax_level()
        y2 = self.canvas_height-10
        for i, name in enumerate(self.working_sample.index):
            x1 = 70 + i*width
            y1 = self.canvas_height-10-self.working_sample.loc[name,'abundance']/max_abundance*(self.canvas_height-10)*scale_value
            x2 = 70 + (i+1)*width
            color = getColor(1, next(self.toggle_color_scheme))
            self.abundances_list = [0] * len(self.working_sample)
            self.samples_names = [None] * len(self.sample_names)
            tax_list=list(self.working_sample.loc[name, self.all_tax_levels[self.all_tax_levels.index(self.get_current_tax_level()):]])
            g = Displaying(x0=x1, 
                        y0=y1, 
                        x1=x2, 
                        y1=y2, 
                        name=self.working_sample.loc[name, current_tax_level],
                        color=color,
                        current_tax_level=self.get_current_tax_level(),
                        abundance=self.working_sample.loc[name, 'abundance'],
                        samples_names=self.samples_names,
                        pop_ups=self.pop_ups, 
                        abundance_df=self.abundance_df,
                        #threshold_slider=self.threshold,
                        tax_list=tax_list,
                        meta_df=self.meta_df,
                        all_tax_levels=self.all_tax_levels)
            bar_id = g.drawBar(self.canvas, self.parent, self.balloon, self.os)
            self.bar_ids.append(bar_id)
        y_axis_line = self.canvas.create_line(70,0,70,self.canvas_height-10)
        self.canvas.itemconfig(y_axis_line, tags=('y_axis'))
        j = 0
        while j < self.canvas_height-20:
            item = self.canvas.create_line(65,self.canvas_height-10-j,70,self.canvas_height-10-j)
            self.canvas.itemconfig(item, tags=('y_axis'))
            number = '{0:.2f}'.format(float(j)/(self.canvas_height-10)*max_abundance/scale_value)
            item = self.canvas.create_text(40, self.canvas_height-10-j, text=number)
            self.canvas.itemconfig(item, tags=('y_axis'))
            j+=40
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        self.canvas.addtag_all("all")
    
    def createTaxLevelList(self):
        """ creates a list of taxonomic levels """
        level = StringVar(value=tuple(self.all_tax_levels))
        self.tax_lbox.config(listvariable=level)
        self.tax_lbox.bind("<<ListboxSelect>>", self.changeTaxLevel)
        self.tax_lbox.selection_set(0)
    
    def changeTaxLevel(self, event):
        """ changes the current taxonomic level """
        index = event.widget.curselection()[0]
        self.set_current_tax_level(index)
        self.abundance_df.reset()
        self.change_tax_level_bool = True
        self.reset()
        self.searchTaxName(self.species_to_search)
        if len(event.widget.curselection()) > 1:
            self.tax_lbox.selection_clear(0)
    
    def undoSelecting(self, event):
        """ undoes the selection of species in the listbox """
        self.lbox.selection_clear(0, END)
        for idx in self.bar_ids:
            tag = self.canvas.gettags(idx)[0]
            self.canvas.itemconfig(idx, outline=tag, width=1)
    
    def highlightBar(self, event=None):
        """ highlight bars in bar graph """
        indexes = event.widget.curselection()
        for index in indexes:
            self.canvas.itemconfigure(self.bar_ids[index], outline='red', width=3)
    
    def speciesListMenu(self, event=None):
        """  """
        idx = self.lbox.index("@%s,%s" % (event.x, event.y))
        name = self.lbox.get(idx)
        #print(self.all_tax_levels[self.all_tax_levels.index(self.get_current_tax_level()):])
        tax_list = list(self.abundance_df.getDataframe().loc[name, self.all_tax_levels[self.all_tax_levels.index(self.get_current_tax_level()):]])
        popup_menu = PopUpMenu(self.parent, name, [], self.abundance_df, tax_list=tax_list, meta_df=None, all_tax_levels=self.all_tax_levels, current_tax_level=self.get_current_tax_level())
        popup_menu.do_popup(event, 1)
    
    def createSpeciesList(self):
        """ creates a list with species shown in graph and in species list """
        species_list = self.working_sample[self.get_current_tax_level()].tolist()
        species = StringVar(value=tuple(species_list))
        
        self.lbox.config(listvariable=species)
        self.lbox.bind("<Double-1>", self.undoSelecting)
        self.lbox.bind('<<ListboxSelect>>', self.highlightBar)
        self.lbox.bind("<Double-2>", self.speciesListMenu)
    
    def overview_bar(self):
        """ opens one popup window with stacked bar graph for all samples """
        popup = PopUpGraph(self.parent, self.all_tax_levels, self.get_current_tax_level(), self.abundance_df)
        if self.abundance_df is not None:
            working_samples = self.abundance_df.groupAllSamples()
            popup.create_overview_scaled_bar(working_samples, self.sample_names, self.get_current_tax_level())#'species')
    
    def overview_line(self):
        """ opens one popup window with a line graph for all samples, 
        each organism (e.g. species) is represented by one line """
        popup = PopUpGraph(self.parent, self.all_tax_levels, self.get_current_tax_level(), self.abundance_df)
        if self.abundance_df is not None:
            working_samples = self.abundance_df.groupAllSamples()
            popup.create_overview_line(working_samples, self.sample_names, self.get_current_tax_level())
    
    def richness_all_samples(self):
        """ create richness plot for all samples """   
        popup_matplotlib = PopUpIncludingMatplotlib(self.parent, self.abundance_df, self.all_tax_levels)
        if self.abundance_df is not None:
            working_samples = self.abundance_df.groupAllSamples()
        popup_matplotlib.richness_all_samples(working_samples, self.sample_names, self.get_current_tax_level())
        
    def shannon_diversity_all_samples(self):
        """ create Shannon diversity index plot of all samples """   
        popup_matplotlib = PopUpIncludingMatplotlib(self.parent, self.abundance_df, self.all_tax_levels)
        if self.abundance_df is not None:
            working_samples = self.abundance_df.groupAllSamples()
        popup_matplotlib.shannon_diversity_all_samples(working_samples, self.sample_names, self.get_current_tax_level())
    
    def beta_diversity_heatmap(self):
        """ create and save as png Braycurtis beta diversity heatmap of all samples """
        popup_matplotlib = PopUpIncludingMatplotlib(self.parent, self.abundance_df, self.all_tax_levels)
        if self.abundance_df is not None:
            working_samples = self.abundance_df.groupAllSamples()
        popup_matplotlib.beta_diversity_heatmap(working_samples, self.sample_names, self.get_current_tax_level())
    
    def compare_groups(self):
        """ compare two presence/absence of species in two groups of samples """
        popup = PopUpGraph(self.parent, 
                            self.all_tax_levels, self.get_current_tax_level(), 
                            self.abundance_df)
        popup.compare_groups_of_samples(self.abundance_df, 
                                        self.sample_names, self.get_current_tax_level())
    
    def get_current_tax_level(self):
        """ gets the current taxonomy level """
        new_level = None
        if len(self.tax_lbox.curselection()) < 1:
            new_level = self.all_tax_levels[0]
        else:
            new_level = self.all_tax_levels[self.tax_lbox.curselection()[-1]]
        return new_level
    
    def correlate(self):
        """ correlation """
        popup = PopUpGraph(self.parent, 
                            self.all_tax_levels, self.get_current_tax_level(), 
                            self.abundance_df)
        popup.corr(self.sample_names, 
                    self.abundance_df.getValuesForColumn(self.all_tax_levels[-1]), 
                    self.abundance_df)
        #self.abundance_df.corr(self.all_tax_levels, self.sample_names, self.get_current_tax_level())
    
    def scatter_plot(self):
        """ scatter plot """
        popup = PopUpGraph(self.parent, 
                            self.all_tax_levels, self.get_current_tax_level(), 
                            self.abundance_df)
        popup.scatter_plot_window(self.sample_names)
    
    def filter_all_samples(self):
        """ filter all samples (displayed)"""
        allsamples = AllSamples(self.parent, self.abundance_df, self.all_tax_levels, self.changed_filter_all_samples)
        self.ChooseSample()
    
    def write_rscript(self, filename):
        """ writes the r script for creating a rarefaction curve """
        with open('rscript.R', 'w') as r_file:
            txt = """#R script 
# load (and install) required packages
if(!require(vegan)) install.packages("permute",repos = "http://cran.r-project.org")
if(!require(vegan)) install.packages("mgcv",repos = "http://cran.r-project.org")
if(!require(vegan)) install.packages("lattice",repos = "http://cran.r-project.org")
if(!require(vegan)) install.packages("vegan",repos = "http://cran.r-project.org")
# import the data
absolute_counts <- read.csv("absolute_counts.csv", header=TRUE, row.names = 1)
# rarefaction curve
library("vegan")
absolute_counts_df <- as.data.frame(t(absolute_counts))
raremax <- min(rowSums(absolute_counts_df))
pdf("{}")
my_plot <- rarecurve(absolute_counts_df, step = 1000, sample = raremax, col = "blue", cex = 0.8)
dev.off()
""".format(filename)
            r_file.write(txt)
        
    
    def r_rarefactioncurve(self):
        """ use R to create a rarefaction curve """
        with open('path.txt', 'r') as path_file:
            r_path = path_file.readline().split('=')[1].strip().strip("'")
        if r_path != '' and r_path is not None:
            
            filename = asksaveasfilename(title = "Select file to save the rarefaction curve", initialfile='rarefactioncurve', filetypes = [('PDF', ".pdf")])
            #print(filename)
            self.abundance_df.save_count_tables()
            self.write_rscript(filename)
            from pathlib import Path
            
            if os.path.isfile(str(Path(__file__).parent) + '/relative_counts.csv') and os.path.isfile(str(Path(__file__).parent) + '/rscript.R'):
                #print(r_path + " --file=rscript.R --vanilla --slave")
                out = os.system(r_path + " --file=rscript.R --vanilla --slave")
            os.remove('rscript.R')    
            try:
                os.remove(str(Path(__file__).parent) + '/relative_counts.csv')
                os.remove(str(Path(__file__).parent) + '/absolute_counts.csv')
            except FileNotFoundError:
                pass
    
    def ShowAbout(self):
        """ shows information """
        tmb.showinfo(title="About", 
                message="Tkinter GUI \nfor displaying metagenomics samples")
    
    def checkDumped(self):
        """ check if contents exists to undump """
        dump_dict = {}
        if os.path.exists('dump_file'):
            UnDumpParsed('dump_file', dump_dict)
            if 'abundance_df' in dump_dict and 'samples' in dump_dict and 'all_tax_levels' in dump_dict:
                dump_df = dump_dict['abundance_df']
                if dump_df.shape() > (2,2):
                    self.abundance_df = dump_dict['abundance_df']
                    self.sample_names = dump_dict['samples']
                    self.all_tax_levels = dump_dict['all_tax_levels']
                    if 'corr_matrix' in dump_dict and 'corr_signature':
                        self.corr_matrix = dump_dict['corr_matrix']
                        self.corr_signature = dump_dict['corr_signature']
                        self.abundance_df.set_corr(self.corr_matrix, 
                                                self.corr_signature)
                    if 'meta_df' in dump_dict:
                        self.meta_df = dump_dict['meta_df']
                    if 'presets' in dump_dict:
                        self.presets_list = dump_dict['presets']
                    if 'sort_list' in dump_dict:
                        self.sort_list= dump_dict['sort_list']
                    
                    self.AddSamplesToMenu()
                    self.sample_names = sorted(self.sample_names)
                    self.ChooseSample()
                else: 
                    self.removeDump()
    
    def OpenFiles(self, *args):
        """ opens one or several files """
        names = askopenfilenames()
        new_files_loaded_bool = True
        if len(names) == 0:
            tmb.showinfo(title="no action", 
                        message="no new samples were loaded")
            new_files_loaded_bool = False
            return
        elif len(names) > 150:
            result = tmb.askretrycancel(title="Error", 
                            message="cannot load more than 150 samples", icon='error')
            if result:
                self.OpenFiles()
            else:
                tmb.showinfo(title="no action", 
                            message="no new samples were loaded")
                new_files_loaded_bool = False
                return
                
        if new_files_loaded_bool:
            self.sortmenu.delete(0, 'end')
            self.sample_names = []
            self.abundance_df = Abundances()
            for filename in list(names):
                samplename = '.'.join(filename.split('/')[-1].split('.')[:-1])
                self.sample_names.append(samplename)
                self.all_tax_levels = self.abundance_df.addSample(samplename, filename)
            self.sort_list = ['abundance'] + [level + ', abundance' for level in self.all_tax_levels[1:]] + self.all_tax_levels
            self.abundance_df.addMasking()
            self.AddSamplesToMenu()
            self.ChooseSample()
            for ind in range(len(self.sort_list)):
                self.sortmenu.add_radiobutton(label=self.sort_list[ind], 
                                            variable=self.sort_ind, 
                                            value=ind, 
                                            command=self.update)
    
    def OpenMGmapper(self, *args):
        names = askopenfilenames()
        new_files_loaded_bool = True
        if len(names) == 0:
            tmb.showinfo(title="no action", 
                        message="no new samples were loaded")
            new_files_loaded_bool = False
            return
        elif len(names) > 150:
            result = tmb.askretrycancel(title="Error", 
                            message="cannot load more than 150 samples", icon='error')
            if result:
                self.OpenMGmapper()
            else:
                tmb.showinfo(title="no action", 
                            message="no new samples were loaded")
                new_files_loaded_bool = False
                return
                
        if new_files_loaded_bool:
            self.sortmenu.delete(0, 'end')
            self.sample_names = []
            self.abundance_df = Abundances()
            for filename in list(names):
                samplename = '.'.join(filename.split('/')[-1].split('.')[:-1])
                self.sample_names.append(samplename)
                self.all_tax_levels = self.abundance_df.addMGmapperSample(samplename, filename)
            self.sort_list = ['abundance'] + [level + ', abundance' for level in self.all_tax_levels[1:]] + self.all_tax_levels
            self.abundance_df.addMasking()
            self.AddSamplesToMenu()
            self.ChooseSample()
            for ind in range(len(self.sort_list)):
                self.sortmenu.add_radiobutton(label=self.sort_list[ind], 
                                            variable=self.sort_ind, 
                                            value=ind, 
                                            command=self.update)
                                            
    def OpenMetaPhlanFiles(self, *args):
        """ opens one or several MetaPhlan files """
        names = askopenfilenames()
        new_files_loaded_bool = True
        if len(names) == 0:
            tmb.showinfo(title="no action", 
                        message="no new samples were loaded")
            new_files_loaded_bool = False
            return
        elif len(names) > 150:
            result = tmb.askretrycancel(title="Error", 
                            message="cannot load more than 150 samples", icon='error')
            if result:
                self.OpenFiles()
            else:
                tmb.showinfo(title="no action", 
                            message="no new samples were loaded")
                new_files_loaded_bool = False
                return
                
        if new_files_loaded_bool:
            self.sortmenu.delete(0, 'end')
            self.sample_names = []
            self.abundance_df = Abundances()
            for filename in list(names):
                samplename = '.'.join(filename.split('/')[-1].split('.')[:-1])
                self.sample_names.append(samplename)
                self.all_tax_levels = self.abundance_df.addMetaPhlanSample(samplename, filename)
            self.sort_list = ['abundance'] + [level + ', abundance' for level in self.all_tax_levels[1:]] + self.all_tax_levels
            self.abundance_df.addMasking()
            self.AddSamplesToMenu()
            self.ChooseSample()
            for ind in range(len(self.sort_list)):
                self.sortmenu.add_radiobutton(label=self.sort_list[ind], 
                                            variable=self.sort_ind, 
                                            value=ind, 
                                            command=self.update)
    
    def OpenMetadata(self):
        """ opens metadata belonging to the samples """
        name = askopenfilename()
        if len(name) == 0:
            tmb.showinfo(title="no action", 
                        message="no metadata was loaded")
            return
        if os.path.exists(name):
            self.meta_df = MetaData(name, self.getSampleName(), self.abundance_df)
            self.update()
    
    def addPreset(self):
        """ adds a preset for highlighting """
        names = askopenfilenames()
        if len(names) == 0:
            return
        for filename in list(names):
            species_list = []
            genus_list = []
            file_path, file_name = os.path.split(filename)
            preset_name = file_name.split('_')[:-1]
            with open(filename) as open_file:
                for line in open_file:
                    fields = line.strip().split(' ')
                    if len(fields)== 1 or fields[1].strip() == 'sp.':
                        genus_list.append(fields[0])
                    elif len(fields) == 2:
                        species_list.append(' '.join(fields))
                        
            self.presets_list.append((preset_name, species_list, genus_list))
            self.highlightmenu.add_radiobutton(label=preset_name, 
                                                variable=self.preset_ind,
                                                value=len(self.presets_list)-1,
                                                command=self.HighlightPresets)
    
    def writeCsv(self):
        df = self.abundance_df.groupAllSamples()  
        df = df[df.columns[:-2]]
        df.set_index(self.get_current_tax_level(), drop=True, inplace=True)
        filename = asksaveasfilename(title = "Select file",filetypes = (("csv","*.csv"),("tab","*.tab")))
        if filename.split('.')[-1] == 'csv':
            sep = ','
        else:
            sep = '\t'
        df.to_csv(filename, sep=sep)
    
    def removeDump(self):
        """ removes the old dump_file """
        if os.path.exists('dump_file'):
            os.remove('dump_file')
            self.parent.destroy()
    
    def AddSamplesToMenu(self):
        """ adds sample names to menu """
        self.samplemenu.delete(0, 'end') 
        for ind, sample in enumerate(self.sample_names):
            self.samplemenu.add_radiobutton(label=sample,
                                            variable=self.sample_index, 
                                            value=ind, 
                                            command=self.ChooseSample)
    
    def ChooseSample(self):
        """ chooses the sample that is displayed """
        sample_name = self.getSampleName()
        self.abundance_df.getSample(sample_name)
        self.parent.title('sample: ' + sample_name)
        self.max_abundance.delete(0, END)
        self.max_abundance.insert(10, '{0:.2f}'.format(self.abundance_df.getMaxAbundanceOfSample()))
        self.update()
        self.searchTaxName(self.species_to_search)
        
    def getSampleName(self):
        """ gets sample to display """
        return self.sample_names[self.sample_index.get()]
    
    def searchTaxName(self, event=None):
        """ searches for species names """
        search_string = event.get().upper().strip()
        search_strings = search_string.split(' ')
        i = 0
        for idx in self.bar_ids:
            tags = self.canvas.gettags(idx)
            if 'orange' in tags:
                self.canvas.itemconfig(idx, outline='orange', width=3)
                self.canvas.focus(idx)
            else:
                self.canvas.itemconfig(idx, outline=tags[0], width=1)
        for index, species in enumerate(self.working_sample.loc[:,self.get_current_tax_level()]):  
            try: species = species.upper()
            except: species = str(species)
            count = 0
            for search_string in search_strings:
                if search_string != '' and search_string in species:
                    count += 1
            if count == len(search_strings):
                self.lbox.itemconfig(index, foreground='red')
                self.canvas.itemconfigure(self.bar_ids[index], outline='red', width=3)
                i+=1
            else:
                self.lbox.itemconfig(index, foreground='black')
            self.tax_name_hits_count.config(text='nuber of hits: '+str(i))    
    
    def set_current_tax_level(self, new_index):
        """ sets the current taxonomy lavel """
        self.tax_lbox.selection_clear(0, END)
        self.tax_lbox.selection_set(new_index)
    
    def QuitProgram(self, *args):
        """ quits the program and dumps """
        dump_dict = {}
        if self.abundance_df is not None:
            dump_dict['abundance_df'] = self.abundance_df
            self.corr_matrix, self.corr_signature = self.abundance_df.get_corr()
            if self.corr_matrix is not None and self.corr_signature[0] == self.abundance_df.getSamplesList:
                dump_dict['corr_matrix'] = self.corr_matrix
                dump_dict['corr_signature'] = self.corr_signature
            if self.sample_names is not None:
                dump_dict['samples'] = self.sample_names
            if self.meta_df is not None:
                dump_dict['meta_df'] = self.meta_df
            if len(self.presets_list) > 1:
                dump_dict['presets'] = self.presets_list
            if self.all_tax_levels is not None:
                dump_dict['all_tax_levels'] = self.all_tax_levels
            if self.sort_list != []:
                dump_dict['sort_list'] = self.sort_list
            if self.abundance_df.groupAbsoluteSamples() is not None:
                dump_dict['abundance_raw_df'] = self.abundance_df.groupAbsoluteSamples()
        if len(dump_dict) > 0:
            DumpParsed('dump_file', dump_dict)
        self.parent.destroy()



def main():
    root = Tk()
    root.title('')
    
    #set window to focus when starting application
    #if platform() == 'Darwin':  # How Mac OS X is identified by Python
    #    #system("""/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "python" to true' """)
    #    pass
    #else:
    #    root.focus_force()
    #if platform() == 'Darwin':
    #    self.os = True
    
    #root.wait_visibility()
    #root.event_generate('<Button-1>', x=0, y=0)    
      
    top = root.winfo_toplevel()
    top.rowconfigure(0,weight=1)
    top.columnconfigure(0, weight=1)
    
    root.rowconfigure(0, weight=2)
    root.columnconfigure(0, weight=2)
    root.rowconfigure(1, weight=1)
    root.columnconfigure(1, weight=1)
    root.minsize(400,300)
    #root.overrideredirect(1)   #removes root border frame (minimize, maximize and close buttons)
    app = Interaction(root)
    #set_window_to_front(root)  #was making the menu bar unresponsive
    root.mainloop()  


if __name__ == '__main__':
    main()  