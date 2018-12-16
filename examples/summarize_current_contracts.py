from pyredictit.pyredictit import pyredictit

pyredictit_api = pyredictit()
pyredictit_api.create_authed_session(username='YOUR_USERNAME',
                                     password='YOUR_PASSWORD')
pyredictit_api.list_my_contracts()

"""
>>> ------
>>> 2017-01-25 19:15:24.276645
>>> Will Raymond Kethledge be the next confirmed Supreme Court justice?
>>> KETHLEDGE.SCOTUS.NEXTJUSTICE
>>> You have 1 Yes share.
>>> Your shares have lost -$0.05 in value.
>>> Your average purchase price of Yes shares is 10¢
>>> Yes shares are currently being sold at 8¢
>>> Yes shares are currently being bought for 5¢
>>> If you sold all of your shares now, you would lose $0.05
>>> The implied odds of this contract resolving to Yes are 8%
>>> If this contract resolves to Yes, you would earn $1.01. Otherwise, you would lose $-0.11}
------
"""
