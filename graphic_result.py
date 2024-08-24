import TSE
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

tickers = TSE.read_tickers_from_files(384)
TSE.change_tickers(tickers)
values = []

is_individual = False
buy_vol = -0.5
buy_pow = 1.0
asc = False
buy_gap = -2
days = 23
sell_vol = 3.0
sell_pow = 2.0
sell_gap = -2
des = False
tp = 5.0
sl = 15.0


def creat_pic(path, o, h, l, c, index, start, end, buy, sell, reason, ticker, prof, mean_vol, vol_std, s_vol, s_b_vol,
              s_b_count, s_s_vol, s_s_count, e_vol, e_b_vol, e_b_count, e_s_vol, e_s_count):
    print(ticker, start, end, prof)
    '''yy = start // 10000
    mm = (start // 100) - (yy * 100)
    dd = start - ((yy * 10000) + (mm * 100))
    start = np.datetime64(f"{yy:02}" + "-" + f"{mm:02}" + "-" + f"{dd:02}")
    yy = end // 10000
    mm = (end // 100) - (yy * 100)
    dd = end - ((yy * 10000) + (mm * 100))
    end = np.datetime64(f"{yy:02}" + "-" + f"{mm:02}" + "-" + f"{dd:02}")
    fig, axes = plt.subplots(2)
    ax = axes[1]
    stock_prices = pd.DataFrame({'open': o, 'close': c, 'high': h, 'low': l}, index=index)
    up = stock_prices[stock_prices.close >= stock_prices.open]
    down = stock_prices[stock_prices.close < stock_prices.open]
    col1 = 'green'
    col2 = 'red'
    width = .3
    width2 = .03
    ax.bar(up.index, up.close - up.open, width, bottom=up.open, color=col1)
    ax.bar(up.index, up.high - up.low, width2, bottom=up.low, color=col1)
    # ax.bar(up.index, up.low - up.open, width2, bottom=up.open, color=col1)
    ax.bar(down.index, down.open - down.close, width, bottom=down.close, color=col2)
    ax.bar(down.index, down.high - down.low, width2, bottom=down.low, color=col2)
    # ax.bar(down.index, down.low - down.close, width2, bottom=down.close, color=col2)
    ax.plot([start, end], [buy, sell])
    # ax.set_title(reason)
    plt.setp(ax.get_xticklabels(), rotation=25, ha="right", rotation_mode="anchor")
    ax = axes[0]
    ax.text(0.01, 0.9, "ticker = " + ticker)
    ax.text(0.01, 0.8, "reason = " + reason)
    ax.text(0.01, 0.7, "start = " + str(start))
    ax.text(0.01, 0.6, "end   = " + str(end))
    ax.text(0.01, 0.5, "buy   = " + str(buy))
    ax.text(0.01, 0.4, "sell  = " + str(sell))
    ax.text(0.01, 0.3, "profit = " + str(prof))
    ax.text(0.01, 0.2, "vol. avg. = " + str(mean_vol))
    ax.text(0.01, 0.1, "vol. std. = " + str(vol_std))
    ax.text(0.51, 0.91, "start vol. = " + str(s_vol))
    ax.text(0.51, 0.82, "start buy vol.  = " + str(s_b_vol))
    ax.text(0.51, 0.73, "start buy count = " + str(s_b_count))
    ax.text(0.51, 0.64, "start sell vol. = " + str(s_s_vol))
    ax.text(0.51, 0.55, "start sell count= " + str(s_s_count))
    ax.text(0.51, 0.46, "end vol. = " + str(e_vol))
    ax.text(0.51, 0.37, "end buy vol.    = " + str(e_b_vol))
    ax.text(0.51, 0.28, "end buy count   = " + str(e_b_count))
    ax.text(0.51, 0.19, "end sell vol.   = " + str(e_s_vol))
    ax.text(0.51, 0.1,  "end sell count  = " + str(e_s_count))
    if s_b_count > 0:
        ax.text(0.91, 0.9, "sbp = " + str(s_b_vol/s_b_count))
    else:
        ax.text(0.91, 0.9, "sbp = inf.")
    if s_s_count > 0:
        ax.text(0.91, 0.8, "ssp = " + str(s_s_vol/s_s_count))
    else:
        ax.text(0.91, 0.8, "ssp = inf.")
    if e_b_count > 0:
        ax.text(0.91, 0.7, "ebp = " + str(e_b_vol/e_b_count))
    else:
        ax.text(0.91, 0.7, "ebp = inf.")
    if s_s_count > 0:
        ax.text(0.91, 0.6, "esp = " + str(e_s_vol/e_s_count))
    else:
        ax.text(0.91, 0.6, "esp = inf.")


    fig.savefig('pic/' + path + '.png', dpi=200)
    plt.close(fig)'''


