# Covalent-Take-Home-Exercise
This is for a take home exercise created by :sparkles: Covalent :sparkles: (https://www.covalenthq.com)


The main program requests an API from https://api.covalenthq.com/v1/pricing/tickers/ each minute.
At the end of each hour, it draws a histogram of the currencies that has null address bug and its frequency of that bug appears


To run and test this code:
```bash
python3 main.py
python3 -m unittest
```

**functions:**
* printTime(): print current time in the format of hour:minute:second
* waitAMinute(starttime): sleep until the next minute begins. Each minute is relative to the starttime
* requestSample(): request an API from https://api.covalenthq.com/v1/pricing/tickers/
* drawHistogram(nullCoinList): This function draws a histogram of the currencies that has null address bug and its frequency of that bug appears
* alwaysLoop(): infinite loop. Each minute it requests API from https://api.covalenthq.com/v1/pricing/tickers/ if a response is success (200), it checks for which currency has the null address bug and append its symbol into the nullCoinList a currency may be appended multiple times if it has the bug in multiple responses at the end of each hour (60 samples), it draws a histogram 
* main: call alwaysLoop()
    
**variables:**
* starttime: the time when this program starts running
* response: API response from https://api.covalenthq.com/v1/pricing/tickers/
* nullCoinList: a list of strings, which are the contract_ticker_symbol of the currencies that has null contract_address bug. The number of occurrence of a currency in this list is the frequency bug appears for that currency
* sampleCount: keep track of how many samples successfully received. Reset after 60 samples (about an hour)

---
### Unit Test
The unit test tests three functions in the main module: *waitAMinute(starttime)*, *requestSample()*, and *drawHistogram(nullCoinList)*

The test_functions are:
* test_waitAMinute(self): test whether the function waitAMinute(starttime) actually waits for 60 seconds. By allowing 1 sec maximum execution time, waitAMinute(starttime) should delay time between 60 seconds and 61 seconds
* test_requestSample(self): test whether function requestSample() can request successfully, including 200 and 503
* test_drawHistogram(self): test whether histogram is draw correctly by function drawHistogram(nullCoinList). For an arbitrary nullCoinList, it compares the expected figure object and the figure object returned by drawHistogram(nullCoinList). For example: 
```python
nullCoinList=['coin_a', 'coin_c', 'coin_b', 'coin_a', 'coin_b', 'coin_a', 'coin_a']
```
the expected result should look like 

symbol | bug frequency
------------ | -------------
'coin_a' | 4
'coin_b' | 2
'coin_c' | 1

The test results:
```bash
$python -m unittest

***testing drawHistogram function***
.
***testing requestSample function***
status code: 200
.
***testing waitAMinute for 1 minute***
.
----------------------------------------------------------------------
Ran 3 tests in 66.286s

OK

```

test output histogram:

<img src="https://github.com/ZzzzHui/Covalent-Take-Home-Exercise/blob/main/test_output.png" height="50%" width="50%">

expected histogram:

<img src="https://github.com/ZzzzHui/Covalent-Take-Home-Exercise/blob/main/text_expected.png" height="50%" width="50%">
