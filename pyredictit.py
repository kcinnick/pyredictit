import ast
import datetime
from time import sleep
from urllib.request import urlopen
import mechanicalsoup
import re


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def floatify(string):
    """
    Converts a string representing cents into an orderable float.
    :param string: str
    :return:
    """
    temporary_string = f"0.{string[:-1]}"
    return float(temporary_string)


class Contract:
    """
    Contains data and methods for an individual contract. For any contract, you can check the latest
    pricing and volume data. Additionally, with a logged in API session, you can check your own
    gains, losses, potential gains/losses depending on resolution, and more!
    """

    def __init__(self, market, cid, name, type_, shares, avg_price, buy_offers,
                 sell_offers, gain_loss, latest, buy, sell, ticker):
        self.timestamp = datetime.datetime.now()
        self.market = market
        self.cid = cid
        self.name = name
        if self.market == self.name:
            self.name = type_.title()
        self.type_ = type_
        self.number_of_shares = int(shares)
        self.avg_price = avg_price
        self.buy_offers = buy_offers
        self.sell_offers = sell_offers
        self.gain_loss = gain_loss
        if '(' in self.gain_loss:
            self.gain_loss = gain_loss.replace('(', '-').replace(')', '')
        self.latest = latest
        self.buy = buy
        self.sell = sell
        self.ticker = ticker
        self.latest_volume = None

    @property
    def shares(self):
        if self.number_of_shares == 1:
            return f"You have {self.number_of_shares} {self.type_} share."
        else:
            return f"You have {self.number_of_shares} {self.type_} shares."

    @property
    def average_price(self):
        return f"Your average purchase price of {self.type_} shares is {self.avg_price}"

    @property
    def gain_or_loss(self):
        if '+' in self.gain_loss:
            return f"Your shares have gained {self.gain_loss} in value."
        else:
            return f"Your shares have lost {self.gain_loss} in value."

    @property
    def sell_price(self):
        return f"{self.type_} shares are currently being bought for {self.sell}"

    @property
    def buy_price(self):
        return f"{self.type_} shares are currently being sold at {self.buy}"

    @property
    def estimate_sale_of_current_shares(self):
        try:
            if float(self.sell[:-1]) - float(self.avg_price[:-1]) > 0:
                return f"If you sold all of your shares now, you would earn ${str(float(float(self.sell[:-1]) - float(self.avg_price[:-1])) * self.number_of_shares * 0.01)}"
            else:
                return f"If you sold all of your shares now, you would lose ${str(float(float(self.sell[:-1]) - float(self.avg_price[:-1])) * self.number_of_shares * 0.01 + (float(self.number_of_shares) * float(self.avg_price[:-1])) * 0.01)}"
        except ValueError as e:
            return e

    @property
    def estimate_best_result(self):
        return f"If this contract resolves to {self.type_}, you would earn ${1 - (float(self.avg_price[:1])) * self.number_of_shares * 0.01 * -1}. Otherwise, you would lose ${float(self.avg_price[:1]) * self.number_of_shares * 0.01 * -1 - (float(self.number_of_shares) * float(self.avg_price[:-1])) * 0.01}}}"

    @property
    def implied_odds(self):
        """Implied odds of a contract are what a given resolution
         in a market is being bought for currently."""
        return f"The implied odds of this contract resolving to {self.type_} are {self.buy.replace('¢', '%')}"

    @property
    def volume(self):
        return f"There have been {self.latest_volume} shares traded today."

    def summary(self):
        print('----')
        print(self.timestamp)
        print(self.market)
        print(self.name)
        print(self.shares)
        print(self.gain_or_loss)
        print(self.average_price)
        print(self.buy_price)
        print(self.sell_price)
        print(self.estimate_sale_of_current_shares)
        print(self.implied_odds)
        print(self.estimate_best_result)
        print('-----')

    def get_current_volume(self):
        """
        Sets or updates volume. Volume data is only updated hourly, so use accordingly.
        """
        latest_data = ast.literal_eval(
            urlopen(
                f'https://www.predictit.org/PublicData/GetChartData?contractIds={self.cid}&timespan=24H').read().decode(
                'utf-8').replace(
                'false', 'False').replace('true', 'True').replace('null', 'None'))[-1]
        self.latest_volume = latest_data['TradeVolume']
        return

    def buy_shares(self, api, number_of_shares, buy_price):
        if self.type_.lower() == 'no' or 'short':
            type_, id_ = 'Short', '0'
        elif self.type_.lower() == 'yes' or 'long':
            type_, id_ = 'Long', '1'
        load_side_page = api.browser.get(f'https://www.predictit.org/Trade/LoadBuy{type_}?contractId={self.cid}')
        token = load_side_page.soup.find(
            'input', attrs={'name': '__RequestVerificationToken'}).get('value')
        r = api.browser.post('https://www.predictit.org/Trade/SubmitTrade',
                             {'__RequestVerificationToken': token,
                              'BuySellViewModel.ContractId': self.cid,
                              'BuySellViewModel.TradeType': id_,
                              'BuySellViewModel.Quantity': number_of_shares,
                              'BuySellViewModel.PricePerShare': f'{float(buy_price)}',
                              'X-Requested-With': 'XMLHttpRequest'})
        if str(r.status_code) == '200':
            if 'Confirmation Pending' in str(r.content):
                print('Purchase offer successful!')
            elif 'You do not have sufficient funds to make this offer' in str(r.content):
                print('You do not have sufficient funds to make this offer!')
            elif 'There was a problem creating your offer' in str(r.content):
                print(f"DEBUGGING INFO - INCLUDE IN GITHUB ISSUE: {r.content}")
                print('There was a problem creating the offer. Check to make sure that you don\'t have any \'yes\' contracts that would prevent you from buying \'no\'s or vice versa.')
            else:
                print(f"DEBUGGING INFO - INCLUDE IN GITHUB ISSUE: {r.content}")
        else:
            print(f"Request returned an invalid {r.status_code} code. Please make sure you're using valid login credentials.")

    def sell_shares(self, api, number_of_shares, sell_price):
        if self.type_.lower() == 'no':
            type_, id_ = 'Short', '2'
        elif self.type_.lower() == 'yes':
            type_, id_ = 'Long', '3'
        print((
            f'https://www.predictit.org/Trade/LoadSel\
            l{type_}?contractId={self.cid}'))
        load_side_page = api.browser.get(
            f'https://www.predictit.org/Trade/\
            LoadSell{type_}?contractId={self.cid}')
        token = load_side_page.soup.find(
            'input', attrs={'name': '__RequestVerificationToken'}).get('value')
        r = api.browser.post('https://www.predictit.org/Trade/SubmitTrade',
                             {'__RequestVerificationToken': token,
                              'BuySellViewModel.ContractId': self.cid,
                              'BuySellViewModel.TradeType': id_,
                              'BuySellViewModel.Quantity': number_of_shares,
                              'BuySellViewModel.PricePerShare':
                              f'{float(sell_price)}',
                              'X-Requested-With': 'XMLHttpRequest'})
        if str(r.status_code) == '200':
            if 'Confirmation Pending' in str(r.content):
                print('Sell offer successful!')
            elif 'There was a problem creating your offer':
                print(f"DEBUGGING INFO - INCLUDE IN GITHUB ISSUE: {r.content}")
                print('There was a problem creating the offer. Check to make \
                    sure that you don\'t have any \'yes\' contracts that\
                     would prevent you from buying \'no\'s or vice versa.')
            else:
                print(f"DEBUGGING INFO - INCLUDE IN GITHUB ISSUE: {r.content}")
                print(r.content)
        else:
            print(f"Request returned an invalid {r.status_code} code. \
                    Please make sure you're using valid login credentials.")

    def update(self):
        r = ast.literal_eval(
            urlopen(
                f'https://www.predictit.org/api/marketdata/ticker/\
                {self.ticker}').read().decode(
                'utf-8').replace('false', 'False').replace(
                'true', 'True').replace(
                'null', 'None'))
        for contract in r['Contracts']:
            if contract['TickerSymbol'] == self.ticker:
                if self.type_.lower() in ['yes', 'long']:
                    self.buy = contract['BestBuyYesCost']
                elif self.type_.lower() in ['no', 'short']:
                    self.buy = contract['BestBuyNoCost']
                elif self.type_.lower() in ['yes', 'long']:
                    self.sell = contract['BestSellYesCost']
                elif self.type_.lower() in ['no', 'short']:
                    self.sell = contract['BestSellNoCost']

    def __str__(self):
        return f"{self.market}, {self.name}, {self.type_}, {self.shares}, \
                 {self.average_price}, {self.buy_offers},{self.sell_offers}, \
                 {self.gain_loss}, {self.latest}, {self.buy}, {self.sell}"


