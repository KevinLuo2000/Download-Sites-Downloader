from bs4 import BeautifulSoup
import requests


def fetch_pc6():
    global results, status, titles, infos, urls
    app_name = input('请输入软件名：\n').replace(' ', '+')
    url = 'http://s.pc6.com/?cid=pc&k={}'.format(app_name)
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    results = soup.select('#result')
    status = results[0].get_text()
    titles = soup.select('#result > dt > a')
    infos = soup.select('#result > dd > div > p.intro > span')
    urls = soup.select('#result > dd > div > p.addr > span.url')
    return status

def analyze_pc6():
    i = 1
    for title, info in zip(titles, infos):
        data = {
            '[' + str(i) + '] title': title.get_text().replace('\n', '').replace(' ', ''),
            'info': info.get_text().replace('\n', '').replace(' ', '')
        }
        print(data)
        i = i + 1
    choose = input('请选择您要下载的软件的数字编号：\n')
    target_url = urls[int(choose)-1].get_text()
    number = target_url.split('_')[1].split('.')[0]
    downurl = 'http://www.pc6.com/down.asp?id='+number
    print('下载地址如下：\n' + downurl)
