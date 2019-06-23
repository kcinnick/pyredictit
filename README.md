# pyredictit

**MY DEVELOPMENT ON THIS LIBRARY IS CURRENTLY CLOSED** 

This repo gets a healthy amount of traffic but unfortunately PredictIt disabled my account because I refused to remove this repository.  Update as of 4/16/19: my attempt to find a way around PredictIt disabling my account didn't work, and I don't really desire to spend a lot more effort on trying to find new ways in to PredictIt, but a couple of people have forked this repo and I figure it may be interesting/a nice starting point for some other intrepid developers so I'm going to leave it public.

pyredictit is a wrapper for the public PredictIt API (https://predictit.freshdesk.com/support/solutions/articles/12000001878-does-predictit-make-market-data-available-via-an-api-).  Running this module requires mechanicalsoup and <b>Python 3.6</b>.  Check out the Examples directory for some ideas on how to use this!

**this can buy or sell shares using the money currently in your account. i am not responsible for any awful (or brilliant) trades you may accidentally or purposefully make with this wrapper. don't risk more than you can afford to lose. **

Things you can do with this currently are:
- Buy or sell shares of contracts that you already own.
- Check your current balance
- Find out how much you'd make if you sold all of your shares in a market
- Find out what you would make (or lose) depending on how the contract resolves
- Summarize all of your current contracts.
- Look up & purchase shares of contracts you don't currently own
- Check latest volume of any contract.

COMING SOON:
* Adding a method where, given a gmail address and a phone number, receive text alerts on any triggers you want to set up!

HOW YOU CAN HELP:

report all exceptions!  Liberally open issues and let me know what's not working or what looks wonky! Include as much info as possible and please check to make sure that you are using valid login info and whatnot if you're copying over from the examples.  Also, *any* feedback is useful! 

UPDATE 1/26/2017 - the number 1 question I've been getting about this is "will it steal my login and password," and the answer is *of course not*, <b>but don't take my word for it!</b> Lines 226-235 are the parts where authentication is handled specifically, and I suspect that even people who don't fully understand Python's syntax will be able to see and verify for themselves that this information isn't transmitted anywhere beyond PI's server.

INSTALLATION:

1. Go to https://www.python.org/downloads/

2. Click "Download Python 3.6.0"

3. Install it and check "Add Python to PATH"  box in setup options.

4. Open up Powershell/Terminal and type: python -m pip install mechanicalsoup

5. Clone this repo

6. CD into the directory where you cloned the repo and type:
`python setup.py install`

7. Use it like a Python module!

TODO:
* C O M M E N T S
* UNIT TESTS
* DOC TESTS
* Custom Exception classes
* Adding to pip
* <s>stop loss and buy-at functionality - this is a priority!</s>
* <s>setup.py script</s>
* <s>Look up & purchase shares of contracts you don't currently own</s>
