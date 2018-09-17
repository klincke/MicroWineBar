import os, sys
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import asksaveasfilename
import itertools
import wikipedia
import webbrowser
import pandas as pd
import numpy as np
import Pmw
import tkinter.messagebox as tmb
from decimal import Decimal

#from sklearn import decomposition

from general_functions import *
from platform import system as platform

from displaying2 import DisplayingText
from popupwindow_matplotlib import PopUpIncludingMatplotlib

#import scholar

from random import shuffle

class PopUpGraph():
    def __init__(self, root, all_tax_levels, tax_level2, abundance_df):
        self.root = root
        self.all_tax_levels = all_tax_levels
        self.tax_level2 = tax_level2
        self.abundance_df = abundance_df
        self.HEIGHT = 400
        #self.WIDTH = 800
        self.COLOR_SCHEME = ['deepskyblue', 
                            'forestgreen', 
                            'navy', 
                            'darkgoldenrod', 
                            'steelblue4', 
                            'blue2', 
                            'seagreen', 
                            'hotpink4', 
                            'deeppink4', 
                            'darkolivegreen4', 
                            'turquoise4', 
                            'gold3', 
                            'dodger blue', 
                            'turquoise3', 
                            'mediumorchid4', 
                            'royalblue1', 
                            'red3', 
                            'springgreen3', 
                            'steelblue2', 
                            'darkorange2', 
                            'springgreen4', 
                            'skyblue4', 
                            'firebrick4']
        self.balloon = Pmw.Balloon(self.root)
        #set_window_to_front(self.root)
        fonts_dict = get_fonts()
        self.root.option_add('*Listbox*Font', fonts_dict['listbox_font'])
        self.pcoa_toggle = itertools.cycle([[0,1], [0,2], [1,2]])
        
    def cancel(self, event=None):
        """ destroys/closes pop up windows """
        self.top.destroy()
    
    def change_tax_level_lbox(self, event):
        """ changes the taxnonoic level (chosen in the listbox) """
        if len(event.widget.curselection()) > 0:
            idx = self.all_tax_levels.index(self.current_tax_level)
            tax_list2 = sorted(list(set(self.working_samples[self.all_tax_levels[idx+event.widget.curselection()[0]]])))
            tax_list2 = [x for x in tax_list2 if x != '-']
        else:
            tax_list2 = []
        tax_l_var = StringVar(value=tuple(tax_list2))
        self.sort_lbox.config(listvariable=tax_l_var)
        
