
# encoding=utf-8
# coding=utf-8
import urllib, urllib2
from bs4 import BeautifulSoup
import re
import os
import string
import shutil


# 得到url的list
def get_url_list(purl):
    # 连接
    req = urllib2.Request(purl, headers={'User-Agent': "Magic Browser"})
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page.read())
    # 读取标签
    a_div = soup.find('div', {'class': 'main'})
    b_div = a_div.find('div', {'class': 'left'})
    c_div = b_div.find('div', {'class': 'newsList'})

    links4 = []
    # 得到url的list
    for link_aa in c_div:
        for link_bb in link_aa:
            links4.append(link_bb.find('a'))

    links4 = list(set(links4))
    links4.remove(-1)
    links4.remove(None)

    return links4


# 从list中找到想要的新闻链接
# 找到要访问的下一个页面的url
def get_url(links):
    url = []
    url2 = ''
    url3 = ''
    url4 = ''

    i = 0

    for link in links:

        if link.contents == [u'后一天']:
            continue

        # 上一页  和  下一页 的标签情况比较复杂
        # 取出“上一页”标签的url（貌似不管用）
        if str(link.contents).find(u'/> ') != -1:
            continue

        # 取出“下一页”标签的url
        if str(link.contents).find(u' <img') != -1:
            url2 = link.get("href")
            i = 1
            continue

        if link.contents == [u'前一天']:
            url3 = link.get("href")
            continue

        url.append(link.get("href"))

    if (i == 1):
        url4 = url2
    else:
        url4 = url3

    return url, url4


def main():
    link_url = []
    link_url_all = []
    link_url_all_temp = []

    next_url = ''

    # 开始的url
    purl = 'http://news.ifeng.com/listpage/11502/0/1/rtlist.shtml'
    link_url = get_url_list(purl)
    link_url_all, next_url = get_url(link_url)

    # 做了10次循环
    for i in range(2):
        link_url = get_url_list(next_url)
        link_url_all_temp, next_url = get_url(link_url)

        link_url_all = link_url_all + link_url_all_temp

    # 将全部url存档
    path = './url.txt'
    fp = open(path, 'w')
    for link in link_url_all:
        fp.write(str(link) + '\n')
    fp.close()

def clean():
    my_cn = ""
    ss = ""
    kk_encode = ""
    kk = ""
    a_div = ""
    b_div = ""
    cnt = ""

if __name__ == '__main__':
    if os.path.isfile("./url.txt"):
        os.remove("./url.txt")
    main()
    links = []
    kk_encode = ""

    path = './url.txt'
    file = open(path, 'r')

    # 得到url
    for line in file:
        links = links + [line]

    file.close()

    print len(links)

    i = 1
    if os.path.exists("./webtext/"):
        shutil.rmtree("./webtext/")
    os.mkdir("./webtext/")

    for link in links:
        print link
        kk_encode = "hello world"
        req = urllib2.Request(link, headers={'User-Agent': "Magic Browser"})
        page = urllib2.urlopen(req)
        respond = page.read()
        soup = BeautifulSoup(respond)

        a_div = soup.find('div', {'id': 'artical_real'}, {'class': 'js_img_share_area'})
        if a_div == None:
            #clean()
            continue
        b_div = a_div.find('div', {'id': 'main_content'}, {'class': 'js_selection_area'})
        if b_div == None:
            #clean()
            continue
        kk = b_div.find_all('p')
        if kk == []:
            #clean()
            continue
        for cnt in kk:
            #print cnt.encode('utf-8')
            kk_encode = kk_encode + str(cnt.encode('utf-8'))
        flag = kk_encode.find("人民的名义")
        if flag == -1:
            #clean()
            continue

        print "find ####################################！！！！！！！！！！！！！！！！"

        ss = str(kk_encode)
        ss = ''.join(ss)

        my_cn = re.sub('<span(.*?)</span>', '', ss)

        my_cn = ''.join(my_cn)
        my_cn = re.sub('<a(.*?)</a>', '', my_cn)

        my_cn = ''.join(my_cn)
        my_cn = re.sub('<strong>(.*?)</strong>', '', my_cn)

        my_cn = ''.join(my_cn)
        my_cn = re.findall('<p>(.*?)</p>', my_cn)

        my_cn = ''.join(my_cn)

        pth = './webtext/' + str(i) + '.txt'
        fp = open(pth, 'w')
        fp.writelines(my_cn)
        fp.close()

        i = i + 1
        page.close()
        #clean()