#!/usr/bin/python
from subprocess import call
import json
import random
import decimal
import os
from shutil import copyfile
import time

#i=1

while 1==1:
	logdir='C:\\Users\\Chase\\Downloads\\gekko-develop (1)\\gekko-develop' # path to your log directory

	logfiles = sorted([ f for f in os.listdir(logdir) if f.startswith('backtest')])
	testNo=time.strftime("%Y%m%d-%H%M%S")
	#i=2


	#generate new MACD parameters
	candleValue=random.choice([5,10,15,30,60,120,240])
	historySize=random.randrange(20,100)
	shortValue = random.randrange(5,15)
	longValue = random.randrange(15,40)
	signalValue = random.randrange(6,12)
	downValue = round(random.uniform(-20,0),3)
	upValue = round(random.uniform(0,20),3)
	persistenceValue= random.randrange(0,9)

	#write new MACD paramters to configuration file
	with open("C:\\Users\\Chase\\Downloads\\gekko-develop (1)\\gekko-develop\\automatedConfig1.js", "w") as myfile:
		myfile.write(
			"var config = {};\n" + 
			"config.debug = true;\n" +
			"config.watch = {\n"+
			"exchange: 'binance',\n" +
			"currency: 'USDT',\n" +
			"asset: 'BTC',}\n" +
			";config.tradingAdvisor = {\n" +
			"enabled: true,\n" +
			"method: 'MACD',\n" +
			"candleSize:"  + str(candleValue) +
			",historySize:" + str(historySize) + ",}\n" +
			"" +
			"config.MACD = {\n" + 
			"short:" + str(shortValue) +
			"\n,long: " + str(longValue) +
			"\n,signal: " + str(signalValue) +
			", thresholds: {\n" +
			" down: " + str(downValue) +
			" \n,up: " + str(upValue) +
			" \n,persistence: " + str(persistenceValue) + "\n}\n};"
			)

	#merge new MACD parameters into configuration file
	filenames = ['C:\\Users\\Chase\\Downloads\\gekko-develop (1)\\gekko-develop\\automatedConfig1.js', 'C:\\Users\\Chase\\Downloads\\gekko-develop (1)\\gekko-develop\\botconfig.js']
	with open('C:\\Users\\Chase\\Downloads\\gekko-develop (1)\\gekko-develop\\botConfig2.js', 'w') as outfile:
	    for fname in filenames:
	        with open(fname) as infile:
	            for line in infile:
	                outfile.write(line)


	#call gekko to test current model and generate new profitibility log
	var = call(["node", "C:\\Users\\Chase\\Downloads\\gekko-develop (1)\\gekko-develop\\gekko.js", "--config", "botconfig2.js","--backtest"]) 


	print (logfiles[-1])
	#open profitibility log results and load to memory for parsing
	file = 'C:\\Users\\Chase\\Downloads\\gekko-develop (1)\\gekko-develop\\' + logfiles[-1]
	with open(file ) as f:
		d = json.load(f)
		

	#write profitibility log results and MACD parameters into log file
	try:
		with open("C:\\Users\\Chase\\Downloads\\gekko-develop (1)\\gekko-develop\\results.txt", "a") as myfile:
		    myfile.write( str(testNo) + "," + d['performanceReport']['startTime'] + "," + d['performanceReport']['endTime'] + "," + 
		    			d['performanceReport']['timespan'] + "," + str(d['performanceReport']['market']) + "," +
		    			str(d['performanceReport']['balance']) + "," +	str(d['performanceReport']['profit']) + "," +
		    			str(d['performanceReport']['relativeProfit']) + "," +	str(d['performanceReport']['yearlyProfit'] )+ "," +
		    			str(d['performanceReport']['startPrice']) + "," +	str(d['performanceReport']['endPrice']) + "," +
		    			str(d['performanceReport']['trades']) + "," +	str(d['performanceReport']['startBalance']) + "," +
		    			str(d['performanceReport']['exposure']) + "," +	str(d['performanceReport']['sharpe']) + "," +
		    			str(d['performanceReport']['downside']) + "," +	str(d['performanceReport']['ratioRoundTrips']) + "," +
		    			str(d['performanceReport']['alpha']) + "," + str(d['strategyParameters']['short']) + "," + str(d['strategyParameters']['long']) + ","  + 
		    			str(d['strategyParameters']['signal']) + ","  + str(d['strategyParameters']['thresholds']['down']) + "," + 
		    			str(d['strategyParameters']['thresholds']['up']) + "," + str(d['strategyParameters']['thresholds']['persistence']) + "," +
		    			str(d['tradingAdvisor']['candleSize']) + "," +str(d['tradingAdvisor']['historySize']) + str("\n") 

		    	)
	except:
		with open("C:\\Users\\Chase\\Downloads\\gekko-develop (1)\\gekko-develop\\results.txt", "a") as myfile:
		    myfile.write(str(testNo) + ", error in output,\n")

