import alpaca_trade_api as tradeapi

api = tradeapi.REST('PKATNIRLZT4O89WBWI3I','K9jBfTQlauku70dfsOqWryZcLcx9RWXDqsdRth3m','https://paper-api.alpaca.markets')
account = api.get_account()
print("$"+account.buying_power+" left in cash.")

for order in api.list_orders():
	api.cancel_order(order.id)
