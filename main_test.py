import unittest
import main
import time
import matplotlib.pyplot as plt
import matplotlib.testing.compare as pltcmp


"""
this program tests the main module for the functions waitAMinute(starttime), requestSample(), and drawHistogram(nullCoinList)

functions:
    test_waitAMinute(self): test whether the function waitAMinute(starttime) actually waits for 60 seconds.
                        By allowing 1 sec maximum execution time, waitAMinute(starttime) should delay time between 
                        60 seconds and 61 seconds
    test_requestSample(self): test whether function requestSample() can request successfully, including 200 and 503
    test_drawHistogram(self): test whether histogram is draw correctly by function drawHistogram(nullCoinList).
                        For an arbitrary nullCoinList, it compares the expected figure object and the figure object
                        returned by drawHistogram(nullCoinList)
                        For example: nullCoinList=['coin_a', 'coin_c', 'coin_b', 'coin_a', 'coin_b', 'coin_a', 'coin_a']
                        the expected histogram should be drawn as {x:'coin_a', y:4;  x:'coin_b', y: 2;  x:'coin_c', y:1} 
"""


class TestMainMethods(unittest.TestCase):

    def test_waitAMinute(self):
        print('\n***testing waitAMinute for 1 minute***')
        oldTime=time.time()
        main.waitAMinute(oldTime)
        newTime=time.time()
        self.assertGreaterEqual(newTime, oldTime+60)
        self.assertLessEqual(newTime, oldTime+61)


    def test_requestSample(self):
        print('\n***testing requestSample function***')
        response=main.requestSample()
        self.assertTrue(response.status_code==200 or response.status_code==503)


    def test_drawHistogram(self):
        print('\n***testing drawHistogram function***')
        nullCoinList=['coin_a', 'coin_c', 'coin_b', 'coin_a', 'coin_b', 'coin_a', 'coin_a']
        fig = plt.figure()
        plt.bar(['coin_a', 'coin_b', 'coin_c'], [4, 2, 1])
        plt.show()
        fig.savefig('expected.png')
        main.drawHistogram(nullCoinList).savefig('output.png')
        pltcmp.compare_images('expected.png', 'output.png', 0.001)
