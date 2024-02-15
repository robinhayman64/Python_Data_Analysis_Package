import DataAnalysis
import datetime
import matplotlib.pyplot as plt

UNIT_TEST = 0
GRAPH_TEST = 5
THREAD_POWER_MIN = 0
THREAD_POWER_MAX = 5

filePath = "Exports/file"
fileList = []
threadCount = []
processTime = []
DA = DataAnalysis.DataAnalysis()

'''
---------------------------Data Analysis Unit Test----------------------------
'''

def dataAnalysis_UnitTest():
    fileList_Import_DA()
    for x in range(len(fileList)):
        DA.addCSV(fileList[x])
    DA.genDataFrames()
    DA.calDataFrameStats_Single(0)
    DA.exportDfToCSV_Single(filePath, 0)
    graphPlot()

def fileList_Import_DA():
    global fileList
    fileList = ["Test_Data/sales-data.csv",
                "Test_Data/447-monica-power-july-2023.csv"]
    
def graphPlot():
    if GRAPH_TEST == 0:
        DA.plotSingleColumn(0, "Revenue")
    elif GRAPH_TEST == 1:
        DA.plotSingleColumn(0, "Product")
    elif GRAPH_TEST == 2:
        DA.plotDoubleColumn(0, "Quantity Sold", "Revenue")
    elif GRAPH_TEST == 3:
        DA.plotDoubleColumn(0, "Product", "Quantity Sold")
    elif GRAPH_TEST == 4:
        DA.plotDoubleColumn(0, "Revenue", "Product")
    elif GRAPH_TEST == 5:
        DA.plotDoubleColumn(0, "Product", "Date")
    
'''
------------------------------Multithread Unit Test----------------------------
'''
    
def mutiThread_UnitTest():
    fileList_Import_MT()
    for x in range(len(fileList)):
        DA.addCSV(fileList[x])
    for x in range(THREAD_POWER_MIN, THREAD_POWER_MAX + 1):
        MT_TestRun(2 ** x)
    plotMT()

def fileList_Import_MT():
    global fileList
    for x in range(32):
        fileList.append("Test_Data_Multi/447-monica-power-july-2023 - Copy (" + str(x) + ").csv")
        
def MT_TestRun(threads):
    DA.clearDataFrames()
    begin = datetime.datetime.now()
    DA.genDataFrames(threads)
    DA.calDataFrameStats_All(threads)
    DA.exportDfToCSV_All(filePath)
    end = datetime.datetime.now()
    threadCount.append(threads)
    processTime.append((end - begin).total_seconds())
    
def plotMT():
    plt.title("Multi-Thread Advantage Plot")
    plt.xlabel("Threads")
    plt.ylabel("Time (sec)")
    plt.grid(True)
    plt.plot(threadCount, processTime)
    
'''
----------------------------------Main Function-------------------------------
'''

def main():
    if UNIT_TEST == 0:
        dataAnalysis_UnitTest()
    if UNIT_TEST == 1:
        mutiThread_UnitTest()

main()