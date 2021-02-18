import time
import requests
from collections import Counter
import matplotlib.pyplot as plt

"""
This program requests an API from https://api.covalenthq.com/v1/pricing/tickers/ each minute.
At the end of each hour, it draws a histogram of the currencies that has null address bug and its frequency of that bug appears

functions:
    printTime(): print current time in the format of hour:minute:second
    waitAMinute(starttime): sleep until the next minute begins. Each minute is relative to the starttime
    requestSample(): request an API from https://api.covalenthq.com/v1/pricing/tickers/
    drawHistogram(nullCoinList): This function draws a histogram of the currencies that has null address bug and its 
                                frequency of that bug appears
    alwaysLoop(): infinite loop. Each minute it requests API from https://api.covalenthq.com/v1/pricing/tickers/
            if a response is success (200), it checks for which currency has the null address bug and append its symbol into the nullCoinList
            a currency may be appended multiple times if it has the bug in multiple responses
            at the end of each hour (60 samples), it draws a histogram 
    main: call alwaysLoop()
    
variables:
    starttime: the time when this program starts running
    response: API response from https://api.covalenthq.com/v1/pricing/tickers/
    nullCoinList: a list of strings, which are the contract_ticker_symbol of the currencies that has null
                contract_address bug. The occurrence in this list is the frequency bug appears for that currency
    sampleCount: keep track of how many samples successfully received. Reset after 60 samples (roughly an hour)
    
"""


def printTime():
    """
    print current time in the format of hour:minute:second
    """
    t = time.localtime()
    current_time = time.strftime("\n%H:%M:%S", t)
    print(current_time)


def waitAMinute(starttime):
    """
    sleep until the next minute begins.
    this function does not actually sleep for 60s, considering the delays caused by code executions
    :param starttime: the time when this program starts running
    """
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))  # adjusted for the time delayed by execution


def requestSample():
    """
    This function requests an API from https://api.covalenthq.com/v1/pricing/tickers/
    response status code will also be printed
    :return: response from the API at the endpoint  v1/pricing/tickers/
    """
    # curl https://api.covalenthq.com/v1/pricing/tickers/ -u ckey_ee1e0e4939bc46aca8aba655bf5:
    response = requests.get('https://api.covalenthq.com/v1/pricing/tickers/',
                            auth=('ckey_ee1e0e4939bc46aca8aba655bf5', ''))
    print('status code: ' + str(response.status_code))
    return response


def drawHistogram(nullCoinList):
    """
    This function draws a histogram of the currencies that has null address bug and the frequency of that bug appears
    :param nullCoinList: a list of strings, which are the contract_ticker_symbol of the currencies that has null
                        contract_address bug. The occurrence in this list is the frequency bug appears for that currency
    :return: the fig object of the histogram
    """
    x = []  # x labels
    y = []  # y labels
    for item in Counter(nullCoinList).most_common():
        x.append(item[0])
        y.append(item[1])
    fig = plt.figure()
    plt.bar(x, y)
    plt.show()
    return fig



def alwaysLoop():
    """
    this function is in an infinite loop. Each minute it requests API from https://api.covalenthq.com/v1/pricing/tickers/
    if a response is success (200), it checks for which currency has the null address bug and append its symbol into the nullCoinList
    a currency may be appended multiple times if it has the bug in multiple responses
    at the end of each hour (60 samples), it draws a histogram
    """
    starttime = time.time()
    nullCoinList = []  # reset after 60 samples
    sampleCount = 0  # reset after 60 samples
    while True:
        printTime()
        response = requestSample()
        if response.status_code == 200:
            sampleCount += 1
            for item in response.json()['data']['items']:
                print(item)  # comment out this line if don't need printing
                if item['contract_address'] is None:
                    nullCoinList.append(item['contract_ticker_symbol'])
        else:
            print('request unsuccessful.')

        # if 60 samples obtained
        if sampleCount >= 60:
            drawHistogram(nullCoinList)
            # reset variables
            nullCoinList = []
            sampleCount = 0

        # wait a minute (take into account the time delayed by execution)
        waitAMinute(starttime)


if __name__ == '__main__':
    alwaysLoop()
