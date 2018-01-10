# -*- coding: utf-8 -*-
"""
# @Time    : 2018/1/9 上午11:33
# @Author  : zhanzecheng
# @File    : baidutieba_spider.py
# @Software: PyCharm
"""

import urllib2
import urllib
import re

class Tool:
    def __init__(self):
        self.removeImg = re.compile('<img.*?>| {7}|')
        self.removeAddr = re.compile('<a.*?>|</a>')
        self.replaceLine = re.compile('<br>|<div>|</div>|<p>')
        self.replaceTD = re.compile('<td>')
        self.replacePara = re.compile('<p.*?>')
        self.replaceBR = re.compile('<br><br>|<br>')
        self.removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()
class BDTB:

    def __init__(self, baseURL, seeLZ):
        self.baseURL = baseURL
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.tool = Tool()
    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            # print(response.read())
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print(u'连接贴吧失败', e.reason)
                return None

    def getTitle(self):
        page = self.getPage(1)
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        result = re.search(pattern, page)
        if result:
            print result.group(1)
            return result.group(1).strip()
        else:
            return None

    def getPageNum(self):
        page = self.getPage(1)
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pattern, page)
        if result:
            print result.group(1)
            return result.group(1).strip()
        else:
            return None
    def getContent(self, page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        for item in items:
            print self.tool.replace(item)
if __name__ == '__main__':
    baseURL = 'http://tieba.baidu.com/p/3138733512'
    bdtb = BDTB(baseURL, 1)
    bdtb.getTitle()
    bdtb.getPageNum()
    bdtb.getContent(bdtb.getPage(2))