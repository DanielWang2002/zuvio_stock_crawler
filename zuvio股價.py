from IPython.display import display, clear_output
from urllib.request import urlopen
import pandas as pd
from datetime import datetime, timezone, timedelta
import requests
import sched
import time
import json


def tableColor(val):
    if val > 0:
        color = 'red'
    elif val < 0:
        color = 'green'
    else:
        color = 'white'
    return 'color: %s' % color

### ================可調整參數================

# 表格更新時間，單位為秒
update_time = 10

# 漲幅(%) > rise_pct 才會顯示於表格
rise_pct = 0.5

### ================可調整參數================

### ================不要動================

# 計時器
s = sched.scheduler(time.time, time.sleep)

# 設定為 +8 時區
tz = timezone(timedelta(hours=+8))

# 不顯示DataFrame的Dimensions
pd.options.display.show_dimensions = False
# 顯示所有資料
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
# default='warn'
pd.options.mode.chained_assignment = None


### ================不要動================


def crawler():
    url = 'https://forum.zuvio.com.tw/api/stock/stocksInfo?api_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NTE1ODk1NDgsImV4cCI6MTY1MTc2MjM0OCwic3lzdGVtX25hbWUiOiJpcnMiLCJ6dXZpb19pZCI6IjIzNjY4NDQiLCJlbWFpbCI6IkMxMDkxNTYxMDdAbmt1c3QuZWR1LnR3IiwibmFtZSI6Ilx1NzM4Ylx1NjYzMVx1N2ZkNCIsIm5pY2tuYW1lIjoiXHU3ZmQ0IiwidW5pdmVyc2l0eV9pZCI6IjU5MjMiLCJ1bml2ZXJzaXR5X25hbWUiOiJcdTlhZDhcdTc5ZDFcdTU5MjciLCJzY2hvb2xfbGV2ZWxfaWQiOiIxIiwic3ViX2RlcGFydG1lbnRfaWQiOiIyMTIxOCIsInN1Yl9kZXBhcnRtZW50X25hbWUiOiJcdTY2N2FcdTYxNjdcdTU1NDZcdTUyZDlcdTdjZmIiLCJjb3VudHlfaWQiOiIyMiIsImNvdW50eV9uYW1lIjoiXHU5YWQ4XHU5NmM0XHU1ZTAyIiwiZ3JhZGVfaWQiOiIxIiwiZ3JhZGVfbmFtZSI6Ilx1NTkyN1x1NGUwMCIsImZvcnVtX3NleF9jb2RlIjoiTSIsInVzZXJfaWQiOiIxMTEzOTM0In0.yP4vFqRY4EwX4X13gLipZmSpaShhB78l_dLugHCmraw'
    data = json.loads(urlopen(url).read())

    # 股票類型數量: 28
    kind_size = len(data['data']['stocks_info'])

    # 股價資訊
    stocks_info = data['data']['stocks_info']

    stocks_list = []

    for i in range(0, kind_size):
        for k in stocks_info[i]['stocks']:
            # print(f"{k['code']} {k['name']} 現價: {k['price']}")
            stock_temp_list = [k['code'], k['name'], k['price'], k['change'], float(k['change_pct'])]
            stocks_list.append(stock_temp_list)
            # print(stock_temp_list)

    columns = ['股票代號', '公司簡稱', '當盤成交價', '漲跌', '漲跌比']
    df = pd.DataFrame(stocks_list, columns=columns)
    # df = df.style.applymap(tableColor, subset=['漲跌百分比'])
    # 紀錄更新時間
    _time = datetime.now(tz)
    print(f"更新時間: {str(_time).split('.')[0]}")

    _time = datetime.now()
    start_time = datetime.strptime(str(_time.date()) + '9:30', '%Y-%m-%d%H:%M')
    end_time = datetime.strptime(str(_time.date()) + '13:30', '%Y-%m-%d%H:%M')

    # 判斷爬蟲終止條件
    if start_time <= _time <= end_time:
        s.enter(update_time, 0, crawler)
    else:
        print("非交易時間，停止抓取資料...")

# 每秒定時器
s.enter(1, 0, crawler)
s.run()