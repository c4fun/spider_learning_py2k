# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

# 处理页面标签类
class Tool:
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()


# 百度贴吧爬虫类
class BaiduTieba:
    # 初始化，传入基地址，是否只看楼主的参数
    def __init__(self, baseUrl, seeLZ, floorTag):
        """
        baseUrl: The url of the main thread, not including the see_LZ or page number tag
        seeLZ: 1-to only see LZ, 2-to see all posts
        floorTag: 1-to add artificial floor in the saved file
        """
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.tool = Tool()
        self.floor = 1
        self.file = None
        self.defaultTitle = u'百度贴吧'
        self.floorTag = floorTag

    # 传入页码，获取该页帖子的代码
    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read()
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接百度贴吧失败,错误原因", e.reason
                return None

    # 获取帖子标题
    def getTitle(self, page):
        pattern = re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>', re.S)
        result = re.search(pattern, page)
        if result:
            # print result.group(1)  #测试输出
            return result.group(1).strip()
        else:
            return None

    # 获取帖子一共有多少页
    def getPageNum(self, page):
        pattern = re.compile('<li class="l_reply_num.*?<span.*?>(.*?)</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pattern, page)
        if result:
            # print result.group(2)  #测试输出
            return result.group(2).strip()
        else:
            return None

    # 获取每一层楼的内容,传入页面内容
    def getContent(self, page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            content = self.tool.replace(item)
            contents.append(content)
        return contents

    # 获取到默认标题
    def setFileTitle(self, title):
        if title is not None:
            self.file = open(title + '.txt', 'w+')
        else:
            self.file = open(self.defaultTitle + '.txt', 'w+')

    def writeData(self, contents):
        for item in contents:
            if self.floorTag == 1:
                self.file.write("\nFloor" + str(self.floor) + "-" * 70 + "\n")
            self.file.write(item)
            self.floor += 1


    # Start to get all information in the text
    def start(self):
        indexPage = self.getPage(1)
        pageTitle = self.getTitle(indexPage)
        self.setFileTitle(pageTitle)

        pageNum = self.getPageNum(indexPage)
        if pageNum == None:
            print u"页面已经失效"
            return
        try:
            print u"该帖子一共有" + str(pageNum) + u"页"
            for eachPageNumber in range(1, int(pageNum)+1):
                print u"正在写入第" + str(eachPageNumber) + u"页数据......"
                page = self.getPage(eachPageNumber)
                contents = self.getContent(page)
                self.writeData(contents)
        except IOError, e:
            print u"写入异常" + e.message
        finally:
            print u"写入成功"





if __name__ == '__main__':
    # baseURL = (u"请输入帖子代号")
    baseURL = 'http://tieba.baidu.com/p/3138733512'
    bdtb = BaiduTieba(baseURL, 1, 1)
    bdtb.start()
