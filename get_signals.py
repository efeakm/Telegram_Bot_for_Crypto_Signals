
def get_signals():

    import requests
    import pandas as pd
    from talib import SMA
    import time
    

    ###PARAMETERS
    #==================================================================================
    SYMBOL_LIST = ['BTCUSDT','ETHUSDT','ADAUSDT',
                   'DOTUSDT','SOLUSDT','LUNAUSDT','UNIUSDT','AVAXUSDT',
                   'LINKUSDT','ATOMUSDT','AAVEUSDT','CAKEUSDT','RUNEUSDT',
                   'SNXUSDT','COMPUSDT','MKRUSDT','SUSHIUSDT','YFIUSDT',
                   'BNBUSDT','XRPUSDT','DOGEUSDT','SHIBUSDT','MATICUSDT',
                   'NEARUSDT','LTCUSDT','TRXUSDT','ALGOUSDT']

    INTERVAL = '30m'




    
    BIN_API = 'YOUR-BINANCE-API'
    URL = 'https://api.binance.com'
    headers = {
        'X-MBX-APIKEY': BIN_API
    }
    PATH = '/api/v3/klines'
    
     
    ###UPDATE DATA
    #===============================================================================
    def update_ohlc_data(SYMBOL, INTERVAL):
        
    
        #GET LOCAL DATA
        df = pd.read_csv(f'Data/{SYMBOL}_{INTERVAL}.csv')
        df['Time'] = pd.to_datetime(df['Time'])
        df['Close'] = df['Close'].astype('float')
        
        starttime = pd.to_datetime(df.iloc[-1,0])
        starttime = (starttime - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s') * 1000  
        params = {
            'symbol': SYMBOL,
            'interval':INTERVAL,
            'limit': 1000,
            'startTime': starttime
        }       
        
        
        r = requests.get(URL+PATH, headers=headers, params=params)
        df_temp = pd.DataFrame(r.json())
        
    
        
        df_temp.iloc[:,0] = pd.to_datetime(df_temp.iloc[:,0], unit = 'ms')
        df_temp = df_temp.iloc[:,[0,4]]
        df_temp.columns = ['Time','Close']
        df_temp['Close'] = df_temp['Close'].astype('float')
        
        
        df = pd.concat([df, df_temp], axis = 0)
        df = df.drop_duplicates('Time', keep = 'last')
        df = df.sort_values('Time', ignore_index = True)
        
        
        #Keep only last 3000 row data        
        df = df.iloc[-3000:,:]
        df = df.reset_index(drop=True)
    
        df.to_csv(f'Data/{SYMBOL}_{INTERVAL}.csv', index = False)
        
        return df
    
    
    
    def over_daily_sma(SYMBOL, DAYS_OVER_SMA = 5):
        
        #Get daily data
        params = {
            'symbol': SYMBOL,
            'interval':'1d',
            'limit': 50,
        }      
        r = requests.get(URL+PATH, headers=headers, params=params)
        df = pd.DataFrame(r.json())
        
    
        #Process data
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit = 'ms')
        df = df.iloc[:,[0,4]]
        df.columns = ['Time','Close']
        df['Close'] = df['Close'].astype('float')
        df = df.sort_values('Time', ignore_index = True)
        
        df['sma'] = SMA(df['Close'], 20)
        df['trend'] = df['Close'] >= df['sma']
        
        trend = df['trend'].tail(DAYS_OVER_SMA).sum()
        
        if trend == DAYS_OVER_SMA:
            return 'up'
        elif trend == 0:
            return 'down'
        else:
            return 'neutral'
    
    
    
    
    def risk_metric(df):
        
        ret = pd.DataFrame()
        ret['close'] = df['Close']
        ret['sma'] = SMA( df['Close'], 50)
        
        
        #WRITE YOUR OWN RISK METRIC
        ret['risk'] = 1

        return ret['risk']
    
    
    longs = []
    shorts = []
    
    for symbol in SYMBOL_LIST:
        
        time.sleep(0.2)
        
        df_sym = update_ohlc_data(symbol, INTERVAL)
        df_sym['indicator'] = risk_metric(df_sym)
        last_point = df_sym.iloc[-1,2]
        
        
        if last_point <= 0.05:
            
            time.sleep(0.2)
            trend = over_daily_sma(symbol, DAYS_OVER_SMA = 5)
            if trend == 'up':
                longs.append(symbol)
                
        if last_point >= 0.95:
            
           time.sleep(0.2)
           trend = over_daily_sma(symbol, DAYS_OVER_SMA = 5)
           if trend == 'down':
               shorts.append(symbol)            
    
    return longs, shorts
    
    







