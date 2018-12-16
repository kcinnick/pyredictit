from time import sleep
from pyredictit.pyredictit import pyredictit

pyredictit_api = pyredictit()
pyredictit_api.create_authed_session(username='MY_USERNAME',
                                     password='MY_PASSWORD')
pyredictit_api.get_my_contracts()

my_contract = pyredictit_api.my_contracts[0]
my_contract.get_current_volume()
print(my_contract.name)
print(my_contract.type_)
print(my_contract.volume)

>>> PENCE.TIEBREAK.033117
>>> Yes
>>> There have been 595 shares traded today.
