from nsetools import Nse
from win10toast import ToastNotifier

toaster = ToastNotifier()
nse = Nse()
STOCKS_TO_MONITOR = {
                    'JUSTDIAL': {'Buy': 441.7, 'Sell': 435.11666669999994, 'Popup_Shown_Already': False},

                    'ABCAPITAL': {'Buy': 163, 'Sell': 157, 'Popup_Shown_Already': False},
                    'EXIDEIND': {'Buy': 268.45, 'Sell': 263.9, 'Popup_Shown_Already': False},
                     'IOC': {'Buy': 167.55, 'Sell': 163.9666667, 'Popup_Shown_Already': False},
                     'DLF': {'Buy': 223.45, 'Sell': 219.3666667, 'Popup_Shown_Already': False},
                     'ADANIENT': {'Buy': 132.45, 'Sell': 129.25, 'Popup_Shown_Already': False},

                     'IRB': {'Buy': 262.75, 'Sell': 263.0833333, 'Popup_Shown_Already': False},

                     'TATACOFFEE': {'Buy': 124.95, 'Sell': 124.06666670000001, 'Popup_Shown_Already': False},
                     #'PRAKASH': {'Buy': 200.45, 'Sell': 200.06666669999998, 'Popup_Shown_Already': False},
                    #'GNFC': {'Buy': 499.9, 'Sell': 493.38333330000006, 'Popup_Shown_Already': False},
                    #'MEGH': {'Buy': 111.75, 'Sell': 110.7, 'Popup_Shown_Already': False},
                    #'AMBUJACEM': {'Buy': 230.45, 'Sell': 230.4833333, 'Popup_Shown_Already': False},
                     'OIL': {'Buy': 227.75, 'Sell': 227.7333333, 'Popup_Shown_Already': False},
                     }


STOCKS_CURRENT_PRICE = {}
DURATION = 10
class Popup:

    def __init__(self):
        self.Check_Stock_CurrentPrice()


    def Check_Stock_CurrentPrice(self):

        for stock in STOCKS_TO_MONITOR:
            Current_Price = float(nse.get_quote(stock)['lastPrice'])
            Buy_Call = STOCKS_TO_MONITOR[stock]['Buy']
            Sell_Call = STOCKS_TO_MONITOR[stock]['Sell']
            print(stock, Current_Price, Buy_Call, Sell_Call)
            self.Validate_For_Buy_Sell_Price(stock, Current_Price, Buy_Call, Sell_Call)


    def Validate_For_Buy_Sell_Price(self, Stock, Current_Price, Buy_Call, Sell_Call):
        print ("Inside Validate_For_Buy_Sell_Price")
        Popup_Shown_Already = STOCKS_TO_MONITOR[Stock]['Popup_Shown_Already']
        if Popup_Shown_Already:
            print("POP Up Already Shown for {}".format(Stock))
            pass
        else:
            if Current_Price >= Buy_Call:
                self.Show_Buy_Popup(Stock, Current_Price, Buy_Call)
                STOCKS_TO_MONITOR[Stock]['Popup_Shown_Already'] = True
            if Current_Price <= Sell_Call:
                self.Show_Sell_Popup(Stock, Current_Price, Sell_Call)
                STOCKS_TO_MONITOR[Stock]['Popup_Shown_Already'] = True


    def Show_Buy_Popup(self, Stock, Current_Price, Buy_Call):
        print ("Showing BUY PopUp")

        global BUY_MSG
        BUY_MSG += "BUY CALL ACTIVATED \n BUY {} \nCurrent Price:\t{} BUY_PRICE:\t{} \n ".format(Stock, Current_Price, Buy_Call)
        toaster.show_toast("BUY CALL ACTIVATED", "BUY {} Current Price:{} BUY_PRICE:{} ".format(Stock, Current_Price, Buy_Call), duration=DURATION)


    def Show_Sell_Popup(self, Stock, Current_Price, Sell_Call):
        global SELL_MSG
        print("Showing SELL PopUp")
        SELL_MSG += "SELL CALL ACTIVATED\n SELL {} Current Price:{} BUY_PRICE:{} ".format(Stock, Current_Price, Sell_Call)
        toaster.show_toast("SELL CALL ACTIVATED","SELL {} Current Price:{} SELL_PRICE:{} ".format(Stock, Current_Price, Sell_Call), duration=DURATION)

#notify2.init("News Notifier")
for _ in range(5):
    BUY_MSG = ""
    SELL_MSG = ""
    Popup()
    print(BUY_MSG)
    print(SELL_MSG)
    # if BUY_MSG or SELL_MSG:
    #     toaster.show_toast(title="PRICE ALERT : \n", msg="{} \n {}".format(BUY_MSG, SELL_MSG), duration=60)
    #     #notify2.Notification(summary="PRICE ALERT : \n", message="{} \n {}".format(BUY_MSG, SELL_MSG))



