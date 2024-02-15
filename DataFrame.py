import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class DataFrame:
    def __init__(self):
        #Private Varibles
        self._df = None
        
        self._min = []
        self._mean = []
        self._median = []
        self._std = []
        self._max = []
        
        self._unique = []
        self._frequency = []
    
    '''
    =========================Public Functions================================
    '''
        
    def genDataFrame(self, path):
        self._df = pd.read_csv(path)
        
    def setDataFrame(self, df):
        self._df = df
    
    def exportDfToCSV(self, path):
        self._df.to_csv(path)
    
    def calDataFrameStats(self):
        self.__resetStats__()
        column_names = self._df.columns.values.tolist()
        key = None
        for x in range(len(self._df.columns)):
            key = column_names[x]
            if pd.api.types.is_numeric_dtype(self._df[key]):
                self.__calNumericalStats__(key)
            else:
                self._df.astype({key : str})
                self.__calCategoricalStats__(key)
                
    def plotStats_Single_Column(self, key):
        if pd.api.types.is_numeric_dtype(self._df[key]):
            self.__boxPlot__(key)
        else:
            self.__barPlot_SC__(key)
    
    def plotStat_Double_Column(self, column_A_key, column_B_key):
        column_types = []
        if pd.api.types.is_numeric_dtype(self._df[column_A_key]):
            column_types.append("Numerical")
        else:
            column_types.append("Categorical")
            
        if pd.api.types.is_numeric_dtype(self._df[column_B_key]):
            column_types.append("Numerical")
        else:
            column_types.append("Categorical")
            
        if column_types[0] == "Numerical" and column_types[1] == "Numerical":
            self.__scatterPlot__(column_A_key, column_B_key)
        elif column_types[0] == "Categorical" and column_types[1] == "Numerical":
            self.__barPlot_DC__(column_A_key, column_B_key)
        elif column_types[0] == "Numerical" and column_types[1] == "Categorical":
            self.__barPlot_DC__(column_B_key, column_A_key)
        elif column_types[0] == "Categorical" and column_types[1] == "Categorical":
            self.__heatMap__(column_A_key, column_B_key)
                
    '''
    =========================Private Functions================================
    '''
    
    def __resetStats__(self):
        self._min = []
        self._mean = []
        self._median = []
        self._std = []
        self._max = []
        
        self._unique = []
        self._frequency = []
    
    def __calNumericalStats__(self, key):
        self._min.append(self._df[key].min())
        self._mean.append(self._df[key].mean())
        self._median.append(self._df[key].median())
        self._std.append(self._df[key].std())
        self._max.append(self._df[key].max())
        
        self._unique.append(None)
        self._frequency.append(None)
    
    def __calCategoricalStats__(self, key):
        self._min.append(None)
        self._mean.append(None)
        self._median.append(None)
        self._std.append(None)
        self._max.append(None)
        
        self._frequency.append(self._df[key].value_counts())
        self._unique.append(self._df[key].unique())
        
    '''
    ------------------------Single Column Plot Functions----------------------
    '''
        
    def __boxPlot__(self, key):
        values = self._df[key].values.tolist()
        column_index = self._df.columns.get_loc(key)
        plt.title(key + " Column Plot")
        plt.xlabel(key)
        plt.ylabel("Graph")
        plt.tick_params(labelleft = False)
        plt.grid(True)
        plt.boxplot(values, vert = False, showmeans=True)
        stdValue_lower = self._mean[column_index] - self._std[column_index]
        stdValue_higher = self._mean[column_index] + self._std[column_index]
        plt.axvline(stdValue_lower, 0.4, 0.6, color = "b")
        plt.axvline(stdValue_higher, 0.4, 0.6, color = "b")
    
    def __barPlot_SC__(self, key):
        column_index = self._df.columns.get_loc(key)
        plt.title(key + " Column Plot")
        plt.xlabel(key)
        plt.ylabel("Frequency")
        plt.grid(True)
        plt.bar(self._unique[column_index].tolist(), self._frequency[column_index].values.tolist())
        
    '''
    ------------------------Double Column Plot Functions----------------------
    '''
    
    
    def __scatterPlot__(self, column_A_key, column_B_key):
        '''
        Scatterplot if both columns are numerical

        Parameters
        ----------
        column_A_key : str
            Column A access key
        column_B_key : str
            Column B access key

        Returns
        -------
        None.

        '''
        plt.title(column_A_key + " VS. " + column_B_key + " Column Plot")
        plt.xlabel(column_A_key)
        plt.ylabel(column_B_key)
        plt.grid(True)
        plt.scatter(self._df[column_A_key].values.tolist(), self._df[column_B_key].values.tolist())
        
        
    def __barPlot_DC__(self, column_Cat_key, column_Num_key):
        '''
        Barplot if one column is categorical and one is numerical

        Parameters
        ----------
        column_Cat_key : str
            Categorical column access key
        column_Num_key : str
            Numerical column access key

        Returns
        -------
        None.

        '''
        column_index = self._df.columns.get_loc(column_Cat_key)
        uv = self._unique[column_index].tolist()
        totals = []
        for x in range(len(uv)):
            df = self._df.query(column_Cat_key + " == '" + uv[x] + "'")
            totals.append(df[column_Num_key].sum())   
        plt.title(column_Cat_key + " VS. " + column_Num_key + " Column Plot")
        plt.xlabel(column_Cat_key)
        plt.ylabel(column_Num_key)
        plt.grid(True)
        plt.bar(uv, totals)
        
        
    def __heatMap__(self, column_A_key, column_B_key):
        '''
        Heatmap if both columns are categorical

        Parameters
        ----------
        column_A_key : str
            Column A access key
        column_B_key : str
            Column B access key

        Returns
        -------
        None.

        '''
        column_index_A = self._df.columns.get_loc(column_A_key)
        column_index_B = self._df.columns.get_loc(column_B_key)
        uv_A = self._unique[column_index_A].tolist()
        uv_B = self._unique[column_index_B].tolist()
        data_count = []
        for x in range(len(uv_A)):
            data_count.append([])
            for y in range(len(uv_B)):
                df = self._df.query(column_A_key + " == '" + uv_A[x] + "'")
                df = df.query(column_B_key + " == '" + uv_B[y] + "'")
                data_count[x].append(len(df))
        plt.title(column_A_key + " VS. " + column_B_key + " Column Plot")
        plt.xlabel(column_B_key)
        plt.ylabel(column_A_key)
        plt.xticks(np.arange(len(uv_B)), labels = uv_B)
        plt.yticks(np.arange(len(uv_A)), labels = uv_A)
        plt.grid(True)
        plt.imshow(data_count)