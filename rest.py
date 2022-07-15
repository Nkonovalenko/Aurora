'''     This file is to experiment with the Finnhub.io API      '''
import finnhub
import pandas as pd
from datetime import datetime
import numpy as numpy
import matplotlib as mpl
import matplotlib.pyplot as plt
from math import floor

# Specify which secret to read
SECRET_TYPE = 'sandbox_secret.txt'

# Read in secret API key
secret_file = open(SECRET_TYPE, 'r')
SECRET_API_KEY = secret_file.read()
secret_file.close()

# Setup client
fhub_client = finnhub.Client(api_key=SECRET_API_KEY)

# Choose ticker
ticker = 'APPLE'

# Get stock candle data for Apple
res = fhub_client.stock_candles(ticker, 'D', 1591100000, 1593572249)

# Count the number of results
num_res = len(res['c'])

# Convert to list of dictionaries
data = []
for i in range(num_res):
    candle = {}
    candle['close'] = res['c'][i]
    candle['high'] = res['h'][i]
    candle['low'] = res['l'][i]
    candle['open'] = res['o'][i] 
    candle['date'] = datetime.fromtimestamp(res['t'][i])
    candle['index'] = i
    res['t'][i] = candle['date'] 
    data.append(candle)

# Convert to Dataframe to visualize
res_pd = pd.DataFrame(res)

print(res_pd)


# Draw candlestick
def draw_candlestick(axis, data, color_up, color_down):
    # Check for direction of close
    if data['close'] > data['open']:
        color = color_up
    else:
        color = color_down

    # Plot candle wick
    axis.plot([data['date'].day, data['date'].day], [data['low'], data['high']], linewidth=1.5, color='black', solid_capstyle='round', zorder=2)

    # Draw the candle body
    rect = mpl.patches.Rectangle((data['date'].day - 0.25, data['open']), 0.5, (data['close'] - data['open']), facecolor=color, edgecolor='black', linewidth=1.5, zorder=3)
    axis.add_patch(rect)

    return axis

# Draw all candlesticks
def draw_all_candlesticks(axis, data, color_up='green', color_down='red'):
    for day in range(len(data)):
        axis = draw_candlestick(axis, data[day], color_up, color_down)
    return axis

# Draw a point(axis, data)
def draw_sma(axis, data, color='purple'):
    for i, datum in enumerate(data):
        if i > 2:
            axis.plot((i-1, i), (int(data[i-1]), int(datum)), linewidth=1.5, color=color, zorder=2)
    return axis

# Get SMA
sma = fhub_client.technical_indicator(symbol=ticker, resolution='D', _from=1591100000, to=1593572249, indicator='sma', indicator_fields={"timeperiod": 1})

# Create candlestick chart
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.size'] = 18
mpl.rcParams['axes.linewidth'] = 0
mpl.rcParams['axes.facecolor'] = '#ededed'
mpl.rcParams['xtick.major.size'] = 0
mpl.rcParams['xtick.major.pad'] = 10
mpl.rcParams['ytick.major.size'] = 0
mpl.rcParams['ytick.major.pad'] = 10

# Create figure and axes
fig = plt.figure(figsize=(10, 5), facecolor='white')
ax = fig.add_subplot(111)

# Grid lines
ax.grid(linestyle='-', linewidth=2, color='white', zorder=1)

# Draw candlesticks
ax = draw_all_candlesticks(ax, data)

# Draw the SMA
ax = draw_sma(ax, sma['sma'])

# Add dollar signs
formatter = mpl.ticker.FormatStrFormatter('$%.2f')
ax.yaxis.set_major_formatter(formatter)

# Append ticker symbol
ax.text(0, 1.05, ticker, va='baseline', ha='left', size=30, transform=ax.transAxes)

# Save the plot
fig.savefig('stock_plot.png')