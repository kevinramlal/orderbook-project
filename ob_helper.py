#Creating an orderbook!

import pandas as pd
import numpy as np
from collections import defaultdict
from IPython.display import display,HTML

import ipywidgets as widgets 

class Book:
    """
    Iniatlize and alter book using mkt and limit orders
    Should display as a dataframe
    """
    def __init__(self,mid):
        self.mid = mid
        self.bid_side = self.bid_side_gen() #think of these as queues 
        self.ask_side = self.ask_side_gen()
        self.book = self.generate_book()
    
    def bid_side_gen(self):
        """
        Initialize Bid side of Book
        Add in more functionality to have imbalance
        """
        self.bid_sched = [self.mid-0.01*i for i in range(1,11,1)] #10 levels deep
        self.bid_vol_sched = [int(100 - 10*i) for i in range(10)] #exponentially decreasing vol sched
        return defaultdict(float,(zip(self.bid_sched,self.bid_vol_sched)))
        

    def ask_side_gen(self):
        """
        Initialize Bid side of Book
        Add in more functionality to have imbalance
        """
        self.ask_sched = [self.mid+0.01*i for i in range(1,11,1)] #10 levels deep
        self.ask_vol_sched = [int(100 - 10*i) for i in range(10)] #exponentially decreasing vol sched
        return defaultdict(float,(zip(self.ask_sched,self.ask_vol_sched)))

    def generate_book(self):
        """
        Always show the top 10 - if none then it should be 0
        """

        ask_side = self.ask_side
        bid_side = self.bid_side

        #remove empty portions
        ask_side = {k:v for k,v in ask_side.items() if v != 0}
        bid_side = {k:v for k,v in bid_side.items() if v != 0}

        #Initialize numpy arrays
     

        book = pd.DataFrame()
        bids = list(bid_side.keys())
        bids.sort(reverse = True)
        bid_vols = pd.Series([bid_side[k] for k in bids ])
        bids = pd.Series(bids)


        asks = list(ask_side.keys())
        asks.sort()
        ask_vols = pd.Series([ask_side[k] for k in asks ])
        asks = pd.Series(asks)

        levels = max(len(bids),len(asks))
        book['Level'] = np.arange(1,levels,1)

        book['Bids'] = bids
        book['Bid_Vol'] = bid_vols
        book['Asks'] = asks
        book['Ask_Vols'] = ask_vols
        
        return book
        
    def display_book(self):
        self.book = self.generate_book()
        return HTML(self.book.to_html(index = False))

    def order_enter(self,action,amount, price=0,type='MKT'):
        total_amount = amount

        if action == "BUY":
            if type == 'MKT':
                avg_price = 0
                
                for k,v in self.ask_side.items(): 
                    new_amount = max(0,amount-v)
                
                    if new_amount == 0:
                        avg_price += amount*k
                        
                        self.ask_side[k] = v - amount
                        msg = "Executed BUY for " + str(amount) + " at price: " + str(avg_price/total_amount)
                        return msg
                    else:
                        avg_price += k*v
                        amount = new_amount
                        self.ask_side[k] = 0                   
                
            elif type =='LMT':
                self.bid_side[price] += amount
                msg = "Entered Limit Order to BUY " + str(amount) + " at price: " + str(price)
                return msg
            else:
                print("Please enter value type: either 'MKT' or 'LMT'")
                return None
        
        elif action == "SELL":
            if type == 'MKT':
                
                avg_price = 0
                
                for k,v in self.bid_side.items(): 
                    new_amount = max(0,amount-v)
                
                    if new_amount == 0:
                        avg_price += amount*k
                        
                        self.bid_side[k] = v - amount
                        msg = "Executed SELL for "+ str(amount)+ " at price: " + str(avg_price/total_amount)
                        return msg
                    else:
                        avg_price += k*v
                        amount = new_amount
                        self.bid_side[k] = 0                   
                
                
            elif type =='LMT':
                self.ask_side[price] += amount
                msg = "Entered Limit Order to SELL " + str(amount) + "at " + str(price)
                return msg
            else:
                print("Please enter value type: either 'MKT' or 'LMT'")
                return None
                
        else:
            print("Please enter a valid Action: either 'BUY' or 'SELL'")
            return None







