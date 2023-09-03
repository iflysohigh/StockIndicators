import indicators as id
import stockdata as sd


### PRINTER METHODS ###

# prints formatted time, atr, movement %, open/close, and heikin ashi bullish/bearish
def printer(val=-2):
    print('{:<14s}{:>10.2f}{:>13s}{:^30s}{:>6.2f}{:^18s}{:^7d}{:>12.2f}'.format(sd.strip_time(val), id.getATR(val), 
                                                                       sd.up_down(val), sd.open_close(val), id.getVWAP(val), 
                                                                       sd.candlestick(val), id.getSuperTrend(val), id.getSuperTrendPassVal(val)))

# prints the header
def print_header():
    print('-'*115)
    print('{:<14s}{:>10s}{:>13s}{:^30s}{:>6s}{:^18s}{:^7s}{:>12s}'.format("TIME", "ATR", "MOVE", 
                                                                     "OPEN/CLOSE", "VWAP", 
                                                                     "HEIKIN", "SUPERTR", "ST S/R"))
    print('-'*115)

### MAIN METHOD ###

def main():
    atr_threshold = 0.6 # Change this to the desired ATR threshold
    searching = True # determines if we're searching for a trend
    count = 0 # determines how many candles left in trend
    current = id.current
    ending = -1

    isSearching = sd.searching()

    if not isSearching:
        ending = 0

    sd.poll_data()
    print_header()

    # printing the last several candlestick values prior to commencing the current
    for candle in range(-7, ending):
        printer(candle)

    # delay time until the next candlestick is completed
    if isSearching:
        sd.time_delay()

    while isSearching:
        # poll data, calculate atr
        sd.poll_data()
        latest_atr = id.getATR()
        inTrend = False
 
        # if below threshold, begin the count
        if latest_atr < atr_threshold:
            # if already counting, continue trend; else, start at count 3
            if count:
                count += 1
            else:
                print('{:-^44}'.format("TREND STARTED"))
                inTrend = True
                count = 3
        
        if inTrend:
            count -= 1
        printer(current)

        # if we just finished a trend
        if inTrend and count == 0:
            # we begin searching again
            inTrend = False
            print('{:-^44}'.format("TREND COMPLETED"))
            print("Searching for next low-ATR...")

        # time interval is 5 minutes; time.sleep() works in seconds, so we multiply by 60
        sd.sleep()

if __name__ == "__main__":
    main()
