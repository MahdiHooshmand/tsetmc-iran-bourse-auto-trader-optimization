import csv
res = []
last_row = None
name = input("name:")
with open('res'+name+'.csv', mode='r', encoding='utf-8', newline='') as file:
    reader = csv.reader(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        if last_row == None:
            last_row = [row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11]]
            res.append(last_row)
        else:
            con = True
            for i in range(12):
                con = con and (row[i] == last_row[i])
            if not con:
                last_row = [row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11]]
                res.append(last_row)
with open('res2'+name+'.csv', mode='w', newline='', encoding='utf-8') as file2:
    writer = csv.writer(file2, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in res:
        writer.writerow([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11]])
