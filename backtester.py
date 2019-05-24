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

	logfiles = sorted([ f for f in os.listdir(logdir) if f.startswith('backtest')])
	testNo=time.strftime("%Y%m%d-%H%M%S")
	
	candleValue=random.choice([5,10,15,30,60,120,240])
	historySize=random.randrange(20,100)
	shortValue = random.randrange(5,15)
	longValue = random.randrange(15,40)
	signalValue = random.randrange(6,12)
	downValue = round(random.uniform(-20,0),3)
	upValue = round(random.uniform(0,20),3)
	persistenceValue= random.randrange(0,9)

	#perform API call on Gekko node to backtest strategy and generate profitibility stats
	url = 'http://localhost:3000/api/backtest/'
	data = { "watch": { "exchange": "binance", "currency": "USDT", "asset": "BTC" }, "paperTrader": { "feeMaker": 0.25, "feeTaker": 0.25, "feeUsing": "maker", "slippage": 0.05, "simulationBalance": { "asset": 1, "currency": 100 }, "reportRoundtrips": "true", "enabled": "true" }, "tradingAdvisor": { "enabled": "true","method": "MACD","candleSize": candleValue,"historySize": historySize},"MACD": {"short": shortValue,"long": longValue,"signal": signalValue,"thresholds": {"down": downValue,"up": upValue,"persistence": persistenceValue}},"backtest": {"daterange": {"from": "2019-01-01T23:37:00Z","to": "2019-03-31T21:37:00Z"}},"backtestResultExporter": {"enabled": "true","writeToDisk": "false","data": {"stratUpdates": "false","roundtrips": "true","stratCandles": "true","stratCandleProps": ["open"],"trades": "true"}},"performanceAnalyzer": {"riskFreeReturn": 2,"enabled": "true"}}
	response = requests.post(url, json=data)
	print(str(response) + "             " + "Test Count: " + str(testCounter))
	r = response.json()
	testCounter+=1


	#write profitibility log results and MACD parameters into log file
	try:
		with open( logdir + "\\results.txt", "a") as myfile:
		    myfile.write( str(testNo) + "," + r['performanceReport']['startTime'] + "," + r['performanceReport']['endTime'] + "," + 
		    			r['performanceReport']['timespan'] + "," + str(r['performanceReport']['market']) + "," +
		    			str(r['performanceReport']['balance']) + "," +	str(r['performanceReport']['profit']) + "," +
		    			str(r['performanceReport']['relativeProfit']) + "," +	str(r['performanceReport']['yearlyProfit'] )+ "," +
		    			str(r['performanceReport']['startPrice']) + "," +	str(r['performanceReport']['endPrice']) + "," +
		    			str(r['performanceReport']['trades']) + "," +	str(r['performanceReport']['startBalance']) + "," +
		    			str(r['performanceReport']['exposure']) + "," +	str(r['performanceReport']['sharpe']) + "," +
		    			str(r['performanceReport']['downside']) + "," +	str(r['performanceReport']['ratioRoundTrips']) + "," +
		    			str(r['performanceReport']['alpha']) + "," + str(r['strategyParameters']['short']) + "," + str(r['strategyParameters']['long']) + ","  + 
		    			str(r['strategyParameters']['signal']) + ","  + str(r['strategyParameters']['thresholds']['down']) + "," + 
		    			str(r['strategyParameters']['thresholds']['up']) + "," + str(r['strategyParameters']['thresholds']['persistence']) + "," +
		    			str(r['tradingAdvisor']['candleSize']) + "," +str(r['tradingAdvisor']['historySize']) + str("\n") 

		    	)
	except:
		with open( logdir + "\\results.txt", "a") as myfile:
		    myfile.write(str(testNo) + ", error in output,\n")

