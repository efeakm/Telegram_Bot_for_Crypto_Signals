# Telegram_Bot_for_Crypto_Signals

## OBJECTIVE<br />
The script gets crypto historical data from Binance API. Then based on a custom risk metric (I did not included my own private metric) creates long and short signals for the cryptocurrencies amongst SYMBOL_LIST. Periodically searches for signals (900 seconds or 15 min is set in the "send_message.py") and then posts those signals to a defined telegram channel if there is a signal.<br />
<br />
## download_data.py <br />
Downloads OHLC/kline data for cryptocurrencies. You can set desired timeframe by changing the INTERVAL parameter and you can choose number of candlesticks by changing the THOUSANDS_OF_CANDLES parameter (the script will return THOUSANDS_OF_CANDLES * 1000 candles).<br />
<br />
## get_signals.py<br />
A function that updates candlestick data for cryptos in SYMBOL_LIST and also returns a long and short list which includes long and short signals for defined cryptocurrencies.<br />
<br />
## send_message.py<br />
Connects to a defined telegram channel by channel_invite_link parameter and periodically searches for signals and sends them to telegram channel. You can set the period by SECONDS_FOR_EACH_PERIOD parameter which sets seconds for each period.

