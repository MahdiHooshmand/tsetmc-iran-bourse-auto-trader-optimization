import pytse_client as tse
import finpy_tse as tse2
import jdatetime
import csv
import os
from threading import Thread
import concurrent.futures
import numpy as np


class TickerInitialInfo:

    def __init__(self, ticker, group, ppe, group_ppe, ppe_standard_deviation=None, is_individual=None):
        self.ticker = ticker  # ticker name
        self.group = group  # ticker group
        self.ppe = ppe  # ticker ppe
        self.group_ppe = group_ppe  # ticker group mean ppe
        self.ppe_standard_deviation = ppe_standard_deviation  # ticker group standard deviation
        self.individual_records = None  # individual and corporate sell and buy count by date
        self.power_records = []  # [['date', 'buy_power', 'sell_power']]
        self.buy_power = np.array([])
        self.sell_power = np.array([])  # [['date', 'buy_power', 'sell_power']]
        self.vol_records = np.array([])  # [['date', 'standard_deviation']]
        self.is_individual = is_individual  # most of the trade by individuals
        self.data = []  # details trades by date
        self.asc_or_dec = np.array([])  # [['date', 'value']]  # ascending and descending tick by date
        self.gap_data = np.array([])  # [['date', 'gap']]  #  gaps by date  # values: -2 , -1 , 0 , 1 ,2
        self.ohlc = np.array([])  # [['date', 'open', 'close', 'high', 'low']]  # ohlc by date
        self.history = np.array([])

    def creat_numpy_arrays(self):
        self.history = np.array([i[0] for i in self.power_records])
        self.power_records = np.array([[i[1], i[2]] for i in self.power_records])
        self.buy_power = np.array([i[0] for i in self.power_records])
        self.sell_power = np.array([i[1] for i in self.power_records])
        self.vol_records = np.array([i[1] for i in self.vol_records])
        self.asc_or_dec = np.array([i[1] for i in self.asc_or_dec])
        self.gap_data = np.array([i[1] for i in self.gap_data])
        self.ohlc = np.array([[i[1], i[3], i[4], i[2]] for i in self.ohlc])

    def download_data(self):
        # print("downloading data for",self.ticker)
        self.data = tse.download(symbols=self.ticker, write_to_csv=False)[self.ticker]

    # noinspection PyTypeChecker
    def ascending_or_descending(self):
        self.asc_or_dec = []
        for i in range(len(self.data)):
            if float(self.data['volume'][i]) > 0:
                if 0.0 < (float(self.data['open'][i]) - float(self.data['low'][i])) < (
                        (float(self.data['close'][i]) - float(self.data['low'][i])) / 2.0):
                    self.asc_or_dec.append(
                        [self.data['date'][i].date(), 1])
                elif 0 < (float(self.data['high'][i]) - float(self.data['open'][i])) < (
                        (float(self.data['high'][i]) - float(self.data['close'][i])) / 2.0):
                    self.asc_or_dec.append(
                        [self.data['date'][i].date(), -1])
                else:
                    self.asc_or_dec.append(
                        [self.data['date'][i].date(), 0])
        self.asc_or_dec.reverse()
        if self.asc_or_dec[0][0] != self.power_records[0][0]:
            self.asc_or_dec.pop(0)

    # noinspection PyTypeChecker
    def gap(self):
        self.gap_data = []
        self.ohlc = list(self.ohlc)
        for i in range(len(self.data)):
            if float(self.data['volume'][i]) > 0:
                self.ohlc.append([self.data['date'][i],
                                  float(self.data['open'][i]),
                                  float(self.data['close'][i]),
                                  float(self.data['high'][i]),
                                  float(self.data['low'][i])])
        self.gap_data.append([self.ohlc[0][0].date(), 0])
        for i in range(1, len(self.ohlc)):
            if self.ohlc[i][1] > self.ohlc[i - 1][2] and self.ohlc[i][1] > self.ohlc[i - 1][3]:
                self.gap_data.append([self.ohlc[i][0].date(), 2])
            elif self.ohlc[i][1] > self.ohlc[i - 1][2]:
                self.gap_data.append([self.ohlc[i][0].date(), 1])
            elif self.ohlc[i][1] < self.ohlc[i - 1][2] and self.ohlc[i][1] < self.ohlc[i - 1][4]:
                self.gap_data.append([self.ohlc[i][0].date(), -2])
            elif self.ohlc[i][1] < self.ohlc[i - 1][2]:
                self.gap_data.append([self.ohlc[i][0].date(), -1])
            else:
                self.gap_data.append([self.ohlc[i][0].date(), 0])
        self.gap_data.reverse()
        self.ohlc.reverse()
        if self.gap_data[0][0] != self.power_records[0][0]:
            self.gap_data.pop(0)
            self.ohlc.pop(0)

    # noinspection PyTypeChecker
    def set_vol_info(self):
        self.vol_records = []
        # print("calculate volume standard deviation for", self.ticker)
        count = 0
        sum_vol = 0
        vol = []
        data_lst = list(i.date() for i in self.data['date'])
        for i in range(len(self.individual_records['date'])):
            if self.individual_records['date'][i].date() in data_lst:
                if float(self.data['volume'][data_lst.index(self.individual_records['date'][i].date())]) > 0:
                    vol.append([self.individual_records['date'][i].date(),
                                int(self.individual_records['individual_buy_count'][i]) +
                                int(self.individual_records['corporate_buy_count'][i])])
                    count = count + 1
                    sum_vol = sum_vol + int(self.individual_records['individual_buy_count'][i]) + int(
                        self.individual_records['corporate_buy_count'][i])
        mean = sum_vol / count
        sum_var = 0
        for i in vol:
            sum_var = sum_var + ((i[1] - mean) ** 2)
        var = sum_var / count
        standard_deviation = var ** 0.5
        for i in vol:
            self.vol_records.append([i[0], float(i[1] - mean) / standard_deviation])

    # noinspection PyTypeChecker
    def set_individual_power(self):
        self.set_individual_records()
        # print('set individual power for', self.ticker)
        data_lst = list(i.date() for i in self.data['date'])
        for i in range(len(self.individual_records["date"])):
            if self.individual_records['date'][i].date() in data_lst:
                if float(self.data['volume'][data_lst.index(self.individual_records['date'][i].date())]) > 0:
                    if (float(self.individual_records["individual_sell_count"][i]) == 0 and
                            float(self.individual_records["individual_buy_count"][i]) == 0):
                        ind = [self.individual_records["date"][i].date(),
                               0, 0]
                    elif float(self.individual_records["individual_sell_count"][i]) == 0:
                        ind = [self.individual_records["date"][i].date(),
                               float(self.individual_records["individual_buy_vol"][i]) / float(
                                   self.individual_records["individual_buy_count"][i]),
                               0]
                    elif float(self.individual_records["individual_buy_count"][i]) == 0:
                        ind = [self.individual_records["date"][i].date(),
                               0,
                               float(self.individual_records["individual_sell_vol"][i]) / float(
                                   self.individual_records["individual_sell_count"][i])]
                    else:
                        ind = [self.individual_records["date"][i].date(),
                               float(self.individual_records["individual_buy_vol"][i]) / float(
                                   self.individual_records["individual_buy_count"][i]),
                               float(self.individual_records["individual_sell_vol"][i]) / float(
                                   self.individual_records["individual_sell_count"][i])]
                    self.power_records.append(ind)

    def set_individual_records(self):
        # print("download individual records for", self.ticker)
        records_dict = tse.download_client_types_records(self.ticker, include_jdate=True)
        self.individual_records = records_dict[self.ticker]

    def is_only_individual(self, percent=50, update=False):

        def update_file(is_ind):
            file_tickers = read_initial_info_from_file()
            temp_name_lst = [str(tic.ticker) for tic in file_tickers]
            file_tickers[temp_name_lst.index(self.ticker)].is_individual = is_ind
            write_initial_info_to_file(file_tickers)

        if update:
            self.set_individual_records()
            # print("checking individual ticker =", self.ticker)
            count = 0
            corporate = 0
            for i in range(len(self.individual_records)):
                c = float(self.individual_records['individual_buy_count'][i]) + \
                    float(self.individual_records['corporate_buy_count'][i]) + \
                    float(self.individual_records['individual_sell_count'][i]) + \
                    float(self.individual_records['corporate_sell_count'][i])
                if c > 0:
                    count = count + 1
                    cor_vol = float(self.individual_records['corporate_buy_vol'][i]) + float(
                        self.individual_records['corporate_sell_vol'][i])
                    total_vol = float(self.individual_records['corporate_buy_vol'][i]) + float(
                        self.individual_records['corporate_sell_vol'][i]) + float(
                        self.individual_records['individual_buy_vol'][i]) + float(
                        self.individual_records['individual_sell_vol'][i])
                    if cor_vol > (percent / 200.0) * total_vol:
                        corporate = corporate + 1
            if corporate * 2 > count:
                self.is_individual = False
            else:
                self.is_individual = True
            update_file(self.is_individual)
            return
        elif self.is_individual is not None:
            return self.is_individual
        else:
            self.is_only_individual(update=True)

    def set_ppe_standard_deviation(self, ppe_standard_deviation):
        self.ppe_standard_deviation = ppe_standard_deviation


