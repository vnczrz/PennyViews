import yfinance as yf
# import yahoo_fin.stock_info as si
from yahoo_fin.stock_info import get_stats, get_live_price, get_holders, get_analysts_info, get_quote_table
import json
from pprint import pprint
import pandas as pd


stock = get_stats('TSLA')

# print(stock.loc['28':, 'Attribute':'Value'])

# balance_sheet = stock.loc['28':, 'Attribute':'Value'].to_dict('records')
price_his = stock.loc[0:8, 'Attribute':'Value'].to_dict('records')

pprint(price_his, indent=2)









# stock = yf.Ticker('TSLA')

# df = stock.balancesheet


# print(df)




# # pprint(stock.info, indent=2)

# # print(stock.info['symbol'])

# def basicInfo(obj):
#     table = ['open','previousClose', 'industry', 'marketCap', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow', 'forwardPE', 'earningsQuarterlyGrowth', 'longBusinessSummary']

#     info = {}

#     for t in table:
#         d = stock.info[f'{t}']
#         x = {f'{t}': f'{d}'}
#         info.update(x)
    
#     return info
    

# # pprint(info)
# def getRecs(obj):
#     recs = stock.recommendations

#     time_mask = recs.last('3M')
#     time_sort = time_mask.sort_values(by='Date', ascending=False)
#     # print(time_sort)

#     dic = time_sort.to_dict('records')

#     return dic

# # pprint(dic, indent=2)
# # rec_mask = (stock.recommendations.index)

# # basic = basicInfo(stock)

# recs = getRecs(stock)

# pprint(recs, indent=2)


# def basicInfo(obj):
#     base = []
    
#     table = ['open','previousClose', 'industry', 'marketCap', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow', 'forwardPE', 'earningsQuarterlyGrowth', 'longBusinessSummary']

#     info = {}

#     for t in table:
#         d = obj.info[f'{t}']
#         x = {f'{t}': f'{d}'}
#         info.update(x)

#     recs = obj.recommendations

#     time_mask = recs.last('3M')
#     time_sort = time_mask.sort_values(by='Date', ascending=False)
#     # print(time_sort)

#     rec = time_sort.to_dict('records')
    
#     base.append(rec)
#     base.append(info)

#     return base

# base = basicInfo(stock)

# pprint(base[0], indent=2)
# pprint(base[1], indent=2)



