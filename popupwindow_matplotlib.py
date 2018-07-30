import os, sys
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import asksaveasfilename
import pandas as pd
import numpy as np
import tkinter.messagebox as tmb

#import matplotlib
#matplotlib.use("TkAgg")

from skbio.diversity.alpha import shannon

from general_functions import *

import matplotlib
matplotlib.use('TkAgg')


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from scipy.spatial.distance import squareform


class PopUpIncludingMatplotlib():
    
    def __init__(self, root, abundance_df, all_tax_levels):
        self.root = root
        self.abundance_df = abundance_df
        self.all_tax_levels = all_tax_levels
        self.HEIGHT = 400
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
        
        
    
    #def richness_groups(self, working_samples, samples_list, tax_level):
    def richness_groups(self, working_samples, sample_names, tax_level, samples1, samples2, richness, samples1_label, samples2_label):
        """  """
        #(self, df)
        
        self.create_window()
        
        #print(working_samples.head())
        #working_samples.index = working_samples.loc[:,tax_level]
        #richness = working_samples.astype(bool).sum(axis=0)[:-1]
        #print(samples1)
        #print(samples2)
        #print(richness)
        fig = Figure(figsize=(5,5), dpi=120)
        ax = fig.add_subplot(111)
        #data = [df[df['year']=='2012']['richness'].values, df[df['year']=='2013']['richness'].values]
        data = [richness[samples1].values, richness[samples2].values]
        
        bp = ax.boxplot(data)
        ax.set_xticklabels([samples1_label,samples2_label], rotation=45, fontsize=8)
        ax.set_title('richness')
        #add median text
        medians = [med.get_ydata()[0] for med in bp['medians']]
        median_labels = [str(np.round(med, 2)) for med in medians]
        for group_num in [0, 1]:
            ax.text(group_num+1, max(richness)*1.005, median_labels[group_num], horizontalalignment='center', size='x-small')
        
        #t-test (Wlech's-test does not assume equal variance)
        from scipy.stats import ttest_ind
        ttest_result = ttest_ind(richness[samples1].values, richness[samples2].values, equal_var=False)
        ax.text(1.5, min(richness)*0.995, 'T_stat: '+str(round(ttest_result[0],2))+', p_val: '+str('{0:.0e}'.format(ttest_result[1])), horizontalalignment='center', size='x-small')
        
        #ax = fig.add_subplot(212)
        #data = [df[df['year']=='2012']['shannon_index'].as_matrix(), df[df['year']=='2013']['shannon_index'].as_matrix()]
        #ax.boxplot(data)
        #ax.set_xticklabels(['2012','2013'], rotation=45, fontsize=8)
        #ax.set_title('shannon_index')
        #plt.show()
        fig.subplots_adjust(left=0.08, right=0.98, bottom=0.2, top=0.95, hspace=0.4, wspace=0.3)
        matplotlib_frame = Frame(self.frame)
        matplotlib_frame.grid(row=0, column=0)
        canvas = FigureCanvasTkAgg(fig, matplotlib_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, matplotlib_frame)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
    
    def richness_all_samples(self, working_samples, samples_list, tax_level):
        self.create_window()
        
        self.top.title('overview of richness of all samples on ' + tax_level + ' level')
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=2, column=0, columnspan=4)
        
        top_space = 20
        width=600
        if len(samples_list)> 20:
            width = 1000
        
        start_idx = len(self.all_tax_levels) - list(self.all_tax_levels).index(tax_level)
        if self.abundance_df.groupAbsoluteSamples() is not None:
            absolute_working_samples = self.abundance_df.groupAbsoluteSamples()
            absolute_working_samples = absolute_working_samples[samples_list].astype('int')
            richness = absolute_working_samples.astype(bool).sum(axis=0)[:-2]
        else:
            richness = working_samples.astype(bool).sum(axis=0)[start_idx:-2]
        
        
        
        fig = Figure(figsize=(4,6), dpi=120)
        ax = fig.add_subplot(211)
        bp = ax.boxplot(richness)
        for val in richness:
            x = np.random.normal(1, 0.04, 1)
            ax.scatter(x, val, c='grey', marker='.', alpha=0.4)

        ax.set_xticklabels(['richness'])
        ax.set_ylabel('number of species')
        
        #add median text
        medians = [med.get_ydata()[0] for med in bp['medians']]
        median_labels = [str(np.round(med, 2)) for med in medians]
        ax.text(1, max(richness)*1.01, median_labels[0], horizontalalignment='center', size='x-small')
        
        ax = fig.add_subplot(212)
        for i,val in enumerate(richness):
            ax.scatter(richness.index[i],val,marker='.')
        ax.set_xticklabels(richness.index, fontsize=8, rotation='vertical')
        ax.set_xlabel('samples')
        ax.set_ylabel('number of species')
        
        fig.subplots_adjust(left=0.1, right=0.98, bottom=0.3, top=0.95, hspace=0.3, wspace=0.3)
        
        matplotlib_frame = Frame(self.frame)
        matplotlib_frame.grid(row=0, column=0, rowspan=2, columnspan=2)
        canvas = FigureCanvasTkAgg(fig, matplotlib_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, matplotlib_frame)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
    
    def shannon_diversity_all_samples(self, working_samples, samples_list, tax_level):
        from skbio.diversity.alpha import shannon
        self.create_window()
        
        self.top.title('overview of Shannon index of all samples on ' + tax_level + ' level')
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=2, column=0, columnspan=4)
        
        top_space = 20
        width=600
        if len(samples_list)> 20:
            width = 1000
        
        #shannon index (alpha diversity)
        if self.abundance_df.groupAbsoluteSamples() is not None:
            absolut_working_samples = self.abundance_df.groupAbsoluteSamples()
            absolut_working_samples = absolut_working_samples[samples_list].astype('int')
            #print(absolut_working_samples.head())
            shannon0 = absolut_working_samples.loc[working_samples.index].apply(shannon)
            #print('missing')
        else:
            shannon0  = []
            for sample in samples_list:
                shannon0.append(shannon_index(working_samples[sample].as_matrix()))
            shannon0 = pd.Series(shannon0, index=samples_list)
            #print('no absolute counts')
        
        fig = Figure(figsize=(4,6), dpi=120)
        ax = fig.add_subplot(211)
        bp = ax.boxplot(shannon0)
        for val, in zip(shannon0):
            x = x = np.random.normal(1, 0.04, 1)
            ax.scatter(x, val, c='grey', marker='.', alpha=0.4)
        #ax.set_title('Shannon diversity index')
        ax.set_xticklabels(['Shannon diversity'])
        #ax.set_ylabel('number of species')
        
        #add median text
        medians = [med.get_ydata()[0] for med in bp['medians']]
        median_labels = [str(np.round(med, 2)) for med in medians]
        ax.text(1, max(shannon0)*1.01, median_labels[0], horizontalalignment='center', size='x-small')
        
        ax = fig.add_subplot(212)
        for i,val in enumerate(shannon0):
            ax.scatter(shannon0.index[i],val,marker='.')
        ax.set_xticklabels(shannon0.index, fontsize=8, rotation='vertical')
        ax.set_xlabel('samples')
        ax.set_ylabel('Shannon diversity index')
        fig.subplots_adjust(left=0.1, right=0.98, bottom=0.3, top=0.95, hspace=0.3, wspace=0.3)
        
        matplotlib_frame = Frame(self.frame)
        matplotlib_frame.grid(row=0, column=0, rowspan=2, columnspan=2)
        canvas = FigureCanvasTkAgg(fig, matplotlib_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, matplotlib_frame)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
    
    def shannon_diversity_groups(self, working_samples, sample_names, tax_level, samples1, samples2, shannon1, samples1_label, samples2_label):
        """  """
        self.create_window()
        
        if self.abundance_df.groupAbsoluteSamples() is not None:
            absolut_working_samples = self.abundance_df.groupAbsoluteSamples()
            absolut_working_samples = absolut_working_samples[sample_names].astype('int')
            #print(absolut_working_samples.head())
            shannon0 = absolut_working_samples.loc[working_samples.index].apply(shannon)
            #print('missing')
        else:
            shannon0  = []
            for sample in sample_names:
                shannon0.append(shannon_index(working_samples[sample].as_matrix()))
            shannon0 = pd.Series(shannon0, index=sample_names)
        
        fig = Figure(figsize=(5,5), dpi=120)
        ax = fig.add_subplot(111)
        data = [shannon0[samples1].values, shannon0[samples2].values]
        bp = ax.boxplot(data)
        ax.set_xticklabels([samples1_label,samples2_label], rotation=45, fontsize=8)
        ax.set_title('shannon')
        
        #add median text
        medians = [med.get_ydata()[0] for med in bp['medians']]
        median_labels = [str(np.round(med, 2)) for med in medians]
        for group_num in [0, 1]:
            ax.text(group_num+1, max(shannon0)*1.005, median_labels[group_num], horizontalalignment='center', size='x-small')
        
        from scipy.stats import ttest_ind
        ttest_result = ttest_ind(shannon0[samples1].values, shannon0[samples2].values, equal_var=False)
        ax.text(1.5, min(shannon0)*0.995, 'T_stat: '+str(round(ttest_result[0],2))+', p_val: '+str('{0:.0e}'.format(ttest_result[1])), horizontalalignment='center', size='x-small')
        
        fig.subplots_adjust(left=0.08, right=0.98, bottom=0.2, top=0.95, hspace=0.4, wspace=0.3)
        matplotlib_frame = Frame(self.frame)
        matplotlib_frame.grid(row=0, column=0)
        canvas = FigureCanvasTkAgg(fig, matplotlib_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, matplotlib_frame)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
    
    def beta_diversity_heatmap(self, working_samples, samples_list, tax_level):
        """  """
        from skbio.diversity import beta_diversity
        import seaborn as sns
        
        #from scipy.spatial.distance import squareform
        
        # self.create_window()
        
        # self.top.title('overview of Shannon index of all samples on ' + tax_level + ' level')
        # self.inner_frame = Frame(self.frame)
        # self.inner_frame.grid(row=2, column=0, columnspan=4)
        
        if self.abundance_df.groupAbsoluteSamples() is not None:
            data0 = self.abundance_df.groupAbsoluteSamples()[samples_list].astype('int')
            data0 = data0.loc[working_samples.index]
            ids = list(data0.columns)
            data = data0.transpose().values.tolist()

            #print(data)
            bc_dm = beta_diversity("braycurtis", data, ids)
            #g = sns.clustermap(pd.DataFrame(bc_dm.data, index=ids, columns=ids), 'braycurtis')#, linewidths=.75, figsize=(30, 30), cmap="Oranges", row_colors=row_colors, col_colors=col_colors,)

            g = sns.clustermap(pd.DataFrame(bc_dm.data, index=ids, columns=ids), metric='braycurtis')
            filename = asksaveasfilename(initialfile='beta_diversity_heatmap', defaultextension='.png')
            g.savefig(filename)
            
            import matplotlib.pyplot as plt
            plt.close("all")

        

    
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
        #self.top.minsize(width=666, height=666)
        #self.top.maxsize(width=666, height=666)
        self.top.focus_set()
        
    def cancel(self, event=None):
        """ destroys/closes pop up windows """
        self.top.destroy()
