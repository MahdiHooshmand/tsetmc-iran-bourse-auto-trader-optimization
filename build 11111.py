import csv
import time

s = input("series:")
vm5 = input("v-5:")
vxx = input("vxx:")
vp5 = input("v+5:")

hm5 = input("h-5:")
hxx = input("hxx:")
hp5 = input("h+5:")

sxxxx = []
sxxm5 = []
sxxp5 = []
sm5xx = []
sp5xx = []

nsxxxx = []


def read_file(li, name):
    with open(name, mode='r', encoding='utf-8', newline='') as file:
        reader = csv.reader(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            if row[0] == "True" or row[0] == "TRUE":
                is_individual_i = True
            elif row[0] == "False" or row[0] == "FALSE":
                is_individual_i = False
            else:
                print("error0")
                print(row[0])
                time.sleep(10)
            if row[3] == "True" or row[3] == "TRUE":
                asc_i = True
            elif row[3] == "False" or row[3] == "FALSE":
                asc_i = False
            else:
                print("error3")
                print(row[3])
                time.sleep(10)
            if row[7] == "True" or row[7] == "TRUE":
                des_i = True
            elif row[7] == "False" or row[7] == "FALSE":
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
            li.append(
                [is_individual_i, buy_vol_i, buy_pow_i, asc_i, buy_gap_i, sell_vol_i, sell_pow_i, des_i, sell_gap_i,
                 days_i, tp_i, sl_i])


read_file(sxxxx, s + vxx + hxx + ".csv")
read_file(sm5xx, s + vm5 + hxx + ".csv")
read_file(sp5xx, s + vp5 + hxx + ".csv")
read_file(sxxm5, s + vxx + hm5 + ".csv")
read_file(sxxp5, s + vxx + hp5 + ".csv")


for ri in sxxxx:
    if ri not in nsxxxx:
        nsxxxx.append(ri)
    ri1 = [ri[0], ri[1], ri[2], not (ri[3]), ri[4], ri[5], ri[6], ri[7], ri[8], ri[9], ri[10], ri[11]]
    if ri1 not in nsxxxx:
        nsxxxx.append(ri1)
    if ri[4] == -2:
        ri2 = [ri[0], ri[1], ri[2], ri[3], -1, ri[5], ri[6], ri[7], ri[8], ri[9], ri[10], ri[11]]
        if ri2 not in sxxxx:
            nsxxxx.append(ri2)
    elif ri[4] == 2:
        ri2 = [ri[0], ri[1], ri[2], ri[3], 1, ri[5], ri[6], ri[7], ri[8], ri[9], ri[10], ri[11]]
        if ri2 not in nsxxxx:
            nsxxxx.append(ri2)
    else:
        ri2 = [ri[0], ri[1], ri[2], ri[3], ri[4] - 1, ri[5], ri[6], ri[7], ri[8], ri[9], ri[10], ri[11]]
        ri3 = [ri[0], ri[1], ri[2], ri[3], ri[4] + 1, ri[5], ri[6], ri[7], ri[8], ri[9], ri[10], ri[11]]
        if ri2 not in nsxxxx:
            nsxxxx.append(ri2)
        if ri3 not in nsxxxx:
            nsxxxx.append(ri3)
    ri4 = [ri[0], ri[1], ri[2], ri[3], ri[4], ri[5] - 0.5, ri[6], ri[7], ri[8], ri[9], ri[10], ri[11]]
    if ri4 not in nsxxxx:
        nsxxxx.append(ri4)
    ri5 = [ri[0], ri[1], ri[2], ri[3], ri[4], ri[5] + 0.5, ri[6], ri[7], ri[8], ri[9], ri[10], ri[11]]
    if ri5 not in nsxxxx:
        nsxxxx.append(ri5)
    ri6 = [ri[0], ri[1], ri[2], ri[3], ri[4], ri[5], ri[6] - 0.5, ri[7], ri[8], ri[9], ri[10], ri[11]]
    if ri6 not in nsxxxx:
        nsxxxx.append(ri6)
    ri7 = [ri[0], ri[1], ri[2], ri[3], ri[4], ri[5], ri[6] + 0.5, ri[7], ri[8], ri[9], ri[10], ri[11]]
    if ri7 not in nsxxxx:
        nsxxxx.append(ri7)
    ri8 = [ri[0], ri[1], ri[2], ri[3], ri[4], ri[5], ri[6], not (ri[7]), ri[8], ri[9], ri[10], ri[11]]
    if ri8 not in nsxxxx:
        nsxxxx.append(ri8)
    if ri[8] == -2:
        ri9 = [ri[0], ri[1], ri[2], ri[3], ri[4], ri[5], ri[6], ri[7], -1, ri[9], ri[10], ri[11]]
        if ri9 not in nsxxxx:
            nsxxxx.append(ri9)
    elif ri[8] == 2:
        ri9 = [ri[0], ri[1], ri[2], ri[3], ri[4], ri[5], ri[6], ri[7], 1, ri[9], ri[10], ri[11]]
        if ri9 not in nsxxxx:
            nsxxxx.append(ri9)
    else:
        ri9 = [ri[0], ri[1], ri[2], ri[3], ri[4], ri[5], ri[6], ri[7], ri[8] - 1, ri[9], ri[10], ri[11]]
        ri10 = [ri[0], ri[1], ri[2], ri[3], ri[4], ri[5], ri[6], ri[7], ri[8] + 1, ri[9], ri[10], ri[11]]
        if ri9 not in nsxxxx:
            nsxxxx.append(ri9)
        if ri10 not in nsxxxx:
            nsxxxx.append(ri10)
    ri11 = [ri[0], ri[1], ri[2], ri[3], ri[4], ri[5], ri[6], ri[7], ri[8], ri[9] + 3, ri[10], ri[11]]
    if ri11 not in nsxxxx:
        nsxxxx.append(ri11)
    ri12 = [ri[0], ri[1], ri[2], ri[3], ri[4], ri[5], ri[6], ri[7], ri[8], ri[9] - 3, ri[10], ri[11]]
    if ri12 not in nsxxxx:
        nsxxxx.append(ri12)
    ri13 = [ri[0], ri[1], ri[2], ri[3], ri[4], ri[5], ri[6], ri[7], ri[8], ri[9], ri[10] + 5.0, ri[11]]
    if ri13 not in nsxxxx:
        nsxxxx.append(ri13)
    ri14 = [ri[0], ri[1], ri[2], ri[3], ri[4], ri[5], ri[6], ri[7], ri[8], ri[9], ri[10] - 5.0, ri[11]]
    if ri14 not in nsxxxx:
        nsxxxx.append(ri14)
    ri15 = [ri[0], ri[1], ri[2], ri[3], ri[4], ri[5], ri[6], ri[7], ri[8], ri[9], ri[10], ri[11] + 5.0]
    if ri15 not in nsxxxx:
        nsxxxx.append(ri15)
    ri16 = [ri[0], ri[1], ri[2], ri[3], ri[4], ri[5], ri[6], ri[7], ri[8], ri[9], ri[10], ri[11] - 5.0]
    if ri16 not in nsxxxx:
        nsxxxx.append(ri16)

for ri in sxxm5:
    ri[2] = ri[2] + 0.5
    if ri not in nsxxxx:
        nsxxxx.append(ri)

for ri in sxxp5:
    ri[2] = ri[2] - 0.5
    if ri not in nsxxxx:
        nsxxxx.append(ri)

for ri in sm5xx:
    ri[1] = ri[1] + 0.5
    if ri not in nsxxxx:
        nsxxxx.append(ri)

for ri in sp5xx:
    ri[1] = ri[1] - 0.5
    if ri not in nsxxxx:
        nsxxxx.append(ri)

with open("x" + s + vxx + hxx + ".csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in nsxxxx:
        writer.writerow(i)
