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
                self.__calCategoricalStats__(key)
                
    def plotStats_Single_Column(self, key):
        if pd.api.types.is_numeric_dtype(self._df[key]):
            self.__boxPlot__(key)
        else:
            self.__histogramPlot__(key)
    
    def plotStat_Double_Column(self, column_A_key, column_B_key):
        pass
                
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
        
    def __boxPlot__(self, key):
        values = self._df[key].values.tolist()
        column_index = self._df.columns.get_loc(key)
        plt.title(key + " Column Plot")
        plt.xlabel(key)
        plt.ylabel("Graph")
        plt.boxplot(values, vert = False, showmeans=True)
        stdValue_lower = self._mean[column_index] - self._std[column_index]
        stdValue_higher = self._mean[column_index] + self._std[column_index]
        plt.axvline(stdValue_lower, 0.4, 0.6, color = "b")
        plt.axvline(stdValue_higher, 0.4, 0.6, color = "b")
    
    def __histogramPlot__(self, key):
        pass
    
    