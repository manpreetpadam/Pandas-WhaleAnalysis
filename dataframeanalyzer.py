from pathlib import Path
import pandas as pd
import numpy as np
import datetime as dt

class dataframeanalayzer:
    
    def __init__(self):
        self.portfolio=pd.DataFrame()
        
    def loadcvstodataframe(self, sourcepath,indexcol):
        csvfile=Path(sourcepath)
        
        #create data frame from csv file
        _df=pd.read_csv(csvfile,index_col=indexcol,infer_datetime_format=True,parse_dates=True)
        return _df

    def createportfolio(self,dataframes):
        self.portfolio=pd.concat(dataframes,axis='columns',join='inner').dropna()
    
    def concatdataframes(self,dataframes,axisvalue):
        return pd.concat(dataframes,axis=axisvalue,join='inner').dropna()

    def nullcount(self,dataframe):
        return dataframe.isnull().sum()

    def dropnulls(self,dataframe):
       dataframe.dropna(inplace=True)

    #Calculate daily returns
    def calculatedailyreturns(self,dataframe):
        return dataframe.pct_change().dropna()

    def removecurrencysign(self,dataframe,colname):
        dataframe[colname]=dataframe[colname].str.replace('$','')

    #Calculates cumulative total based on daily returns
    def calculatecumulativereturns(self,dailyreturns):
        return (1 + dailyreturns).cumprod().dropna()

    def changecolumndatatype(self,dataframe,colname,newdatatype):
        dataframe[colname]=dataframe[colname].astype(newdatatype)

    def renamecolumns(self,dataframe,columnmapper):
        dataframe.rename(columns=columnmapper,inplace=True)

    def calculatestandarddevation(self,dailyreturns,sortascending=True):
        return dailyreturns.std().sort_values(ascending=sortascending)

    def calculateannulizedstandarddevation(self,dailyreturns,workingdays=252,sortascending=True):
        return (dailyreturns * np.sqrt(workingdays)).sort_values(ascending=sortascending)
    
    def calculaterollingstandarddeviation(self,dataframe,daywindow):
        return dataframe.rolling(window=daywindow).std()

    def calculatecorrelation(self,dataframe):
        return dataframe.corr()
    
    def calculatebeta(self,dailyreturns,convarienceportfolio,varianceportfolio,workingdays=0):
        _covariance=0
        _variance=0
        _calculated_beta=0
        if (workingdays==0):
            _covariance=dailyreturns[convarienceportfolio].cov(dailyreturns[varianceportfolio])
            _variance=dailyreturns[varianceportfolio].var()
        else:
            _covariance=dailyreturns[convarienceportfolio].rolling(window=workingdays).cov(dailyreturns[varianceportfolio])
            _variance=dailyreturns[varianceportfolio].rolling(window=workingdays).var()
        _calculated_beta=_covariance/_variance
        return _calculated_beta
    
    def determineriskyportfolio(self,stddata,baseportfolioname):
        return stddata.gt(stddata[baseportfolioname])
    
    def calculateexpotentialweightedaverage(self,dataframe,halflifevalue):
        return dataframe.ewm(halflife=halflifevalue).mean()
    
    def calculatesharpieratio(self,dailyreturns):
        return (dailyreturns.mean() * 252) / (dailyreturns.std() * np.sqrt(252))

    def calculateweightedreturns(self,dailyreturns,weights):
        return dailyreturns.dot(weights)