temp_s_vol = 0
temp_buy_vol = 0
temp_buy_count = 0
temp_sell_count = 0
temp_sell_vol = 0
d_type = [('start', int), ('end', int), ('profit', float)]

for tick in tickers:
    # print(tick.ticker)
    op = []
    hi = []
    lo = []
    cl = []
    da = []
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
            op.append(tick.history.open[i])
            hi.append(tick.history.high[i])
            lo.append(tick.history.low[i])
            cl.append(tick.history.close[i])
            yy1 = tick.history.date[i] // 10000
            mm1 = (tick.history.date[i] // 100) - (yy1 * 100)
            dd1 = tick.history.date[i] - ((yy1 * 10000) + (mm1 * 100))
            da.append(np.datetime64(f"{yy1:02}" + "-" + f"{mm1:02}" + "-" + f"{dd1:02}"))
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
                                temp_s_vol = tick.history.vol[i]
                                temp_buy_vol = tick.history.buy_vol[i]
                                temp_buy_count = tick.history.buy_count[i]
                                temp_sell_vol = tick.history.sell_vol[i]
                                temp_sell_count = tick.history.sell_count[i]

            else:
                d = d + 1
                if d > days:
                    profit = ((float(tick.history.open[i] - price) / price) * 100.0) - 1.23
                    values.append((date1, tick.history.date[i], profit))
                    op.append(tick.history.open[i + 1])
                    hi.append(tick.history.high[i + 1])
                    lo.append(tick.history.low[i + 1])
                    cl.append(tick.history.close[i + 1])
                    yy1 = tick.history.date[i + 1] // 10000
                    mm1 = (tick.history.date[i + 1] // 100) - (yy1 * 100)
                    dd1 = tick.history.date[i + 1] - ((yy1 * 10000) + (mm1 * 100))
                    da.append(np.datetime64(f"{yy1:02}" + "-" + f"{mm1:02}" + "-" + f"{dd1:02}"))
                    creat_pic(path=tick.ticker + str(da[0]), o=op, h=hi, l=lo, c=cl, index=da, start=date1,
                              end=tick.history.date[i], buy=price, sell=tick.history.open[i], reason="max days",
                              ticker=tick.ticker, prof=profit, mean_vol=tick.mean_vol, vol_std=tick.vol_std,
                              s_vol=temp_s_vol, s_b_vol=temp_buy_vol, s_b_count=temp_buy_count, s_s_vol=temp_sell_vol,
                              s_s_count=temp_sell_count, e_vol=tick.history.vol[i], e_b_vol=tick.history.buy_vol[i],
                              e_b_count=tick.history.buy_count[i], e_s_vol=tick.history.sell_vol[i],
                              e_s_count=tick.history.sell_count[i])
                    op = []
                    hi = []
                    lo = []
                    cl = []
                    da = []
                    # writer.writerow(
                    #     [tick.ticker, date1, tick.history.date[i], 'max days', price, tick.history.open[i],
                    #      profit])
                    price = 0.0
                elif (float(price - tick.history.low[i]) / price) * 100.0 >= sl:
                    profit = ((float(tick.history.low[i] - price) / price) * 100.0) - 1.23
                    values.append((date1, tick.history.date[i], profit))
                    op.append(tick.history.open[i + 1])
                    hi.append(tick.history.high[i + 1])
                    lo.append(tick.history.low[i + 1])
                    cl.append(tick.history.close[i + 1])
                    yy1 = tick.history.date[i + 1] // 10000
                    mm1 = (tick.history.date[i + 1] // 100) - (yy1 * 100)
                    dd1 = tick.history.date[i + 1] - ((yy1 * 10000) + (mm1 * 100))
                    da.append(np.datetime64(f"{yy1:02}" + "-" + f"{mm1:02}" + "-" + f"{dd1:02}"))
                    creat_pic(path=tick.ticker + str(da[0]), o=op, h=hi, l=lo, c=cl, index=da, start=date1,
                              end=tick.history.date[i], buy=price, sell=tick.history.low[i], reason="stop loss",
                              ticker=tick.ticker, prof=profit, mean_vol=tick.mean_vol, vol_std=tick.vol_std,
                              s_vol=temp_s_vol, s_b_vol=temp_buy_vol, s_b_count=temp_buy_count, s_s_vol=temp_sell_vol,
                              s_s_count=temp_sell_count, e_vol=tick.history.vol[i], e_b_vol=tick.history.buy_vol[i],
                              e_b_count=tick.history.buy_count[i], e_s_vol=tick.history.sell_vol[i],
                              e_s_count=tick.history.sell_count[i])
                    op = []
                    hi = []
                    lo = []
                    cl = []
                    da = []
                    # writer.writerow(
                    #     [tick.ticker, date1, tick.history.date[i], 'stop loss', price, tick.history.low[i],
                    #      profit])
                    price = 0.0
                elif (float(tick.history.high[i] - price) / price) * 100 >= tp:
                    profit = tp - 1.23
                    values.append((date1, tick.history.date[i], profit))
                    op.append(tick.history.open[i + 1])
                    hi.append(tick.history.high[i + 1])
                    lo.append(tick.history.low[i + 1])
                    cl.append(tick.history.close[i + 1])
                    yy1 = tick.history.date[i + 1] // 10000
                    mm1 = (tick.history.date[i + 1] // 100) - (yy1 * 100)
                    dd1 = tick.history.date[i + 1] - ((yy1 * 10000) + (mm1 * 100))
                    da.append(np.datetime64(f"{yy1:02}" + "-" + f"{mm1:02}" + "-" + f"{dd1:02}"))
                    creat_pic(path=tick.ticker + str(da[0]), o=op, h=hi, l=lo, c=cl, index=da, start=date1,
                              end=tick.history.date[i], buy=price, sell=tick.history.high[i], reason="take profit",
                              ticker=tick.ticker, prof=profit, mean_vol=tick.mean_vol, vol_std=tick.vol_std,
                              s_vol=temp_s_vol, s_b_vol=temp_buy_vol, s_b_count=temp_buy_count, s_s_vol=temp_sell_vol,
                              s_s_count=temp_sell_count, e_vol=tick.history.vol[i], e_b_vol=tick.history.buy_vol[i],
                              e_b_count=tick.history.buy_count[i], e_s_vol=tick.history.sell_vol[i],
                              e_s_count=tick.history.sell_count[i])
                    op = []
                    hi = []
                    lo = []
                    cl = []
                    da = []
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
                            op.append(tick.history.open[i + 1])
                            hi.append(tick.history.high[i + 1])
                            lo.append(tick.history.low[i + 1])
                            cl.append(tick.history.close[i + 1])
                            yy1 = tick.history.date[i + 1] // 10000
                            mm1 = (tick.history.date[i + 1] // 100) - (yy1 * 100)
                            dd1 = tick.history.date[i + 1] - ((yy1 * 10000) + (mm1 * 100))
                            da.append(np.datetime64(f"{yy1:02}" + "-" + f"{mm1:02}" + "-" + f"{dd1:02}"))
                            creat_pic(path=tick.ticker + str(da[0]), o=op, h=hi, l=lo, c=cl, index=da, start=date1,
                                      end=tick.history.date[i + 1], buy=price, sell=tick.history.open[i + 1],
                                      reason="sell power", ticker=tick.ticker, prof=profit, mean_vol=tick.mean_vol,
                                      vol_std=tick.vol_std, s_vol=temp_s_vol, s_b_vol=temp_buy_vol,
                                      s_b_count=temp_buy_count, s_s_vol=temp_sell_vol, s_s_count=temp_sell_count,
                                      e_vol=tick.history.vol[i], e_b_vol=tick.history.buy_vol[i],
                                      e_b_count=tick.history.buy_count[i], e_s_vol=tick.history.sell_vol[i],
                                      e_s_count=tick.history.sell_count[i])
                            op = []
                            hi = []
                            lo = []
                            cl = []
                            da = []
                            # writer.writerow([tick.ticker, date1, tick.history.date[i + 1], 'sell power', price,
                            #                  tick.history.open[i + 1], profit])
                            price = 0.0
                        elif (tick.history.high[i] > tick.history.open[i] > tick.history.close[i]) and des:
                            profit = ((float(tick.history.open[i + 1] - price) / price) * 100.0) - 1.23
                            values.append((date1, tick.history.date[i + 1], profit))
                            op.append(tick.history.open[i + 1])
                            hi.append(tick.history.high[i + 1])
                            lo.append(tick.history.low[i + 1])
                            cl.append(tick.history.close[i + 1])
                            yy1 = tick.history.date[i + 1] // 10000
                            mm1 = (tick.history.date[i + 1] // 100) - (yy1 * 100)
                            dd1 = tick.history.date[i + 1] - ((yy1 * 10000) + (mm1 * 100))
                            da.append(np.datetime64(f"{yy1:02}" + "-" + f"{mm1:02}" + "-" + f"{dd1:02}"))
                            creat_pic(path=tick.ticker + str(da[0]), o=op, h=hi, l=lo, c=cl, index=da, start=date1,
                                      end=tick.history.date[i + 1], buy=price, sell=tick.history.open[i + 1],
                                      reason="descending", ticker=tick.ticker, prof=profit, mean_vol=tick.mean_vol,
                                      vol_std=tick.vol_std, s_vol=temp_s_vol, s_b_vol=temp_buy_vol,
                                      s_b_count=temp_buy_count, s_s_vol=temp_sell_vol, s_s_count=temp_sell_count,
                                      e_vol=tick.history.vol[i], e_b_vol=tick.history.buy_vol[i],
                                      e_b_count=tick.history.buy_count[i], e_s_vol=tick.history.sell_vol[i],
                                      e_s_count=tick.history.sell_count[i])
                            op = []
                            hi = []
                            lo = []
                            cl = []
                            da = []
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
                                op.append(tick.history.open[i + 1])
                                hi.append(tick.history.high[i + 1])
                                lo.append(tick.history.low[i + 1])
                                cl.append(tick.history.close[i + 1])
                                yy1 = tick.history.date[i + 1] // 10000
                                mm1 = (tick.history.date[i + 1] // 100) - (yy1 * 100)
                                dd1 = tick.history.date[i + 1] - ((yy1 * 10000) + (mm1 * 100))
                                da.append(np.datetime64(f"{yy1:02}" + "-" + f"{mm1:02}" + "-" + f"{dd1:02}"))
                                creat_pic(path=tick.ticker + str(da[0]), o=op, h=hi, l=lo, c=cl, index=da, start=date1,
                                          end=tick.history.date[i + 1], buy=price, sell=tick.history.open[i + 1],
                                          reason="gap",
                                          ticker=tick.ticker, prof=profit, mean_vol=tick.mean_vol, vol_std=tick.vol_std,
                                          s_vol=temp_s_vol, s_b_vol=temp_buy_vol, s_b_count=temp_buy_count,
                                          s_s_vol=temp_sell_vol, s_s_count=temp_sell_count, e_vol=tick.history.vol[i],
                                          e_b_vol=tick.history.buy_vol[i], e_b_count=tick.history.buy_count[i],
                                          e_s_vol=tick.history.sell_vol[i], e_s_count=tick.history.sell_count[i])
                                op = []
                                hi = []
                                lo = []
                                cl = []
                                da = []
                                # writer.writerow([tick.ticker, date1, tick.history.date[i + 1], 'gap', price,
                                #                  tick.history.open[i + 1], profit])
                                price = 0.0
a = np.array(values, dtype=d_type)
a.sort(order='start')
resume = True
split = 0
while resume:
    split = split + 1
    if split > 1:
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
    print(is_individual, buy_vol, buy_pow, asc, buy_gap, sell_vol, sell_pow, des, sell_gap, days, tp, sl, split,
          pr / float(split))
    if pr / float(split) >= 90:
        print("good")
        # good.append((is_individual, buy_vol, buy_pow, asc, buy_gap, sell_vol, sell_pow, des, sell_gap, days, tp, sl, split, pr/float(split)))
