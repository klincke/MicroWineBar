import os, sys
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import asksaveasfilename
import pandas as pd
import numpy as np
import tkinter.messagebox as tmb

from skbio.diversity.alpha import shannon

from .general_functions import *

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
matplotlib.rcParams.update({'font.size': 10})

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
        
    def save_high_resolution_figure(self, fig, title, initialfile, defaultextension='.png'):
        """ saves a figure in high resolution """
        filename = asksaveasfilename(title=title, initialfile=initialfile, defaultextension=defaultextension, filetypes=(("PNG files","*.png"), ("EPS files","*.eps"), ("JPEG files","*.jpg"), ("TIFF files","*.tiff")))
        fig.savefig(filename, dpi=600)
        return filename
        
    
    #def richness_groups(self, working_samples, samples_list, tax_level):
    def richness_groups(self, working_samples, sample_names, tax_level, samples1, samples2, richness, samples1_label, samples2_label):
        """  """
        
        self.create_window()
        self.top.title('Richness')
        
        fig = Figure(figsize=(5,6), dpi=120)
        ax = fig.add_subplot(111)
        data = [richness[samples1].values, richness[samples2].values]
        
        bp = ax.boxplot(data)
        ax.set_xticklabels([samples1_label,samples2_label], rotation=45, fontsize=12)
        ax.set_ylabel('richness', fontsize=12)
        #add median text
        medians = [med.get_ydata()[0] for med in bp['medians']]
        median_labels = [str(np.round(med, 2)) for med in medians]
        #t-test (Wlech's-test does not assume equal variance)
        from scipy.stats import ttest_ind
        ttest_result = ttest_ind(richness[samples1].values, richness[samples2].values, equal_var=False)
        ttest_res = ['T_stat: '+str(round(ttest_result[0],2)), 'p_val: '+str('{0:.0e}'.format(ttest_result[1]))]

        #fig.subplots_adjust(left=0.08, right=0.98, bottom=0.2, top=0.97, hspace=0.2, wspace=0.2)
        fig.set_tight_layout(True)
        matplotlib_frame = Frame(self.frame)
        matplotlib_frame.grid(row=2, column=0)
        canvas = FigureCanvasTkAgg(fig, matplotlib_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        save_button = Button(self.frame, text="Save (high resolution)", command=lambda fig=fig, title='Richness', initialfile='richness_groups': self.save_high_resolution_figure(fig, title, initialfile))
        save_button.grid(row=1, column=0)
        return (median_labels, ttest_res)
    
    def richness_all_samples(self, working_samples, samples_list, tax_level):
        self.create_window()
        self.top.title('Richness')
        
        self.top.title('overview of richness of all samples on ' + tax_level + ' level')
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=1, column=0, columnspan=4)
        
        top_space = 20
        width=600
        if len(samples_list)> 20:
            width = 1000
        
        start_idx = len(self.all_tax_levels) - list(self.all_tax_levels).index(tax_level)
        if self.abundance_df.groupAbsoluteSamples() is not None:
            absolute_working_samples = self.abundance_df.groupAbsoluteSamples()
            absolute_working_samples = absolute_working_samples[samples_list].astype('int')
            richness = absolute_working_samples.astype(bool).sum(axis=0)
        else:
            richness = working_samples.astype(bool).sum(axis=0)[start_idx:-2]
        
        fig = Figure(figsize=(4,6), dpi=120)#, tight_layout=True)
        ax = fig.add_subplot(211)
        bp = ax.boxplot(richness)
        for val in richness:
            x = np.random.normal(1, 0.04, 1)
            ax.scatter(x, val, c='grey', marker='.', alpha=0.4)

        ax.set_xticklabels([''])
        ax.set_ylabel('number of ' + tax_level)
        
        
        ax = fig.add_subplot(212)
        for i,val in enumerate(richness):
            ax.scatter(richness.index[i],val,marker='.')
        ax.set_xticklabels(richness.index, fontsize=8, rotation='vertical')
        ax.set_xlabel('samples')
        ax.set_ylabel('number of ' + tax_level)
        
        fig.subplots_adjust(left=0.1, right=0.98, bottom=0.2, top=0.95, hspace=0.2, wspace=0.2)
        
        matplotlib_frame = Frame(self.frame)
        matplotlib_frame.grid(row=2, column=0, rowspan=2, columnspan=2)
        canvas = FigureCanvasTkAgg(fig, matplotlib_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=4)

        save_button = Button(self.inner_frame, text="Save (high resolution)", command=lambda fig=fig, title='Richness', initialfile='richness_all_samples': self.save_high_resolution_figure(fig, title, initialfile))
        save_button.grid(row=1, column=0)

    
    def shannon_diversity_all_samples(self, working_samples, samples_list, tax_level):
        from skbio.diversity.alpha import shannon
        self.create_window()
        self.top.title('Shannon diversity')
        
        self.top.title('overview of Shannon index of all samples on ' + tax_level + ' level')
        self.inner_frame = Frame(self.frame)
        self.inner_frame.grid(row=1, column=0, columnspan=4)
        
        top_space = 20
        width=600
        if len(samples_list)> 20:
            width = 1000
        
        #shannon index (alpha diversity)
        if self.abundance_df.groupAbsoluteSamples() is not None:
            absolut_working_samples = self.abundance_df.groupAbsoluteSamples()
            absolut_working_samples = absolut_working_samples[samples_list].astype('int')
            shannon0 = absolut_working_samples.loc[[tax+'_' for tax in list(working_samples[tax_level])]].apply(shannon)
        else:
            shannon0  = []
            for sample in samples_list:
                shannon0.append(shannon_index(working_samples[sample].as_matrix()))
            shannon0 = pd.Series(shannon0, index=samples_list)
        
        fig = Figure(figsize=(4,6), dpi=120)#, tight_layout=True)
        ax = fig.add_subplot(211)
        bp = ax.boxplot(shannon0)
        for val, in zip(shannon0):
            x = x = np.random.normal(1, 0.04, 1)
            ax.scatter(x, val, c='grey', marker='.', alpha=0.4)
        ax.set_xticklabels(['Shannon diversity'])
        #ax.set_ylabel('number of species')
        
        ax = fig.add_subplot(212)
        for i,val in enumerate(shannon0):
            ax.scatter(shannon0.index[i],val,marker='.')
        ax.set_xticklabels(shannon0.index, fontsize=8, rotation='vertical')
        ax.set_xlabel('samples')
        ax.set_ylabel('Shannon diversity index')
        fig.subplots_adjust(left=0.1, right=0.98, bottom=0.2, top=0.95, hspace=0.3, wspace=0.3)
        
        matplotlib_frame = Frame(self.frame)
        matplotlib_frame.grid(row=2, column=0, rowspan=2, columnspan=2)
        canvas = FigureCanvasTkAgg(fig, matplotlib_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        save_button = Button(self.inner_frame, text="Save (high resolution)", command=lambda fig=fig, title='Shannon diversity', initialfile='shannon_all_samples': self.save_high_resolution_figure(fig, title, initialfile))
        save_button.grid(row=1, column=0)
    

    def shannon_diversity_groups(self, working_samples, sample_names, tax_level, samples1, samples2, shannon1, samples1_label, samples2_label):
        """  """
        self.create_window()
        self.top.title('Shannon diversity')
        
        if self.abundance_df.groupAbsoluteSamples() is not None:
            absolut_working_samples = self.abundance_df.groupAbsoluteSamples()
            absolut_working_samples = absolut_working_samples[sample_names].astype('int')
            shannon0 = absolut_working_samples.loc[[tax+'_' for tax in list(working_samples[tax_level])]].apply(shannon)
        else:
            shannon0  = []
            for sample in sample_names:
                shannon0.append(shannon_index(working_samples[sample].as_matrix()))
            shannon0 = pd.Series(shannon0, index=sample_names)
        
        fig = Figure(figsize=(5,6), dpi=120)
        ax = fig.add_subplot(111)
        data = [shannon0[samples1].values, shannon0[samples2].values]
        bp = ax.boxplot(data)
        ax.set_xticklabels([samples1_label,samples2_label], rotation=45, fontsize=12)
        ax.set_ylabel('Shannon diversity', fontsize=12)
        
        #add median text
        medians = [med.get_ydata()[0] for med in bp['medians']]
        median_labels = [str(np.round(med, 2)) for med in medians]
         
        from scipy.stats import ttest_ind
        ttest_result = ttest_ind(shannon0[samples1].values, shannon0[samples2].values, equal_var=False)
        ttest_res = ['T_stat: '+str(round(ttest_result[0],2)), 'p_val: '+str('{0:.0e}'.format(ttest_result[1]))]

        #fig.subplots_adjust(left=0.1, right=0.98, bottom=0.2, top=0.97, hspace=0.2, wspace=0.2)
        fig.set_tight_layout(True)
        matplotlib_frame = Frame(self.frame)
        matplotlib_frame.grid(row=2, column=0)
        canvas = FigureCanvasTkAgg(fig, matplotlib_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        save_button = Button(self.frame, text="Save (high resolution)", command=lambda fig=fig, title='Shannon diversity', initialfile='shannon_groups': self.save_high_resolution_figure(fig, title, initialfile))
        save_button.grid(row=1, column=0)
        return (median_labels, ttest_res)

    
    def beta_diversity_heatmap(self, working_samples, samples_list, tax_level):
        """  """
        from skbio.diversity import beta_diversity
        import seaborn as sns
        
        if self.abundance_df.groupAbsoluteSamples() is not None:
            data0 = self.abundance_df.groupAbsoluteSamples()[samples_list].astype('int')
            ids = list(data0.columns)
            data = data0.transpose().values.tolist()

            bc_dm = beta_diversity("braycurtis", data, ids)
            
            g = sns.clustermap(pd.DataFrame(bc_dm.data, index=ids, columns=ids), metric='braycurtis', annot_kws={"size": 8})

            self.save_high_resolution_figure(g, 'Select file to save the beta diversity heatmap', 'beta_diversity_heatmap', defaultextension='.png')
            
            import matplotlib.pyplot as plt
            plt.close("all")
    
    def cluster_heatmap(self, working_samples, samples_list, tax_level):
        """ saves a cluster heatmap based on Aitchison distance and the y-axis labels"""
        from skbio.stats.composition import clr
        from skbio.stats.composition import multiplicative_replacement
        import seaborn as sns

        if self.abundance_df.groupAbsoluteSamples() is not None:
            data0 = self.abundance_df.groupAbsoluteSamples()[samples_list].astype('int')
            ids = list(data0.columns)
            index0 = list(data0.index)
            data1 = clr(data0.transpose().values.tolist())
            mr_df = multiplicative_replacement(data0.T)
            mr_clr = clr(mr_df)
            mr_clr_df = pd.DataFrame(mr_clr.T, index=index0, columns=ids)

            #g = sns.clustermap(mr_clr_df, metric="correlation", cmap="mako", robust=True, annot_kws={"size": 6})
            g = sns.clustermap(mr_clr_df, metric="euclidean", cmap="mako", robust=True, annot_kws={"size": 6}, yticklabels=False)

            filename = self.save_high_resolution_figure(g, 'Select file to save the cluster heatmap', 'cluster_heatmap', defaultextension='.png')
            filename = ('.').join(filename.split('.')[:-1])
            #save y-axis labels
            y_labels = list(data0.iloc[g.dendrogram_row.reordered_ind].index)
            with open(filename+'_yaxis_labels.txt', 'w') as f:
                f.write('\n'.join([x.strip('_') for x in y_labels]))

            import matplotlib.pyplot as plt
            plt.close("all")

    def pcoa(self, pco1_group2, pco1_group1, pco2_group2, pco2_group1, samples1_label, samples2_label, pc_nums, pca=False):
        
        self.create_window()
        if pca:
            self.top.title('PCA - Principal Component Analysis')
            method = 'PCA'
        else:
            self.top.title('PCoA - Principal Coordinate Analysis')
            method = 'PCoA'
        fig = Figure(figsize=(6,6), dpi=120)
        ax = fig.add_subplot(111)
    
        ax.scatter(x=pco1_group1, y=pco2_group1, c='darkgreen', label=samples1_label)
        ax.scatter(x=pco1_group2, y=pco2_group2, c='cornflowerblue', label=samples2_label)
        #if pca:
        #    ax.set_title('PCA')
        #else:
        #    ax.set_title('PCoA')
        ax.set_xlabel('PC'+str(pc_nums[0]+1), fontsize=12)
        ax.set_ylabel('PC'+str(pc_nums[1]+1), fontsize=12)
        ax.legend(loc='best', shadow=False, scatterpoints=1)
    
        fig.subplots_adjust(left=0.14, right=0.98, bottom=0.1, top=0.95, hspace=0.4, wspace=0.3)
        matplotlib_frame = Frame(self.frame)
        matplotlib_frame.grid(row=2, column=0)
        canvas = FigureCanvasTkAgg(fig, matplotlib_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        save_button = Button(self.frame, text="Save (high resolution)", command=lambda fig=fig, title=method, initialfile=method: self.save_high_resolution_figure(fig, title, initialfile))
        save_button.grid(row=1, column=0)

    
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
