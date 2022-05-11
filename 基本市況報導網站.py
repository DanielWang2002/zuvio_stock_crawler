from IPython.display import display, clear_output
from urllib.request import urlopen
import pandas as pd
import datetime
import requests
import sched
import time
import json

s = sched.scheduler(time.time, time.sleep)

# 表格更新時間，單位為秒
update_time = 10

# 漲幅 > rise_pct 才會顯示於表格
rise_pct = 0.5

# 不顯示DataFrame的Dimensions
pd.options.display.show_dimensions = False
# 顯示所有資料
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
# default='warn'
pd.options.mode.chained_assignment = None

def tableColor(val):
    if val > 0:
        color = 'red'
    elif val < 0:
        color = 'green'
    else:
        color = 'white'
    return 'color: %s' % color

def stock_crawler(targets):
    clear_output(wait=True)

    # 組成stock_list
    stock_list = '|'.join('tse_{}.tw'.format(target) for target in targets)

    # 　query data
    now_time = int(time.time()*1000)
    query_url = f"http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={stock_list}&_={now_time}"
    data = json.loads(urlopen(query_url).read())

    # 過濾出有用到的欄位

    columns = ['c', 'n', 'z', 'tv', 'v', 'o', 'h', 'l', 'y']
    df = pd.DataFrame(data['msgArray'], columns=columns)
    df.columns = ['股票代號', '公司簡稱', '當盤成交價', '當盤成交量', '累積成交量', '開盤價', '最高價', '最低價', '昨收價']
    df.insert(9, "漲跌百分比", 0.0)

    s_list = []

    # 新增漲跌百分比
    for x in range(len(df.index)):
        if (df['當盤成交價'].iloc[x] != "-") and (df['當盤成交量'].iloc[x] != "-"):
            df.iloc[x, [2, 3, 4, 5, 6, 7, 8]] = df.iloc[x, [2, 3, 4, 5, 6, 7, 8]].astype(float)
            df['漲跌百分比'].iloc[x] = (df['當盤成交價'].iloc[x] - df['昨收價'].iloc[x]) / df['昨收價'].iloc[x] * 100
            if df['漲跌百分比'].iloc[x] > rise_pct:
                s_list.append(df.iloc[x])
    df2 = pd.DataFrame(s_list)
    print(df2)

    # 紀錄更新時間
    _time = datetime.datetime.now()
    print("更新時間:" + str(_time.hour) + ":" + str(_time.minute))

    # show table
    # df = df.style.applymap(tableColor, subset=['漲跌百分比'])
    # print(df)

    start_time = datetime.datetime.strptime(str(_time.date()) + '9:30', '%Y-%m-%d%H:%M')
    end_time = datetime.datetime.strptime(str(_time.date()) + '13:30', '%Y-%m-%d%H:%M')

    # 判斷爬蟲終止條件
    if start_time <= _time <= end_time:
        s.enter(update_time, 0, stock_crawler, argument=(targets,))
    else:
        print("非交易時間，停止抓取資料...")

# 欲爬取的股票代碼
stock_list = ['1101',
              '1102',
              '1216',
              '1219',
              '1220',
              '1217',
              '1301',
              '1303',
              '1326',
              '1314',
              '1402',
              '1444',
              '1409',
              '1455',
              '1590',
              '1504',
              '2371',
              '1560',
              '1609',
              '1611',
              '1605',
              '1802',
              '1810',
              '1909',
              '1905',
              '2002',
              '2014',
              '2029',
              '2105',
              '2108',
              '2207',
              '2497',
              '2542',
              '2515',
              '2618',
              '2603',
              '2610',
              '2615',
              '2609',
              '5706',
              '2731',
              '2881',
              '2882',
              '2891',
              '2886',
              '2884',
              '2885',
              '2892',
              '2883',
              '2887',
              '2912',
              '8454',
              '2601',
              '2915',
              '1722',
              '1708',
              '1712',
              '1717',
              '1760',
              '4142',
              '4133',
              '2303',
              '2330',
              '2454',
              '3711',
              '3034',
              '2379',
              '2408',
              '2357',
              '2382',
              '4938',
              '2395',
              '6669',
              '3008',
              '3481',
              '2409',
              '6443',
              '6477',
              '2412',
              '3045',
              '4904',
              '2498',
              '2308',
              '2327',
              '8046',
              '3037',
              '8112',
              '3702',
              '2347',
              '2317',
              '2474',
              '2312',
              '3552',
              '6505',
              '5871',
              '9910',
              '9955',
              '9907',
              '0050',
              '0056']
# 每秒定時器
s.enter(1, 0, stock_crawler, argument=(stock_list,))
s.run()

