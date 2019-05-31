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

for stock in targets:
	if stock[0] not in current_positions:
		print(stock[0] + " not currently in portfolio")
		data = Stock(stock[0])
		try:
			api.submit_order(stock[0], 1, "buy", "market", "gtc")
			print("Bought " + stock[0] + " shares")
		except:
			print("Could not buy a share of ",stock[0])

for stock in api.list_positions():		
		if stock.symbol in target_tickers:
			print("Found " + stock.symbol)
			for target in targets:
				if target[0] == stock.symbol:
					current_percentage = float(stock.market_value)/float(account.portfolio_value)
					if current_percentage < target[1]:
						try:
							buy = (float(target[1]) - current_percentage)*float(account.portfolio_value)/float(stock.current_price)
							if buy > 1:
								api.submit_order(stock.symbol, int(buy), "buy", "market", "gtc")
								print("Bought " + str(buy) + " shares of " + str(stock.symbol) + " at " + stock.current_price)
							else:
								print("Perfectly balanced!")
							print(account.buying_power)
						except:
							print("Could not buy " + stock.symbol)
					if current_percentage > target[1]:
						try:
							sell = (float(target[1]) - current_percentage)*float(account.portfolio_value)/float(stock.current_price)
							api.submit_order(stock.symbol, -int(sell)+1, "sell", "market", "gtc")
							print("Sold " + str(-sell+1) + " shares of " + str(stock.symbol))
						except:
							print("Could not sell " + stock.symbol)
		else:
			try:
				api.submit_order(stock.symbol, stock.qty, "sell", "market", "gtc")
				print("Sold " + stock.symbol)
			except:
				print("Tried selling " + stock.symbol)

print("Balanced. Good luck!")
