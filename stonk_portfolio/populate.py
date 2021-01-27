import sqlite3
import config
import alpaca_trade_api as tradeapi



"""init REST obj from alpaca package"""
api = tradeapi.REST(config.API_KEY_ID, config.SECRET_KEY, base_url=config.BASE_URL)

"""establish connection to DB"""
connection = sqlite3.connect(config.DB_FILE)

##This will tell the SQLite connection to return sqlite Row objects.
connection.row_factory = sqlite3.Row
##create cursor objet so we can run queries
cursor = connection.cursor()

cursor.execute("""
    SELECT symbol, name FROM stonk_portfolio_stock
""")

rows = cursor.fetchall()

##list comprehension loop through rows in rows and pull out symbol then make a list with it
symbols = [row['symbol'] for row in rows]


### call list assets method to get list of assets from alpaca 
assets = api.list_assets()

##loop through list, parse and insert into db
for asset in assets:
    try:
        ##check db against list of assets and insert new stocks
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            print(f'Added a new stock {asset.symbol} {asset.name}')
            cursor.execute("INSERT INTO stonk_portfolio_stock (symbol, name, exchange) VALUES (?, ?, ?)", (asset.symbol, asset.name, asset.exchange))
    except Exception as e:
        print(asset.symbol)
        print(e)
        

connection.commit()




