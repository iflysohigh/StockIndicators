import yfinance as yf
from datetime import datetime
import time

# desired stock symbol
__stockSymbol = 'TSLA'

# data import of stock symbol at a 5m interval over five days
time_interval = 5
__timeStr = str(time_interval) + 'm'

# initializing all data
data = yf.download(__stockSymbol, period='3d', interval=__timeStr, progress=False)
high = data['High']
low = data['Low']
__opn = data['Open']
close = data['Close']
volume = data['Volume']

# establishing heikin ashi
__haOpen = [__opn[0]]
__haClose = [(__opn[0] + high[0] + low[0] + close[0]) / 4]

# generates Heikin Ashi candlestick open/closes, as well as SuperTrend high and lows
for cand in range(1, len(high) - 7):
    __haOpen.append((__haOpen[cand - 1] + __haClose[cand - 1]) / 2)
    __haClose.append((__opn[cand] + high[cand] + low[cand] + close[cand]) / 4)

# polling data
def poll_data():
    # must use global first, to ensure the data is accurately updated (?) may fix the issue with non-updating data
    global data
    global high
    global low
    global __opn
    global close
    global volume

    data = yf.download(__stockSymbol, period='3d', interval=__timeStr, progress=False)
    high = data['High']
    low = data['Low']
    __opn = data['Open']
    close = data['Close']
    volume = data['Volume']

### CANDLESTICK METHODS ###

# returns open close with parentheses around it
def open_close(index):
    return '({:.2f}, {:.2f})'.format(__opn[index], close[index])

# returns percent return on the candlestick as well as a +, -, or = depending on the direction
def up_down(index):
    openC = __opn[index]
    closeC = close[index]
    percentage = 100 * (closeC - openC) / openC

    result = '{:3.2f}%'.format(percentage)

    if closeC > openC:
        return "+" + result
    elif closeC < openC:
        return result
    else:
        return "=" + result

# heikin ashi candlesticks
def candlestick(index):
    global __haOpen
    global __haClose

    # determines bearish/bullish based on Heikin Ashi candlestick calculations
    open_p = __haOpen[-1]
    close_p = __haClose[-1]

    open_now = __opn[index]
    close_now = close[index]
    high_now = high[index]
    low_now = low[index]

    # heikin ashi formulas
    # open = average of previous HEIKIN ASHI OPEN/CLOSE
    openC = round((open_p + close_p) / 2, 2)
    # close = average of current OHLC
    closeC = round((open_now + close_now + high_now + low_now) / 4, 2)

    #print(str(openC) + " " + str(closeC))
    __haOpen.append(openC)
    __haClose.append(closeC)

    # we know how bull/bear goes; if close higher, bull... etc
    if closeC > openC:
        return "BULL"
    elif closeC < openC:
        return "BEAR"
    else:
        return "NTRL"


### TIME METHODS ###
 
# sleeps for specified time-interval
def sleep():
    time.sleep(time_interval * 60)

# delays time until the minute-hand is at a multiple of 5 + 10 seconds
def time_delay():
    # take current time
    curr_time = datetime.now()
    # take minute time mod-5, subtract it from 5 to obtain the time from the next five-minute interval

    # after doing some calculations, it should be every 5 minutes + 1 (so 56, :01, :06, etc) with a 30-second addition
    mod = curr_time.minute % time_interval
    if mod < 1 or (mod == 1 and curr_time.second < 30):
        add_time = 80 - mod * 60 - curr_time.second
    else:
        add_time = (time_interval + 1 - (curr_time.minute % time_interval)) * 60 - curr_time.second + 20

    #print(add_time)

    time.sleep(add_time)

# stripping the time to only include hour and minutes
def strip_time(index):
    return str(data.index[index])[5:-9]

# returns true if we're within time frame parameters (9:35am to 16:05pm)
def searching():
    curr_time = datetime.now()
    curr_hour = int(curr_time.strftime("%H"))
    curr_min = int(curr_time.strftime("%M"))

    if ((curr_hour == 16 and curr_min < 5) and (curr_hour == 9 and curr_min > 30)) or (curr_hour > 9 and curr_hour < 16):
        return True
    return False
