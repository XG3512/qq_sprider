import csv
stufile='student.csv'
qqfile='test.csv'
with open(stufile,'r',encoding="utf-8") as stufile:
    readerstu = csv.DictReader(stufile)
    print(readerstu['name'])
    for stu in readerstu:
        print(type(stu['name']))
    with open(qqfile,'r',encoding="utf-8") as qqfile:
        readerqq = csv.DictReader(qqfile)
        for stu in readerqq:
            if stu['name'] in readerstu['name']:
                print('ok')
            else:
                print("notok")