class Tickers:

    def __init__(self):
        self.tickers_name = bourse_tickers()
        print("number of tickers = ", len(self.tickers_name))
        self.tickers_init = set_initial_info(self.tickers_name)
        print("initiated tickers = ", len(self.tickers_init))
        self.ppe_filtered_tickers = []
        for t in self.tickers_init:
            if t.ppe is None or t.group_ppe is None:
                self.ppe_filtered_tickers.append(t)
            elif t.ppe - t.group_ppe < t.ppe_standard_deviation:
                self.ppe_filtered_tickers.append(t)
        print("number of ppe filtered tickers = ", len(self.ppe_filtered_tickers))
        self.individual_tickers = []
        for t in self.ppe_filtered_tickers:
            if t.is_only_individual():
                self.individual_tickers.append(t)
        print("individual tickers = ", len(self.individual_tickers))
        print("downloading data")
        for t in self.individual_tickers:
            t.download_data()
        print("downloading data finished")
        print('set individual power')
        for t in self.individual_tickers:
            t.set_individual_power()
        print("setting individual power finished")
        print("calculate volume standard deviation")
        for t in self.individual_tickers:
            t.set_vol_info()
        print("calculating volume standard deviation finished")
        print("calculating ascending and descending")
        for t in self.individual_tickers:
            t.ascending_or_descending()
        print("calculating ascending and descending finished")
        print("calculating gap")
        for t in self.individual_tickers:
            t.gap()
        print("calculating gap finished")
        print("checking downloaded data")
        check_downloaded_data(self.individual_tickers)
        print("creat numpy arrays")
        for t in self.individual_tickers:
            t.creat_numpy_arrays()
        print("finished")


