
import requests
import pandas as pd
import matplotlib.pyplot as plt
import time
plt.style.use('seaborn')

###PARAMETERS
#================================================================================
SYMBOL_LIST = ['BTCUSDT','ETHUSDT','ADAUSDT',
                'DOTUSDT','SOLUSDT','LUNAUSDT','UNIUSDT','AVAXUSDT',
                'LINKUSDT','ATOMUSDT','AAVEUSDT','CAKEUSDT','RUNEUSDT',
                'SNXUSDT','COMPUSDT','MKRUSDT','SUSHIUSDT','YFIUSDT',
                'BNBUSDT','XRPUSDT','DOGEUSDT','SHIBUSDT','MATICUSDT',
                'NEARUSDT','LTCUSDT','TRXUSDT','ALGOUSDT']

INTERVAL = '30m'

#This parameter will be multiplied by 1000 for example, setting it 3 will return 3000 candles
THOUSANDS_OF_CANDLES = 3 

BIN_API = 'YOUR-BINANCE-API'
URL = 'https://api.binance.com'
headers = {
    'X-MBX-APIKEY': BIN_API
}
PATH = '/api/v3/klines'



#Get the data
def get_ohlc_data(SYMBOL, INTERVAL, ENDTIME = None):
    

    params = {
        'symbol': SYMBOL,
        'interval':INTERVAL,
        'limit': 1000,
        'endTime': ENDTIME
    }       
    
    
    r = requests.get(URL+PATH, headers=headers, params=params)
    df = pd.DataFrame(r.json())
    ENDTIME = df.iloc[0,0]
    
    df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit = 'ms')
    df = df.iloc[:,[0,4]]
    df.columns = ['Time','Close']
    df['Close'] = df['Close'].astype('float')
    
    return df, ENDTIME



### GET 3*1000 CANDLESTICKS
#===========================================================================

for symbol in SYMBOL_LIST:
    
    df = pd.DataFrame(columns = ['Time','Close'])
    df_temp, endtime = get_ohlc_data(symbol,INTERVAL)
    df = pd.concat([df,df_temp], axis = 0)
    
    for i in range(THOUSANDS_OF_CANDLES-1):
        
        time.sleep(0.5)
        df_temp, endtime = get_ohlc_data(symbol,INTERVAL, endtime)
        df = pd.concat([df,df_temp], axis = 0)
    
    
    df = df.sort_values('Time', ignore_index=True)
    df = df.drop_duplicates('Time')
    df.to_csv(f'Data/{symbol}_{INTERVAL}.csv', index = False)
    print(f'{symbol}_{INTERVAL} downloaded')














