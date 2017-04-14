# coding=utf-8

import HTMLParser
import urllib
import sys
import re
import os


# 定义HTML解析器
class parseLinks(HTMLParser.HTMLParser):
    # 该方法用来处理开始标签的，eg:<div id="main">
    def handle_starttag(self, tag, attrs):
        def _attr(attrlist, attrname):
            for each in attrlist:
                if attrname == each[0]:
                    return each[1]
            return None

        if tag == 'a' or tag == "li" or tag == "link":  # 如果为<a>标签
            # name为标签的属性名，如href、name、id、onClick等等
            for name, value in attrs:
                if name == 'href':  # 这时选择href属性
                    #print "name_value: ", value  # href属性的值
                    link_file.write(value)
                    link_file.write("\n")
                    #print "title: ", _attr(attrs, 'title')
                    #print "first tag:", self.get_starttag_text()  # <a>标签的开始tag
                    #print "\n"

def search_info(link, key):
    name = key
    text = urllib.urlopen(link).read()
    file_object = open("text.txt", "w")
    file_object.write(text)
    file_object.close()

    file_read = open("text.txt", "r")
    for line in file_read:
        if re.search(name, line):
            print line
            file_result.write(line)
            file_result.write("\n")
    file_read.close()


def deep_search(link, depth):
    lParser.feed(urllib.urlopen(link).read())

if __name__ == "__main__":
    #处理输入
    website = raw_input("请输入需要搜索的网站（exp:http://www.baidu.com）： ")
    key = raw_input("请输入需要搜索的关键字： ")
    print "需要查找的网站是：", website
    print "我知道了主人，您需要找关键字：", key
    # 创建HTML解析器的实例
    lParser = parseLinks()
    # 深度搜索子链接
    link_file = open("sub_link.txt", "w")
    deep_search("http://www.baidu.com", 10)
    link_file.close()

    # 查找子链接中的信息
    sub_link = open("sub_link.txt", "r")
    file_result = open("result.txt", "w")
    for sublink in sub_link:
        #print sublink
        if re.search("http", sublink):
            search_info(sublink, key)
    file_result.close()
    sub_link.close()

    lParser.close()