class pyredictit:
    """
    This class provides access to the API and the methods below.
    You have to create an authed session with a valid email and password
    to use account-specific methods (buying, selling, etc.),
    but not to look up current share data.
    """

    def __init__(self):
        self.my_contracts = None
        self.gain_loss = None
        self.available = None
        self.invested = None
        self.browser = mechanicalsoup.Browser()
        self.browser.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36\
             (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'}
        )

    def __validate_login(self, response):
        assert 'access_token' in str(response.content), "Invalid login."

    def update_balances(self):
        user_funds = self.browser.get(
            'https://www.predictit.org/api/Account/Status').json()
        print(user_funds)
        self.available = user_funds['accountBalance']
        #self.gain_loss = user_funds['SharesText']
        #self.invested = user_funds['PortfolioText']

    def money_available(self):
        self.update_balances()
        print(f"You have {self.available} available.")

    def current_gain_loss(self):
        self.update_balances()
        if '-' in self.gain_loss:
            print(f"You've lost {self.gain_loss[1:]}.")
        else:
            print(f"You've gained {self.gain_loss[1:]}.")

    def money_invested(self):
        self.update_balances()
        print(f"You have {self.invested} currently invested in contracts.")

    def create_authed_session(self, username, password):
        """
        Authenticates a given user.
        :type username: str
        :type password: str
        """
        login_page = self.browser.get('https://www.predictit.org/')
        r = self.browser.post('https://www.predictit.org/api/Account/token',
                              {'email': username,
                               'password': password,
                               'grant_type': 'password',
                               'rememberMe': 'false'})
        self.__validate_login(r)
        return self.browser

    def get_my_contracts(self):
        """
        Initially retrieves info for currently authed user's contracts.
        """
        self.my_contracts = []
        my_shares = self.browser.get(
            'https://www.predictit.org/Profile/GetSharesAjax')
        for market in my_shares.soup.find_all('table', class_='table table-striped table-center'):
            market_title = market.previous_element.previous_element.find('div', class_='outcome-title').find('a').get(
                'title')
            market_data = [i.text.strip().replace(
                "\n", "").replace("    ", "").replace('\r', '') for i in market.find_all('td')]
            market_data_lists = [market_data[x:x + 10]
                                 for x in range(0, len(market_data), 10)]
            cid = None
            for list_ in market_data_lists:
                parsed_market_data = [market_title]
                for string in list_:
                    try:
                        cid = re.search(
                            pattern='#\w+\-(\d+)', string=string
                        ).group(1)
                        string = re.search(
                            pattern='(.*)\$\(.*\)\;', string=string
                        ).group(1)
                    except AttributeError:
                        pass
                    parsed_market_data.append(string)
                for line in urlopen(f'https://www.predictit.org/Contract/{cid}/#data').read().splitlines():
                    if 'ChartTicker' in str(line):
                        ticker = re.search(
                            pattern="= '(.*)';", string=str(line)).group(1)
                        break
                parsed_market_data.insert(1, cid)
                parsed_market_data.append(ticker)
                contract = Contract(*parsed_market_data)
                self.my_contracts.append(contract)

    def update_my_contracts(self):
        """
        Updates info on contracts currently held by the authenticated user.
        """
        my_shares = self.browser.get(
            'https://www.predictit.org/Profile/GetSharesAjax')
        for market in my_shares.soup.find_all('table', class_='table table-striped table-center'):
            market_title = market.previous_element.previous_element.find('div', class_='outcome-title').find('a').get(
                'title')
            for contract in self.my_contracts:
                if market_title == contract.market:
                    market_data = [i.text.strip().replace(
                        "\n", "").replace("    ", "").replace('\r', '') for i in market.find_all('td')]
                    market_data_lists = [market_data[x:x + 10]
                                         for x in range(0, len(market_data), 10)]
                    cid = None
                    for list_ in market_data_lists:
                        parsed_market_data = [market_title]
                        for string in list_:
                            try:
                                cid = re.search(
                                    pattern='#\w+\-(\d+)', string=string
                                ).group(1)
                                string = re.search(
                                    pattern='(.*)\$\(.*\)\;', string=string
                                ).group(1)
                            except AttributeError:
                                pass
                            parsed_market_data.append(string)
                        parsed_market_data.insert(1, cid)
                        self.timestamp = datetime.datetime.now()
                        self.avg_price = parsed_market_data[5]
                        self.gain_loss = parsed_market_data[8]
                        self.latest = parsed_market_data[9]
                        self.buy = parsed_market_data[-2]
                        self.sell = parsed_market_data[-1]
            else:
                continue

    def list_my_contracts(self):
        """
        Provides a quick summary of currently held contracts.
        """
        self.get_my_contracts()
        try:
            for contract in self.my_contracts:
                print('------')
                print(contract.timestamp)
                print(contract.market)
                print(contract.ticker)
                print(contract.shares)
                print(contract.gain_or_loss)
                print(contract.average_price)
                print(contract.buy_price)
                print(contract.sell_price)
                print(contract.estimate_sale_of_current_shares)
                print(contract.implied_odds)
                print(contract.estimate_best_result)
                print('------')
        except TypeError:
            print('You don\'t have any active contracts!')
            return

    def search_for_contracts(self, market, buy_sell, type_, contracts=None):
        """
        Search for contracts that aren't currently owned and add them to
        the contracts list, which is created if it isn't supplied.
        :param market: dict
        :param buy_sell: str
        :param type_: str
        :param contracts: list
        :return: list, contracts
        """
        if not contracts:
            contracts = []
        if type_.lower() in ['yes', 'long'] and buy_sell == 'buy':
            type_ = {'long': 'BestBuyYesCost'}
        elif type_.lower() in ['no', 'short'] and buy_sell == 'buy':
            type_ = {'short': 'BestBuyNoCost'}
        elif type_.lower() in ['yes', 'long'] and buy_sell == 'sell':
            type_ = {'long': 'BestSellYesCost'}
        elif type_.lower() in ['no', 'short'] and buy_sell == 'sell':
            type_ = {'short': 'BestSellNoCost'}
        if 'us' and 'election' in market.replace('.', '').lower():
            market_link = 'https://www.predictit.org/api/marketdata/category/6'
        elif 'us' and 'politic' in market.replace('.', '').lower():
            market_link = 'https://www.predictit.org/api/marketdata/category/13'
        elif 'world' in market.lower():
            market_link = 'https://www.predictit.org/api/marketdata/category/4'
        else:
            print('Invalid market selected.')
            return
        raw_market_data = self.browser.get(market_link).json()['Markets']
        for market in raw_market_data:
            for contract in market['Contracts']:
                if list(type_.keys())[0].title() == 'Long' and buy_sell == 'sell':
                    new_contract = Contract(type_='long', sell=contract[list(type_.values())[0]], buy='0.00',
                                            buy_offers=0, sell_offers=0, avg_price='0.00', gain_loss='0.00',
                                            latest=contract['LastTradePrice'], market=market['Name'],
                                            name=contract['Name'], shares='0', cid=contract['ID'],
                                            ticker=contract['TickerSymbol']
                                            )
                    contracts.append(new_contract)
                elif list(type_.keys())[0].title() == 'Short' and buy_sell == 'sell':
                    new_contract = Contract(type_='short', sell=contract[list(type_.values())[0]], buy='0.00',
                                            buy_offers=0, sell_offers=0, avg_price='0.00', gain_loss='0.00',
                                            latest=contract['LastTradePrice'], market=market['Name'],
                                            name=contract['Name'], shares='0', cid=contract['ID'],
                                            ticker=contract['TickerSymbol']
                                            )
                    contracts.append(new_contract)
                elif list(type_.keys())[0].title() == 'Long' and buy_sell == 'buy':
                    new_contract = Contract(type_='long', sell='0.00', buy=contract[list(type_.values())[0]],
                                            buy_offers=0, sell_offers=0, avg_price='0.00', gain_loss='0.00',
                                            latest=contract['LastTradePrice'], market=market['Name'],
                                            name=contract['Name'], shares='0', cid=contract['ID'],
                                            ticker=contract['TickerSymbol']
                                            )
                    contracts.append(new_contract)
                elif list(type_.keys())[0].title() == 'Short' and buy_sell == 'buy':
                    new_contract = Contract(type_='short', sell='0.00', buy=contract[list(type_.values())[0]],
                                            buy_offers=0, sell_offers=0, avg_price='0.00', gain_loss='0.00',
                                            latest=contract['LastTradePrice'], market=market['Name'],
                                            name=contract['Name'], shares='0', cid=contract['ID'],
                                            ticker=contract['TickerSymbol']
                                            )
                    contracts.append(new_contract)
        return contracts

    def trigger_stop_loss(self, contract, number_of_shares, trigger_price):
        contract.sell_shares(
            api=self, number_of_shares=number_of_shares, sell_price=trigger_price)

    def monitor_price_of_contract(self, contract, trigger_price, monitor_type, number_of_shares=None):
        """
        :param contract: Contract
        :param trigger_price: float
        :param monitor_type: str
        :param number_of_shares: int
        :return:
        """
        contract.update()
        if monitor_type == 'stop_loss':
            if floatify(contract.latest) <= trigger_price:
                contract.sell_shares(
                    api=self, number_of_shares=number_of_shares, sell_price=trigger_price)
            else:
                print(f'Your sell price is {trigger_price}. The current price is {floatify(contract.latest)}')
        elif monitor_type == 'buy_at':
            if floatify(contract.latest) <= trigger_price:
                contract.buy_shares(
                    api=self, number_of_shares=number_of_shares, buy_price=trigger_price)
            else:
                print(f'Your buy in price is {trigger_price}. The current price is {floatify(contract.latest)}')
        elif monitor_type == 'generic':
            print(contract.latest)

    def set_stop_loss(self, contract, stop_loss, number_of_shares):
        """
        :param contract: Contract
        :param stop_loss: float
        :param number_of_shares: int
        :return:
        """
        while True:
            sleep(2)
            self.monitor_price_of_contract(contract, monitor_type='stop_loss',
                                           number_of_shares=number_of_shares, trigger_price=stop_loss)
