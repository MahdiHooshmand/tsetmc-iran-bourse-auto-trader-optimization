import pytse_client as tse
import finpy_tse as tse2
import numpy as np
import csv
import json




class TickerInfo:

    def __init__(self, ticker, group, ppe, group_ppe,
                 vol, op, hp, lp, cp, cpm1, lpm1, hpm1,
                 mean_vol, vol_std,
                 bc, bv, sc, sv,
                 history: TickerHistory):
        self.ticker = ticker
        self.group = group
        self.ppe = ppe
        self.group_ppe = group_ppe
        self.vol = vol
        self.open = op
        self.high = hp
        self.low = lp
        self.close = cp
        self.yesterday_close = cpm1
        self.yesterday_low = lpm1
        self.yesterday_high = hpm1
        self.mean_vol = mean_vol
        self.vol_std = vol_std
        self.buy_count = bc
        self.buy_vol = bv
        self.sell_count = sc
        self.sell_vol = sv
        self.history = history
        self.start = 0


def write_tickers_to_file(tickers: list[TickerInfo], file_dir):
    for i in range(len(tickers)):
        with open(file_dir + str(i) + '.csv', mode='x', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([str(tickers[i].ticker), str(tickers[i].group), str(tickers[i].ppe),
                             str(tickers[i].group_ppe), str(tickers[i].vol), str(tickers[i].open), str(tickers[i].high),
                             str(tickers[i].low), str(tickers[i].close), str(tickers[i].yesterday_close),
                             str(tickers[i].yesterday_low), str(tickers[i].yesterday_high), str(tickers[i].mean_vol),
                             str(tickers[i].vol_std), str(tickers[i].buy_vol), str(tickers[i].buy_count),
                             str(tickers[i].sell_vol), str(tickers[i].sell_count)])
            for j in range(len(tickers[i].history.date)):
                writer.writerow([str(tickers[i].history.date[j]), str(tickers[i].history.open[j]),
                                 str(tickers[i].history.high[j]), str(tickers[i].history.low[j]),
                                 str(tickers[i].history.close[j]), str(tickers[i].history.vol[j]),
                                 str(tickers[i].history.buy_vol[j]), str(tickers[i].history.buy_count[j]),
                                 str(tickers[i].history.sell_vol[j]), str(tickers[i].history.sell_count[j])])


def read_tickers_from_files(count):
    tickers = []
    for i in range(count):
        with open('t1/' + str(i) + '.csv', mode='r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            rows = []
            for row in reader:
                rows.append(row)
            first_row: list = rows.pop(0)
            for j in range(len(first_row)):
                if first_row[j] == 'None':
                    first_row[j] = -1
            tic = TickerInfo(first_row[0], first_row[1], float(first_row[2]), float(first_row[3]),
                             int(float(first_row[4])), int(float(first_row[5])), int(float(first_row[6])),
                             int(float(first_row[7])), int(float(first_row[8])), int(float(first_row[9])),
                             int(float(first_row[10])), int(float(first_row[11])), float(first_row[12]),
                             float(first_row[13]), int(float(first_row[15])), int(float(first_row[14])),
                             int(float(first_row[17])), int(float(first_row[16])), None)
            d = []
            o = []
            h = []
            l = []
            c = []
            v = []
            bv = []
            bc = []
            sv = []
            sc = []
            for row in rows:
                d.append(int(float(row[0])))
                o.append(int(float(row[1])))
                h.append(int(float(row[2])))
                l.append(int(float(row[3])))
                c.append(int(float(row[4])))
                v.append(int(float(row[5])))
                bv.append(int(float(row[6])))
                bc.append(int(float(row[7])))
                sv.append(int(float(row[8])))
                sc.append(int(float(row[9])))
            tic.history = TickerHistory(np.array(d), np.array(o), np.array(h), np.array(l), np.array(c), np.array(v),
                                        np.array(bc), np.array(bv), np.array(sc), np.array(sv))
            tickers.append(tic)
    return tickers


def bourse_tickers():
    df1 = tse2.Build_Market_StockList(bourse=True, farabourse=False, payeh=False, detailed_list=True,
                                      show_progress=False, save_excel=False, save_csv=False)
    tickers = df1.index.to_list()
    print(len(tickers))
    return tickers


def download(symbols: list):
    tick_res = []
    for name in symbols:
        print(name)
        try:
            tick = tse.Ticker(symbol=name)
            dates = np.array([i.year * 10000 + i.month * 100 + i.day for i in tick.history['date']])
            dates2 = [int(i) for i in tick.client_types['date']]
            bc2 = tick.client_types['individual_buy_count'].to_numpy()
            bv2 = tick.client_types['individual_buy_vol'].to_numpy()
            sc2 = tick.client_types['individual_sell_count'].to_numpy()
            sv2 = tick.client_types['individual_sell_vol'].to_numpy()
            bc = []
            bv = []
            sc = []
            sv = []
            for i in dates:
                if i in dates2:
                    bc.append(int(bc2[dates2.index(i)]))
                    bv.append(int(bv2[dates2.index(i)]))
                    sc.append(int(sc2[dates2.index(i)]))
                    sv.append(int(sv2[dates2.index(i)]))
                else:
                    bc.append(-1)
                    bv.append(-1)
                    sc.append(-1)
                    sv.append(-1)
            tick_res.append(TickerInfo(
                name,
                tick.group_name,
                tick.p_e_ratio,
                tick.group_p_e_ratio,
                tick.volume,
                tick.open_price,
                tick.high_price,
                tick.low_price,
                tick.last_price,
                tick.history['close'].get(tick.history['close'].count() - 2),
                tick.history['low'].get(tick.history['low'].count() - 2),
                tick.history['high'].get(tick.history['high'].count() - 2),
                tick.history['volume'].mean(),
                tick.history['volume'].std(),
                bc[-1],
                bv[-1],
                sc[-1],
                sv[-1],
                TickerHistory(
                    np.array([i.year * 10000 + i.month * 100 + i.day for i in tick.history['date']]),
                    tick.history['open'].to_numpy(),
                    tick.history['high'].to_numpy(),
                    tick.history['low'].to_numpy(),
                    tick.history['close'].to_numpy(),
                    tick.history['volume'].to_numpy(),
                    np.array(bc),
                    np.array(bv),
                    np.array(sc),
                    np.array(sv)
                )

            )
            )
        except:
            print("error in download", name)
    print(len(tick_res))
    return tick_res


good = []
max_pr = 0.0


def check(ticks: list[TickerInfo], is_individual: bool,
          buy_vol, buy_pow, asc, buy_gap,
          sell_vol, sell_pow, des, sell_gap,
          days, tp, sl):
    global max_pr
    global good
    d_type = [('start', int), ('end', int), ('profit', float)]
    values = []
    profit = 0.0
    # file_name = ''
    # if is_individual:
    #     file_name = file_name + 'I'
    # else:
    #     file_name = file_name + 'C'
    # file_name = file_name + 'bv' + str(buy_vol)
    # file_name = file_name + 'bp' + str(buy_pow)
    # file_name = file_name + 'bg' + str(buy_gap)
    # if asc:
    #     file_name = file_name + 'Tasc'
    # else:
    #     file_name = file_name + 'Fasc'
    # file_name = file_name + 'sv' + str(sell_vol)
    # file_name = file_name + 'sp' + str(sell_pow)
    # file_name = file_name + 'sg' + str(sell_gap)
    # if des:
    #     file_name = file_name + 'Tdes'
    # else:
    #     file_name = file_name + 'Fdes'
    # file_name = file_name + 'days' + str(days)
    # file_name = file_name + 'tp' + str(tp)
    # file_name = file_name + 'sl' + str(sl)
    # with open(file_name + '.csv', mode='w', newline='', encoding='utf-8') as file:
    # writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # writer.writerow(['is individual', 'buy volume', 'buy power', 'buy gap', 'ascending',
    #                  'sell volume', 'sell power', 'sell gap', 'descending', 'max days', 'take profit', 'stop loss'])
    # writer.writerow(
    #     [is_individual, buy_vol, buy_pow, buy_gap, asc, sell_vol, sell_pow, sell_gap, des, days, tp, sl])
    # writer.writerow(['ticker', 'buy date', 'sell date', 'reason', 'buy', 'sell', 'profit'])
    for tick in ticks:
        bool_temp1 = False
        if is_individual:
            if float(tick.history.vol.sum()) / float(
                    float(tick.history.buy_vol.sum()) + float(tick.history.sell_vol.sum())) < 1.0:
                bool_temp1 = True
        else:
            bool_temp1 = True
        if bool_temp1:
            price = 0.0
            date1 = None
            d = 0
            for i in range(tick.start, len(tick.history.date) - 1):
                if price == 0.0:
                    if float(tick.history.vol[i] - tick.mean_vol) / float(tick.vol_std) >= buy_vol:
                        bool_temp2 = False
                        if tick.history.buy_count[i] == -1 or tick.history.buy_count[i] == 0:
                            pass
                        elif tick.history.sell_count[i] == 0 or tick.history.sell_vol[i] == 0:
                            bool_temp2 = True
                        elif (float(tick.history.buy_vol[i]) / float(tick.history.buy_count[i])) / (
                                float(tick.history.sell_vol[i]) / float(tick.history.sell_count[i])) >= buy_pow:
                            bool_temp2 = True
                        if bool_temp2:
                            temp_asc = False
                            if asc:
                                if tick.history.low[i] < tick.history.open[i] < tick.history.close[i]:
                                    temp_asc = True
                            else:
                                temp_asc = True
                            if temp_asc:
                                gap = 0
                                if tick.history.open[i + 1] > tick.history.high[i]:
                                    gap = 2
                                elif tick.history.open[i + 1] > tick.history.close[i]:
                                    gap = 1
                                elif tick.history.open[i + 1] < tick.history.low[i]:
                                    gap = -2
                                elif tick.history.open[i + 1] < tick.history.close[i]:
                                    gap = -1
                                if gap >= buy_gap:
                                    d = 0
                                    price = tick.history.open[i + 1]
                                    date1 = tick.history.date[i + 1]
                else:
                    d = d + 1
                    if d > days:
                        profit = ((float(tick.history.open[i] - price) / price) * 100.0) - 1.23
                        values.append((date1, tick.history.date[i], profit))
                        # writer.writerow(
                        #     [tick.ticker, date1, tick.history.date[i], 'max days', price, tick.history.open[i],
                        #      profit])
                        price = 0.0
                    elif (float(price - tick.history.low[i]) / price) * 100.0 >= sl:
                        profit = ((float(tick.history.low[i] - price) / price) * 100.0) - 1.23
                        values.append((date1, tick.history.date[i], profit))
                        # writer.writerow(
                        #     [tick.ticker, date1, tick.history.date[i], 'stop loss', price, tick.history.low[i],
                        #      profit])
                        price = 0.0
                    elif (float(tick.history.high[i] - price) / price) * 100 >= tp:
                        profit = tp - 1.23
                        values.append((date1, tick.history.date[i], profit))
                        # writer.writerow([tick.ticker, date1, tick.history.date[i], 'take profit', price,
                        #                  tick.history.high[i], profit])
                        price = 0.0
                    else:
                        if float(tick.history.vol[i] - tick.mean_vol) / tick.vol_std >= sell_vol:
                            bool_temp3 = False
                            if tick.history.sell_count[i] == -1 or tick.history.sell_count[i] == 0:
                                pass
                            elif tick.history.buy_vol[i] == 0 or tick.history.buy_count[i] == 0:
                                bool_temp3 = True
                            elif (float(tick.history.sell_vol[i]) / float(tick.history.sell_count[i])) / (
                                    float(tick.history.buy_vol[i]) / float(tick.history.buy_count[i])) >= sell_pow:
                                bool_temp3 = True
                            if bool_temp3:
                                profit = ((float(tick.history.open[i + 1] - price) / price) * 100.0) - 1.23
                                values.append((date1, tick.history.date[i + 1], profit))
                                # writer.writerow([tick.ticker, date1, tick.history.date[i + 1], 'sell power', price,
                                #                  tick.history.open[i + 1], profit])
                                price = 0.0
                            elif (tick.history.high[i] > tick.history.open[i] > tick.history.close[i]) and des:
                                profit = ((float(tick.history.open[i + 1] - price) / price) * 100.0) - 1.23
                                values.append((date1, tick.history.date[i + 1], profit))
                                # writer.writerow([tick.ticker, date1, tick.history.date[i + 1], 'descending', price,
                                #                  tick.history.open[i + 1], profit])
                                price = 0.0
                            else:
                                gap = 0
                                if tick.history.open[i + 1] > tick.history.high[i]:
                                    gap = 2
                                elif tick.history.open[i + 1] > tick.history.close[i]:
                                    gap = 1
                                elif tick.history.open[i + 1] < tick.history.low[i]:
                                    gap = -2
                                elif tick.history.open[i + 1] < tick.history.close[i]:
                                    gap = -1
                                if gap <= sell_gap:
                                    profit = ((float(tick.history.open[i + 1] - price) / price) * 100.0) - 1.23
                                    values.append((date1, tick.history.date[i + 1], profit))
                                    # writer.writerow([tick.ticker, date1, tick.history.date[i + 1], 'gap', price,
                                    #                  tick.history.open[i + 1], profit])
                                    price = 0.0
    a = np.array(values, dtype=d_type)
    a.sort(order='start')
    resume = True
    split = 0
    while resume:
        split = split + 1
        if split > 36:
            break
        resume = False
        dates = []
        pr = 0
        for s, e, p in a:
            active_trades = 0
            for ds, de in dates:
                if ds <= s <= de:
                    active_trades = active_trades + 1
            if active_trades < split:
                dates.append((s, e))
                pr = pr + p
            else:
                resume = True
        print(is_individual, buy_vol, buy_pow, asc, buy_gap, sell_vol, sell_pow, des, sell_gap, days, tp, sl, split, pr/float(split))
        if pr/float(split) >= 110:
            print("good")
            good.append((is_individual, buy_vol, buy_pow, asc, buy_gap, sell_vol, sell_pow, des, sell_gap, days, tp, sl, split, pr/float(split)))



def change_tickers(tickers: list[TickerInfo]):
    for tic in tickers:
        date = 0
        for i in range(len(tic.history.date)):
            if (tic.history.open[i] == -1 or tic.history.high[i] == -1 or tic.history.low[i] == -1 or
                    tic.history.close[i] == -1 or tic.history.buy_vol[i] == -1 or tic.history.buy_count[i] == -1 or
                    tic.history.sell_vol[i] == -1 or tic.history.sell_count[i] == -1 or tic.history.vol[i] == -1):
                if tic.history.date[i] > date:
                    date = tic.history.date[i]
                    tic.start = i + 1
        for i in range(len(tic.history.date) - 1):
            if tic.history.close[i + 1] < tic.history.close[i]:
                if tic.start < i + 1:
                    tic.start = i + 1
                break
        for i in range(len(tic.history.date) - 1):
            if tic.history.date[i] < 20231220 <= tic.history.date[i + 1]:
                if i > tic.start:
                    tic.start = i
                break
