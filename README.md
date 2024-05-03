## NOTE: StockIndicators is currently broken due to yfinance being depreciated.

# StockIndicators (Broken)
Replication of stock indicators used in day-to-day trading on a 5-minute candlestick chart. Includes Heikin Ashi trends, VWAP calculations, and SuperTrend bullish &amp; bearish turns, 

The intention of this program is to emulate stock indicators as a side project. With a primary goal of breaking into quant trading and research, I have honed my skills by manually creating stock indicators such as these. By creating these types of programs, I hope to learn more about coding financially relevant projects. My end-goal is to utilize AI (ChatGPT and others) to allow everyday people like myself to achieve financial freedom. 

In a world that ties happiness to money, allowing normal people to achieve financial freedom provides a sense of accomplishment and freedom. As the youngest child of a middle-class family, I have seen the ups and downs of financial institutions. My parents both worked in accounting but struggled to maintain financial stability. By creating programs like these, I hope to provide useful tools to experienced traders in hopes of creating a net-positive learning cycle: I learn from the traders and the traders learn from me. 

## Data Polling
All data was polled from Yahoo Finance. Because of delayed information provided by Yahoo Finance, I am unable to provide up-to-date information. However, I have precisely timed my code to allow candlesticks to be updated exactly 80 seconds after close - this was determined using manual trial and error processes. 

## Stock Choice
I chose Tesla (Stock Ticker: TSLA) as the stock of choice due to its volatile state and interesting background. Tesla stands at the forefront of electric vehicle (EV) innovation with private and government deals in place. Combined with Elon Musk's social media presence, Tesla has a stark balance between social media, technological advances, and government influence. 

## Indicators
There are currently four indicators in place: VWAP (volume-weighted average price), SuperTrend, ATR (average true range), and Heikin Ashi. 

### Heikin Ashi
Heikin Ashi allows us to better determine price movement trends in basic terms: upwards or downwards. The Heikin Ashi (HA) opening is calculated by taking the average of the stock's previous Heikin Ashi open and close. The HA closing is calculated by average the stock's *actual* OHLC (open, high, low, close). This process repeats. 

To calculate prior Heikin Ashi open and closes, we begin by using data up to five days prior. This allows the program to have accuracy similar to trading platforms such as WeBull or TradingView, who poll decades of data. 

### ATR (Average True Range)
Similar to Heikin Ashi, average true range (ATR) is calculated using past data. However, we limit it to a period of 14 - that is, 13 candlesticks prior to the one we are calculated. This is how an 'average' true range is calculated. To calculate individual true range (TR), we take the max between three different values: 1) high - low, 2) absolute value of high - previous close, and 3) absolute value of low - previous high. The max of these three values is the true range of a candlestick. My ATR calculation is ATR-14, meaning the current candlestick is calculated using the current TR in addition to the prior 13 candlesticks' true ranges.

### SuperTrend
To calculate SuperTrend, we utilize ATR-10. That is, the current candlestick TR in addition to the last 9 candlesticks' true ranges. We utilize a multiplier of 3, which is the default (SuperTrend[10, 3]). The calculations are as follows: 1) we generate high and low value limits, and 2) should the stock price pass the low value - then we enter a bearish downtrend, followed by 3) should the stock price surprass the high value - then we enter a bullish downtrend. 

We first create an average of the high and low of each candlestick, and call it AVG.
High ST is calculated as follows: AVG + (ATR * 3)
Low ST is calculated as follows: AVG - (ATR * 3)

We initialize to a 0-trend, meaning we are neutral - neither bullish or bearish. Following, we can enter a bullish or bearish SuperTrend by breaking a low or high. However, it becomes a little more tricky once we are in an up or downtrend. 

In the instance we are in an uptrend and make a lower low, we change the low limit to the previous value. Similarly, if we are in a downtrend and make a higher high, we change the high limit to the prior value. Anything else, we maintain. This ensures that a downtrend has lower and lower highs to break, and that an uptrend has higher and higher lows to break - but we never have a downtrend with higher highs, nor do we have an uptrend with lower lows. Economically, we would never break out of an up or downtrend if this were the case. 

### VWAP (Volume-Weighted Average Price)
Volume weighted average price (VWAP) is calculated by taking the average price of high, low, close - and multiply by the volume. The equation is as follows:
VWAP = ((low + high + close) / 3) * volume. This indicator provides the average price over a period of time; until volume or price action increases, we will stay below VWAP (and likely a downtrend). Similarly, until volume or price action decreases, we will stay above VWAP (and likely an uptrend). A key indicator is bouncing or rejecting off of VWAP, so this proves to be a useful indicator for volatile stocks like TSLA. 
