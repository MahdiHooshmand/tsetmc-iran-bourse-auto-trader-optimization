import TSE
import numpy as np
import csv

tickers = TSE.read_tickers_from_files(378)

TSE.change_tickers(tickers)
c = 0
for is_individual in np.array([True, False]):
    for buy_vol in np.array([1, 2, 3, 4, 5, 6]):
        for buy_pow in np.array([1, 2, 3]):
            for asc in np.array([True, False]):
                for buy_gap in np.array([-2, -1, 0, 1, 2]):
                    for sell_vol in np.array([1, 2, 3, 4, 5, 6]):
                        for sell_pow in np.array([1, 2, 3]):
                            for des in np.array([True, False]):
                                for sell_gap in np.array([-2, -1, 0, 1, 2]):
                                    for days in np.array([5, 10, 15, 20, 25, 30]):
                                        for tp in np.array([10, 20, 30, 40, 50]):
                                            for sl in np.array([10, 20, 30]):
                                                print(c)
                                                TSE.check(tickers, is_individual=is_individual, buy_vol=buy_vol,
                                                          buy_pow=buy_pow, asc=asc, buy_gap=buy_gap, sell_vol=sell_vol,
                                                          sell_pow=sell_pow, des=des, sell_gap=sell_gap, days=days,
                                                          tp=tp,
                                                          sl=sl)
                                                c = c + 1