def read_initial_info_from_file():
    file_tickers = []
    with open("files/tickers_init.csv", mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            if len(row) > 0:
                r2 = None
                r3 = None
                r4 = None
                r5 = None
                try:
                    r2 = float(row[2])
                except:
                    pass
                try:
                    r3 = float(row[3])
                except:
                    pass
                try:
                    r4 = float(row[4])
                except:
                    pass
                try:
                    r5 = int(row[5])
                    if r5 == 1:
                        r5 = True
                    elif r5 == 0:
                        r5 = None
                    elif r5 == -1:
                        r5 = False
                except:
                    pass
                file_tickers.append(TickerInitialInfo(row[0], row[1], r2, r3, r4, r5))
    return file_tickers


def write_initial_info_to_file(tickers: list[TickerInitialInfo]):
    if os.path.exists("files/tickers_init.csv"):
        os.remove("files/tickers_init.csv")
    with open("files/tickers_init.csv", mode='w', encoding='utf-8-sig') as in_file:
        wr = csv.writer(in_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for tick in tickers:
            if tick.is_individual is None:
                is_ind = 0
            elif tick.is_individual:
                is_ind = 1
            else:
                is_ind = -1
            wr.writerow([tick.ticker, tick.group, tick.ppe, tick.group_ppe, tick.ppe_standard_deviation, is_ind])


def ticker_ppe_deviation(lst: list[TickerInitialInfo]):
    for t in lst:
        t.set_ppe_standard_deviation(None)
    for ticker in lst:
        if ticker.ppe_standard_deviation is None:
            sum_var = 0
            count = 0
            for t in lst:
                if t.group == ticker.group and t.ppe is not None and ticker.group_ppe is not None:
                    sum_var = sum_var + (t.ppe - ticker.group_ppe) ** 2
                    count = count + 1
            if count > 0:
                var = sum_var / count
                standard_deviation = var ** 0.5
                for t in lst:
                    if t.group == ticker.group:
                        print('set standard deviation for', t.ticker)
                        t.set_ppe_standard_deviation(standard_deviation)


def bourse_tickers(update=False):
    if update:
        df1 = tse2.Build_Market_StockList(bourse=True, farabourse=False, payeh=False, detailed_list=True,
                                          show_progress=False, save_excel=False, save_csv=False)
        tickers = df1.index.to_list()
        with open("files/bourse_tickers.csv", mode='w', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(tickers)
        return tickers
    else:
        if os.path.exists("files/bourse_tickers.csv"):
            with open("files/bourse_tickers.csv", mode='r', encoding='utf-8-sig') as file:
                reader = csv.reader(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in reader:
                    return row
        else:
            return bourse_tickers(update=True)


def set_initial_info(tickers: list, update=False):
    def download(symbols: list):
        in_res = []
        for name in symbols:
            # print("downloading", name, "initial info")
            cond = True
            while cond:
                try:
                    tick = tse.Ticker(symbol=name)
                    in_res.append(TickerInitialInfo(name, tick.group_name, tick.p_e_ratio, tick.group_p_e_ratio))
                    cond = False
                except:
                    # print("error in download", name)
                    cond = False
        return in_res

    res = []
    if os.path.exists("files/tickers_init.csv"):
        file_tickers = read_initial_info_from_file()
    else:
        res = download(tickers)
        ticker_ppe_deviation(res)
        write_initial_info_to_file(res)
        return res
    temp_name_lst = [str(tic.ticker) for tic in file_tickers]
    new_tickers = []
    if update:
        res = download(tickers)
        ticker_ppe_deviation(res)
        for tic in res:
            if tic.ticker in temp_name_lst:
                file_tickers.pop(temp_name_lst.index(tic.ticker))
            file_tickers.append(tic)
        write_initial_info_to_file(file_tickers)
        return res
    else:
        for tic in tickers:
            if tic in temp_name_lst:
                res.append(file_tickers[temp_name_lst.index(tic)])
            else:
                new_tickers.append(tic)
        temp_res = download(new_tickers)
        ticker_ppe_deviation(temp_res)
        for tic in temp_res:
            res.append(tic)
            file_tickers.append(tic)
        write_initial_info_to_file(file_tickers)
        return res


def check_downloaded_data(tickers: list[TickerInitialInfo]):
    for tic in tickers:
        for i in range(len(tic.power_records)):
            if tic.power_records[i][0] != tic.vol_records[i][0] != tic.gap_data[i][0] != tic.asc_or_dec[i][0]:
                print(tic.ticker, i)
                break


def op_task2(ticker: TickerInitialInfo,
             buy_vol: float,
             buy_power_ratio: float,
             sell_vol: float,
             sell_power_ratio: float,
             stop_loss: float,
             take_profit: float,
             asc: int,
             b_gap: int,
             des: int,
             s_gap: int) -> None:
    profit = 0.0
    price = 0.0
    buy_array = np.less(ticker.vol_records, buy_vol)
    buy_array = np.logical_or(np.equal(ticker.sell_power, 0.0),
                              np.logical_and(np.greater(ticker.buy_power / ticker.sell_power, buy_power_ratio),
                                             buy_array))
    buy_array = np.logical_and(np.greater_equal(ticker.asc_or_dec, asc), buy_array)
    buy_array = np.logical_and(np.greater_equal(np.roll(ticker.gap_data, 1), b_gap), buy_array)
    sell_array = np.greater(ticker.vol_records, sell_vol)
    sell_array = np.logical_and(np.logical_or(np.equal(ticker.buy_power, 0.0),
                                              np.greater(ticker.sell_power / ticker.buy_power, sell_power_ratio)),
                                sell_array)
    sell_array = np.logical_and(np.less_equal(ticker.asc_or_dec, des), sell_array)
    sell_array = np.logical_and(np.less_equal(np.roll(ticker.gap_data, 1), s_gap), sell_array)
    for i in np.arange(len(ticker.vol_records) - 1, 0, -1):
        if price == 0.0 and buy_array[i]:
            price = ticker.ohlc[i - 1][0]
        if price != 0.0 and ticker.ohlc[i - 1][2] <= price * ((100 - stop_loss) / 100.0):
            price = 0.0
            profit = profit - stop_loss - 1.23
        if price != 0.0 and ticker.ohlc[i - 1][1] >= price * ((100 + take_profit) / 100.0):
            price = 0.0
            profit = profit + take_profit - 1.23
        if price != 0.0 and sell_array[i]:
            profit = profit + (((ticker.ohlc[i - 1][0] - price) / price) * 100) - 1.23
            price = 0.0


def op_task(ticker: TickerInitialInfo,
            buy_vol: float,
            buy_power_ratio: float,
            sell_vol: float,
            sell_power_ratio: float,
            stop_loss: float,
            take_profit: float,
            asc: int,
            b_gap: int,
            des: int,
            s_gap: int) -> float:
    profit = 0.0
    price = 0.0
    for i in np.arange(len(ticker.vol_records) - 1, 0, -1):
        if price == 0.0:
            if ticker.vol_records[i] > buy_vol:
                temp_con1 = False
                if ticker.power_records[i][1] == 0:
                    temp_con1 = True
                elif ticker.power_records[i][0] / ticker.power_records[i][1] > buy_power_ratio:
                    temp_con1 = True
                if temp_con1:
                    if ticker.asc_or_dec[i] >= asc:
                        if ticker.gap_data[i - 1] >= b_gap:
                            price = ticker.ohlc[i - 1][0]
        if price != 0.0:
            if ticker.ohlc[i - 1][2] <= price * ((100 - stop_loss) / 100.0):
                price = 0.0
                profit = profit - stop_loss - 1.23
        if price != 0.0:
            if ticker.ohlc[i - 1][1] >= price * ((100 + take_profit) / 100.0):
                price = 0.0
                profit = profit + take_profit - 1.23
        if price != 0.0:
            if ticker.vol_records[i] > sell_vol:
                temp_con2 = False
                if ticker.power_records[i][0] == 0:
                    temp_con2 = True
                elif ticker.power_records[i][1] / ticker.power_records[i][0] > sell_power_ratio:
                    temp_con2 = True
                if temp_con2:
                    if ticker.asc_or_dec[i] <= des:
                        if ticker.gap_data[i - 1] <= s_gap:
                            profit = profit + (((ticker.ohlc[i - 1][0] - price) / price) * 100) - 1.23
                            price = 0.0

    return profit


def cpu(ticker: TickerInitialInfo):
    res = []
    for bv in np.array([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]):
        for bp in np.array([0.0, 0.5, 1.0, 1.5]):
            for asc in np.array([-1, 0, 1, 2]):
                for sv in np.array([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]):
                    for b_gap in np.array([-2, -1, 0, 1, 2]):
                        for sp in np.array([0.0, 0.5, 1.0, 1.5]):
                            for sl in np.array([5.0, 10.0, 15.0]):
                                for tp in np.array([5.0, 10.0, 15.0, 20.0]):
                                    for des in np.array([-2, -1, 0, 1, 2]):
                                        for s_gap in np.array([-2, -1, 0, 1, 2]):
                                            res.append(op_task(ticker, bv, bp, sv, sp, sl, tp, asc, b_gap, des, s_gap))
    return res
