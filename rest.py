'''     This file is to experiment with the Finnhub.io API      '''
import finnhub
import pandas as pd

# Specify which secret to read
SECRET_TYPE = 'sandbox_secret.txt'

# Read in secret API key
secret_file = open(SECRET_TYPE, 'r')
SECRET_API_KEY = secret_file.read()
secret_file.close()

# Setup client
fhub_client = finnhub.Client(api_key=SECRET_API_KEY)

# Get stock candle data for Apple
res = fhub_client.stock_candles('AAPL', 'D', 1590988249, 1591852249)

# Convert to Dataframe
res_pd = pd.DataFrame(res)
print(res_pd)