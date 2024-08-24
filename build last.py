import csv
import time
import os
import math


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
            li.append([is_individual_i, buy_vol_i, buy_pow_i, asc_i, buy_gap_i, sell_vol_i, sell_pow_i, des_i, sell_gap_i, days_i, tp_i, sl_i])


read_file(sxxxx,"input.csv")

complated = []
for i in range(len(sxxxx)):
    """
    * build directory name
    """
    dir_name = ""
    if i[0]: #is_individual
        dir_name = dir_name + "T-"
    else:
        dir_name = dir_name + "F-"
    if i[1] == 0: #buy_vol
        dir_name = dir_name + "00-"
    else:
        if i[1] > 0:
            dir_name = dir_name +"P"
        else:
            dir_name = dir_name +"N"
        dir_name = dir_name + str(int(math.abs(i[1]*10))) + "-"
    if i[2] == 0: #buy_pow
        dir_name = dir_name + "00-"
    else:
        if i[2] > 0:
            dir_name = dir_name +"P"
        else:
            dir_name = dir_name +"N"
        dir_name = dir_name + str(int(math.abs(i[2]*10))) + "-"
    if i[3]: #asc
        dir_name = dir_name + "T-"
    else:
        dir_name = dir_name + "F-"
    if i[4] == 0: #buy_gap
        dir_name = dir_name + "00-"
    else:
        if i[4] > 0:
            dir_name = dir_name +"P"
        else:
            dir_name = dir_name +"N"
        dir_name = dir_name + str(int(math.abs(i[4]))) + "-"
    if i[5] == 0: #sell_vol
        dir_name = dir_name + "00-"
    else:
        if i[5] > 0:
            dir_name = dir_name +"P"
        else:
            dir_name = dir_name +"N"
        dir_name = dir_name + str(int(math.abs(i[5]*10))) + "-"
    if i[6] == 0: #sell_pow
        dir_name = dir_name + "00-"
    else:
        if i[6] > 0:
            dir_name = dir_name +"P"
        else:
            dir_name = dir_name +"N"
        dir_name = dir_name + str(int(math.abs(i[6]*10))) + "-"
    if i[7]: #des
        dir_name = dir_name + "T-"
    else:
        dir_name = dir_name + "F-"
    if i[8] == 0: #sell_gap
        dir_name = dir_name + "00-"
    else:
        if i[8] > 0:
            dir_name = dir_name +"P"
        else:
            dir_name = dir_name +"N"
        dir_name = dir_name + str(int(math.abs(i[8]))) + "-"
    if i[9] == 0: #days
        dir_name = dir_name + "00-"
    else:
        if i[9] > 0:
            dir_name = dir_name +"P"
        else:
            dir_name = dir_name +"N"
        dir_name = dir_name + str(int(math.abs(i[9]))) + "-"
    if i[10] == 0: #tp
        dir_name = dir_name + "00-"
    else:
        if i[10] > 0:
            dir_name = dir_name +"P"
        else:
            dir_name = dir_name +"N"
        dir_name = dir_name + str(int(math.abs(i[10]*10))) + "-"
    if i[11] == 0: #sl
        dir_name = dir_name + "00"
    else:
        if i[11] > 0:
            dir_name = dir_name +"P"
        else:
            dir_name = dir_name +"N"
        dir_name = dir_name + str(int(math.abs(i[11]*10)))
    os.mkdir(dir_name)
    """
    * build all available modes
    """
    ii = [True,False]
    bv = [i[1]-0.3,i[1]-0.2,i[1]-0.1,i[1],i[1]+0.1,i[1]+0.2,i[1]+0.3]
    bp = [i[2]-0.3,i[2]-0.2,i[2]-0.1,i[2],i[2]+0.1,i[2]+0.2,i[2]+0.3]
    asc = [True,False]
    bg = []
    if i[4] == -2:
        bg = [-2,-1]
    elif i[4] == 2:
        bg = [1,2]
    else:
        bg = [i[4]-1,i[4],i[4]+1]
    sv = [i[5]-0.3,i[5]-0.2,i[5]-0.1,i[5],i[5]+0.1,i[5]+0.2,i[5]+0.3]
    sp = [i[6]-0.3,i[6]-0.2,i[6]-0.1,i[6],i[6]+0.1,i[6]+0.2,i[6]+0.3]
    des = [True,False]
    sg = []
    if i[8] == -2:
        sg = [-2,-1]
    elif i[8] == 2:
        sg = [1,2]
    else:
        sg = [i[8]-1,i[8],i[8]+1]
    days = []
    if i[9] < 1:
        days = [0]
    elif i[9] == 1:
        days = [1,2,3]
    elif i[9] == 2:
        days = [1,2,3,4]
    elif i[9] == 3:
        days = [1,2,3,4,5]
    else:
        days = [i[9]-2,i[9]-1,i[9],i[9]+1,i[9]+2]
    tp = [i[10]-3.0,i[10]-2.0,i[10]-1.0,i[10],i[10]+1.0,i[10]+2.0,i[10]+3.0]
    sl = [i[11]-3.0,i[11]-2.0,i[11]-1.0,i[11],i[11]+1.0,i[11]+2.0,i[11]+3.0]
    """
    * write to files
    """
    for iij in ii:
        for bvj in bv:
            for bpj in bp:
                file_name = dir_name + "/"
                if iij :
                    file_name = file name + "T_"
                else :
                    file_name = file_name + "F_"
                file_name = file_name + str(bvj) + "_" + str(bpj) + ".csv"
                with open(file_name, mode='w' newline='', encoding='utf-8') as file:
                    writer = csv.writer(file, delimiter=',',quotechar'|',quoting=csv.QUOTE_MINIMAL)
                    for ascj in asc:
                        for bgj in bg:
                            for svj in sv:
                                for spj in sp:
                                    for desj in des:
                                        for sgj in sg:
                                            for daysj in days:
                                                for tpj in tp:
                                                    for slj in sl:
                                                        flag = 0
                                                        for c in complated:
                                                            if math.abs(c[1]-bvj) <= 0.3 and math.abs(c[2]-bpj) <= 0.3 math.abs(c[4]-bgj) <= 1 and math.abs(c[5]-svj) <= 0.3 and math.abs(c[6]-spj) <= 0.3 and math.abs(c[8]-sgj) <= 1 and math.abs(c[9]-daysj) <= 2 and math.abs(c[10]-tpj) <= 3 and math.abs(c[11]-slj) <= 3 :
                                                                flag = 1
                                                                break
                                                        if flag == 0 :
                                                            writer.writerow([iij,bvj,bpj,ascj,bgj,svj,spj,des,sgj,daysj,tpj,slj])
    complated.append(i)
