import pandas as pd
stufile='student.csv'
qqfile='test.csv'
qqdf=pd.read_csv(qqfile)
studf=pd.read_csv(stufile)
print(type(qqdf['name']))
for index, data in qqdf.iterrows():
    # print(index)
    flag=0
    for stuindex,studata in studf.iterrows():
        if data['name']==studata['name'] and data['sex']==studata['sex']:
            flag=1
            print(stuindex)
            break
    if flag==0:
        print(data['name'])
        print(data['QQnum'])