#     def compare_groups_old(self, abundance_df):
#         """ compares presence/absence of species in two groups of samples """
#         self.data = abundance_df.getPresenceAbsenceDF(self.threshold.get())
#         self.inner_frame.destroy()
#         self.inner_frame = Frame(self.frame)
#         self.inner_frame.grid(row=6, column=0, columnspan=6)
#         canvas = create_canvas(frame=self.inner_frame, col=0, height=300, width=500, xscroll=False, colspan=2)
#         canvas2 = create_canvas(frame=self.inner_frame, col=3, height=300, width=500, xscroll=False, colspan=2)
#         samples_1 = self.samples_lbox.curselection()
#         samples_2 = self.samples_lbox2.curselection()
#         if len(set(samples_1).intersection(set(samples_2))) > 0:
#             tmb.showinfo(title="error",
#                         message="At least one sample is in both groups.\nPlease select unique samples for the two groups")
#             return
#         else:
#             compare_1 = self.data[self.samples_list[samples_1[0]]]
#             compare_2 = self.data[self.samples_list[samples_2[0]]]
#             print('compare_1')
#             print(compare_1)
#             print(self.data.columns)
#             print(self.data.index)
#             print('self.data.iloc[1,1]')
#             print(self.data.iloc[1,1])
#             for i in samples_1[1:]:
#                 compare_1 = np.where(compare_1 == self.data[self.samples_list[i]], compare_1, -2)
#             for i in samples_2[1:]:
#                 compare_2 = np.where(compare_2 == self.data[self.samples_list[i]], compare_2, -5)
#             compared = np.where(compare_1 == compare_2, compare_1, compare_1+compare_2-3)
#             index_present_both = np.where(compared == 1)[0]
#             index_present_only1 = np.where(compared == -2)[0]
#
#             col = self.data.columns.tolist().index(self.samples_list[samples_1[0]])#1
#             group_1 = []
#             group_2 = []
#             for idx in index_present_only1:
#                 if self.data.iloc[idx,col] == 1:
#                     group_1.append(self.data.index[idx])
#                 else:
#                     group_2.append(self.data.index[idx])
#             if len(group_1)>0 or len(group_2)>0:
#
#                 pass
#             txt = 'only in '+self.samples1_label.get()+':\n\n' + '\n'.join(sorted(group_1))
#             canvas.create_text(10,10, text=txt, tags='renew', anchor=NW)
#             canvas.config(scrollregion=[canvas.bbox(ALL)[0], canvas.bbox(ALL)[1], 500, canvas.bbox(ALL)[3]])
#             txt = 'only in '+self.samples1_label.get()+':\n\n' + '\n'.join(sorted(group_2))
#             canvas2.create_text(10,10, text=txt, tags='renew', anchor=NW)
#             canvas2.config(scrollregion=[canvas2.bbox(ALL)[0], canvas2.bbox(ALL)[1], 500, canvas2.bbox(ALL)[3]])
        
            
    def compare_groups(self, abundance_df, all_samples=True):
        """ compares presence/absence of species in two groups of samples """
        self.data = abundance_df.getPresenceAbsenceDF(self.threshold.get())
        self.inner_frame.destroy()
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=6, column=0, columnspan=6)
        canvas = create_canvas(frame=self.inner_frame, col=0, height=300, width=500, xscroll=False, colspan=2)
        canvas2 = create_canvas(frame=self.inner_frame, col=3, height=300, width=500, xscroll=False, colspan=2)
        samples_1_idx = self.samples_lbox.curselection()
        samples_2_idx = self.samples_lbox2.curselection()
        if len(set(samples_1_idx).intersection(set(samples_2_idx))) > 0:
            tmb.showinfo(title="error", 
                        message="At least one sample is in both groups.\nPlease select unique samples for the two groups")
            return
        else:

            samples_1 = [self.samples_list[idx] for idx in samples_1_idx]
            samples_2 = [self.samples_list[idx] for idx in samples_2_idx]
            in_samples_1 = set(self.data[self.data[samples_1].sum(axis=1)>0].index)
            in_samples_2 = set(self.data[self.data[samples_2].sum(axis=1)>0].index)
            if all_samples:
                in_samples_1 = set(self.data[self.data[samples_1].sum(axis=1)==len(samples_1)].index)
                in_samples_2 = set(self.data[self.data[samples_2].sum(axis=1)==len(samples_2)].index)
            else:
                in_samples_1 = set(self.data[self.data[samples_1].sum(axis=1)>0].index)
                in_samples_2 = set(self.data[self.data[samples_2].sum(axis=1)>0].index)
            txt = 'only in '+self.samples1_label.get()+':\n\n' + '\n'.join(sorted(in_samples_1 - in_samples_2)) 
            canvas.create_text(10,10, text=txt, tags='renew', anchor=NW)
            canvas.config(scrollregion=[canvas.bbox(ALL)[0], canvas.bbox(ALL)[1], 500, canvas.bbox(ALL)[3]])
            txt = 'only in '+self.samples2_label.get()+':\n\n' + '\n'.join(sorted(in_samples_2 - in_samples_1))
            canvas2.create_text(10,10, text=txt, tags='renew', anchor=NW)
            canvas2.config(scrollregion=[canvas2.bbox(ALL)[0], canvas2.bbox(ALL)[1], 500, canvas2.bbox(ALL)[3]])
            
            
            
    def compare_groups_of_samples(self, abundance_df, samples_list, tax_level):
        """ creates two listboxes with samples for comparing """
        self.create_window()
        self.tax_level = tax_level
        self.top.title('compare 2 groups of samples on ' + tax_level + ' level')
        self.samples_list = samples_list
        
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=7, column=0, columnspan=4)
        
        samples_var = StringVar(value=tuple(samples_list))
        yscroll = Scrollbar(self.frame, orient=VERTICAL)
        yscroll.grid(row=1, column=2, sticky = 'NW' + 'SW')
        self.samples1_label = StringVar()
        self.samples1_label.set('group1')
        samples1_label = Entry(self.frame, textvariable=self.samples1_label)
        samples1_label.grid(row=0, column=0)
        self.samples_lbox = Listbox(self.frame, height=7, width=45, listvariable=samples_var, selectmode='extended', yscrollcommand=yscroll.set, exportselection=0)
        self.samples_lbox.grid(row=1, column=0, columnspan=2)
        yscroll.config(command=self.samples_lbox.yview)
        yscroll2 = Scrollbar(self.frame, orient=VERTICAL)
        yscroll2.grid(row=1, column=5, sticky = 'NW' + 'SW')
        self.samples2_label = StringVar()
        self.samples2_label.set('group2')
        samples2_label = Entry(self.frame, textvariable=self.samples2_label)
        samples2_label.grid(row=0, column=3)
        self.samples_lbox2 = Listbox(self.frame, height=7, width=45, listvariable=samples_var, selectmode='extended', yscrollcommand=yscroll2.set, exportselection=0)
        self.samples_lbox2.grid(row=1, column=3, columnspan=2)
        yscroll2.config(command=self.samples_lbox2.yview)

        working_samples = abundance_df.groupAllSamples(tax_level)
        working_samples.set_index(tax_level, drop=False, inplace=True)
        presence_frame = LabelFrame(self.frame, text='compare presence/absence', padx=10, pady=2)
        presence_frame.grid(row=2, column=0, columnspan=4)
        
        self.threshold = DoubleVar()
        self.threshold.set(0.00)
        threshold_label = Label(presence_frame, text='threshold:')
        threshold_label.grid(row=0, column=0, padx=5, pady=2)
        threshold_spinbox = Spinbox(presence_frame, from_=0, to=10, increment=0.01, textvariable=self.threshold, width=10)
        threshold_spinbox.grid(row=0, column=1, padx=5, pady=2)#, columnspan=1)
        
        compare_one_button = Button(presence_frame, text='present in at least 1 sample', command=lambda abundance_df=abundance_df, all_samples=False: self.compare_groups(abundance_df, all_samples))
        compare_one_button.grid(row=0, column=3, padx=5, pady=2)
        compare_all_button = Button(presence_frame, text='present in all samples', command=lambda abundance_df=abundance_df , all_samples=True: self.compare_groups(abundance_df, all_samples))
        compare_all_button.grid(row=0, column=4, padx=5, pady=2)
        
        graph_button = Button(self.frame, text='create 2 line graphs', command=lambda working_samples=working_samples, graph='line' : self.graph_groups(working_samples, graph))
        graph_button.grid(row=2, column=4)
        
        fsel_frame = LabelFrame(self.frame, text='', padx=10, pady=2)
        fsel_frame.grid(row=3, column=0, columnspan=5)
        
        self.feature_selction_var = IntVar()
        feature_selction_check_button = Checkbutton(fsel_frame, text='feature selection', variable=self.feature_selction_var)
        feature_selction_check_button.grid(row=0, column=0, padx=5, pady=2)
        if len(samples_list) < 50:
            random_forest_button = Button(fsel_frame, text='random forest', state=DISABLED, command=self.calculate_classification)
        
        else:
            random_forest_button = Button(fsel_frame, text='random forest', command=self.calculate_classification)
        random_forest_button.grid(row=0, column=4, padx=5, pady=2)
        
        deseq_button = Button(fsel_frame, text='DESeq2', command=self.deseq2)
        self.balloon.bind(deseq_button, 'differential abundance analysis based on DESeq2')
        deseq_button.grid(row=0, column=5, padx=5, pady=2)
        
        ancom_button = Button(fsel_frame, text='ANCOM', command=self.ancom)
        self.balloon.bind(ancom_button, 'ANalysis of COmposition of Microbiomes for differential abundance')
        ancom_button.grid(row=0, column=6, padx=5, pady=2)
        
        correlation_frame = LabelFrame(self.frame, text='correlation', padx=10, pady=2)
        correlation_frame.grid(row=4, column=0, columnspan=3)
        
        corr_r_threshold_label = Label(correlation_frame, text='threshold:')
        corr_r_threshold_label.grid(row=0, column=1, padx=5, pady=2)
        self.corr_r_threshold = Scale(correlation_frame, from_=0.0, to=1.0, orient=HORIZONTAL, length=50, resolution=0.1)
        self.corr_r_threshold.grid(row=0, column=3, padx=5, pady=2)
        self.corr_r_threshold.set(0.5)
        corr_button = Button(correlation_frame, text='calculate', command=self.correlation_groups)   #time series?
        corr_button.grid(row=0, column=0, padx=5, pady=2)
        corr_filter_button = Button(correlation_frame, text='filter', command=self.correlation_groups_filter)
        corr_filter_button.grid(row=0, column=4, padx=5, pady=2)
        
        pca_button = Button(fsel_frame, text='PCA', command=self.pca)
        self.balloon.bind(pca_button, 'PCA based on isometric log ratio of the count data')
        pca_button.grid(row=0, column=2, padx=5, pady=2)
        pcoa_button = Button(fsel_frame, text='PCoA (Bray-Curtis)', command=self.pcoa)
        self.balloon.bind(pcoa_button, 'Principal Coordindate analysis scatter plot based on Bray-Curtis dissimilarity')
        pcoa_button.grid(row=0, column=1, padx=5, pady=2)
        
        diversity_frame = LabelFrame(self.frame, text='diversity', padx=10, pady=2)
        diversity_frame.grid(row=4, column=3, columnspan=2)
        
        wilcoxon_button = Button(fsel_frame, text='wilcoxon', command=self.wilcoxon_ranksum_test)
        self.balloon.bind(wilcoxon_button, 'nonprametrical Wilcoxon rank sum test')
        wilcoxon_button.grid(row=0, column=3, padx=5, pady=2)
        
        richness_button = Button(diversity_frame, text='richness', command=self.richness_groups)
        richness_button.grid(row=0, column=0, padx=5, pady=2)
        shannon_diversity_button = Button(diversity_frame, text='Shannon diversity', command=self.shannon_diversity_groups)
        shannon_diversity_button.grid(row=0, column=1, padx=5, pady=2)
    
    def create_overview_line(self, working_samples, samples_list, tax_level):
        """ creates the overview line graph """
        self.create_window()
        if len(samples_list)<2:
            tmb.showinfo(title="error", message='not enough samples')
            return
        elif len(samples_list) > 25:
            tmb.showinfo(title="error", message='too many samples')
            return
        self.top.title('overview of all samples on ' + tax_level + ' level')
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=2, column=0, columnspan=4)
        self.create_overview_line_graph(working_samples, samples_list, tax_level)
    
    
    def writeCsv(event, df):
        filename = asksaveasfilename(title = "Select file",filetypes = (("csv","*.csv"),("tab","*.tab")))
        if filename.split('.')[-1] == 'csv':
            sep = ','
        else:
            sep = '\t'
        df.transpose().to_csv(filename, sep=sep, header=['richness', 'shannon index'], index_label='sample name')
    

    def create_overview_line_graph(self, working_samples, samples_list, tax_level, height=400, width=600, row=0, xscroll=False, yscroll=False):
        """ create line graph and list of samples displayed in graph """
        #canvas = self.create_canvas(frame=self.inner_frame, row=row+0, height=120, width=600, yscroll=False, xscroll=False)
        canvas = create_canvas(frame=self.inner_frame, row=row+0, height=140, width=width, yscroll=False, xscroll=False, take_focus=True)
        #canvas_list = self.create_canvas(frame=self.inner_frame, row=row+2, height=15, width=600, xscroll=False)
        #canvas_list = create_canvas(frame=self.inner_frame, row=row+2, height=10, width=width, xscroll=False)
        displaying_text = DisplayingText(self.root, canvas)
        if len(samples_list)> 20:
            width = 1000
        width = round(width/(len(samples_list)-1))
        max_height = working_samples.max(numeric_only=True).max()
        for j, sample in enumerate(samples_list[:-1]):
            x1 = j * width + 70
            x2 = (j+1) * width + 70
            for i, idx in enumerate(working_samples.index):
                idx = working_samples.index[i]
                y1 = height - working_samples.loc[idx, sample]/max_height*height
                y2 = height - working_samples.loc[idx, samples_list[j+1]]/max_height*height
                coords = (x1, y1, x2, y2)
                col = getColor(i, self.COLOR_SCHEME)
                tag = working_samples.loc[idx, tax_level]
                item = canvas.create_line(coords, width=3, fill=col, tags=tag)
                self.balloon.tagbind(canvas, item, tag)
            #canvas.create_text(70+j*width,height+30, text=str(j+1))
            displaying_text.drawText(sample, j, 70+j*width, height+30)
        
        displaying_text.drawText(samples_list[-1], len(samples_list)-1, 70+(len(samples_list)-1)*width-10, height+30)
        canvas.create_line(70, 0, 70, height)
        canvas.create_line(70, 
                            height, 
                            (len(samples_list)-1)*width + 70, 
                            height)                    
        for j in range(0,int(height),50):
            canvas.create_line(65, 
                                height-j, 
                                70, 
                                height-j)
            canvas.create_text(40, 
                                height-j, 
                                text='{0:.2f}'.format(float(j)/height*max_height))

        all_covered = canvas.bbox(ALL)
        canvas.config(height=all_covered[3]-all_covered[1], width=all_covered[2]-all_covered[0])
        canvas.config(scrollregion=canvas.bbox(ALL))
        #self.create_overview_list(samples_list, canvas_list)
        #canvas_list.config(height=120)
    
    def create_overview_scaled_bar(self, working_samples, samples_list, current_tax_level):
        """ creates the overview bar graph """
        self.first_stacked_bar = True
        self.working_samples = working_samples
        self.current_tax_level = current_tax_level
        self.new_samples_list = list(samples_list)
        self.all_sample_names = list(samples_list)
        
        self.create_window()
        #self.inner_frame = Frame(self.frame)
        #self.inner_frame.grid(row=0, column=0, columnspan=4)
        #popup_canvas = self.create_canvas(xscroll=False)
        popup_canvas = create_canvas(frame=self.frame, xscroll=False, yscroll=False, colspan=12, take_focus=True)
        #popup_canvas = self.create_canvas(frame=self.inner_frame)
        #canvas_list = self.create_canvas(frame=self.inner_frame)
        #canvas_list = self.create_canvas(row=2, height=120, xscroll=False)
        #canvas_list = create_canvas(frame=self.frame, row=2, height=100, xscroll=False, colspan=3)
        #canvas_list = create_canvas(frame=self.frame, row=2, height=100, width=300, xscroll=False, colspan=9, rowspan=2)
        self.samples_lbox = Listbox(self.frame, 
                                listvariable=StringVar(value=tuple(samples_list)),
                                height=5,
                                width=50,
                                selectmode='extended',
                                exportselection=0)
        self.samples_lbox.grid(row=2, column=0, columnspan=9, rowspan=2)
        #reset_sort_button = Button(self.frame, text='reset ordering', command=lambda canvas=popup_canvas, canvas_list=canvas_list: self.sort_bars_time(canvas, canvas_list))
        
        select_samples_button = Button(self.frame, text='select samples', command=lambda canvas=popup_canvas : self.select_samples_for_stacked_bargraph(canvas))
        select_samples_button.grid(row=2, column=10)
        reset_sort_button = Button(self.frame, text='reset ordering', command=lambda canvas=popup_canvas: self.sort_bars_time(canvas))
        reset_sort_button.grid(row=3, column=10)
        
        #reset_samples_button = Button(self.frame, text='include all samples', command=lambda canvas=popup_canvas, canvas_list=canvas_list: self.reset_to_all_samples(canvas, canvas_list))
        #reset_samples_button = Button(self.frame, text='include all samples', command=lambda canvas=popup_canvas: self.reset_to_all_samples(canvas))
        #reset_samples_button.grid(row=3, column=10)
        self.top.title('overview of all samples on ' + current_tax_level + ' level')
        #HEIGHT = 400
        #WIDTH = 800
        #if len(samples_list)> 20:
        #    WIDTH = 1000
        #width = round((WIDTH-70)/len(samples_list))

        #self.stacked_bar_graph(popup_canvas, [], samples_list, canvas_list)
 #       #self.stacked_bar_graph(popup_canvas, [], samples_list)
        #self.create_overview_list(samples_list, canvas_list, tags="renew")
        #if canvas_list.bbox(ALL)[3] < 100:
        #    canvas_list.config(height=canvas_list.bbox(ALL)[3])
        

        #all_covered = popup_canvas.bbox(ALL)
        #popup_canvas.config(height=all_covered[3]-all_covered[1], width=all_covered[2]-all_covered[0])

        tax_l = StringVar(value=tuple(self.all_tax_levels[self.all_tax_levels.index(current_tax_level):]))
        self.tax_level_lbox = Listbox(self.frame, height=7, width=20, listvariable=tax_l, selectmode='browse', exportselection=0)
        self.tax_level_lbox.grid(row=4, column=0, columnspan=5)
        self.tax_level_lbox.bind("<<ListboxSelect>>", self.change_tax_level_lbox)
        
        tax_list2 = []
        tax_l_var = StringVar(value=tuple(tax_list2))
        yscroll = Scrollbar(self.frame, orient=VERTICAL)
        yscroll.grid(row=4, column=11, sticky = 'NW' + 'SW')
        self.sort_lbox = Listbox(self.frame, height=7, width=50, listvariable=tax_l_var, selectmode='browse', yscrollcommand=yscroll.set, exportselection=0)
        self.sort_lbox.grid(row=4, column=5, columnspan=6)
        yscroll.config(command=self.sort_lbox.yview)
        #self.sort_lbox.bind("<<ListboxSelect>>", lambda event, popup_canvas=popup_canvas, canvas_list=canvas_list : self.sort_bars(popup_canvas, canvas_list))
        self.sort_lbox.bind("<<ListboxSelect>>", lambda event, popup_canvas=popup_canvas : self.sort_bars(popup_canvas))
        self.sort_lbox.bind("<Button-2>", lambda event, canvas=popup_canvas : self.highlight_bars_black(event, canvas))
        
    def select_samples_for_stacked_bargraph(self, canvas):   
        """ selects samples for the stacked bar graph """
        self.selected_samples_dict = dict(zip(self.all_sample_names, [True]*len(self.all_sample_names)))
        selected_samples = [self.all_sample_names[i] for i in self.samples_lbox.curselection()]
        try:
            if len(selected_samples)>10:
                raise ValueError("no more than 10 samples can be chosen for the stacked bar graph")
            if self.new_samples_list != selected_samples:
                self.first_stacked_bar = True
            self.new_samples_list = selected_samples
            if self.first_stacked_bar:
                #self.stacked_bar_graph(canvas, [], self.all_sample_names)
                self.stacked_bar_graph(canvas, [], selected_samples)
                #self.first_stacked_bar = False
            indexes = self.samples_lbox.curselection()
            for i in range(len(self.all_sample_names)):
                if i not in indexes:
                    self.selected_samples_dict[self.all_sample_names[i]] = False
            if not self.first_stacked_bar:
                self.redraw_bars(canvas)
            self.first_stacked_bar = False
        except ValueError as error:
            tmb.showinfo(title="error", message=error)
        
    def highlight_bars_black(self, event, canvas):
        """ hilights bars of the stacked bargraph """
        widget = event.widget
        ind = widget.nearest(event.y)
        org =  self.sort_lbox.get(ind)
        indexes = canvas.find_withtag(org.replace(' ', '_'))
        canvas.delete('black')
        for ind in indexes:
            coords = canvas.coords(ind)
            canvas.create_rectangle(coords, outline='black', width=4, tags=('renew','black'))
            
    
    def create_window(self):
        """ creates a popup window """
        self.top = Toplevel(self.root)
        self.top.protocol("WM_DELETE_WINDOW", self.cancel)
        self.top.attributes("-topmost", 1)
        self.top.attributes("-topmost", 0)
        self.top.columnconfigure(0, weight=1)
        self.top.rowconfigure(0, weight=1)
        self.frame = Frame(self.top)
        self.frame.grid(row=0, column=0, sticky=N+S+W+E)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        #self.top.title(self.name)
        self.top.focus_set()
        
    
    def graph_groups(self, working_samples, graph):
        """ creates 2 line graphs, one for each group """
        self.inner_frame.destroy()
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=6, column=0, columnspan=6)

        samples_1 = [self.samples_list[idx] for idx in self.samples_lbox.curselection()]
        samples_2 = [self.samples_list[idx] for idx in self.samples_lbox2.curselection()]
        if len(set(samples_1).intersection(set(samples_2))) > 0:
            tmb.showinfo(title='error', message='cannot compare samples that are in both groups at the same time')
            return
        elif len(samples_1) > 25 or len(samples_2)> 25:
            tmb.showinfo(title='error', message='too many samples in (at least) one group')
            return
        else:
            if graph == 'line':
                self.create_overview_line_graph(working_samples, samples_1, 'species', height=140, width=750, row=0)
                self.create_overview_line_graph(working_samples, samples_2, 'species', height=140, width=750, row=3)
            else:
                self.create_overview_bar_graph(working_samples, samples_1, 'species', height=140, width=750, row=0)
                self.create_overview_bar_graph(working_samples, samples_2, 'species', height=140, width=750, row=3)
            #self.add_title_to_canvas()    
    
    def create_overview_list(self, samples_list, canvas, tags=None):
        """ creates of species names which are displayed in a graph """
        canvas.create_text(20, 0, text='number\t sample name', anchor=NW)
        for i, sample in enumerate(samples_list):
            canvas.create_text(30, (i+1)*15, text=str(i+1) + '\t' + sample, anchor=NW, tags=tags)
        canvas.config(scrollregion=canvas.bbox(ALL))
        #canvas.config(height=80)
    
    def stacked_bar_graph(self, popup_canvas, indexes, samples_list):
        """ creates the stacked bar graph (bars etc.) """
        popup_canvas.delete("all")
        HEIGHT = 400
        WIDTH = 800
        if len(self.new_samples_list) > 20:
            WIDTH = 1300
        self.width = round((WIDTH-80)/(len(self.new_samples_list)+1))-10
        max_height = self.working_samples.sum(axis=0, numeric_only=True).max()
        self.stacked_bar_dict = {}
        self.frames_height_dict = {}
        self.displaying_height = DisplayingText(self.root, popup_canvas)
        for j, sample in enumerate(samples_list):
            self.stacked_bar_dict[sample] = {}
            sample_height = self.working_samples.sum(axis=0, numeric_only=True)[sample]
            y1 = HEIGHT #+ 10
            x1 = j * self.width + 70
            x2 = (j+1) * self.width + 70
            highlight_height = 0
            for i, idx in enumerate(self.working_samples.index):
                y2 = y1
                y1 = y1 - self.working_samples.loc[idx, sample]*HEIGHT/sample_height
                coords = (x1, y1, x2, y2)
                col = getColor(i, self.COLOR_SCHEME)
                if self.working_samples.loc[idx,'colour'] != 'undefined':
                    col = self.working_samples.loc[idx,'colour']
    
                #tax_list = list(self.working_samples.loc[idx,:samples_list[0]])[:-1]
                tag = self.working_samples.loc[idx, self.current_tax_level]
                if idx in indexes:
                    highlight_height += self.working_samples.loc[idx, sample]*HEIGHT/sample_height
                #b = BarBox(canvas=popup_canvas, coords=coords, color=col, name=tag, root=self.root)
                b = BarBox(self.root, samples_list, self.abundance_df, self.all_tax_levels)
                item = b.drawBar(canvas=popup_canvas, coords=coords, color=col, name=tag, sample=sample)
                #item = popup_canvas.create_rectangle(coords, outline=col, fill=col, tags=tag.replace(' ','_'))
                #self.balloon.tagbind(popup_canvas, item, tag)
                #popup_info = PopUpInfo(self.root, tag, tax_list, self.all_tax_levels)
                #popup_canvas.tag_bind(item, '<Command-Button-2>', lambda event, new_bool=1: popup_info.do_popup(event, new_bool))
                #popup_canvas.tag_bind(item, '<Button-2>', lambda event, new_bool=0: popup_info.do_popup(event, new_bool))
                item_height = self.working_samples.loc[idx, sample]*HEIGHT/sample_height
                self.stacked_bar_dict[sample][idx] = (item, item_height)
            if highlight_height != 0:
                tag = idx.replace(' ', '_')
                popup_canvas.create_rectangle((x1, HEIGHT-highlight_height, x2, HEIGHT), outline='red', width=4, tags='renew') 
            height2 = self.working_samples.sum(axis=0, numeric_only=True)[sample]*50/max_height
            self.frames_height_dict[sample] = height2
            coords2 = (70+j*self.width, HEIGHT+60-height2, 70+(j+1)*self.width, HEIGHT+60)
            #item = popup_canvas.create_rectangle(coords2, fill='forestgreen', tags=('renew', sample))
            self.displaying_height.drawHeight(coords2, sample)
            #if platform() == 'Windows':  #windows
            #    popup_canvas.tag_bind(item, '<Button-3>', lambda event, canvas=popup_canvas, sample=sample, canvas_list=canvas_list: self.removeSample(event, canvas, sample, canvas_list))
            #else:
            #    popup_canvas.tag_bind(item, '<Button-2>', lambda event, canvas=popup_canvas, sample=sample, canvas_list=canvas_list: self.removeSample(event, canvas, sample, canvas_list))
            #b.drawBox(canvas=popup_canvas, coords=coords2, color='forestgreen', sample=sample)
            popup_canvas.create_text(70+(j+0.5)*self.width,HEIGHT+80, text=str(j+1), anchor=NW)
            #popup_canvas.create_text(20, HEIGHT+110+(j+1)*15, text=str(j+1) + '\t' + sample, tags='renew', anchor=NW)#, justify=CENTER)
        popup_canvas.create_line(70, 0, 70, HEIGHT)
        popup_canvas.create_line(70, 
                                HEIGHT, 
                                #len(self.new_samples_list)*self.width + 70, 
                                len(samples_list)*self.width + 70, 
                                HEIGHT)
        popup_canvas.create_line(70, 
                                HEIGHT+60, 
                                #len(self.new_samples_list)*self.width + 70, 
                                len(samples_list)*self.width + 70, 
                                HEIGHT+60)
        popup_canvas.create_line(70, HEIGHT+10, 70, HEIGHT+60)
        popup_canvas.create_text(20, HEIGHT+40, text='actual \nheight', anchor=NW)
        #popup_canvas.create_text(20, HEIGHT+110, text='number\t sample name', anchor=NW)
        n = 10
        idx = 0
        for j in range(0, HEIGHT, int(HEIGHT/n)):
            popup_canvas.create_line(65, 
                                        HEIGHT-j, 
                                        70, 
                                        HEIGHT-j)
            popup_canvas.create_text(40, 
                                        HEIGHT-j, 
                                        text=str(idx) + '%')
            idx += 10
        all_covered = popup_canvas.bbox(ALL)
        popup_canvas.config(height=all_covered[3]-all_covered[1], width=all_covered[2]-all_covered[0])
        
    def redraw_bars(self, canvas, new_samples_list=None):
        """ redraws the bars in the stacked bar graph """
        if new_samples_list is None:
            new_samples_list = self.new_samples_list
        canvas.delete("renew")

        
        for i, sample in enumerate(self.new_samples_list):
        #for i, sample in enumerate(new_samples_list):
            old_start_height = self.HEIGHT
            x1 = 70+i*self.width
            x2 = 70+(i+1)*self.width
            for idx in self.working_samples.index:
                item = self.stacked_bar_dict[sample][idx][0]
                new_coords = (x1, old_start_height, x2, old_start_height-self.stacked_bar_dict[sample][idx][1])
                old_start_height -= self.stacked_bar_dict[sample][idx][1]
                canvas.coords(item, new_coords)
            new_coords2 = (x1, self.HEIGHT+60, x2, self.HEIGHT+60-self.frames_height_dict[sample])    
            #item = canvas.create_rectangle(new_coords2, fill='forestgreen', tags='renew') 
            self.displaying_height.drawHeight(new_coords2, sample)
            #if platform() == 'Windows':  #windows
            #    canvas.tag_bind(item, '<Button-3>', lambda event, canvas=canvas, sample=sample, canvas_list=canvas_list: self.removeSample(event, canvas, sample, canvas_list))
            #else:
            #    canvas.tag_bind(item, '<Button-2>', lambda event, canvas=canvas, sample=sample, canvas_list=canvas_list: self.removeSample(event, canvas, sample, canvas_list))
            #if heights_series[sample] != 0:
            #    canvas.create_rectangle((x1, (1-heights_series[sample])*self.HEIGHT, x2, self.HEIGHT), outline='red', width=4, tags='renew')     
        #self.highlight_bars(heights_series, canvas, 'red')
        #self.create_overview_list(self.new_samples_list, canvas_list, tags='renew')
        
    def highlight_bars(self, heights_series, canvas, color):
        """ hightlights the bars in colour """
        for i, sample in enumerate(self.new_samples_list):
            x1 = 70+i*self.width
            x2 = 70+(i+1)*self.width
            if heights_series[sample] != 0:
                canvas.create_rectangle((x1, (1-heights_series[sample])*self.HEIGHT, x2, self.HEIGHT), outline=color, width=4, tags=('renew', color))     
    
    def sort_bars(self, canvas):
        """ sorts bars and redraws them """
        heights_series = self.sort_bars1(canvas)
        self.redraw_bars(canvas, list(heights_series.index))
        self.highlight_bars(heights_series, canvas, 'red')
        
    def reset_to_all_samples(self, canvas):
        """ resets the stacked bar graph to include all samples """
        self.new_samples_list = list(self.all_sample_names)
        self.redraw_bars(canvas)
    
            
    def sort_bars1(self, canvas):
        """ resorts the bars of the stacked bargraph """
        org = self.sort_lbox.get(self.sort_lbox.curselection()[0])
        level = self.tax_level_lbox.get(self.tax_level_lbox.curselection()[0])
        indexes = self.working_samples[self.working_samples[level] == org].index.tolist()
        series = pd.Series([0.0]*len(self.all_sample_names), index=self.all_sample_names)

        first_df = self.working_samples.loc[indexes,:]
        for idx in indexes:
            series = series.add(self.working_samples.loc[idx, self.all_sample_names])

        series = series.divide(self.working_samples.sum(axis=0, numeric_only=True)[:-1])
        series.sort_values(inplace=True)
        self.working_samples.drop(indexes, inplace=True)
        result = pd.concat([first_df, self.working_samples])
        num_of_tax_levels = len(self.all_tax_levels[self.all_tax_levels.index(self.current_tax_level):])
        cols = self.working_samples.columns.tolist()[:num_of_tax_levels-1] + series.index.tolist() + ['masked']
        self.working_samples = result.reindex_axis(cols, axis=1)#, copy=False)
        #self.new_samples_list = series.loc[self.new_samples_list].index.tolist()
        new_samples = []
        for sample1 in series.index:
            if sample1 in self.new_samples_list:
                new_samples.append(sample1)
            #else:
            #    series.drop(sample1, inplace=True)
        self.new_samples_list = new_samples
        #self.redraw_bars(series, canvas, canvas_list)
        return series
        #self.highlight_bars(heights_series, canvas, 'red')
        
    def sort_bars_time(self, canvas):
        """ sorts the bars in the stacked bar graph alphabetically (original order) """
        series = pd.Series(np.array(range(len(self.all_sample_names))), index=sorted(self.all_sample_names))
        num_of_tax_levels = len(self.all_tax_levels[self.all_tax_levels.index(self.current_tax_level):])
        cols = self.working_samples.columns.tolist()[:num_of_tax_levels-1] + series.index.tolist() + ['masked']
        self.working_samples = self.working_samples.reindex_axis(cols, axis=1)
        new_samples = []
        for sample1 in series.index:
            if sample1 in self.new_samples_list:
                new_samples.append(sample1)
        self.new_samples_list = new_samples
        self.redraw_bars(canvas)
        
     
    def scatter_plot_window(self, samples):
        """ creates a scatter plot pop up window """
        self.create_window()
        self.top.title('scatter plot')
        
        self.samples_lbox = Listbox(self.frame, selectmode='extended', exportselection=0, height=7, listvariable=StringVar(value=tuple(samples)), width=60)
        self.samples_lbox.grid(column=1, row=1, sticky='nswe')
        samples_scroll = Scrollbar(self.frame, orient=VERTICAL, command=self.samples_lbox.yview)
        samples_scroll.grid(column=2, row=1, sticky = 'NW' + 'SW')
        self.samples_lbox.config(yscrollcommand=samples_scroll.set)
        
        df = self.abundance_df.getDataframe()
        df = df.loc[df.max(axis=1, numeric_only=True)>=0.01,:]
        df.index = list(df['species'])
        species_list = sorted(list(df.loc[:, 'species']))
        self.species_lbox = Listbox(self.frame, selectmode='extended', exportselection=0, height=7, listvariable=StringVar(value=tuple(species_list)), width=50)
        self.species_lbox.grid(column=3, row=1, sticky='nswe')
        species_scroll = Scrollbar(self.frame, orient=VERTICAL, command=self.species_lbox.yview)
        species_scroll.grid(column=4, row=1, sticky = 'NW' + 'SW')
        self.species_lbox.config(yscrollcommand=species_scroll.set)
        
        plot_button = Button(self.frame, text='plot', command=lambda samples=samples, species_list=species_list, df=df: self.plot_scatter_plot(samples, species_list, df))
        plot_button.grid(column=1, row=2)
        
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=6, column=0, columnspan=4)

    def draw_scatter_plot(self, canvas, species1, species2, abundance1, abundance2, samples, colours=None):
        """ draws a scatter plot """
        
        if colours is None:
            colours = ['black']*len(samples)
        
        abundance1_min = min(abundance1)
        abundance1_max = max(abundance1)
        abundance2_min = min(abundance2)
        abundance2_max = max(abundance2)
        compensate_ab1 = 0
        if abundance1_min < 0:
            compensate_ab1 = - abundance1_min
        compensate_ab2 = 0
        if abundance2_min < 0:
            compensate_ab2 = - abundance2_min
        eps = 0.0001
        new_abundance1_max = (abundance1_max - abundance1_min + eps) * 1.1
        new_abundance2_max = (abundance2_max - abundance2_min + eps) * 1.1
        
        top_space = 20
        HEIGHT = 400 -top_space
        WIDTH = 400 -top_space
        height = HEIGHT - 50
        width = WIDTH - 50
        r = 3
        
        displaying_sample_name = DisplayingText(self.root, canvas)
        
        for i, sample in enumerate(samples):
            x = 50 + (compensate_ab1+abundance1[i])/new_abundance1_max*height
            y = top_space+height - (compensate_ab2+abundance2[i])/new_abundance2_max*height
            #canvas.create_oval(x-r, y-r, x+r, y+r)
            displaying_sample_name.drawCircle((x-r, y-r, x+r, y+r), sample, colour=colours[i])
            canvas.create_line(50, top_space+0, 50, top_space+height)
            canvas.create_line(50, top_space+height, WIDTH, top_space+height)
            #for j in xrange(0, int(height), 50):
            #    canvas.create_line((45, top_space+height-j, 50, top_space+height-j))
            #    #canvas.create_text(0, top_space+height-j, text='{0:.2f}'.format(float(j)/height*abundance2_max), anchor=NW)
            #for j in xrange(0, int(width), 50):
            #    canvas.create_line(50+j, top_space+height, 50+j, top_space+height+5)
            #    #canvas.create_text(50+j, top_space+height+10, text='{0:.2f}'.format(float(j)/height*abundance1_max), anchor=NW)
        for n, j in enumerate(np.linspace(abundance2_min, abundance2_max, num=7)):
            n *= 50
            canvas.create_line((45, top_space+height-n, 50, top_space+height-n))
            canvas.create_text(0, top_space+height-n, text='{0:.2f}'.format(j), anchor=NW)
            #print(float(j)/height*abundance2_max)
        for n, j in enumerate(np.linspace(abundance1_min, abundance1_max, num=7)):
            n *= 50
            canvas.create_line(50+n, top_space+height, 50+n, top_space+height+5)
            canvas.create_text(50+n, top_space+height+10, text='{0:.2f}'.format(j), anchor=NW)
            
        canvas.create_text(0, 0, text=species2, anchor=NW)
        canvas.create_text(WIDTH, top_space+height, text=species1, anchor=NW)
        canvas.config(scrollregion=canvas.bbox(ALL))   
         
    
    def plot_scatter_plot(self, samples, species_list, df):
        """ prepares the scatter plot and renews it """
        self.inner_frame.destroy()
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=6, column=0, columnspan=4)
        canvas = create_canvas(frame=self.inner_frame, xscroll=False, yscroll=False, colspan=2, take_focus=True)
        try:
            selected_samples = [samples[idx] for idx in self.samples_lbox.curselection()]
        except:
            print('error')
        try: 
            if len(self.species_lbox.curselection()) != 2:
                raise ValueError('Exactly two species are needed for the scatter plot')
        except ValueError as error:
            print('The exceptions is:' + str(error))
        species1 = species_list[self.species_lbox.curselection()[0]]
        species2 = species_list[self.species_lbox.curselection()[1]]
        abundance1 = df.loc[species1, selected_samples]
        abundance2 = df.loc[species2, selected_samples]
        self.draw_scatter_plot(canvas, species1, species2, abundance1, abundance2, selected_samples)
        
    def corr(self, samples, highest_taxlevel, abundance_df):
        """ correlation """
        self.create_window()
        self.top.title('correlation')
        self.corr_results_dict = None
        fonts_dict = get_fonts()
        tax_level_label = Label(self.frame, text='taxonomic level:')
        tax_level_label.grid(column=0, row=1)
        self.tax_level_lbox = Listbox(self.frame, selectmode='browse', exportselection=0, height=7, listvariable=StringVar(value=tuple(self.all_tax_levels)))
        #, width=20
        self.tax_level_lbox.grid(column=1, row=1, columnspan=2, sticky='NESW')
        tax_level_scroll = Scrollbar(self.frame, orient=VERTICAL, command=self.tax_level_lbox.yview)
        tax_level_scroll.grid(column=3, row=1, sticky = 'NW' + 'SW')
        self.tax_level_lbox.config(yscrollcommand=tax_level_scroll.set)
        superfamily_label = Label(self.frame, text='groups:')# (' +  + ')')
        superfamily_label.grid(column=0, row=2)
        self.superfamily_lbox = Listbox(self.frame, selectmode='multiple', exportselection=0, height=5, listvariable=StringVar(value=tuple(sorted(highest_taxlevel))))
        self.superfamily_lbox.grid(column=1, row=2, columnspan=2, sticky='NESW')
        superfamily_scroll = Scrollbar(self.frame, orient=VERTICAL, command=self.superfamily_lbox.yview)
        superfamily_scroll.grid(column=3, row=2, sticky = 'NW' + 'SW')
        self.superfamily_lbox.config(yscrollcommand=superfamily_scroll.set)
        samples_label = Label(self.frame, text='samples:')
        samples_label.grid(column=0, row=3)
        self.num_samples_t = StringVar
        num_samples_threshold = Entry(self.frame, width=4, textvariable=self.num_samples_t)
        self.samples_lbox = Listbox(self.frame, selectmode='extended', exportselection=0, height=7, listvariable=StringVar(value=tuple(samples)))
        self.samples_lbox.grid(column=1, row=3, columnspan=2, sticky='NESW')
        samples_scroll = Scrollbar(self.frame, orient=VERTICAL, command=self.samples_lbox.yview)
        samples_scroll.grid(column=3, row=3, sticky = 'NW' + 'SW')
        self.samples_lbox.config(yscrollcommand=samples_scroll.set)
        min_samples_label1 = Label(self.frame, text='in min ')
        min_samples_label1.grid(column=0, row=4)
        self.min_samples_t = IntVar()
        self.min_samples_t.set(1)
        min_samples_spinbox = Spinbox(self.frame, from_=0, to=len(samples), increment=1, textvariable=self.min_samples_t, width=5)
        min_samples_spinbox.grid(column=1, row=4)
        min_samples_label2 = Label(self.frame, text=' samples present')
        min_samples_label2.grid(column=2, row=4)
        
        calculate_button = Button(self.frame, 
                                text='calculate correlation', 
                                command=lambda samples=samples, 
                                    highest_taxlevel=sorted(highest_taxlevel), 
                                    abundance_df=abundance_df : self.calculate_correlation(samples, highest_taxlevel, abundance_df))
        calculate_button.grid(column=0, row=5)
        r_label = Label(self.frame, text='correlation coefficient \nthreshold')
        r_label.grid(column=0, row=6)
        self.r = StringVar()
        r_threshold = Entry(self.frame, width=8, textvariable=self.r)
        self.r.set('0.7')
        r_threshold.grid(column=1, row=6)
        p_label = Label(self.frame, text='pvalue threshold')
        p_label.grid(column=0, row=7)
        self.p = StringVar()
        p_threshold = Entry(self.frame, width=8, textvariable=self.p)
        self.p.set('0.05')
        p_threshold.grid(column=1, row=7)
        
        results_label = Label(self.frame, text='correlation results:')
        results_label.grid(column=4, row=0)
        results_xscroll = Scrollbar(self.frame, orient=HORIZONTAL)
        results_xscroll.grid(column=4, row=8, sticky = 'NW' + 'NE')
        results_yscroll = Scrollbar(self.frame, orient=VERTICAL)
        results_yscroll.grid(column=5, row=1, rowspan=7, sticky = 'NW' + 'SW')
        filter_button = Button(self.frame, text='filter/sort results', command=self.filter_correlation)
        filter_button.grid(column=1, row=8)
        self.sort_var = StringVar()
        self.sort_combobox = Combobox(self.frame, textvariable=self.sort_var, exportselection=0, height=4, state='readonly')
        self.sort_combobox['values'] = ('name1', 'name2', 'correlation coefficient r', 'p value')
        #sort_combobox.bind('<<ComboboxSelected>>', function)
        self.sort_combobox.current(0)
        self.sort_combobox.grid(column=0, row=8)
        save_button = Button(self.frame, text='save to file')#, command=)
        save_button.grid(column=2, row=8)
        self.root.option_add('*Listbox*Font', fonts_dict['listbox_font'])
        self.results_lbox = Listbox(self.frame, selectmode='multiple', exportselection=0, xscrollcommand=results_xscroll.set, yscrollcommand=results_yscroll.set, width=80)
        self.results_lbox.grid(column=4, row=1, rowspan=7, sticky='NWSE')
        results_xscroll.config(command=self.results_lbox.xview)
        results_yscroll.config(command=self.results_lbox.yview)
        
        
    def calculate_correlation(self, samples, highest_taxlevel, abundance_df):
        """ calculates the correlation """
        try:
            tax_level = self.all_tax_levels[self.tax_level_lbox.curselection()[0]]
            superfamily_groups = [highest_taxlevel[i] for i in self.superfamily_lbox.curselection()]
            if len(superfamily_groups) == 1:
                superfamily_groups = superfamily_groups * 2
            selected_samples = [samples[i] for i in self.samples_lbox.curselection()]
        except:
            print('values missing')
            return

        if len(selected_samples) >= 2:
            self.results_lbox.delete(0, END)
            self.corr_results_df = abundance_df.corr(self.all_tax_levels , selected_samples, tax_level, superfamily_groups, self.min_samples_t.get())
        else:
            print('need at least 2 samples')
        
    def filter_correlation(self):
        """ filters the correlation for correlation coefficient and pvalue """
        if self.corr_results_df is not None:
            r = float(self.r.get())
            p = float(self.p.get())
            self.results_lbox.delete(0, END)
            if self.sort_var.get() == 'correlation coefficient r':
                sortkey = 'r'
            elif self.sort_var.get() == 'p value':
                sortkey = 'p'
            else:
                sortkey = self.sort_var.get()
            self.corr_results_df.sort_values(by=sortkey, inplace=True)
            header = '{:40s} {:40s} {:7s} {:10s} {:11s} {:11s}'.format('name1', 'name2', 'r', 'p', 'max_name1', 'max_name2')
            self.results_lbox.insert(END, header)
            for key in self.corr_results_df.index:
                if self.corr_results_df.loc[key, 'r'] >= r and self.corr_results_df.loc[key, 'p'] < p:
                    if self.corr_results_df.loc[key, 'name1'] != self.corr_results_df.loc[key, 'name2']:
                        entry = '{:40s} {:40s} {:7.2f} {:7.2e} {:11.3f} {:11.3f}'.format(self.corr_results_df.loc[key, 'name1'], self.corr_results_df.loc[key, 'name2'], self.corr_results_df.loc[key, 'r'], self.corr_results_df.loc[key, 'p'], self.corr_results_df.loc[key, 'max_name1'], self.corr_results_df.loc[key, 'max_name2'])
                        #entry = '{:40s} {:40s} {:7.2f} {:7.2e}'.format(self.corr_results_df.loc[key, 'name1'], self.corr_results_df.loc[key, 'name2'], self.corr_results_df.loc[key, 'r'], self.corr_results_df.loc[key, 'p'])
                        self.results_lbox.insert(END, entry)
        
    def calculate_classification(self):
        """ runs a random forest classification """
        self.inner_frame.destroy()
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=6, column=0, columnspan=6)
        try:
            train_cols = [self.samples_list[x] for x in list(self.samples_lbox.curselection() + self.samples_lbox2.curselection())]
            if len(train_cols)<50:
                raise ValueError("at least 50 samples are needed to run the random forest")
            test_cols = self.samples_list
            targets = [0]*len(self.samples_lbox.curselection()) + [1]*len(self.samples_lbox2.curselection())
            names_list = self.abundance_df.randomForestClassifier(train_cols, test_cols, targets, self.feature_selction_var.get(), float(self.threshold.get()))
        
            #shuffle data
            from random import shuffle
            shuffle(targets)
            shuffled_names_list2 = self.abundance_df.randomForestClassifier(train_cols, test_cols, targets, self.feature_selction_var.get(), float(self.threshold.get()))
            
            group1 = [self.samples_list[x] for x in list(self.samples_lbox.curselection())]
            group2 = [self.samples_list[x] for x in list(self.samples_lbox2.curselection())]
            open_popup_window = OpenPopUpWindow(self.root, self.all_tax_levels, self.samples_list, self.abundance_df, group1, group2)
            
            forest_df = pd.DataFrame(columns=['species', 'contribution', 'contribution_shuffled', 'max_abundance'])
            self.tree_frame = Frame(self.inner_frame)
            self.tree_frame.grid(row=1, column=0)
            self.forest_tree = Treeview(self.tree_frame, height='10', columns=list(forest_df.columns))#, show="headings", selectmode="extended")
            self.forest_tree.column("#0", anchor="w", width=0)
            for col in forest_df.columns:
                self.forest_tree.heading(col,text=col.capitalize(),command=lambda each=col: self.treeview_sort_column(self.forest_tree, each, False))
                self.forest_tree.column(col, anchor='w', width=130)
            self.forest_tree.column(forest_df.columns[0], anchor='w', width=220)
            self.forest_tree.grid(row=1, column=0, columnspan=5)
            treeScroll = Scrollbar(self.tree_frame, command=self.forest_tree.yview)
            treeScroll.grid(row=1, column=5, sticky='nsew')
            self.forest_tree.configure(yscrollcommand=treeScroll.set)
            
            shuffled_names_dict2 = dict()
            for entry_list in shuffled_names_list2:
                shuffled_names_dict2[entry_list[1]] = [entry_list[0], entry_list[2]]
            for i, entry in enumerate(names_list):
                if 1:
                    try:
                        contribution3 = shuffled_names_dict2[entry[1]][0]
                    except:
                        contribution3 = 0.0
                    txt = '{:10.3f} {:20.3f} {:13.3f} {:55s}'.format(entry[0], contribution3, entry[2], '  '+entry[1]) + '\n'
                    forest_df.loc[entry[1]] = np.array([entry[1], abs(entry[0]), abs(contribution3), entry[2]])
            for species in forest_df.index:
                if forest_df.loc[species,'contribution'] > 0.001 or forest_df.loc[species,'contribution_shuffled'] > 0.001:
                    item = self.forest_tree.insert('', 'end', iid=species, values=list(forest_df.loc[species]))
                    
            popup_info = PopUpInfo(self.root, [], self.all_tax_levels, self.tax_level2, self.samples_list, self.abundance_df, groups=(group1, group2))
            self.forest_tree.bind("<Double-Button-1>", lambda event, tree=self.forest_tree, new_bool=1 : popup_info.do_tree_popup(event, tree, new_bool))
        except ValueError as error:
            print(error)
            tmb.showinfo(title="error", message=error)
              
    
    def richness_groups_boxplot(self):
        """  """
        import matplotlib
        matplotlib.use("TkAgg")
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

        from matplotlib.figure import Figure
        
        top = Toplevel(self.top)
        top.protocol("WM_DELETE_WINDOW", self.cancel)
        top.attributes("-topmost", 1)
        top.attributes("-topmost", 0)
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)
        frame = Frame(top)
        frame.grid(row=0, column=0, sticky=N+S+W+E)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        #self.top.title(self.name)
        #top.focus_set()
        
        #get data
        df = self.abundance_df.groupAllSamples()
        df = df[df.columns[:-1]]
        df = df[df['masked']==False]
        df.index = df.loc[:,self.tax_level]
        df = df.drop('-', errors='ignore')
        samples_1 = [self.samples_list[x] for x in list(self.samples_lbox.curselection())]
        samples_2 = [self.samples_list[x] for x in list(self.samples_lbox2.curselection())]
        samples = samples_1+samples_2
        
        #calculate richness and shannon index
        start_idx = len(self.all_tax_levels) - list(self.all_tax_levels).index(self.tax_level2)
        richness = df.astype(bool).sum(axis=0)[start_idx:-1]
        shannon  = []
        for sample in samples:
            #shannon.append(shannon_index(df[sample].as_matrix()))
            shannon.append(shannon_index(df[sample].values))
        shannon = pd.Series(shannon, index=samples)
        
        #create dataframe from the results to plot
        df2 = pd.DataFrame([richness, shannon], index=['richness','shannon_index'], columns=samples)
        df2 = df2.transpose()
        df2['group'] = np.array([self.samples1_label.get()]*len(samples_1) + [self.samples2_label.get()]*len(samples_2))
        
        #fig, ax = plt.subplots()
        fig = Figure(figsize=(5,7), dpi=100)
        ax = fig.add_subplot(211)
        #data = [df2[df2['group']==self.samples1_label.get()]['richness'].as_matrix(), df2[df2['group']==self.samples2_label.get()]['richness'].as_matrix()]
        data = [df2[df2['group']==self.samples1_label.get()]['richness'].values, df2[df2['group']==self.samples2_label.get()]['richness'].values]
        labels = [self.samples1_label.get(),self.samples2_label.get()]
        ax.boxplot(data)
        ax.set_xticklabels(labels, rotation=45, fontsize=8)
        ax.set_title('richness')
        ax = fig.add_subplot(212)
        #data = [df2[df2['group']==self.samples1_label.get()]['shannon_index'].as_matrix(), df2[df2['group']==self.samples2_label.get()]['shannon_index'].as_matrix()]
        data = [df2[df2['group']==self.samples1_label.get()]['shannon_index'].values, df2[df2['group']==self.samples2_label.get()]['shannon_index'].values]
        ax.boxplot(data)
        ax.set_xticklabels(labels, rotation=45, fontsize=8)
        ax.set_title('shannon_index')
        #plt.show()
        fig.subplots_adjust(left=0.08, right=0.98, bottom=0.05, top=0.9, hspace=0.4, wspace=0.3)
        #canvas = FigureCanvasTkAgg(fig, self.frame)
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        #canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        canvas.get_tk_widget().grid(row=1, column=1)

        toolbar_frame = Frame(frame)
        toolbar_frame.grid(row=2,column=2)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        #canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
        #canvas._tkcanvas.grid(row=2, column=1)
        
    
    def treeview_sort_column(self, tv, col, reverse):
        """ sorts the table by coloumn """
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        try:
            l = [(float(item[0]), item[1]) for item in l]
            l.sort(reverse=reverse)
            l = [('{0:.0e}'.format(item[0]), item[1]) for item in l]
        except ValueError:
            l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))
    
    def create_tree_popup_menu(self, event, root, a, all_tax_levels, samples, abundance_df, groups):
        """ creates popup menu """
        popup_info = PopUpInfo(root, a, all_tax_levels, self.tax_level2, samples, abundance_df, groups)
        popup_info.do_popup(event, new_bool=1, name=name)
    
    def wilcoxon_ranksum_test(self):
        """ calculate Wilxocon rank sum test to get the differences between the two groups """
        self.inner_frame.destroy()
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=6, column=0, columnspan=6)
        
        from scipy.stats import ranksums
        df = self.abundance_df.groupAllSamples()
        df = df[df.columns[:-1]]
        df = df[df['masked']==False]
        df.index = df.loc[:,self.tax_level]
        df = df.drop('-', errors='ignore')
        samples_1 = [self.samples_list[x] for x in list(self.samples_lbox.curselection())]
        samples_2 = [self.samples_list[x] for x in list(self.samples_lbox2.curselection())]
        samples = samples_1+samples_2
        open_popup_window = OpenPopUpWindow(self.root, self.all_tax_levels, self.samples_list, self.abundance_df, samples_1, samples_2)
         
        df = df.loc[:,samples]
        data_intersection = df.loc[(df!=0).all(1)]
        group_i1 = data_intersection.loc[:,samples_1]
        group_i2 = data_intersection.loc[:,samples_2]

        wilcox_df = pd.DataFrame(index=group_i1.index, columns=[self.tax_level, 'p_val', 'p_adj', 't_stat', 'max_abundance', 'var_'+self.samples1_label.get(), 'var_'+self.samples2_label.get(), 'mean_'+self.samples1_label.get(), 'mean_'+self.samples2_label.get()])
        for species in group_i1.index:
            x = group_i1.loc[species].values
            y = group_i2.loc[species].values
            t_stat, p_val = ranksums(x,y)
            wilcox_df.loc[species] = np.array([species, p_val, None, round(t_stat,3), round(max(x.max(), y.max()),3), round(x.var(),3), round(y.var(),3), round(x.mean(),3), round(y.mean(),3)])
            
        p_adj = p_adjust_bh(wilcox_df['p_val'])
        wilcox_df['p_adj'] = p_adj
        
        self.tree_frame = Frame(self.inner_frame)
        self.tree_frame.grid(row=1, column=0)
        self.wilcoxon_tree = Treeview(self.tree_frame, height='10', columns=list(wilcox_df.columns))#, show="headings", selectmode="extended")
        self.wilcoxon_tree.column("#0", anchor="w", width=0)
        
        for col in wilcox_df.columns:
            self.wilcoxon_tree.heading(col,text=col.capitalize(),command=lambda each=col: self.treeview_sort_column(self.wilcoxon_tree, each, False))
            self.wilcoxon_tree.column(col, anchor='w', width=90)
        self.wilcoxon_tree.column(wilcox_df.columns[0], anchor='w', width=200)
        self.wilcoxon_tree.grid(row=1, column=0, columnspan=5)
        treeScroll = Scrollbar(self.tree_frame, command=self.wilcoxon_tree.yview)
        treeScroll.grid(row=1, column=5, sticky='nsew')
        self.wilcoxon_tree.configure(yscrollcommand=treeScroll.set)
        
        for species in wilcox_df[wilcox_df['p_adj']<1].index:
            p_val = '{0:.0e}'.format(wilcox_df.loc[species,'p_val'])
            p_adj = '{0:.0e}'.format(wilcox_df.loc[species,'p_adj'])
            item = self.wilcoxon_tree.insert('', 'end', iid=species,  values=[species,p_val,p_adj]+list(wilcox_df.loc[species])[3:])
        popup_info = PopUpInfo(self.root, [], self.all_tax_levels, self.tax_level2, samples, self.abundance_df, groups=(samples_1, samples_2))
        self.wilcoxon_tree.bind("<Double-Button-1>", lambda event, tree=self.wilcoxon_tree, new_bool=1 : popup_info.do_tree_popup(event, tree, new_bool))

    def deseq2(self):
        """  """
        from rpy2 import robjects
        import rpy2.robjects.numpy2ri
        robjects.numpy2ri.activate()
        from rpy2.robjects.packages import importr
        from rpy2.robjects import Formula
        
        import warnings
        from rpy2.rinterface import RRuntimeWarning
        warnings.filterwarnings("ignore", category=RRuntimeWarning)
        
        self.inner_frame.destroy()
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=6, column=0, columnspan=6)
        
        deseq = importr('DESeq2')
        
        absolute_counts = self.abundance_df.groupAbsoluteSamples()
        
        if absolute_counts is not None:
        
            # Make the data frame
            d = {}
            samples_1 = [self.samples_list[x] for x in list(self.samples_lbox.curselection())]
            samples_2 = [self.samples_list[x] for x in list(self.samples_lbox2.curselection())]
            samples = samples_1+samples_2
        
            absolute_counts = absolute_counts[samples]
        
            categories = (1,) * len(samples_1) + (2,) * len(samples_2)

            d["group"] = robjects.IntVector(categories)
            dataframe = robjects.DataFrame(d)

            design = Formula("~ group")
            dds = deseq.DESeqDataSetFromMatrix(countData=absolute_counts.values, colData=dataframe, design=design)
            dds = deseq.DESeq(dds)
            res = deseq.results(dds)

            rownames = res.slots['rownames']
            listdata = res.slots['listData']

            listdata_array = np.array(listdata)
            listdata_names_array = np.array(listdata.names)
            df = pd.DataFrame(listdata_array.T, columns=listdata_names_array, index=absolute_counts.index)
        
            self.tree_frame = Frame(self.inner_frame)
            self.tree_frame.grid(row=1, column=0)
            self.deseq_tree = Treeview(self.tree_frame, height='10', columns=[self.tax_level]+list(df.columns))#, show="headings", selectmode="extended")
            self.deseq_tree.column("#0", anchor="w", width=0)
            for col in [self.tax_level]+list(df.columns):
                self.deseq_tree.heading(col,text=col.capitalize(), command=lambda each=col: self.treeview_sort_column(self.deseq_tree, each, False))
                self.deseq_tree.column(col, anchor='w', width=90)
            self.deseq_tree.column(self.tax_level, anchor='w', width=200)
            self.deseq_tree.grid(row=1, column=0, columnspan=5)
            treeScroll = Scrollbar(self.tree_frame, command=self.deseq_tree.yview)
            treeScroll.grid(row=1, column=5, sticky='nsew')
            self.deseq_tree.configure(yscrollcommand=treeScroll.set)
            for species in df.index:
                p_val = '{0:.0e}'.format(df.loc[species,'pvalue'])
                p_adj = '{0:.0e}'.format(df.loc[species,'padj'])
                item = self.deseq_tree.insert('', 'end', iid=species,  values=[species]+[round(item, 2) for item in list(df.loc[species])[:-2]]+[p_val, p_adj])
            popup_info = PopUpInfo(self.root, [], self.all_tax_levels, self.tax_level2, samples, self.abundance_df, groups=(samples_1, samples_2))
            self.deseq_tree.bind("<Double-Button-1>", lambda event, tree=self.deseq_tree, new_bool=1 : popup_info.do_tree_popup(event, tree, new_bool))
            
            filename = asksaveasfilename(title = "Select file to save DESeq2 results", initialfile='deseq2_results', filetypes = [('CSV', ".csv")])
            if filename:
                df.to_csv(filename)
            
            popup_matplotlib = PopUpIncludingMatplotlib(self.root, self.abundance_df, self.all_tax_levels)
            popup_matplotlib.deseq2(df, self.samples1_label.get(), self.samples2_label.get())
            
    def ancom(self):
        """  """
        from skbio.stats.composition import ancom, multiplicative_replacement
        self.inner_frame.destroy()
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=6, column=0, columnspan=6)
        
        samples_1 = [self.samples_list[x] for x in list(self.samples_lbox.curselection())]
        samples_2 = [self.samples_list[x] for x in list(self.samples_lbox2.curselection())]
        samples = samples_1+samples_2
        
        open_popup_window = OpenPopUpWindow(self.root, self.all_tax_levels, self.samples_list, self.abundance_df, samples_1, samples_2)
        df = self.abundance_df.groupAbsoluteSamples()[samples]
        
        mr_df = multiplicative_replacement(df.T)
        grouping = pd.Series([self.samples1_label.get()] *len(samples_1) + [self.samples2_label.get()] *len(samples_2), index=samples)
        ancom_df, percentile_df = ancom(pd.DataFrame(mr_df, index=df.columns, columns=df.index), grouping, multiple_comparisons_correction='holm-bonferroni')

        self.tree_frame = Frame(self.inner_frame)
        self.tree_frame.grid(row=1, column=0)
        columns = [self.tax_level2, 'W', self.samples1_label.get()+'_median', self.samples2_label.get()+'_median']
        self.ancom_tree = Treeview(self.tree_frame, height='10', columns=columns)#, show="headings", selectmode="extended")
        self.ancom_tree.column("#0", anchor="w", width=0)
        
        for col in columns:
            self.ancom_tree.heading(col,text=col.capitalize(),command=lambda each=col: self.treeview_sort_column(self.ancom_tree, each, False))
            self.ancom_tree.column(col, anchor='w', width=150)
        self.ancom_tree.column(columns[0], anchor='w', width=250)
        self.ancom_tree.grid(row=1, column=0, columnspan=5)
        treeScroll = Scrollbar(self.tree_frame, command=self.ancom_tree.yview)
        treeScroll.grid(row=1, column=5, sticky='nsew')
        self.ancom_tree.configure(yscrollcommand=treeScroll.set)
        
        percentiles = [0.0, 25.0, 50.0, 75.0, 100.0]
        columns2 =['W']
        for percentile in percentiles:
            columns2 += ['{}_{}percentile'.format(self.samples1_label.get(), percentile), '{}_{}percentile'.format(self.samples2_label.get(), percentile)]
        results_df = pd.DataFrame(columns=columns2, index=sorted(ancom_df[ancom_df['Reject null hypothesis']==True].index))
        for species in sorted(ancom_df[ancom_df['Reject null hypothesis']==True].index):
            values = [species, ancom_df.loc[species,'W'], '{0:.2e}'.format(percentile_df[50.0].loc[species,self.samples1_label.get()]), '{0:.2e}'.format(percentile_df[50.0].loc[species,self.samples2_label.get()])]
            values2 = ['{0:.2e}'.format(percentile_df[0.0].loc[species,self.samples1_label.get()]), '{0:.2e}'.format(percentile_df[0.0].loc[species,self.samples2_label.get()]), '{0:.2e}'.format(percentile_df[25.0].loc[species,self.samples1_label.get()]), '{0:.2e}'.format(percentile_df[25.0].loc[species,self.samples2_label.get()]), '{0:.2e}'.format(percentile_df[50.0].loc[species,self.samples1_label.get()]), '{0:.2e}'.format(percentile_df[50.0].loc[species,self.samples2_label.get()]), '{0:.2e}'.format(percentile_df[75.0].loc[species,self.samples1_label.get()]), '{0:.2e}'.format(percentile_df[75.0].loc[species,self.samples2_label.get()]), '{0:.2e}'.format(percentile_df[100.0].loc[species,self.samples1_label.get()]), '{0:.2e}'.format(percentile_df[100.0].loc[species,self.samples2_label.get()])]
            results_df.loc[species] = [ancom_df.loc[species,'W']] + values2
            item = self.ancom_tree.insert('', 'end', iid=species,  values=values)
        popup_info = PopUpInfo(self.root, [], self.all_tax_levels, self.tax_level2, samples, self.abundance_df, groups=(samples_1, samples_2))
        self.ancom_tree.bind("<Double-Button-1>", lambda event, tree=self.ancom_tree, new_bool=1 : popup_info.do_tree_popup(event, tree, new_bool))
        
        filename = asksaveasfilename(title = "Select file to save ANCOM results", initialfile='ancom_results', filetypes = [('CSV', ".csv")])
        if filename:
            results_df.to_csv(filename)

    def richness_groups(self):
        """ creates a boxplot of the richness for each group of samples """
        self.inner_frame.destroy()
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=6, column=0, columnspan=6)
        
        df = self.abundance_df.groupAllSamples(self.all_tax_levels[self.all_tax_levels.index(self.tax_level2):])
        df = df[df.columns[:-1]]
        df = df[df['masked']==False]
        df.index = df.loc[:,self.tax_level]
        df = df.drop('-', errors='ignore')
        samples_1 = [self.samples_list[x] for x in list(self.samples_lbox.curselection())]
        samples_2 = [self.samples_list[x] for x in list(self.samples_lbox2.curselection())]
        samples = samples_1+samples_2
        
        df = df.loc[:,samples]
        
        start_idx = list(self.all_tax_levels).index(self.tax_level2)
        richness = df.astype(bool).sum(axis=0)#[start_idx:]
        
        popup_matplotlib = PopUpIncludingMatplotlib(self.root, self.abundance_df, self.all_tax_levels)
        if self.abundance_df is not None:
            working_samples = self.abundance_df.groupAllSamples()
        popup_matplotlib.richness_groups(working_samples, self.samples_list, self.tax_level2, samples_1, samples_2, richness, self.samples1_label.get(), self.samples2_label.get())

    def shannon_diversity_groups(self):
        """ creates a boxplot of the Shannon diversity index for each group of samples """
        self.inner_frame.destroy()
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=6, column=0, columnspan=6)
        
        df = self.abundance_df.groupAllSamples(self.all_tax_levels[self.all_tax_levels.index(self.tax_level2):])
        df = df[df.columns[:-1]]
        df = df[df['masked']==False]
        df.index = df.loc[:,self.tax_level]
        df = df.drop('-', errors='ignore')
        samples_1 = [self.samples_list[x] for x in list(self.samples_lbox.curselection())]
        samples_2 = [self.samples_list[x] for x in list(self.samples_lbox2.curselection())]
        samples = samples_1+samples_2
        
        df = df.loc[:,samples]
        
        shannon  = []
        for sample in samples:
            shannon.append(shannon_index(df[sample].values))
        shannon = pd.Series(shannon, index=samples)
        
        popup_matplotlib = PopUpIncludingMatplotlib(self.root, self.abundance_df, self.all_tax_levels)
        if self.abundance_df is not None:
            working_samples = self.abundance_df.groupAllSamples()
        popup_matplotlib.shannon_diversity_groups(working_samples, self.samples_list, self.tax_level2, samples_1, samples_2, shannon, self.samples1_label.get(), self.samples2_label.get())

    def correlation_groups(self):
        """ correaltion """
        self.inner_frame.destroy()
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=6, column=0, columnspan=6)
        
        #correlation for groups
        from scipy.stats import spearmanr
        df = self.abundance_df.getDataframe()
        df = df[df['masked']==False]
        df.index = df.loc[:,'species']
        samples_1 = [self.samples_list[x] for x in list(self.samples_lbox.curselection())]
        samples_2 = [self.samples_list[x] for x in list(self.samples_lbox2.curselection())]
        samples = samples_1+samples_2
        df = df.loc[:,samples]
        data_intersection = df.loc[(df!=0).all(1)]
        group_i1 = data_intersection.loc[:,samples_1]
        group_i2 = data_intersection.loc[:,samples_2]
        taxlevelnum = len(self.all_tax_levels)
        corr_df = pd.DataFrame(columns=['r1', 'p1', 'r2', 'p2', 'r_all', 'p_all'])
        for i, idx in enumerate(group_i1.index):
            abundance1 = group_i1.iloc[i, :]
            abundance1_2 = group_i2.iloc[i, :]
            name1 = idx
            for j in range(i+1, len(group_i1.index)):
                jdx = group_i1.index[j]
                abundance2 = group_i1.iloc[j, :]
                abundance2_2 = group_i2.iloc[j, :]
                name2 = jdx
                rho, pval = spearmanr(abundance1, abundance2)
                rho_2, pval_2 = spearmanr(abundance1_2, abundance2_2)
                rho_all, pval_all = spearmanr(list(abundance1)+list(abundance1_2), list(abundance2)+list(abundance2_2))
                corr_df.loc[name1+' / '+name2] = [rho, pval, rho_2, pval_2, rho_all, pval_all]
        corr_df['p1_adj'] = p_adjust_bh(corr_df['p1'])
        corr_df['p2_adj'] = p_adjust_bh(corr_df['p2'])
            
        sbary = Scrollbar(self.inner_frame, orient=VERTICAL)
        sbary.grid(row=1, column=1, sticky = 'NW' + 'SW')
        results_list = []

        results_var = StringVar(value=tuple(results_list))
        self.results_lbox = Listbox(self.inner_frame, 
                        listvariable=results_var, 
                        height=25, 
                        width=120, 
                        yscrollcommand=sbary.set,
                        exportselection=0)
        self.results_lbox.grid(row=1, column=0)
        self.groups_corr_df = corr_df
        
        
    def correlation_groups_filter(self):
        """ filters correlation for groups by padj """
        corr_df = self.groups_corr_df
        results_list = []
        #txt = '{:45s} {:45s} {:9s} {:13s} {:9s} {:13s}'.format('species1', 'species2', 'R (group1)', 'padj (group1)', 'R (group2)', 'padj (group2)')
        txt = '{:25s} {:42s} {:9s} {:13s} {:9s} {:13s}'.format('species1', 'species2', 'R ('+self.samples1_label.get()+')', 'padj ('+self.samples1_label.get()+')', 'R ('+self.samples2_label.get()+')', 'padj ('+self.samples2_label.get()+')')
        results_list.append(txt)
        for idx in corr_df.index:
            if float(corr_df.loc[idx,'p1_adj']) < 0.05 and float(corr_df.loc[idx,'p2_adj']) < 0.05:
                if float(corr_df.loc[idx,'r1']) + float(self.corr_r_threshold.get()) < float(corr_df.loc[idx,'r2']) or float(corr_df.loc[idx,'r1']) - float(self.corr_r_threshold.get()) > float(corr_df.loc[idx,'r2']):
                    species1, species2 = idx.split(' / ')
                    #txt = '{:45s} {:45s} {:9.2f} {:13.2E} {:9.2f} {:13.2E}'.format(species1, species2, round(corr_df.loc[idx, 'r1'],2), Decimal(corr_df.loc[idx, 'p1_adj']), round(corr_df.loc[idx, 'r2'],2), Decimal(corr_df.loc[idx, 'p1_adj']))
                    txt = '{:25s} {:42s} {:9.2f} {:13.2E} {:9.2f} {:13.2E}'.format(species1, species2, round(corr_df.loc[idx, 'r1'],2), Decimal(corr_df.loc[idx, 'p1_adj']), round(corr_df.loc[idx, 'r2'],2), Decimal(corr_df.loc[idx, 'p1_adj']))
                    results_list.append(txt)
        results_var = StringVar(value=tuple(results_list))
        self.results_lbox.config(listvariable=results_var)
        
    def add_legend_to_canvas(self, canvas, colours, labels):
        """ adds the legend for the groups to a pca plot """
        for i,label in enumerate(labels):
            canvas.create_oval((417,55+i*20,423,55+i*20+6), width=3, outline=colours[i])
            canvas.create_text(430, 50+i*20, text=label, anchor=NW)
        
    def pca_old(self):
        train_cols = [self.samples_list[x] for x in list(self.samples_lbox.curselection() + self.samples_lbox2.curselection())]
        targets = [0]*len(self.samples_lbox.curselection()) + [1]*len(self.samples_lbox2.curselection())
        self.inner_frame.destroy()
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=6, column=0, columnspan=6)

        canvas = create_canvas(frame=self.inner_frame, xscroll=False, yscroll=False, colspan=2, take_focus=True)

        from sklearn.preprocessing import scale #module that normalizes data
        from sklearn.decomposition import PCA #PCA module
        df = self.abundance_df.getDataframe()
        df = df[df['masked']==False]
        train = df.loc[:,train_cols]
        train_norm = scale(train.values)
        pca = PCA()
        reduced_data = pca.fit_transform(train_norm) #PCA SVD calculations
        #pc1 = pca.components_[0]
        from sklearn.feature_selection import VarianceThreshold
        sel = VarianceThreshold(threshold=(0.999 * (1 - 0.999)))

        if self.feature_selction_var.get():
            X_var = sel.fit_transform(np.transpose(train.values))
            new_names = df.loc[:,'species'].values[sel.get_support()]
        else:
            X_var = np.transpose(train.values)
            new_names = df.loc[:,'species'].values
        X_varN = scale(X_var) #Scaled version of X_var
        #pca = PCA()
        reduced_data = pca.fit_transform(np.transpose(X_varN))
        pc1 = pca.components_[0]
        pc2 = pca.components_[1]
        pc1_expl_var, pc2_expl_var = pca.explained_variance_ratio_[:2]
        pc1_expl_var = str(round(pc1_expl_var*100,2))
        pc2_expl_var = str(round(pc2_expl_var*100,2))
        sample_names = list(df.loc[:,train_cols].columns)
       
        targets_bool = np.array(targets, dtype=bool)
        pc1_group2 = pc1[targets_bool]
        pc1_group1 = pc1[np.invert(targets_bool)]
        pc2_group2 = pc2[targets_bool]
        pc2_group1 = pc2[np.invert(targets_bool)]
       
        colours = ['cornflowerblue' if target else 'darkgreen' for target in targets]

        self.draw_scatter_plot(canvas, 'PC1 ('+pc1_expl_var+'%)', 'PC2 ('+pc2_expl_var+'%)', pc1, pc2, sample_names, colours)
        self.add_legend_to_canvas(canvas, ['darkgreen','cornflowerblue'], [self.samples1_label.get(), self.samples2_label.get()])
    
    def pca(self):
        from skbio.stats.composition import ilr, multiplicative_replacement
        from sklearn.decomposition import PCA
        self.inner_frame.destroy()
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=6, column=0, columnspan=6)
        
        canvas = create_canvas(frame=self.inner_frame, xscroll=False, yscroll=False, colspan=2, take_focus=True)
        
        samples_1 = [self.samples_list[x] for x in list(self.samples_lbox.curselection())]
        samples_2 = [self.samples_list[x] for x in list(self.samples_lbox2.curselection())]
        samples = samples_1+samples_2
        targets = [0]*len(samples_1) + [1]*len(samples_2)
        
        open_popup_window = OpenPopUpWindow(self.root, self.all_tax_levels, self.samples_list, self.abundance_df, samples_1, samples_2)
        df = self.abundance_df.groupAbsoluteSamples()[samples]
        
        mr_df = multiplicative_replacement(df.T)
        mr_ilr = ilr(mr_df)
        
        pca = PCA(n_components=2)
        principalComponents = pca.fit_transform(mr_ilr)
        pc1 = []
        pc2 = []
        for item in principalComponents:
            pc1.append(item[0])
            pc2.append(item[1])
        #print(pc1)
        #print(pc2)
        explained_variance = [str(round(item*100,2)) for item in pca.explained_variance_ratio_]
        colours = ['cornflowerblue' if target else 'darkgreen' for target in targets]
        self.draw_scatter_plot(canvas, 'PC1 ('+explained_variance[0]+'%)', 'PC2 ('+explained_variance[1]+'%)', pc1, pc2, samples, colours)
        self.add_legend_to_canvas(canvas, ['darkgreen','cornflowerblue'], [self.samples1_label.get(), self.samples2_label.get()])
        
        popup_matplotlib = PopUpIncludingMatplotlib(self.root, self.abundance_df, self.all_tax_levels)
        popup_matplotlib.pcoa(pc1[len(samples_1):], pc1[:len(samples_1)], pc2[len(samples_1):], pc2[:len(samples_1)], self.samples1_label.get(), self.samples2_label.get(), (0,1), pca=True)
        
    def pcoa(self):
        from skbio.diversity import beta_diversity
        from sklearn.preprocessing import scale #module that normalizes data
        from skbio.stats.ordination import pcoa
        train_cols = [self.samples_list[x] for x in list(self.samples_lbox.curselection() + self.samples_lbox2.curselection())]
        targets = [0]*len(self.samples_lbox.curselection()) + [1]*len(self.samples_lbox2.curselection())
        self.inner_frame.destroy()
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=6, column=0, columnspan=6)

        canvas = create_canvas(frame=self.inner_frame, xscroll=False, yscroll=False, colspan=2, take_focus=True)
        
        df = self.abundance_df.getDataframe()
        df = df[df['masked']==False]
        train = df.loc[:,train_cols]
        train_norm = scale(train.values)
        
        if self.feature_selction_var.get():
            from sklearn.feature_selection import VarianceThreshold
            sel = VarianceThreshold(threshold=(0.999 * (1 - 0.999)))
            X_var = sel.fit_transform(np.transpose(train.values))
        else:
            X_var = np.transpose(train.values)
        new_names = train_cols

        bc_dm = beta_diversity('braycurtis', X_var, list(new_names), validate=False) #bray-curtis dissimilarity matrix
        pc_nums = next(self.pcoa_toggle)
        bc_pc = pcoa(bc_dm)
        #pco1_prp_expl, pco2_prp_expl = list(bc_pc.proportion_explained)[:2]
        pco1_prp_expl = list(bc_pc.proportion_explained)[pc_nums[0]]
        pco2_prp_expl = list(bc_pc.proportion_explained)[pc_nums[1]]
        pco1_prp_expl = str(round(pco1_prp_expl*100,2))
        pco2_prp_expl = str(round(pco2_prp_expl*100,2))
        coord_matrix = bc_pc.samples.values.T
        #pco1 = coord_matrix[0]
        #pco2 = coord_matrix[1]
        pco1 = coord_matrix[pc_nums[0]]
        pco2 = coord_matrix[pc_nums[1]]
        sample_names = list(df.loc[:,train_cols].columns)
        targets_bool = np.array(targets, dtype=bool)
        pco1_group2 = pco1[targets_bool]
        pco1_group1 = pco1[np.invert(targets_bool)]
        pco2_group2 = pco2[targets_bool]
        pco2_group1 = pco2[np.invert(targets_bool)]
       
        colours = ['cornflowerblue' if target else 'darkgreen' for target in targets]

        self.draw_scatter_plot(canvas, 'PCo'+str(pc_nums[0]+1)+' ('+pco1_prp_expl+'%)', 'PCo'+str(pc_nums[1]+1)+' ('+pco2_prp_expl+'%)', pco1, pco2, sample_names, colours)
        self.add_legend_to_canvas(canvas, ['darkgreen','cornflowerblue'], [self.samples1_label.get(), self.samples2_label.get()])
        
        targets_names = [self.samples1_label.get() if item==0 else self.samples2_label.get() for item in targets]
        popup_matplotlib = PopUpIncludingMatplotlib(self.root, self.abundance_df, self.all_tax_levels)
        popup_matplotlib.pcoa(pco1_group2, pco1_group1, pco2_group2, pco2_group1, self.samples1_label.get(), self.samples2_label.get(), pc_nums)
        
    def do_pop_up(self, event, name):
        """ do popup """
        popup_info = PopUpInfo(self.root, [], self.all_tax_levels, self.tax_level2, self.samples_list, self.abundance_df)
        popup_info.do_popup(event, new_bool=1, name=name)
        
    def get_info(self, name):
        """ get info """
        popup_menu = PopUpMenu(self.root, name, None, self.abundance_df, threshold_slider=None, tax_list=[], meta_df=None, all_tax_levels=self.all_tax_levels, current_tax_level='species')   


        
