# -*- coding: utf-8 -*-
#Copyright (c) 2020, KarjaKAK
#All rights reserved.

from urllib import request
from CreatePassword import CreatePassword as cp

class Fixio:
    """
    This is the wrapper class for fixer.io calling API
    Only for basic calling of EndPoints:
        - LatestEndpoint
        - SymbolsEndpoint
        - HistoricalEndpoint
        - ConvertEndpoint
    For details please go to https://fixer.io/documentation
    """
    def __init__(self, base = None, symbols = None, amount = None, apik = None):
        self.base = base
        self.symbols = symbols
        self.amount = amount
        self.apik = apik
    
    def converlatest(self):
        """
        Get latest convert rate.
        The default base is "EUR" only for free version API.
        If user have subscription, than the base can be change.
        """
        if self.apik:
            try:
                if self.base is not None:
                    if self.symbols is None:
                        gd = request.urlopen(f'https://data.fixer.io/api/latest?access_key={self.apik}&base={self.base}')
                    else:
                        gd = request.urlopen(f'https://data.fixer.io/api/latest?access_key={self.apik}&base={self.base}&symbols={self.symbols}')
                else:
                    gd = request.urlopen(f'https://data.fixer.io/api/latest?access_key={self.apik}')
                gd = eval(gd.readlines()[0].decode('utf-8').replace('false', '"false"').replace('true', '"true"'))
                return gd
            except:
                import traceback
                traceback.print_exc()
        else:
            print('Please get api in https://fixer.io')
    
    def conversymbols(self):
        """
        Get all curencies symbols.
        """
        if self.apik:
            try:
                gd = request.urlopen(f'https://data.fixer.io/api/symbols?access_key={self.apik}')
                gd = eval(gd.readlines()[0].decode('utf-8').replace('false', '"false"').replace('true', '"true"'))
                return gd
            except:
                import traceback
                traceback.print_exc()
        else:
            print('Please get api in https://fixer.io')
    
    def converhist(self, date):
        """
        Get conversion rate from past dates.
        note: only for subscription.
        """
        if self.apik:
            try:
                if self.base:
                    if self.symbols:
                        gd = request.urlopen(f'https://data.fixer.io/api/{date}?access_key={self.apik}&base={self.base}&symbols={self.symbols}')
                    else:
                        gd = request.urlopen(f'https://data.fixer.io/api/{date}?access_key={self.apik}&base={self.base}')
                else:
                    gd = request.urlopen(f'https://data.fixer.io/api/{date}?access_key={self.apik}')
                gd = eval(gd.readlines()[0].decode('utf-8').replace('false', '"false"').replace('true', '"true"'))
                return gd
            except:
                import traceback
                traceback.print_exc()
        else:
            print('Please get api in https://fixer.io')
    
    def converconv(self, date = None):
        """
        Get conversion rate 'from' a currency 'to' other currency with specific 'amount'
        note: only for subscription.
        """
        if self.apik:
            try:
                if self.base and self.symbols and self.amount:
                    if date:
                        gd = request.urlopen(f'https://data.fixer.io/api/convert?access_key={self.apik}&from={self.base}&to={self.symbols}&amount={self.amount}&date={date}')
                    else:
                        gd = request.urlopen(f'https://data.fixer.io/api/convert?access_key={self.apik}&from={self.base}&to={self.symbols}&amount={self.amount}')
                    gd = eval(gd.readlines()[0].decode('utf-8').replace('false', '"false"').replace('true', '"true"'))
                    return gd
                else:
                    print('Unable to convert as the base, symbols, and amount are not complete!')
            except:
                import traceback
                traceback.print_exc()
        else:
            print('Please get api in https://fixer.io')

if __name__ == '__main__':
    from pprint import pprint
    
    key = cp.readcpd('fixio')
    lbs = ['USD', 'AUD', 'EUR', 'SGD', 'CNY', 'GBP']
    for i in lbs:
        a = Fixio(base = i, symbols = 'IDR', amount = 1, apik = key)
        pprint(a.converconv())
        print()
    #a = Fixio(apik = key)
    #b = a.conversymbols()
    #pprint(b)
    #with open('curiso', 'wb') as cf:
        #cf.write(str(b).encode())