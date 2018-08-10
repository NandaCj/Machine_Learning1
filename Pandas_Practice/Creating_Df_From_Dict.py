import pandas as pd
"""
To Treat Dict-Keys as the Index , pass Orient = "index"

"""
Dict = {'SOLARINDS': 18.1, 'THEMISMED': 13.72, 'SALASAR': 9.96, 'ELAND': 47.99, 'MUKTAARTS': 11.29,
        'GESHIP': 150.78, 'KDDL': 13.43, 'ERIS': 13.75, 'UNIONBANK': 1228.44, 'MEGH': 25.43, 'GEECEE': 21.73,
        'SUPREMEINF': 41.98, 'MAANALU': 3.38, 'RECLTD': 1974.92, 'SORILINFRA': 30.57, 'UNIVCABLES': 34.7,
        'MERCATOR': 26.99, 'ESTER': 41.7, 'MINDAIND': 315.87, 'SUPREMEIND': 25.41, 'LAOPALA': 11.1}

Dict = {"Name":'Nandha', 'Details':{'Age':'27', 'Loc':'CN'}}

Dict = {u'Jun_17':{u'Stock_Adjustments': 3.79, u'PAT': -38.28, u'Operating_Profit': -0.28, u'Equity_Capital': 47.99, u'P_L_Year': -2.17,
                 u'Other_Adjustment': 0.0, u'Interest': 2.22, u'Provisions_Made': 0.0, u'Employee_Exp': 15.04, u'Dividend_Rate': 0.0,
                 u'Total_Income': 44.84, u'Govt_Share': 0.0, u'P_Year_Adjustment': 0.0, u'Raw_Material': 21.36, u'Total_Exp': 44.33,
                 u'Power_Fuel': 0.0, u'Net_Sales': 44.05, u'Non_Promoter_Holding': 0.0, u'Exp_Capitialised': 0.0, u'Extraordinary': 0.0,
                 u'Other_Income': 0.79, u'Ebit': 0.04, u'Capital_Adeq_Ratio': 0.0, u'Reserves_Back': 0.0, u'Eps': 'NAN', u'Taxes': 0.0,
                 u'RD_Exp': 0.0, u'Other_Exp': 4.15, u'Surplus': 0.0, u'Admin_Selling_Exp': 0.0, u'Ebt': -2.17, u'Depriciation': 0.47,
                 u'Close': 21.4, u'Non_Promoter_Share': 0.0, u'Ebitda': 0.51},
        u'_id': u'ELAND'}

df = pd.DataFrame.from_dict(Dict)

print (df)
# print (df.info())
# print (df.describe())




