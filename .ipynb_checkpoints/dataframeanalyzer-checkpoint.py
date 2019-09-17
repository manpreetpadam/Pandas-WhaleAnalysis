from pathlib import Path
import pandas as pd
import numpy as numpy
import datetime as dt

class dataframeanalayzer:
    
    def __init__(self):
        self.dataframe=pd.DataFrame()
        

    def loadcvstodataframe(self, sourcepath):
        csvfile=Path(sourcepath)
        
        #create data frame from csv file
        _df=pd.read_csv(csvfile,index_col='Date',infer_datetime_format=True,parse_dates=True)
        return _df

    def combinedataframes(self,dataframes):
        combined_df=pd.concat(dataframes,axis='columns',join='inner')
        return combined_df
    
    def nullcount(self):
        return self.dataframe.isnull().sum()

    def dropnulls(self):
        self.dataframe.dropna(inplace=True)

    #Calculate daily returns
    def calculatedailyreturns(self):
        return self.dataframe.pct_change()

    def removecurrencysign(self,colname):
        self.dataframe[colname]=self.dataframe[colname].str.replace('$','')

    #Calculates cumulative total based on daily returns
    def calculatecumulativereturns(self,dailyreturns):
        return dailyreturns.cumprod()




