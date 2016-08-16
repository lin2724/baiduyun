from __future__ import print_function
import csv
with open('eggs2.csv','wb') as csvfile:
    writer = csv.writer(csvfile)
    lis =[]
    lis+=["ls1","ls2"]
    liss=[]
    lis.append(["ap1","ap2"])

    writer.writerows([["sub1","sub2"]])
    for i in range(10):
        lis.append(i)
    writer.writerow(lis)
    writer.writerow(['Spam'] * 3 + ['Baked Beans'])
    writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

lis = ("12346789")
print(lis[1:-2])
