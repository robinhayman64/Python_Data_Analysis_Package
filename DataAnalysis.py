import DataFrame
import subprocess
import threading

class DataAnalysis:
    def __init__(self):
        #Private Members
        self._fileList = []
        self._dataFrames = []
        self._execSuccessFlags = []
        
        self._threads = []
        self._threadFlags = []
        
        
        self._filePath = ''
        
    '''
    =========================Public Functions=================================
    '''
    
    #Clears all dataframes
    def clearDataFrames(self):
        self._dataFrames = []
        self._execSuccessFlags = []
    
    #Adds a CSV file to generate a dataframe
    def addCSV(self, fileDir):
        self._fileList.append(fileDir)
    
    #Generates dataframes from the CSV file list in a multi-threaded manner 
    def genDataFrames(self, threadCount = 1):
        for x in range(len(self._fileList)):
            self._dataFrames.append(DataFrame.DataFrame())
            self._execSuccessFlags.append(True)
        self.__threadMachine__(self.__genDataFrame_Thread__, threadCount)
        return self._execSuccessFlags
        
    #Append dataframe to dataframe list
    def appendDataFrame(self, df):
        self._dataFrames.append(DataFrame.DataFrame())
        self._execSuccessFlags.append(True)
        index = len(self._dataFrames) - 1
        self._dataFrames[index].setDataFrame(df)
        
        
    def exportDfToCSV_Single(self, filePath, dfID):
        self._execSuccessFlags[dfID] = True
        try:
            self._dataFrames[dfID].exportDfToCSV(filePath + ".csv")
        except:
            self._execSuccessFlags[dfID] = False
        return self._execSuccessFlags[dfID]
        
    def exportDfToCSV_All(self, filePath, threadCount = 1):
        self._filePath = filePath
        self.__threadMachine__(self.__exportToCSV_Thread__, threadCount)
        return self._execSuccessFlags
    
    def calDataFrameStats_Single(self, dfID):
        self._execSuccessFlags[dfID] = True
        try:
            self._dataFrames[dfID].calDataFrameStats()
        except:
            self._execSuccessFlags[dfID] = False
        return self._execSuccessFlags[dfID]
    
    def calDataFrameStats_All(self, threadCount):
        self.__threadMachine__(self.__calDataFrameStats_Thread__, threadCount)
        return self._execSuccessFlags
    
    def plotSingleColumn(self, dfID, key):
        self._dataFrames[dfID].plotStats_Single_Column(key)
        
    def plotDoubleColumn(self, dfID, column_A_key, column_B_key):
        self._dataFrames[dfID].plotStat_Double_Column(column_A_key, column_B_key)
    
    def rsync(self, filePath_source, filePath_dest):
        subprocess.call(["rsync", "-a", filePath_source, filePath_dest])
    
    '''
    =========================Private Functions================================
    '''
    
    '''
    ------------------------Thread Machine Function----------------------------
    '''
    
    def __threadMachine__(self, function, threadCount):
        self._threads = []
        self._threadFlags = []
        for x in range(threadCount):
            self._threads.append(None)
            self._threadFlags.append(False)
        dfIndex = 0
        endFlag = False
        #Main Thread Loop
        while endFlag == False:
            endFlag = True
            for threadID in range(threadCount):
                #Check if thread is active
                if self._threadFlags[threadID] == True:
                    endFlag = False
                #Check if new thread should be allocated
                elif dfIndex < len(self._dataFrames):
                    self._threadFlags[threadID] = True
                    self._threads[threadID] = threading.Thread(target = function, 
                                                    args = (dfIndex, threadID))
                    self._threads[threadID].start()
                    dfIndex += 1
                    endFlag = False
        
    '''
    ---------------------------Thread Functions-------------------------------
    '''
        
    def __genDataFrame_Thread__(self, dfID, threadID):
        self._execSuccessFlags[dfID] = True
        #self._dataFrames[dfID].genDataFrame(self._fileList[dfID])
        try:
            self._dataFrames[dfID].genDataFrame(self._fileList[dfID])
        except:
            self._execSuccessFlags[dfID] = False
        self._threadFlags[threadID] = False
        
    def __exportToCSV_Thread__(self, dfID, threadID):
        self._execSuccessFlags[dfID] = True
        try:
            self._dataFrames[dfID].exportDfToCSV(self._filePath + "_" + str(dfID) + ".csv")
        except:
            self._execSuccessFlags[dfID] = False
        self._threadFlags[threadID] = False
        
    def __calDataFrameStats_Thread__(self, dfID, threadID):
        self._execSuccessFlags[dfID] = True
        #self._dataFrames[dfID].calDataFrameStats()
        try:
            self._dataFrames[dfID].calDataFrameStats()
        except:
            self._execSuccessFlags[dfID] = False
        self._threadFlags[threadID] = False
        
