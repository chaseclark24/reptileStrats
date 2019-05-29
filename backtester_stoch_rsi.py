#!/usr/bin/python
import random
import os
import time
import requests
import multiprocessing


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
	print(str(response))
	r = response.json()
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




if __name__ == '__main__':
	testCounter = 1
	jobs = []
	while 1==1:
		print("Test Count: " + str(testCounter))
		time.sleep(sleepTimer)
		testCounter += 1
		p = multiprocessing.Process(target=runBackTest)
		jobs.append(p)
		p.start()
















