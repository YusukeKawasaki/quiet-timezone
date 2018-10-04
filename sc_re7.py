import requests
import re
import csv
import calendar



URL = "http://www2.med.osaka-u.ac.jp/resv/"
UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"

payload = {
    'uid': '1188',
    'upw': 'cB8V'
}

headers = {"User-Agent": UserAgent}
s = requests.Session()
resp = s.get(URL, timeout=1, headers=headers)

# ログイン
s.post(URL, data=payload)

def tomin(posis): ##px→分
    i = int(posis[1])/9 * 10 
    a = int(posis[0])/9 * 10
    b = a + i
    return (a,b)

def union(min_list): #期間データ結合
    union_list = [(0,0)]
    if min_list:
        min_list.sort()
        for mins in min_list:
            a = union_list[-1][0]
            b = union_list[-1][1]
            if b < mins[0]:
                union_list.append(mins)
            else:
                union_list[-1] = (a, max(b , mins[1]))
    
    return union_list

def totime(a): #分→時間
    return str(int(7 + a/60)) + ":" + str("{0:02d}".format(int(a%60)))

f = open('otokin.csv', 'w')

writer = csv.writer(f, lineterminator='\n')

year = int(input("please input year."))
month = int(input("please input month."))
_, lastday = calendar.monthrange(2014,12)

for i in range(lastday):
    day = i + 1
    daystr = "%d-%d-%d"%(year, month, day)
    otokin_url = "http://www2.med.osaka-u.ac.jp/resv/rsvMain.php?t=0&y=%d&m=%d&d=%d"%(year, month, day)
    resp = s.get(otokin_url, timeout=1, headers=headers)


    pattern = r'<div class="scScheduleBox sc" id="[0-9]*" style="left:[0-9]*px;width:[0-9]*px;">'
    text = resp.text

    matchlist = re.findall(pattern , text)


    min_list = []
    for st in matchlist:
        stlist = re.split('left:|px;width:|px;"', st)
        posis =  [ stlist[1], stlist[2] ]
        min_list.append(tomin(posis))

    min_list = union(min_list)

    timestr = ""
    for mins in min_list:
        if mins[0] != mins[1]:
            a = totime(mins[0]) + "-" + totime(mins[1]) + " "
            timestr += a
    writer.writerow([daystr, timestr])
f.close()

print("complete! Check 'otokin.csv'")