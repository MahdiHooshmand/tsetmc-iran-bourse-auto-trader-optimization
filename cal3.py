import TSE
import csv

tickers = TSE.read_tickers_from_files(378)

TSE.change_tickers(tickers)
c = 0

name = input("name:")

with open(name, mode='r', encoding='utf-8', newline='') as file:
    reader = csv.reader(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        if row[0] == "True":
            is_individual_i = True
        elif row[0] == "False":
            is_individual_i = False
        else:
            print("error0")
            print(row[0])
            time.sleep(10)
        if row[3] == "True":
            asc_i = True
        elif row[3] == "False":
            asc_i = False
        else:
            print("error3")
            print(row[3])
            time.sleep(10)
        if row[7] == "True":
            des_i = True
        elif row[7] == "False":
            des_i = False
        else:
            print("error7")
            print(row[7])
            time.sleep(10)
        buy_vol_i = float(row[1])
        buy_pow_i = float(row[2])
        buy_gap_i = int(row[4])
        sell_vol_i = float(row[5])
        sell_pow_i = float(row[6])
        sell_gap_i = int(row[8])
        days_i = int(row[9])
        tp_i = float(row[10])
        sl_i = float(row[11])
        TSE.check(tickers, is_individual=is_individual_i, buy_vol=buy_vol_i, buy_pow=buy_pow_i, asc=asc_i, buy_gap=buy_gap_i, sell_vol=sell_vol_i, sell_pow=sell_pow_i, des=des_i, sell_gap=sell_gap_i, days=days_i, tp=tp_i, sl=sl_i)
        c = c + 1
        print(c)
        #li.append([is_individual_i,buy_vol_i,buy_pow_i,asc_i,buy_gap_i,sell_vol_i,sell_pow_i,des_i,sell_gap_i,days_i,tp_i,sl_i])

with open('res_'+name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in TSE.good:
        writer.writerow([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[13]])

