#!/usr/bin/python
import random
import os
import time
import requests
import multiprocessing

testCounter =  1
logDir='C:\\Users\\Chase\\Downloads\\gekko-develop (1)\\gekko-develop\\'
outFile='\\results.txt'
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
		self.shortValue = random.randrange(5,15)
		self.longValue = random.randrange(15,40)
		self.signalValue = random.randrange(6,12)
		self.downValue = round(random.uniform(-20,0),3)
		self.upValue = round(random.uniform(0,20),3)
		self.persistenceValue= random.randrange(0,9)


def runBackTest():
	global testCounter
	parameters = Parameters()
	url = 'http://localhost:3000/api/backtest/'
	data = {"watch": {"exchange": "binance", "currency": "USDT", "asset": "BTC"},
			"paperTrader": {"feeMaker": 0.25, "feeTaker": 0.25, "feeUsing": "maker", "slippage": 0.05,
							"simulationBalance": {"asset": 1, "currency": 100}, "reportRoundtrips": "true",
							"enabled": "true"},
			"tradingAdvisor": {"enabled": "true", "method": "MACD", "candleSize": parameters.candleValue,
							   "historySize": parameters.historySize},
			"MACD": {"short": parameters.shortValue, "long": parameters.longValue, "signal": parameters.signalValue,
					 "thresholds": {"down": parameters.downValue, "up": parameters.upValue, "persistence": parameters.persistenceValue}},
			"backtest": {"daterange": {"from": "2019-01-01T23:37:00Z", "to": "2019-03-31T21:37:00Z"}},
			"backtestResultExporter": {"enabled": "true", "writeToDisk": "false",
									   "data": {"stratUpdates": "false", "roundtrips": "true", "stratCandles": "true",
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
			myFile.write(str(parameters.testNo) + "," + r['performanceReport']['startTime'] + "," + r['performanceReport']['endTime'] + "," +
				r['performanceReport']['timespan'] + "," + str(r['performanceReport']['market']) + "," +
				str(r['performanceReport']['balance']) + "," + str(r['performanceReport']['profit']) + "," +
				str(r['performanceReport']['relativeProfit']) + "," +str(r['performanceReport']['yearlyProfit']) + "," +
				str(r['performanceReport']['startPrice']) + "," + str(r['performanceReport']['endPrice']) + "," +
				str(r['performanceReport']['trades']) + "," + str(r['performanceReport']['startBalance']) + "," +
				str(r['performanceReport']['exposure']) + "," + str(r['performanceReport']['sharpe']) + "," +
				str(r['performanceReport']['downside']) + "," + str(r['performanceReport']['ratioRoundTrips']) + "," +
				str(r['performanceReport']['alpha']) + "," + str(r['strategyParameters']['short']) + "," + str(r['strategyParameters']['long']) + "," +
				str(r['strategyParameters']['signal']) + "," + str(r['strategyParameters']['thresholds']['down']) + "," +
				str(r['strategyParameters']['thresholds']['up']) + "," + str(r['strategyParameters']['thresholds']['persistence']) + "," +
				str(r['tradingAdvisor']['candleSize']) + "," +str(r['tradingAdvisor']['historySize']) + str("\n")

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