class PopUpWindow():
    def __init__(self, root, name, pop_ups=None, abundance_df=None, tax_list=None, all_tax_levels=None):    
        self.root = root
        self.name = name
        self.pop_ups = pop_ups
        self.abundance_df = abundance_df
        self.tax_list = tax_list
        self.all_tax_levels = all_tax_levels
        self.top = None
        self.SPECIES_CANVAS_HEIGHT = 200
        self.SPECIES_CANVAS_WIDTH = 400
        self.COLORS = ['orange red', 
                'maroon', 
                'red4', 
                'DarkOrange2', 
                'medium violet red', 
                'red', 
                'DeepPink4', 
                'magenta3', 
                'brown4', 
                'deep pink']
        self.create_window()
        self.balloon = Pmw.Balloon(self.root)
        self.COLOR_SCHEME = ['navy',
                         'seagreen3', 
                         'dark goldenrod', 
                         'blue2', 
                         'orangered', 
                         'steelblue4', 
                         'forestgreen',
                         'deepskyblue', 
                         'deeppink4', 
                         'olivedrab4', 
                         'turquoise4',
                         'blue4', 
                         'medium aquamarine', 
                         'orange3', 
                         'medium blue', 
                         'OrangeRed2', 
                         'DeepSkyBlue4', 
                         'dark green', 
                         'DeepSkyBlue2', 
                         'HotPink4', 
                         'DarkOliveGreen4', 
                         'cyan4']
        
    def highlight_hits(self, event):
        """ highlight bars in yellow that match the names in the preset """
        search_txt = event.get().upper().strip()
        if "highlight" in self.text.tag_names():
            self.text.tag_delete("highlight")
        search_txt_len = len(search_txt)
        hit_nr = 0
        if search_txt_len > 1:
            idx = "1.0"
            while idx != '':
                idx = self.text.search(search_txt, idx, nocase=1, stopindex='end')
                if idx:
                    hit_nr += 1
                    if hit_nr == 1:
                        self.text.see(idx)
                    idx2 = self.text.index("%s+%dc" % (idx, search_txt_len))
                    self.text.tag_add("highlight", idx, idx2)
                    self.text.tag_config("highlight", background="yellow")
                    idx = idx2
        self.hits_count_label.config(text='nuber of hits: '+str(hit_nr))
    
    def always_together(self, pattern_dict, singletons_dict):
        """ displays the groups of species which are always together in a sample """
        self.top.title('species that are always together in samples')
        ##self.get_top_level_id()
        #canvas = create_canvas(frame=self.frame, height=400, width=700, xscroll=False)
        #WIDTH = 700-10
        #canvas.create_text(10,30, text="{:<8}{:}".format('group', 'species\n'), anchor=NW, width=WIDTH, font='bold')
        
        scroll = Scrollbar(self.frame, orient=VERTICAL)
        scroll.grid(row=0, column=3, sticky=N+S)
        self.text = Text(self.frame, width=100)
        self.text.grid(row=0, column=0, columnspan=3)
        
        txt = ''
        for idx, species_list in enumerate(pattern_dict.values()):
            #txt += str(idx) + '\t' + ', '.join(sorted(species_list)) + '\n'
            txt += "{:<10}{:}".format(str(idx), ', '.join(sorted(species_list)) + '\n')
            txt = "{:<10}{:}".format(str(idx), ', '.join(sorted(species_list)) + '\n')
            self.text.insert(END, txt)
        #txt += '\n\nspecies that have a unique presence/absence pattern in all samples:\n'
        txt = '\n\nspecies that have a unique presence/absence pattern in all samples:\n'
        self.text.insert(END, txt)
        #txt += '\n'.join(sorted(singletons_dict.values()))
        txt = '\n'.join(sorted(singletons_dict.values()))
        self.text.insert(END, txt)
        self.text.config(state=DISABLED)
        ##countVar = StringVar()
        ##text.tag_configure("search", background="green")
        ##pos = text.search('cerevisiae', "1.0", stopindex="end", count=countVar)
        ##text.tag_add("search", pos, "%s + %sc" (pos, countVar.get()))
        #start = 1.0
        #pos = self.text.search("cerevisiae", start, stopindex=END)
        #self.text.see(pos)
        #self.highlight("cerevisiae")
        ##while 1:
        ##    pos = text.search("cerevisiae", start, stopindex=END)
        ##    if not pos:
        ##        break
        ##    print(pos)
        ##    start = pos + "+1c"
        ##canvas.create_text(10,50, text=txt, anchor=NW, width=WIDTH)
        ##canvas.config(height=500, width=700)
        ##canvas.config(scrollregion=canvas.bbox(ALL))#, height=self.popup_canvas.bbox(ALL)[3])
        
        #text.insert(END, txt)
        scroll.config(command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)
        
        species_to_search = StringVar()
        
        species_to_search.trace("w", lambda name, index, mode, species_to_search=species_to_search: self.highlight_hits(species_to_search))
        search_species = Entry(self.frame, 
                                textvariable=species_to_search)
        search_species.grid(row=1, column=1)
        search_specie_label = Label(self.frame, text='search for:')
        search_specie_label.grid(row=1, column=0)
        
        self.hits_count_label = Label(self.frame, text='nuber of hits: 0')
        self.hits_count_label.grid(row=1, column=2)
        
    def create_window(self):
        """ creates a popup window """
        self.top = Toplevel(self.root)
        self.top.protocol("WM_DELETE_WINDOW", self.cancel)
        self.top.attributes("-topmost", 1)
        self.top.attributes("-topmost", 0)
        self.top.columnconfigure(0, weight=1)
        self.top.rowconfigure(0, weight=1)
        self.frame = Frame(self.top)
        self.frame.grid(row=0, column=0, sticky=N+S+W+E)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.top.title(self.name)
        self.top.focus_set()
        
    def get_top_level_id(self):
        """ returns the toplevel id to the class Display """
        return self.top
    
    def empty_window(self, name):
        """ empties the graph in a pop up window """
        try: 
            self.frame.destroy()
            self.frame = Frame(self.top)
            self.frame.grid(row=0, column=0)
        except TclError:
            pass
        self.top.attributes("-topmost", 1)
        self.top.attributes("-topmost", 0)
        self.top.title(name)
        
    def create_graph(self, abundances, sample_names):
        """ creates a graph that shows the abundances of several samples for one organism (e.g. species) """
        self.top.title('abundances for ' + self.name + ' in all samples')
        HEIGHT = 300
        WIDTH = 600
        if len(sample_names) <= 20:
            WIDTH = 600
        elif len(sample_names) <= 40:
            WIDTH = 900
        else: 
            WIDTH = 1200
        height = HEIGHT - 50
        canvas = create_canvas(frame=self.frame, width=WIDTH, height=HEIGHT, xscroll=False, yscroll=False, colspan=2, take_focus=True)
        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=3)
        toggle_color = itertools.cycle(['olivedrab', 'darkolivegreen'])
        
        width = round((WIDTH-70)/len(abundances))
        displaying_text = DisplayingText(self.root, canvas)
        for i, num in enumerate(abundances):
            x1 = i * width + 70
            y1 = height - num/max(abundances)*height
            x2 = (i+1) * width + 70
            y2 = height
            coords = (x1, y1, x2, y2)
            col = next(toggle_color)
            canvas.create_rectangle(coords, outline=col, fill= col)
            displaying_text.drawText(sample_names[i], i, 70+(i+0.5)*width, height+30)
            canvas.create_line(70, 0, 70, height)  
            canvas.create_line(70, 
                                height, 
                                WIDTH, 
                                height)               
            for j in range(0,int(height),50):
                canvas.create_line(65,
                                height-j, 
                                70, 
                                height-j)
                canvas.create_text(20, 
                                height-j, 
                                text='{0:.2f}'.format(float(j)/height*max(abundances)),
                                anchor = NW)
            canvas.config(scrollregion=canvas.bbox(ALL))
    
    def correlation_groups(self):
        """ correaltion """
        self.inner_frame.destroy()
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=6, column=0, columnspan=6)
        
        #correlation for groups
        from scipy.stats import spearmanr
        df = self.abundance_df.getDataframe()
        df = df[df['masked']==False]
        df.index = df.loc[:,'species']
        samples_1 = [self.samples_list[x] for x in list(self.samples_lbox.curselection())]
        samples_2 = [self.samples_list[x] for x in list(self.samples_lbox2.curselection())]
        samples = samples_1+samples_2
        df = df.loc[:,samples]
        data_intersection = df.loc[(df!=0).all(1)]
        group_i1 = data_intersection.loc[:,samples_1]
        group_i2 = data_intersection.loc[:,samples_2]
        taxlevelnum = len(self.all_tax_levels)
        corr_df = pd.DataFrame(columns=['r1', 'p1', 'r2', 'p2', 'r_all', 'p_all'])
        for i, idx in enumerate(group_i1.index):
            abundance1 = group_i1.iloc[i, :]
            abundance1_2 = group_i2.iloc[i, :]
            name1 = idx
            for j in range(i+1, len(group_i1.index)):
                jdx = group_i1.index[j]
                abundance2 = group_i1.iloc[j, :]
                abundance2_2 = group_i2.iloc[j, :]
                name2 = jdx
                rho, pval = spearmanr(abundance1, abundance2)
                rho_2, pval_2 = spearmanr(abundance1_2, abundance2_2)
                rho_all, pval_all = spearmanr(list(abundance1)+list(abundance1_2), list(abundance2)+list(abundance2_2))
                corr_df.loc[name1+' / '+name2] = [rho, pval, rho_2, pval_2, rho_all, pval_all]
        corr_df['p1_adj'] = p_adjust_bh(corr_df['p1'])
        corr_df['p2_adj'] = p_adjust_bh(corr_df['p2'])
            
        sbary = Scrollbar(self.inner_frame, orient=VERTICAL)
        sbary.grid(row=1, column=1, sticky = 'NW' + 'SW')
        results_list = []

        results_var = StringVar(value=tuple(results_list))
        self.results_lbox = Listbox(self.inner_frame, 
                        listvariable=results_var, 
                        height=25, 
                        width=120, 
                        yscrollcommand=sbary.set,
                        exportselection=0)
        self.results_lbox.grid(row=1, column=0)
        self.groups_corr_df = corr_df
    
    def create_groups_graph(self, abundances_all, samples, groups):
        """ creates two graphs, one for each group """
        samples1, samples2 = groups
        abundances1 = [float(abundances_all[sample]) for sample in samples1]
        abundances2 = [float(abundances_all[sample]) for sample in samples2]
        max_abundance = max(abundances1 + abundances2)
        toggle_color = itertools.cycle(['olivedrab', 'darkolivegreen'])
        self.create_groups_one_graph(abundances1, samples1, max_abundance, toggle_color, col=0)
        toggle_color = itertools.cycle(['blue', 'navy'])
        self.create_groups_one_graph(abundances2, samples2, max_abundance, toggle_color, col=1,)
        
    def create_groups_one_graph(self,abundances, samples, max_abundance, toggle_color, col=0):
        """ creates one graph """
        if len(samples) >= 25:
            WIDTH = 800
        elif len(samples) >= 40:
            WIDTH = 600
        else:
            WIDTH = 400
        HEIGHT = 400
        canvas = create_canvas(frame=self.frame, width=WIDTH, height=HEIGHT, xscroll=False, yscroll=False, take_focus=True, col=col)
        width = round((WIDTH-70)/len(abundances))
        height = HEIGHT-50
        displaying_text = DisplayingText(self.root, canvas)
        for i, num in enumerate(abundances):
            x1 = i * width + 70
            y1 = height - num/max_abundance*height
            x2 = (i+1) * width + 70
            y2 = height
            coords = (x1, y1, x2, y2)
            col = next(toggle_color)
            canvas.create_rectangle(coords, outline=col, fill= col)
            displaying_text.drawText(samples[i], i, 70+(i+0.5)*width, height+30)
            canvas.create_line(70, 0, 70, height)  
            canvas.create_line(70, 
                                height, 
                                WIDTH, 
                                height)               
            for j in range(0,int(height),50):
                canvas.create_line(65,
                                height-j, 
                                70, 
                                height-j)
                canvas.create_text(20, 
                                height-j-5, 
                                text='{0:.2f}'.format(round(float(j)/height*max_abundance, 2)),
                                anchor = NW)
            canvas.config(scrollregion=canvas.bbox(ALL))
    
    def create_wiki(self, name):
        """ displays the summary of a wikipedia article in a popup window """
        self.top.title('information about ' + self.name)
        WIDTH = 700
        canvas = create_canvas(frame=self.frame, row=1, height=400, width=WIDTH, xscroll=False, colspan=6)
        url = ''
        text = ''
        noentry = ''
        try:
            entry = wikipedia.page(name)
            url += entry.url
            self.url = entry.url
            text += entry.title + '\n\nSummary:\n' + entry.summary + '\n\n'
        except(wikipedia.exceptions.PageError):
            noentry = 'there exists no Wikipedia entry'# for:\n' + name
        if self.tax_list != []:
            text += 'Taxonomy:\n'
            for i, level in enumerate(self.all_tax_levels[-len(self.tax_list):]):
                text += "%-*s%s" % (30, level + ':', str(self.tax_list[i]) + '\n')
        name_list = name.split(' ')
        pubmed_url='https://www.ncbi.nlm.nih.gov/pubmed?term='+'+'.join(name_list)+'%5BTitle%2FAbstract%5D'
        pubmed_button = Button(self.frame, text="PubMed search", command=lambda pubmed_url=pubmed_url : self.open_url(pubmed_url))
        pubmed_button.grid(row=0, column=0)
        if 0:
            name_list = name.split(' ')
            pubmed_url='https://www.ncbi.nlm.nih.gov/pubmed?term='+'+'.join(name_list)+'%5BTitle%2FAbstract%5D'
            webbrowser.open_new(url3)
            
        if url:
            wiki_button = Button(self.frame, text="Wikipedia search", command=lambda pubmed_url=pubmed_url : self.open_url(url))
            wiki_button.grid(row=0, column=1)
            canvas.create_text(10,40, text=text, anchor=NW, width=WIDTH)
        else:
            canvas.create_text(10,10, text=noentry, anchor=NW, width=WIDTH, fill='red')
            canvas.create_text(10,50, text=text, anchor=NW, width=WIDTH)
        canvas.config(scrollregion=canvas.bbox(ALL), height=min(350, canvas.bbox(ALL)[3]), width=700)    
    
    def open_url(self, url):
        """ opens url in browser """
        webbrowser.open_new(url)
    
    def cancel(self, event=None):
        """ destroys/closes pop up windows """
        self.top.destroy()
        if self.pop_ups is not None:
            for instance, toplevel in self.pop_ups:
                if toplevel == self.top:
                    self.pop_ups.remove((instance, toplevel))
        
    def create_correlation(self, name, current_taxlevel, col2=400, meta=False):
        """ creates correlation coefficients for all species to the current species """
        if not meta:
            scale_corr_label = Label(self.frame,
                                        text='correlation threshold:')#,
                                        #background='white')
            scale_corr_label.grid(row=0, column=0)
            self.threshold = DoubleVar()
            self.threshold.set(0.95)
            scale_corr_slider = Spinbox(self.frame, 
                                        from_=0, 
                                        to=1, 
                                        increment=0.01,
                                        textvariable=self.threshold,
                                        width=6)
            scale_corr_slider.grid(row=0, column=1)
        
            title = 'correlation with other %s for %s' % (current_taxlevel, name)
            corr_button = Button(self.frame, text='calculate correlation', command=lambda name=name, current_taxlevel=current_taxlevel, col2=col2, meta=meta : self.create_correlation_button(name, current_taxlevel, col2, meta))
            #corr_button = Button(self.frame, text='calculate correlation', command=lambda name=name, current_taxlevel=current_taxlevel, col2=col2 : self.create_correlation_button(name, current_taxlevel, col2))
            corr_button.grid(row=0, column=2)
        else:
            title = 'correlation with metadata for ' + name
            self.create_correlation_button(name, current_taxlevel, col2, meta)
            #corr_button = Button(self.frame, text='calculate correlation', command=lambda name=name, current_taxlevel=current_taxlevel, col2=col2 : self.create_correlation_button(name, col2))
        self.top.title(title)# + self.name)
        
        
        
    def create_correlation_button(self, name, current_taxlevel, col2, meta):
        #print(self.threshold.get())
        header = (current_taxlevel, 'correlation coefficient')
        if meta:
            text, corr_series = meta.getCorrelationForMetaData(name, current_taxlevel)
        else:
            text, corr_series = self.abundance_df.getCorrelationForSpecies(name, float(self.threshold.get()))
        canvas = create_canvas(frame=self.frame, xscroll=False, row=1, colspan=3)
        WIDTH = 700
        if len(corr_series) > 0:
            canvas.create_text(10, 10, text=header[0], anchor=NW)
            canvas.create_text(col2, 10, text=header[1], anchor=NW)
            corr_series.sort_values(ascending=False, inplace=True)
            for idx, name in enumerate(corr_series.index):
                txt=str(name)
                canvas.create_text(10,idx*15+30, text=txt, anchor=NW, width=WIDTH)
                txt=str(corr_series[name])
                #print(corr_series[name])
                col = 'black'
                #split on tab, convert to number, check absolute value, print
                #if corr_series[name] > 0.8:
                #    col = 'darkgreen'
                #elif corr_series[name] < 0.3:
                #    col = 'darkred'
                canvas.create_text(col2,idx*15+30, text=txt, anchor=NW, width=WIDTH, fill=col)
        else:
            if header[0] != 'metadata':
                text = 'there exist no ' + header[0] + ' that correlate with ' + self.name
            canvas.create_text(10,30, text=text, anchor=NW, width=WIDTH, fill='red')
        canvas.config(scrollregion=canvas.bbox(ALL), height=canvas.bbox(ALL)[3], width =WIDTH)
                
    def setVariable(self, name, tax_list):
        """ sets variables inside the class """
        self.name = name
        self.tax_list = tax_list
    


     
                    
