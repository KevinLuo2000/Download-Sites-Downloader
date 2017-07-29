from bs4 import BeautifulSoup
import requests
import re


def fetch_pconline():
    global titles, urls, result
    app_name = input('请输入软件名：\n').replace(' ', '+').encode('gb2312')
    app_name_ = str(app_name).split('\'')[1].replace('\\x', '%')
    url_begin = 'http://ks.pconline.com.cn/download.shtml?q={}&downloadType=%C8%ED%BC%FE%CF%C2%D4%D8'.format(app_name_)
    wb_data = requests.get(url_begin)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    result = soup.select('#Jwrap > div.main > div > div')[0].get_text()
    titles = soup.select('#Jwrap > div.main > div.col-ab > div.dl-list > div > dl > dt > a')
    urls = soup.select('#Jwrap > div.main > div.col-ab > div.dl-list > div > dl > dt > a')
    return result


def analyze_pconline():
    infos = []
    downurl = []
    for url in urls:
        url = url.get('href')
        wb_data_1 = requests.get(url)
        soup_1 = BeautifulSoup(wb_data_1.text, 'lxml')
        info_select = soup_1.select('#JsoftDes > div.tab-wrap > div > div')[0]
        if len(info_select.get_text()) >= 109:
            infos.append(info_select.get_text()[:109].replace('\n', '').replace('\r', '').replace('\t', '') + '......')
        else:
            infos.append(info_select.get_text().replace('\n', '').replace('\r', '').replace('\t', ''))

        direct = soup_1.select('#Jnavi > div.navi-top > div > a')[0].get('onclick')
        print(direct)
        number = direct.split('\'')[3]
        downurl.append(str(url)[:-5] + number)

    i = 1
    for title, info in zip(titles, infos):
        data = {
            '[' + str(i) + '] title': title.get('title').replace('\n', ''),
            'info': info,
        }
        print(data)
        i += 1
    choose = input('请选择您要下载的软件的数字编号：\n')
    downurl_choose = downurl[int(choose)-1]
    wb_data_choose = requests.get(downurl_choose)
    soup_choose = BeautifulSoup(wb_data_choose.text, 'lxml')
    prepared = soup_choose.select('#Jwrap > div.area.sc-1 > div.col-ab > div.soft-msg > div > div.link-area > div.link-area-item > div.link-area-wrap > div.links > p.mb10 > span.links-wrap > a')
    carrier_url = 'http://whois.pconline.com.cn/ipJson.jsp?callback=checkComm&callback=checkComm'
    wb_data_carrier = requests.get(carrier_url)
    soup_carrier = BeautifulSoup(wb_data_carrier.text, 'lxml')
    if str(prepared) != '[]':
        if (str(soup_carrier).find('网通') != -1) or (str(soup_carrier).find('联通') != -1):
            downurl_final = str(prepared).split(',')[3].split('\"')[5]
        else:
            downurl_final = str(prepared).split(',')[0].split('\"')[5]
    else:
        print('暂无下载地址')
        return
    url_js = soup_choose.find('script', {'src': re.compile('http://dlc2.pconline.com.cn/dltoken/[0-9]+_genLink.js')}).get('src')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Referer": "{}".format(urls[int(choose)-1].get('href'))
    }
    wb_data_js = requests.get(url_js, headers=headers)
    soup_js = BeautifulSoup(wb_data_js.text, 'lxml')
    code = str(soup_js).split('\'')[1]
    downurl_ultimate = downurl_final.rsplit('/', 1)
    downurl_ultimate = downurl_ultimate[0]+'/'+code+'/'+downurl_ultimate[1]
    print('下载地址如下：\n' + downurl_ultimate)

