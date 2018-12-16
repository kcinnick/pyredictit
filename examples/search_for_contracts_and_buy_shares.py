from pyredictit.pyredictit import pyredictit

pyredictit_api = pyredictit()
pyredictit_api.create_authed_session(username='YOUR_USERNAME',
                                     password='YOUR_PASSWORD')
long_sell_contracts = pyredictit_api.search_for_contracts(market='politics', buy_sell='buy', type_='long')
first_contract = long_sell_contracts[0]
print(first_contract.market)
print(first_contract.type_)
first_contract.buy_shares(number_of_shares=1, api=pyredictit_api, buy_price=first_contract.buy)

"""
>>> Will a federal minimum wage increase go into effect by year-end 2017?
>>> long
>>> You do not have sufficient funds to make this offer!
"""
