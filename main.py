from pconline import fetch_pconline
from pconline import analyze_pconline
from pc6 import fetch_pc6
from pc6 import analyze_pc6
from _3987 import fetch_3987
from _3987 import analyze_3987


if __name__ == "__main__":
    print('请选择下载站：')
    print('[1] 太平洋软件下载中心     [2]pc6下载站     [3]统一下载站')
    num = input()
    while num != '1' and num != '2' and num != '3':
        print('输入有误，请重新输入')
        print('请选择下载站：')
        print('[1] 太平洋软件下载中心     [2]pc6下载站     [3]统一下载站')
        num = input()
    else:
        if num == '1':
            while fetch_pconline().find('抱歉') != -1:
                print('未找到结果，请调整关键词重新输入')
            analyze_pconline()

        if num == '2':
            while fetch_pc6().find('抱歉') != -1:
                print('未找到结果，请调整关键词重新输入')
            analyze_pc6()

        if num == '3':
            while int(fetch_3987()[0].get_text()) == 0:
                print('未找到结果，请调整关键词重新输入')
            analyze_3987()

