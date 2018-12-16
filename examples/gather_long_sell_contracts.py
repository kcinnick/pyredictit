from pyredictit.pyredictit import pyredictit

pyredictit_api = pyredictit()
pyredictit_api.create_authed_session(username='YOUR_USERNAME',
                                     password='YOUR_PASSWORD')
long_sell_contracts = pyredictit_api.search_for_contracts(market='politics', buy_sell='sell', type_='long')
for contract in long_sell_contracts:
    print('------')
    print(contract.market)
    print(contract.name)

"""
>>> ------
>>> Will a federal minimum wage increase go into effect by year-end 2017?
>>> Long
>>> ------
>>> Will the individual tax rate be cut by the end of 2017?
>>> Long
>>> ------
>>> Will the corporate tax rate be cut by the end of 2017?
>>> Long
>>> ------
>>> Will the Senate invoke the nuclear option for SCOTUS nominees by end of 2017?
>>> Long
>>> ------
>>> Will the ACA individual mandate be repealed by the end of 2017?
>>> Long
>>> ------
>>> Will the ACA employer mandate be repealed by the end of 2017?
>>> Long
>>> .....
"""
