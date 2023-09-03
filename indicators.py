import stockdata as sd
import pytz

current = -2
__previous = -3

### Calculation Methods ### 

# calculate tr based on input
def calculate_tr(curr_h, curr_l, prev_cl):
    return round(max(curr_h - curr_l, abs(curr_h - prev_cl), abs(curr_l - prev_cl)), 4)

# calculate tp (typical price) based on input
def calculate_tp(curr_h, curr_l, prev_cl):
    return round((curr_h + curr_l + prev_cl) / 3, 4)


### Get Methods ### 

# calculate atr provided last 13 candlesticks' true ranges
def getATR(index=current, num_candles=14):
    atr = 0

    # we take into account the former *num* candlesticks
    for candles in range(index - (num_candles - 1), index + 1):
        curr_h = sd.high[candles]
        curr_l = sd.low[candles]
        prev_cl = sd.close[candles - 1]

        atr += calculate_tr(curr_h, curr_l, prev_cl)

    atr /= num_candles
    # subtract to adjust
    return atr#- 0.003

# establishing supertrend
__multiplier = 3
__period = 10
__highLow = (sd.high + sd.low) / 2

__highST = [0 for i in range(__period - 1)]
__lowST = [0 for i in range(__period - 1)]
__strend = [0 for i in range(__period - 1)]

for cand in range(__period - 1, len(sd.high) - 7):
    __highST.append(__highLow[cand] + getATR(index=cand, num_candles=__period) * __multiplier)
    __lowST.append(__highLow[cand] - getATR(index=cand, num_candles=__period) * __multiplier)

    # we check for breaks 
    if sd.close[cand] > __highST[cand - 1]:
        __strend.append(1)
    elif sd.close[cand] < __lowST[cand - 1]:
        __strend.append(-1)
    else:
        __strend.append(__strend[-1])

    # check if we are in an uptrend/downtrend from previous
    trending = __strend[-1]
    prev_trend = __strend[-2]

    if prev_trend == trending:
        # if we are in an uptrend, then check to see if new low is lower compared to last time; we set it to the previous value
        if trending > 0 and __lowST[-1] < __lowST[-2]:
                __lowST[-1] = __lowST[-2]
        # same with downtrend; if making higher highs, set it to previous value
        elif trending < 0 and __highST[-1] > __highST[-2]:
                __highST[-1] = __highST[-2]

    #b = cand
    #print('{:>5s} {:^5d} {:<5.2f} {:<5.2f} {:<5.2f} {:5.2f} {:5.2f}'.format(sd.strip_time(b), __strend[b], sd.close[b], __lowST[b], __highST[b], getATR(b), __highLow[b]))

# calculate supertrend based on atr and multipliers
# we assume a period of 10 and a multipler of 3
def getSuperTrend(index):
    global __highLow
    global __highST
    global __lowST
    global __strend

    __highLow = (sd.high + sd.low) / 2

    __highST.append(round(__highLow[index] + getATR(index=index, num_candles=__period) * __multiplier, 2))
    __lowST.append(round(__highLow[index] - getATR(index=index, num_candles=__period) * __multiplier, 2))

    #print(str(__highST[-1]) + " " + str(__lowST[-1]))

    # check if we are in an uptrend/downtrend from previous

    # we check for breaks 
    if round(sd.close[index], 2) > round(__highST[index - 1], 2):
        __strend.append(1)
    elif round(sd.close[index], 2) < round(__lowST[index - 1], 2):
        __strend.append(-1)
    else:
        __strend.append(__strend[index])

    trending = __strend[-1]
    prev_trend = __strend[-2]

    # if the trend has not changed, then update them
    if prev_trend == trending:
        # if we are in an uptrend, then check to see if new low is lower compared to last time; we set it to the previous value
        if trending > 0 and __lowST[-1] < __lowST[-2]:
                __lowST[-1] = __lowST[-2]
        # same with downtrend; if making higher highs, set it to previous value
        elif trending < 0 and __highST[-1] > __highST[-2]:
                __highST[-1] = __highST[-2]

    #b = index
    #print('{:^5d} {:<5.2f} {:<5.2f} {:<5.2f}'.format(__strend[b], sd.close[b], __lowST[b - 1], __highST[b - 1]))
    
    return __strend[index]

# returns the value to beat above/below
def getSuperTrendPassVal(index):
    global __strend
    if __strend[index] > 0:
        return __lowST[index]
    else:
        return __highST[index]


# calculate vwap on the daily chart
def getVWAP(index = -1):
    earliest_index = index
    current_date = sd.strip_time(index)
    vwap = ((sd.low[index] + sd.high[index] + sd.close[index]) / 3) * sd.volume[index]
    vol = sd.volume[index]

    while current_date[:-6] == sd.strip_time(earliest_index - 1)[:-6]:
        earliest_index -= 1

    for candlesticks in range(earliest_index, index):
        typPrice = (sd.low[candlesticks] + sd.high[candlesticks] + sd.close[candlesticks]) / 3
        vwap += typPrice * sd.volume[candlesticks]
        vol += sd.volume[candlesticks]

    return round(vwap / vol, 2) - .05
