import csv
with open('./dataset_20210821/418225383.csv','rt',encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    column = [row['群名片'] for row in reader]
for i in column:
    if i[:7]!='Boy-21-' and i[:8]!='Girl-21-':
        print('@'+i)