class PopUpMenu():

    def __init__(self, root, name, pop_ups, abundance_df, tax_list, meta_df, all_tax_levels, current_tax_level):
        self.root = root
        self.name = name
        self.pop_ups = pop_ups
        self.abundance_df = abundance_df
        #self.threshold_slider = threshold_slider
        self.tax_list = tax_list
        self.meta_df = meta_df
        self.all_tax_levels = all_tax_levels
        self.current_tax_level = current_tax_level
        self.create_menu()
        
    def check_if_new_window(self):
        """ check if a new window should be opened """
        if self.new_bool:
            self.open_new_window()
        else:
            self.check_if_popup_open()
        
    def check_if_popup_open(self):
        """ checks if a popup window is already open, if not it creates a new one """
        if len(self.pop_ups) > 0:
            self.window = self.pop_ups[-1][0]
            self.window.empty_window(self.name)
        else:
            self.open_new_window()
    
    def compare_samples(self, event=None):
        """ displays bar graph for several samples """
        self.check_if_new_window()
        grouped = self.abundance_df.groupAllSamples()
        grouped.set_index(self.all_tax_levels[-len(self.tax_list)], drop=False, inplace=True) 
        self.window.create_graph(list(grouped.loc[self.name, grouped.columns[len(self.tax_list):-2]]), self.abundance_df.getSamplesList())
        
    def corr_metadata(self):
        """ displays the correlation of the metadata with a chosen species """
        self.check_if_new_window()
        tax_level = self.all_tax_levels[-len(self.tax_list)]
        if self.meta_df is not None:
            text, corr_series = self.meta_df.getCorrelationForMetaData(self.name, tax_level)
        else:
            text = 'no metadata loaded'
            corr_series = ''
        title = 'correlation with metadata for ' + self.name + ':'
        #self.window.create_correlation(text, corr_series, title, ('metadata', 'correlation coefficients (normal & shifted by one time point)'), 250)
        self.window.create_correlation(self.name, self.current_tax_level, col2=250, meta=self.meta_df)
        
    def corr_species(self, event=None):
        """ displays the species that have a similar abundance in all samples """
        self.check_if_new_window()
        #text, corr_series = self.abundance_df.getCorrelationForSpecies(self.name, float(self.threshold_slider.get()))
        #title = 'correlation with other species for ' + self.name + ':'
        #self.window.create_correlation(text, corr_series, title)
        self.window.create_correlation(self.name, self.current_tax_level)
    
    def create_menu(self):
        """ creates a popup menu  """
        self.popup_menu = Menu(self.root, tearoff=0)
        self.popup_menu.add_command(label='abundances in all samples', command=self.compare_samples)
        self.popup_menu.add_command(label='show information', command=self.show_information)
        self.popup_menu.add_command(label='correlation on '+self.current_tax_level+' level', command=self.corr_species)
        self.popup_menu.add_command(label='correlation wirh metadata', command=self.corr_metadata)

    def do_popup(self, event, new_bool):
        """ displays the popup menu """
        self.new_bool = new_bool
        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def open_new_window(self):
        """ opens a new popup window """
        self.window = PopUpWindow(self.root, self.name, self.pop_ups, self.abundance_df, self.tax_list, self.all_tax_levels)
        current_id = self.window.get_top_level_id()
        self.pop_ups.append((self.window, current_id))

    def show_information(self, event=None):
        """ displays wikipedia information about a species """
        self.check_if_new_window()
        self.window.create_wiki(self.name)

       
       
