# -*- coding:utf-8 -*-
import urllib2
from urllib2 import Request, urlopen, URLError
import openPageWithProxy


class MainPage:
    def __init__(self, URL=None):
        self.main_page_url = URL
        pass

    def set_url(self, URL):
        self.main_page_url = URL
        pass

    def show_url_content(self):
        header_info = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Proxy-Connection': 'keep-alive',
            'Connection': 'keep-alive'
        }
        req = Request(self.main_page_url, headers=header_info)
        try:
            response = urlopen(req)
            content = response.read()
            # print type(content) yield <type 'str'>
            # todo 在写入内容之前先正则表达式处理一下
            # 处理包含： 搜索到相应的关键词对应的标题。保存下相应的标题&URL
            self.writeContent(content, 'OpenMainPageResult.html')
        except URLError, e:
            if hasattr(e, 'code'):
                print "The server couldn\'t fulfill the request."
                print "Error code: ", e.code
            if hasattr(e, 'reason'):
                print "We failed to reach a server."
                print "Error code: ", e.reason
        else:
            print "No exception was raised."

    def writeContent(self, contents, fileName):
        f = open(fileName, "w+")
        f.write(contents)
        f.close()


if __name__ == '__main__':
    proxy_setting = openPageWithProxy.setup_proxy_opener()
    url_to_open = '******'
    new_main_page = MainPage(url_to_open)
    new_main_page.show_url_content()