Dict = {u'Jun_17':
                {u'Stock_Adjustments': 3.79, u'PAT': -38.28, u'Operating_Profit': -0.28, u'Equity_Capital': 47.99, u'P_L_Year': -2.17,
                 u'Other_Adjustment': 0.0, u'Interest': 2.22, u'Provisions_Made': 0.0, u'Employee_Exp': 15.04, u'Dividend_Rate': 0.0,
                 u'Total_Income': 44.84, u'Govt_Share': 0.0, u'P_Year_Adjustment': 0.0, u'Raw_Material': 21.36, u'Total_Exp': 44.33,
                 u'Power_Fuel': 0.0, u'Net_Sales': 44.05, u'Non_Promoter_Holding': 0.0, u'Exp_Capitialised': 0.0, u'Extraordinary': 0.0,
                 u'Other_Income': 0.79, u'Ebit': 0.04, u'Capital_Adeq_Ratio': 0.0, u'Reserves_Back': 0.0, u'Eps': 'NAN', u'Taxes': 0.0,
                 u'RD_Exp': 0.0, u'Other_Exp': 4.15, u'Surplus': 0.0, u'Admin_Selling_Exp': 0.0, u'Ebt': -2.17, u'Depriciation': 0.47,
                 u'Close': 21.4, u'Non_Promoter_Share': 0.0, u'Ebitda': 0.51},
        u'Sep_17': {u'Stock_Adjustments': 3.79, u'PAT': -38.28, u'Operating_Profit': -0.28, u'Equity_Capital': 47.99, u'P_L_Year': -2.17,
                    u'Other_Adjustment': 0.0, u'Interest': 2.22, u'Provisions_Made': 0.0, u'Employee_Exp': 15.04, u'Dividend_Rate': 0.0,
                    u'Total_Income': 44.84, u'Govt_Share': 0.0, u'P_Year_Adjustment': 0.0, u'Raw_Material': 21.36, u'Total_Exp': 44.33,
                    u'Power_Fuel': 0.0, u'Net_Sales': 44.05, u'Non_Promoter_Holding': 0.0, u'Exp_Capitialised': 0.0, u'Extraordinary': 0.0,
                    u'Other_Income': 0.79, u'Ebit': 0.04, u'Capital_Adeq_Ratio': 0.0, u'Reserves_Back': 0.0, u'Eps': 'NAN', u'Taxes': 0.0,
                    u'RD_Exp': 0.0, u'Other_Exp': 4.15, u'Surplus': 0.0, u'Admin_Selling_Exp': 0.0, u'Ebt': -2.17, u'Depriciation': 0.47,
                    u'Close': 16.2, u'Non_Promoter_Share': 0.0, u'Ebitda': 0.51},
        u'Dec_17': {u'Stock_Adjustments': 3.79, u'PAT': -38.28, u'Operating_Profit': -0.28, u'Equity_Capital': 47.99, u'P_L_Year': -2.17,
                    u'Other_Adjustment': 0.0, u'Interest': 2.22, u'Provisions_Made': 0.0, u'Employee_Exp': 15.04, u'Dividend_Rate': 0.0,
                    u'Total_Income': 44.84, u'Govt_Share': 0.0, u'P_Year_Adjustment': 0.0, u'Raw_Material': 21.36, u'Total_Exp': 44.33,
                    u'Power_Fuel': 0.0, u'Net_Sales': 44.05, u'Non_Promoter_Holding': 0.0, u'Exp_Capitialised': 0.0, u'Extraordinary': 0.0,
                    u'Other_Income': 0.79, u'Ebit': 0.04, u'Capital_Adeq_Ratio': 0.0, u'Reserves_Back': 0.0, u'Eps': 'NAN', u'Taxes': 0.0,
                    u'RD_Exp': 0.0, u'Other_Exp': 4.15, u'Surplus': 0.0, u'Admin_Selling_Exp': 0.0, u'Ebt': -2.17, u'Depriciation': 0.47,
                    u'Close': 23.5, u'Non_Promoter_Share': 0.0, u'Ebitda': 0.51},
        u'Mar_17': {u'Stock_Adjustments': 3.79, u'PAT': -38.28, u'Operating_Profit': -0.28, u'Equity_Capital': 47.99, u'P_L_Year': -2.17,
                    u'Other_Adjustment': 0.0, u'Interest': 2.22, u'Provisions_Made': 0.0, u'Employee_Exp': 15.04, u'Dividend_Rate': 0.0,
                    u'Total_Income': 44.84, u'Govt_Share': 0.0, u'P_Year_Adjustment': 0.0, u'Raw_Material': 21.36, u'Total_Exp': 44.33,
                    u'Power_Fuel': 0.0, u'Net_Sales': 44.05, u'Non_Promoter_Holding': 0.0, u'Exp_Capitialised': 0.0, u'Extraordinary': 0.0,
                    u'Other_Income': 0.79, u'Ebit': 0.04, u'Capital_Adeq_Ratio': 0.0, u'Reserves_Back': 0.0, u'Eps': 'NAN', u'Taxes': 0.0,
                    u'RD_Exp': 0.0, u'Other_Exp': 4.15, u'Surplus': 0.0, u'Admin_Selling_Exp': 0.0, u'Ebt': -2.17, u'Depriciation': 0.47,
                    u'Close': 22.05, u'Non_Promoter_Share': 0.0, u'Ebitda': 0.51},
        u'Mar_18': {u'Stock_Adjustments': 3.79, u'PAT': -38.28, u'Operating_Profit': -0.28, u'Equity_Capital': 47.99, u'P_L_Year': -2.17,
                    u'Other_Adjustment': 0.0, u'Interest': 2.22, u'Provisions_Made': 0.0, u'Employee_Exp': 15.04, u'Dividend_Rate': 0.0,
                    u'Total_Income': 44.84, u'Govt_Share': 0.0, u'P_Year_Adjustment': 0.0, u'Raw_Material': 21.36, u'Total_Exp': 44.33,
                    u'Power_Fuel': 0.0, u'Net_Sales': 44.05, u'Non_Promoter_Holding': 0.0, u'Exp_Capitialised': 0.0, u'Extraordinary': 0.0,
                    u'Other_Income': 0.79, u'Ebit': 0.04, u'Capital_Adeq_Ratio': 0.0, u'Reserves_Back': 0.0, u'Eps': 'NAN', u'Taxes': 0.0,
                    u'RD_Exp': 0.0, u'Other_Exp': 4.15, u'Surplus': 0.0, u'Admin_Selling_Exp': 0.0, u'Ebt': -2.17, u'Depriciation': 0.47,
                    u'Close': 11.7, u'Non_Promoter_Share': 0.0, u'Ebitda': 0.51},
        u'_id': u'ELAND'}
