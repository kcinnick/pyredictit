from pyredictit.pyredictit import pyredictit

pyredictit_api = pyredictit()
pyredictit_api.create_authed_session(username='YOUR_USERNAME',
                                     password='YOUR_PASSWORD')
pyredictit_api.current_gain_loss()
"""
>>> $0.00
"""
