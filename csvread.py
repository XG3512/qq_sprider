import csv

filename='./dataset_20210821/418225383.csv'
def write(datas):
    with open ('test.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter (f, fieldnames=header)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
        writer.writerow (datas)  # 写入数据
def check(row):
    with open('whiteList.txt','r',encoding='utf-8') as Data:
        whiteListData=Data.read().splitlines()
    if row['群名片'][:7]=='Boy-21-':
        # print('性别:男  姓名：'+row['群名片'][7:])
        userName= row['群名片'][7:]
        message=dict(name=userName, sex='男',QQnum=row['QQ号'])
        write(message)
    elif row['群名片'][:8]=='Girl-21-':
        # print('性别:女  姓名：'+row['群名片'][8:])
        userName= row['群名片'][8:]
        message=dict(name=userName, sex='女',QQnum=row['QQ号'])
        write(message)
    else:
        if row['群名片'] not in whiteListData:
            print(row['群名片']+'  '+row['QQ号'])
with open(filename,'r',encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    header = ['name', 'sex','QQnum']  # 数据列名
    with open ('test.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter (f, fieldnames=header)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
        writer.writeheader ()  # 写入列名
    for row in reader:
        check(row)
        # print(row['群名片'])