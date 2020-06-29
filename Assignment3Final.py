#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os
import datetime

print(os.getcwd())
bankingDF = pd.DataFrame()
bankingDFBkup = pd.DataFrame()

fileName = 'bse-graded-assignment-banking-dataset_upd.xlsx'

def loadFile(fileName): 
    print('Reading file: ', fileName)

    startTime = datetime.datetime.now()
    print('Start Reading xls file', startTime)
    bankingDF = pd.read_excel(fileName)
    endTime = datetime.datetime.now()
    print('End Reading xls file ', endTime, '\n')
      
    readDuration = endTime - startTime
    print('Overall Duration took to load file (in Seconds)', readDuration.total_seconds(), '\n')
    
    print('----------------------------------------\n')
    print("Total Number of Rows {0}:", format(len(bankingDF)), '\n')
    print("First 5 records in Banking Dataframe: ", bankingDF.head(), '\n')
    print("Banking Dataframe Describe details: ", bankingDF.describe(), '\n')
    print("Banking Dataframe Columns: ", bankingDF.columns, '\n')
    return bankingDF


def basicCheckBankDF(bankingDF):
     bankingNullDF = bankingDF[bankingDF.isnull().any(1)]
     bankingNegativeDF = bankingDF.loc[bankingDF['LoansRejected'] == -2]
     bankingDup = bankingDF[bankingDF.duplicated(['Year', 'DayOffset', 'BranchID'])]
     bankingYr5Dg = bankingDF[bankingDF['Year'].apply(lambda x: len(str(x))> 4)]
     bankingDayOffset = bankingDF[bankingDF['DayOffset'].apply(lambda x: x > 365)]
     dfList = []
     dfList.append(bankingNullDF)
     dfList.append(bankingNegativeDF)
     dfList.append(bankingDup)
     dfList.append(bankingYr5Dg)
     dfList.append(bankingDayOffset)
     writer = pd.ExcelWriter('CleansingFile.xlsx')
     for n, df in enumerate(dfList):
        df.to_excel(writer, 'sheet%s' % str(n + 1))
     writer.save()
     return bankingDF


def cleansingData(bankingDF):
    bankingDFNo = bankingDF.dropna()
    bankingDFNoUpd = bankingDFNo.mask(bankingDFNo < 0, 0)
    bankingDFNoUpd.lt(0).sum().sum()
    bankingDFNoUpd.lt(0).sum()
    bankingDF = bankingDFNoUpd.drop_duplicates(subset=['Year', 'DayOffset', 'BranchID'], keep='first')
    return bankingDF

#--------------------------------------------------------------------------
    
def populateDate(bankingDF):    
    list =[]
    initiaDate = '01/01/'
    
    for row in bankingDF.itertuples(index = True, name ='Pandas'): 
        print(row)
        myString = initiaDate+str(getattr(row, "Year"))[0:4]
        dayOffset = getattr(row, "DayOffset")
        updateDate = pd.to_datetime(myString) + pd.DateOffset(days=dayOffset)
        updateDateExp = updateDate.strftime('%d/%m/%Y')
        list.append(updateDateExp)
    
    bankingDF.insert(0, "FinaleDate", list)    
    bankingDF.info()
    return bankingDF
#--------------------------------------------------------------------------

listLeap = []
def checkLeap(year):
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                listLeap.append('LeapYr')
            else:
                listLeap.append('NotLeapYr')
        else:
            listLeap.append('LeapYr')
    else:
        listLeap.append('NotLeapYr')
    return listLeap

def populateLeapYear(bankingDF):
    for row in bankingDF.itertuples(index = True, name ='Pandas'): 
        yearVal = str(getattr(row, "Year"))[0:4]
        listLeap = checkLeap(int(yearVal))
        print(len(listLeap))
        bankingDF.insert(0,'LeapYrCheck', listLeap)
    return bankingDF
#--------------------------------------------------------------------------
def overallTxn(bankingDF):
    dfTotalval = []
    for row in bankingDF.itertuples(index = True, name ='Pandas'): 
        value = getattr(row, "NewAccounts") + getattr(row, "ClosedAccounts") + getattr(row, "LoansApplied") +getattr(row, "LoansRejected") + getattr(row, "LoansApproved") +getattr(row, "NumberOfDDs") + getattr(row, "NumberOfCheques") +getattr(row, "NumberOfCashDep") +getattr(row, "NumberOfWithdrawal")   
        dfTotalval.append(value)
        bankingDF["TotalTxn"] = pd.DataFrame(dfTotalval)
    return bankingDF

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
bankingDF.columns
print(bankingDF.info())
listDayOffset = []
def updateLeapYearDayOffset(bankingDF):
    for iterator in bankingDF.itertuples(index = True, name ='Pandas'): 
        leapYear = getattr(iterator, "LeapYrCheck")
        dayOffset = getattr(iterator, "DayOffset")
        if leapYear == "LeapYr" and dayOffset > 366:
           print(leapYear, "...", dayOffset)
           print("LeapYear dayoffset is gr 366")
    return bankingDF
#--------------------------------------------------------------------------
    
def exportFinalDF(bankingDFinal):
    bankingDFinal.to_excel('AssignmentFinal.xlsx', sheet_name='Txn')
    bankingDF.to_excel('AssignmentFinal.xlsx', sheet_name='Txn')
    return None

#--------------------------------------------------------------------------

bankingDF = loadFile(fileName)
bankingDF = basicCheckBankDF(bankingDF)
bankingDF = cleansingData(bankingDF)
bankingDF = populateDate(bankingDF)
bankingDF = populateLeapYear(bankingDF)
#bankingDF = updateLeapYearDayOffset(bankingDF)
#bankingDF = overallTxn(bankingDF)
overallTxn(bankingDF)
exportFinalDF(bankingDF)

#bankingDFBkup = bankingDF
#bankingDF = bankingDFBkup
