#!/usr/bin/python
import random
import os
import time
import requests
import multiprocessing

testCounter =  1
logDir='C:\\Users\\Chase\\Downloads\\gekko-develop (1)\\gekko-develop\\'
outFile='\\results3.txt'
sleepTimer=2

def removeLogFiles():
	logFiles = sorted([ f for f in os.listdir(logDir) if f.startswith('backtest')])
	for file in logFiles:
		os.remove(logDir+file)
	return



class Parameters(object):
	def __init__(self):
		self.testNo = time.strftime("%Y%m%d-%H%M%S")
		self.candleValue = random.choice([5,10,15,30,60,120,240])
		self.historySize=random.randrange(20,100)
		self.intervalValue = random.randrange(1,10)
		self.lowValue = random.randrange(1,50)
		self.highValue = random.randrange(50,100)
		self.persistenceValue = random.randrange(1,10)



def runBackTest():
	global testCounter
	parameters = Parameters()
	url = 'http://localhost:3000/api/backtest/'

	data = {"watch": {"exchange": "binance", "currency": "USDT", "asset": "BTC"},
			"paperTrader": {"feeMaker": 0.25, "feeTaker": 0.25, "feeUsing": "maker", "slippage": 0.05,
							"simulationBalance": {"asset": 1, "currency": 100}, "reportRoundtrips": "true",
							"enabled": "true"},
			"tradingAdvisor": {"enabled": "true", "method": "StochRSI", "candleSize": parameters.candleValue,
							   "historySize": parameters.historySize}, "StochRSI": {"interval": parameters.intervalValue,
																		  "thresholds": {"low": parameters.lowValue,
																						 "high": parameters.highValue,
																						 "persistence": parameters.persistenceValue}},
			"backtest": {"daterange": {"from": "2019-01-01T23:37:00Z", "to": "2019-03-31T21:37:00Z"}},
			"backtestResultExporter": {"enabled": "true", "writeToDisk": "false",
									   "data": {"stratUpdates": "false", "roundtrips": "true", "stratCandles": "false",
												"stratCandleProps": ["open"], "trades": "true"}},
			"performanceAnalyzer": {"riskFreeReturn": 2, "enabled": "true"}}

	response = requests.post(url, json=data)
	print(str(response) + "             " + "Test Count: " + str(testCounter))
	r = response.json()
	testCounter += 1
	writeLog(r, parameters)
	return

def writeLog(r, parameters):
	try:
		with open( logDir + outFile, "a") as myFile:
			myfile.write(str(testNo) + "," + r['performanceReport']['startTime'] + "," + r['performanceReport'][
				'endTime'] + "," +
						 r['performanceReport']['timespan'] + "," + str(r['performanceReport']['market']) + "," +
						 str(r['performanceReport']['balance']) + "," + str(r['performanceReport']['profit']) + "," +
						 str(r['performanceReport']['relativeProfit']) + "," + str(
				r['performanceReport']['yearlyProfit']) + "," +
						 str(r['performanceReport']['startPrice']) + "," + str(
				r['performanceReport']['endPrice']) + "," +
						 str(r['performanceReport']['trades']) + "," + str(
				r['performanceReport']['startBalance']) + "," +
						 str(r['performanceReport']['exposure']) + "," + str(r['performanceReport']['sharpe']) + "," +
						 str(r['performanceReport']['downside']) + "," + str(
				r['performanceReport']['ratioRoundTrips']) + "," +
						 str(r['performanceReport']['alpha']) + "," + str(r['strategyParameters']['interval']) + "," +
						 str(r['strategyParameters']['thresholds']['low']) + "," + str(
				r['strategyParameters']['thresholds']['high']) + "," +
						 str(r['strategyParameters']['thresholds']['persistence']) + "," +
						 str(r['tradingAdvisor']['candleSize']) + "," + str(r['tradingAdvisor']['historySize']) + str(
				"\n")

						  )
	except:
		with open( logDir + outFile, "a") as myFile:
			myFile.write(str(parameters.testNo) + ", error in output,\n")
	return


