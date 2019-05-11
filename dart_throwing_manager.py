import alpaca_trade_api as tradeapi
from iexfinance.refdata import get_symbols
import random

api = tradeapi.REST('AKQ44XUEJY1T01Q9I0DJ','D3cEq/UUv3F8vTqZ92mFUItBufvjzjapFzvSO0Ud','https://paper-api.alpaca.markets')
account = api.get_account()
print("$"+account.buying_power+" left in purchasing power.")

while True:
	try:
		api.submit_order(random.choice(get_symbols())["symbol"], 1, "buy", "market", "gtc")
		print("Order submitted.")
	except:
		print("Something went wrong.")

print("Done. Good luck!")
