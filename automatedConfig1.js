var config = {};
config.debug = true;
config.watch = {
exchange: 'binance',
currency: 'USDT',
asset: 'BTC',}
;config.tradingAdvisor = {
enabled: true,
method: 'MACD',
candleSize:120,historySize:21,}
config.MACD = {
short:14
,long: 17
,signal: 6, thresholds: {
 down: -11.883 
,up: 7.715 
,persistence: 5
}
};