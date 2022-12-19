import requests
from bs4 import BeautifulSoup
import datetime
import os
import requests
import time
import slackweb


slack  = slackweb.Slack(url='https://hooks.slack.com/services/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')
dict_keyball = {
        'keyball44': ['https://shirogane-lab.com/products/keyball44', '#price-template--15303865303085__main', None],
        'keyball39': ['https://shirogane-lab.com/products/keyball39', '#price-template--14679726325805__main', None],
        'keyball61': ['https://shirogane-lab.com/products/keyball61', '#price-template--14536341848109__main', None],
        }



def scraping(name, url, select):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    result = soup.select(select)
    return result


def comp_result(before, after, name):
    is_difference = before!=after
    txt = f'[{time.ctime()}][{name}]:{"difference" if is_difference else "same"}'
    print(txt)
    return is_difference


def notify_slack(name, url):
    slack.notify(text=f'{name} が更新されたぽいよ！\n{url}')


def main():
    idx = 0
    keys = dict_keyball.keys()
    while True:
        for key in keys:
            list_ = dict_keyball[key]
            before_result = list_[2]

            result = scraping(key, list_[0], list_[1])
            is_difference = comp_result(before_result, result, key)

            # 更新
            list_[2] = result

            # 通知
            print(idx, is_difference)
            if idx!=0 and is_difference:
                notify_slack(key, list_[0])
        idx += 1
        time.sleep(60)


if __name__=="__main__":
    main()
