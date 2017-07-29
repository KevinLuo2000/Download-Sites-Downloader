from bs4 import BeautifulSoup
import requests


def fetch_3987():
    global soup, results_number, titles, infos
    # another method of replacement
    # for i in range(len(app_name)):
    #     if app_name[i] == ' ':
    #         app_name = app_name[:i]+'+'+app_name[(i+1):]
    app_name = input('请输入软件名：\n').replace(' ', '+')
    url = 'http://www.3987.com/index.php?m=search&c=index&a=init&typeid=2&q={}'.format(app_name)
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    results_number = soup.select('#main > div > div.searchResult.fl > div.searchhead > span > font')
    titles = soup.select('#tabnew_0 > ul > li > dl > dt > a ')
    infos = soup.select('#tabnew_0 > ul > li > dl > dd.desc')
    return results_number


def analyze_3987():
    i = 1
    for title, info in zip(titles, infos):
        data = {
            '[' + str(i) + '] title': title.get_text(),
            'info': info.get_text()
        }
        print(data)
        i = i + 1
    choose = input('请选择您要下载的软件的数字编号：\n')
    css = '#tabnew_0 > ul > li:nth-of-type(' + choose + ') > a.btn-dl'
    downurls = soup.select(css)
    for downurl in downurls:
        print('下载地址如下：\n' + downurl["href"])
