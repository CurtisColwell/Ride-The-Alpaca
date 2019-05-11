import alpaca_trade_api as tradeapi
from iexfinance.stocks import Stock
import csv

# Gets account.txt as a list of lists
account = open('account.txt','r').read().splitlines()
api = tradeapi.REST(account[0].split()[1],account[1].split()[1],account[2].split()[1])

account = api.get_account()
print("$"+account.buying_power+" left in cash.")

with open('portfolio_targets.csv', 'r') as csvfile:
	target_file = csv.reader(csvfile, delimiter=',')
	targets = []
	target_tickers = []
	for stock in target_file:
		targets.append([stock[0],float(stock[1])])
		target_tickers.append(stock[0])

	current_positions = []

	for line in targets:
		print("Targeting " + str(line[1]) + " " + line[0])

	for stock in api.list_positions():
		current_positions.append(stock.symbol)

	for stock in api.list_positions():		
		try:
			if stock.symbol in target_tickers:
				print("Found " + stock.symbol)
				for target in targets:
					if target[0] == stock.symbol:
						current_percentage = float(stock.market_value)/float(account.portfolio_value)
						if current_percentage < target[1]:
							buy = (float(target[1]) - current_percentage)*float(account.portfolio_value)/float(stock.current_price)*.9
							api.submit_order(stock.symbol, int(buy), "buy", "market", "gtc")
							print("Bought " + str(buy) + " shares of " + str(stock.symbol) + " at " + stock.current_price)
							print(account.buying_power)
						if current_percentage > target[1]:
							sell = (float(target[1]) - current_percentage)*float(account.portfolio_value)/float(stock.current_price)*.9
							api.submit_order(stock.symbol, -int(sell), "sell", "market", "gtc")
							print("Sold " + str(sell) + " shares of " + str(stock.symbol))
			else:
				api.submit_order(stock.symbol, stock.qty, "sell", "market", "gtc")
				print("Sold " + stock.symbol)
		except:
			print("Problem with " + stock.symbol)

for stock in targets:
	if stock[0] not in current_positions:
		print(stock[0] + " not currently in portfolio")
		data = Stock(stock[0])
		api.submit_order(stock[0], 1, "buy", "market", "gtc")
		print("Bought " + stock[0] + " shares")
print("Balanced. Good luck!")