#runBackTest()


if __name__ == '__main__':
	jobs = []
	while 1==1:
		time.sleep(sleepTimer)
		p = multiprocessing.Process(target=runBackTest)
		jobs.append(p)
		p.start()














































#!/usr/bin/python
from subprocess import call
import json
import random
import decimal
import os
from shutil import copyfile
import time
import requests
import json

testCounter=0

while 1==1:
	logdir='C:\\Users\\Chase\\Downloads\\gekko-develop (1)\\gekko-develop' 

	
	testNo=time.strftime("%Y%m%d-%H%M%S")
	
	candleValue=random.choice([5,10,15,30,60,120,240])
	historyValue=random.randrange(20,100)
	intervalValue = random.randrange(1,10)
	highValue = random.randrange(50,100)
	lowValue = random.randrange(1,50)
	persistenceValue = random.randrange(1,10)


	#perform API call on Gekko node to backtest strategy and generate profitibility stats
	url = 'http://localhost:3000/api/backtest/'
	data = { "watch": { "exchange": "binance", "currency": "USDT", "asset": "BTC" }, "paperTrader": { "feeMaker": 0.25, "feeTaker": 0.25, "feeUsing": "maker", "slippage": 0.05, "simulationBalance": { "asset": 1, "currency": 100 }, "reportRoundtrips": "true", "enabled": "true" }, "tradingAdvisor": { "enabled": "true","method": "tulip-multi-strat","candleSize": 1,"historySize": 10},"tulip-multi-strat": {"optInTimePeriod": 2,"optInFastPeriod": 4,"optInSlowPeriod": 7,"optInSignalPeriod": 23,"candleSize": 1,"historySize": 4,"up": 24,"down": 55,"macd_up": 14,"macd_down": -9},"backtest": {"daterange": {"from": "2019-01-01T23:37:00Z","to": "2019-03-31T21:37:00Z"}},"backtestResultExporter": {"enabled": "true","writeToDisk": "false","data": {"stratUpdates": "false","roundtrips": "true","stratCandles": "false","stratCandleProps": ["open"],"trades": "true"}},"performanceAnalyzer": {"riskFreeReturn": 2,"enabled": "true"}}
	response = requests.post(url, json=data)
	print(str(response) + "             " + "Test Count: " + str(testCounter))
	r = response.json()
	testCounter+=1


	#write profitibility log results and MACD parameters into log file
	try:
		with open( logdir + "\\results_stochrsi.txt", "a") as myfile:
		    myfile.write( str(testNo) + "," + r['performanceReport']['startTime'] + "," + r['performanceReport']['endTime'] + "," + 
		    			r['performanceReport']['timespan'] + "," + str(r['performanceReport']['market']) + "," +
		    			str(r['performanceReport']['balance']) + "," +	str(r['performanceReport']['profit']) + "," +
		    			str(r['performanceReport']['relativeProfit']) + "," +	str(r['performanceReport']['yearlyProfit'] )+ "," +
		    			str(r['performanceReport']['startPrice']) + "," +	str(r['performanceReport']['endPrice']) + "," +
		    			str(r['performanceReport']['trades']) + "," +	str(r['performanceReport']['startBalance']) + "," +
		    			str(r['performanceReport']['exposure']) + "," +	str(r['performanceReport']['sharpe']) + "," +
		    			str(r['performanceReport']['downside']) + "," +	str(r['performanceReport']['ratioRoundTrips']) + "," +
		    			str(r['performanceReport']['alpha']) + "," + str(r['strategyParameters']['interval']) + "," + 
		    			str(r['strategyParameters']['thresholds']['low']) + "," + str(r['strategyParameters']['thresholds']['high'])  + "," +
		    			str(r['strategyParameters']['thresholds']['persistence'])  + "," +
		    			str(r['tradingAdvisor']['candleSize']) + "," +str(r['tradingAdvisor']['historySize']) + str("\n") 

		    	)
	except:
		with open( logdir + "\\results2.txt", "a") as myfile:
		    myfile.write(str(testNo) + ", error in output,\n")

