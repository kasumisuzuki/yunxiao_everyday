import schedule
import datetime
import time

import main

# 用户名密码
USERNAME = ""
PASSWORD = ""

if __name__ == '__main__':
    print('开始运行')
    def job(t):
        nowtime = str(datetime.datetime.now())
        print(t)
        print(nowtime)
        main.go(USERNAME, PASSWORD)
    # 执行时间 这边可以设置多个时间点
    for i in ["09:30"]:
        schedule.every().monday.at(i).do(job, i)
        schedule.every().tuesday.at(i).do(job, i)
        schedule.every().wednesday.at(i).do(job, i)
        schedule.every().thursday.at(i).do(job, i)
        schedule.every().friday.at(i).do(job, i)
        # schedule.every().saturday.at(i).do(job, i)
    while True:
        schedule.run_pending()
        time.sleep(1)
