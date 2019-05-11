import alpaca_trade_api as tradeapi
from iexfinance.refdata import get_symbols
import random

# Gets account.txt as a list of lists
account = open('account.txt','r').read().splitlines()
api = tradeapi.REST(account[0].split()[1],account[1].split()[1],account[2].split()[1])

account = api.get_account()
print("$"+account.buying_power+" left in purchasing power.")

while True:
	try:
		api.submit_order(random.choice(get_symbols())["symbol"], 1, "buy", "market", "gtc")
		print("Order submitted.")
	except:
		print("Something went wrong.")

print("Done. Good luck!")
