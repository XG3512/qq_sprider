import csv

import pandas as pd
stufile='student.csv'
qqfile='test.csv'
qqdf=pd.read_csv(qqfile)
studf=pd.read_csv(stufile)
print(type(qqdf['name']))

def write(filename,datas):
    with open (filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter (f, fieldnames=header)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
        writer.writerow (datas)  # 写入数据
def cleanfile(filename,header):
    with open (filename, 'w', newline='', encoding='utf-8') as f:
        # header = ['name', 'QQsex','QQnum','reason']  # 数据列名
        writer = csv.DictWriter (f, fieldnames=header)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
        writer.writeheader ()  # 写入列名
header = ['name', 'QQsex','QQnum','reason']
cleanfile('illegal.csv',header)
for index, data in qqdf.iterrows():
    flag=0
    for stuindex,studata in studf.iterrows():
        if data['name']==studata['name'] and data['sex']==studata['sex']:
            flag=1
            break
    if flag==0:
        info=dict(name=data['name'],QQsex=data['sex'],QQnum=data['QQnum'],reason='不在新生名单中')
        write('illegal.csv',info)
header = ['STUname', 'STUsex','STUphone','STUclass','STUnum','reason']
cleanfile('NotInGroup.csv',header)
for stuindex, studata in studf.iterrows():
    flag=0
    for qqindex,qqdata in qqdf.iterrows():
        if studata['name']==qqdata['name'] and studata['sex']==qqdata['sex']:
            flag=1
            break
    if flag==0:
        info=dict(STUname=studata['name'],STUsex=studata['sex'],STUphone=studata['phone'],STUclass=studata['class'],STUnum=studata['stuNum'],reason='当前不在群聊中')
        write('NotInGroup.csv',info)
        #wee