class PopUpInfo():
    def __init__(self, root, tax_list, all_tax_levels, tax_level, samples, abundance_df, groups=False):
        self.root = root
        self.tax_list = tax_list
        self.all_tax_levels = all_tax_levels
        self.tax_level = tax_level
        self.samples = samples
        self.abundance_df = abundance_df
        self.groups = groups
        self.create_menu()
        
    def create_menu(self):
        """ creates a popup menu  """
        self.popup_menu = Menu(self.root, tearoff=0)
        self.popup_menu.add_command(label='show information', command=self.show_information)
        if self.groups:
            self.popup_menu.add_command(label='abudances in two groups', command =  lambda groups=self.groups : self.groups_abundances(groups))
        else:
            self.popup_menu.add_command(label='abudances in all samples', command=self.all_abundances)
        
    def do_popup(self, event, new_bool, name):
        """ displays the popup menu """
        self.name = name
        self.popup_menu.post(event.x_root, event.y_root)
        
    def do_tree_popup(self, event, tree, new_bool=1):
        """ displays the popup menu """
        self.name = tree.identify_row(event.y)
        self.popup_menu.post(event.x_root, event.y_root)
    
    def all_abundances(self, event=None):
        """ creates popup window for abundance graph """
        window = PopUpWindow(self.root, self.name)
        df = self.abundance_df.getDataframe()
        df2 = df.loc[df['species']==self.name]
        abundances = df2[self.samples].values[0]
        window.create_graph(abundances, self.samples)
        
    def groups_abundances(self, event=None):
        """ creates popup window for abundance graph for two groups """
        window = PopUpWindow(self.root, self.name)
        
        df = self.abundance_df.groupAllSamples()
        df = df[df.columns[:-1]]
        df = df[df['masked']==False]
        df2 = df.loc[df[self.tax_level]==self.name]
        abundances = df2
        window.create_groups_graph(abundances, self.samples, self.groups)
        
    def show_information(self, event=None):
        """ displays wikipedia information about a species """
        window = PopUpWindow(self.root, self.name, tax_list=self.tax_list, all_tax_levels=self.all_tax_levels)
        window.create_wiki(self.name)
        
        



