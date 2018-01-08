# -*- coding: utf-8 -*-
"""
# @Time    : 2018/1/8 下午4:16
# @Author  : zhanzecheng
# @File    : xiushibaike_spider.py
# @Software: PyCharm
"""
'''
使用了正则表达式的方法爬取了糗事百科的文字，并利用面向对象的方法来重构代码
'''
import urllib
import urllib2
import cookielib
import re
# page = 1
# url = 'http://www.qiushibaike.com/hot/page/' + str(page)
# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# headers = {'User-Agent' : user_agent}
# try:
#     request = urllib2.Request(url, headers=headers)
#     response = urllib2.urlopen(request)
#     content =  response.read().decode('utf-8')
#     #pattern = re.compile('h2>(.*?)</h2.*?content">(.*?)</.*?number">(.*?)</',re.S)
#     pattern = re.compile('<h2>(.*?)</h2.*?class="content">.*?<span>..(.*?)</.*?number">(.*?)</',re.S)
#     items = re.findall(pattern, content)
#     for count, item in enumerate(items):
#         print item[0].strip(), item[1], item[2]
#         quit()
# except urllib2.URLError, e:
#     if hasattr(e, 'code'):
#         print(e.code)
#     if hasattr(e, 'reason'):
#         print(e.reason)

class QSBK:

    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent' : self.user_agent}
        self.stories = []
        self.enable = False

    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')
            return content
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print(u"connected false", e.reason)
            return None

    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print '页面加载失败...'
            return None
        pattern = re.compile('<h2>(.*?)</h2.*?class="content">.*?<span>..(.*?)</.*?number">(.*?)</', re.S)
        items = re.findall(pattern, pageCode)
        pageStories =[]
        for item in items:
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR, "\n", item[1])
            pageStories.append([item[0].strip(), text.strip(), item[2].strip()])
        return pageStories

    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    def getOneStory(self, pageStories, page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == 'Q':
                self.enable = False
                return
            print u'a: %d, %s, %s, %s' %(page, story[0], story[1], story[2])

    def start(self):
        print(u'正在开始读取百科，按回车重新查看段子，Q键退出')
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories, nowPage)

spider = QSBK()
spider.start()