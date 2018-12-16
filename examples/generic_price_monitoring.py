from time import sleep
from pyredictit.pyredictit import pyredictit

pyredictit_api = pyredictit()
pyredictit_api.create_authed_session(username='YOUR_USERNAME',
                                     password='YOUR_PASSWORD')
pyredictit_api.get_my_contracts()

my_contract = pyredictit_api.my_contracts[0]
print(my_contract.name)
print(my_contract.type_)
while True:
    pyredictit_api.monitor_price_of_contract(contract=my_contract, monitor_type='generic',
                                             number_of_shares=0, trigger_price=0.00)
    sleep(30)

>>> PENCE.TIEBREAK.033117
>>> Yes
>>> 76¢
>>> 76¢