class BarBox():    
    def __init__(self,
                root,
                samples,
                abundance_df, 
                all_tax_levels):
        self.root = root
        self.balloon = Pmw.Balloon(root)
        self.popupinfo = PopUpInfo(self.root, [], all_tax_levels, '', samples, abundance_df)
        
    def drawBar(self, canvas, coords, color, name, sample):   
        """ draws one bar in a bar graph """          
        item = canvas.create_rectangle(coords, outline=color, fill=color, tags=(name.replace(' ','_'), sample))
        self.balloon.tagbind(canvas, item, name)
        
        canvas.tag_bind(item, '<Button-2>', lambda event, new_bool=1, name=name : self.popupinfo.do_popup(event, new_bool, name))
        return item
        
        
class OpenPopUpWindow():
    def __init__(self, root, all_tax_levels, samples, abundance_df, group1, group2):
        self.root = root
        self.all_tax_levels = all_tax_levels
        self.samples = samples
        self.abundance_df = abundance_df
        self.group1 = group1
        self.group2 = group2
        
    def open_pop_up_menu(self, event, names_list, pca=False):
        """ opens popup menu """
        index = event.widget.curselection()[0]
        if pca:
            name = names_list[index-1]
        else:
            name = names_list[index-1][1]
        popup_info = PopUpInfo(self.root, [], self.all_tax_levels, '', self.samples, self.abundance_df, groups=(self.group1, self.group2))
        popup_info.do_popup(event, new_bool=1, name=name)
             