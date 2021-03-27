# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 12:41:35 2020

@author: begon
"""
from scipy import stats
import numpy as np
from scipy.stats import kstest
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from random import seed
from random import random
from math import log
import statistics

#Determines how many prices are >= than a particular price 
def empiricDistribution(prices, price):
    counter = 0
    for p in prices:
        if p <= price:
            counter = counter + 1
    return counter/len(prices)

#Given a list of profits, and a initial amount, calcualtes the resulting amount after executing all profits
def profitCalculator(initialAmount, profits):
    amount = initialAmount
    try:
        for profit in profits:
            amount = amount + amount * (profit/100)
            if amount <= 0:
                print('RUN OUT OF MONEY')
                return None
        print(f'Initial amount was = {initialAmount}')
        print(f'Final amount is = {round(amount, 2)}')
        print(f'Profit = {round((amount-initialAmount)/initialAmount * 100, 2)} %')
        return round((amount-initialAmount)/initialAmount * 100, 2)
    except:
        TypeError
        
def buyAndHold(stock, sYear, sMonth, sDay, eYear, eMonth, eDay):
    df = web.DataReader(stock, 'yahoo', dt.datetime(sYear, sMonth, sDay), dt.datetime(eYear, eMonth, eDay))
    prices = [] 
    for i in range(df['Close'].size):
        prices = prices + [df['Close'][i]]            
    first = round(prices[0], 2)
    last = round(prices[len(prices)-1], 2)  
    print(f'First and last price = {(first, last)}')
    print(f'Buy and hold during the same period = { round((last-first)/first*100, 2)} %')
    return round((last-first)/first*100, 2)

#Strategy used, where:
# -sampleSize is the amount of prices taken to calculate the cumulative probability      
# -stock is the name of the stock whose historic prices are analyzed
# -prob is the probability that the values in the sample are <= than the price being considered
# -sYear, sMonth, sDay, eYear, eMonth, eDay are the starting and ending year, month and day, respectively, where the analysis begins 
def system(sampleSize, stock, prob, sYear, sMonth, sDay, eYear, eMonth, eDay):
    df = web.DataReader(stock, 'yahoo', dt.datetime(sYear, sMonth, sDay), dt.datetime(eYear, eMonth, eDay))
    prices = [] 
    for i in range(df['Close'].size):
        prices = prices + [df['Close'][i]]
    chosenValues = []    
    i = sampleSize-1
    while i < len(prices):
        sample1 = prices[i+1-sampleSize:i+1]
        cumulative = empiricDistribution(sample1, sample1[sampleSize-1])
        if cumulative <= prob:
            for j in range(i+1, len(prices)):
                sample2 = prices[j+1-sampleSize:j+1]
                cumulative = empiricDistribution(sample2, sample2[sampleSize-1])
                if cumulative > 0.6:
                    chosenValues = chosenValues + [(round(sample1[sampleSize-1], 2), round(sample2[sampleSize-1], 2))]
                    i = j + 1
                    break
                if j == len(prices):
                    i = len(prices)
        i = i + 1
    differences = []
    for k in range(len(chosenValues)):
        differences = differences + [chosenValues[k][1] - chosenValues[k][0]]
    positives = [difference for difference in differences if difference > 0]
    profits = [round((chosenValues[k][1] - chosenValues[k][0])/chosenValues[k][0] * 100, 2) for k in range(len(chosenValues))]
    try:
        perCorrectChoices = len(positives)/len(differences) * 100
        print(f'Accuracy = {round(perCorrectChoices, 2)} %')
        print(f'Average profit = {round(statistics.mean(profits), 2)} %')
#        print(f'Chosen values = {chosenValues}')
        print(f'{len(profits)} trades in {len(prices)} days or 1 trade every {round(len(prices)/len(profits), 2)} days')
        return profits
    except:
        ZeroDivisionError
        return [0]
    
def momentumSystem(ema1, ema2, stock, sYear, sMonth, sDay, eYear, eMonth, eDay):
    df = web.DataReader(stock, 'yahoo', dt.datetime(sYear, sMonth, sDay), dt.datetime(eYear, eMonth, eDay))
    
        
# =============================================================================
# TESTS
# =============================================================================

# =============================================================================
# Merval index test
# =============================================================================
def TEST_MERVAL_0():
    sYear = 2019
    sMonth = 6
    sDay = 1
    eYear = 2020
    eMonth = 6
    eDay = 1
    stocks = ["BBAR.BA", "BMA.BA", "BYMA.BA", "CEPU.BA", "COME.BA", "CRES.BA", "CVH.BA", "EDN.BA", "GGAL.BA", "MIRG.BA", "PAMP.BA",
              "SUPV.BA", "TECO2.BA", "TGNO4.BA", "TGSU2.BA", "TRAN.BA", "TXAR.BA", "VALO.BA", "YPFD.BA"
             ]
    averageProfit = []
    averageBuyAndHold = []
    for stock in stocks:
        print(stock)
        profits = system(10, stock, 0.2, sYear, sMonth, sDay, eYear, eMonth, eDay)
        averageProfit = averageProfit + [profitCalculator(50000, profits)]
        averageBuyAndHold = averageBuyAndHold + [buyAndHold(stock, sYear, sMonth, sDay, eYear, eMonth, eDay)]
        meanBuyAndHold = round(statistics.mean(averageBuyAndHold), 2)
        print('\n')
    try:
        print(f'Average profit = {round(statistics.mean(averageProfit), 2)} %')
        print(f'Average profit using buy and hold {meanBuyAndHold} %')
    except:
        TypeError
        
        #print the output to a file by doing "python finance.py > results.txt (or any name)

# =============================================================================
# NASDAQ index test
# =============================================================================
def TEST_NASDAQ_0():
    sYear = 2018
    sMonth = 1
    sDay = 1
    eYear = 2020
    eMonth = 1
    eDay = 1
    stocks = {"AAPL", "MSFT", "AMZN", "FB", "GOOGL", "GOOG", "INTC", "NVDA", "NFLX", "ADBE", "PYPL", "CSCO",
              "PEP", "CMCSA", "AMGN", "COST", "TMUS", "AVGO", "TXN", "CHTR", "QCOM", "GILD", "SBUX", "INTU", "VRTX",
              "MDLZ", "BKNG", "ISRG", "FISV", "REGN", "ADP", "AMD", "ATVI", "JD", "AMAT", "ILMN", "MU", "CSX", "ADSK"
             }
#    stocks = ["TSLA"] no funciona
#    averageProfit = []
    averageBuyAndHold = []
    for stock in stocks:
        print(stock)
#        profits = system(100, stock, 0.05, sYear, sMonth, sDay, eYear, eMonth, eDay)
#        averageProfit = averageProfit + [profitCalculator(50000, profits)]
        averageBuyAndHold = averageBuyAndHold + [buyAndHold(stock, sYear, sMonth, sDay, eYear, eMonth, eDay)]
        meanBuyAndHold = round(statistics.mean(averageBuyAndHold), 2)
        print('\n')
    try:
#        print(f'Average profit = {round(statistics.mean(averageProfit), 2)} %')
        print(f'Average profit using buy and hold {meanBuyAndHold} %')
    except: 
        TypeError
        
        #print the output to a file by doing "python finance.py > results.txt (or any name)

#Choose a test
#TEST_MERVAL_0()
TEST_NASDAQ_0()
