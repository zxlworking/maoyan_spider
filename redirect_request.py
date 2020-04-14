#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# def request(flow):
#     print("request host = ", flow.request.pretty_host)
#    if flow.request.pretty_host == 'www.baidu.com':
#        flow.request.host = '192.168.29.128'
#        flow.request.port = 8080
import platform


def request(flow):
    # flow.request.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    # flow.request.headers['Accept-Language'] = 'zh-CN,zh;q=0.9'

    sys_str = platform.system()
    if sys_str == 'Darwin':
        flow.request.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    elif sys_str == 'Windows':
        pass
    elif sys_str == 'Linux':
        flow.request.headers['User-Agent'] = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Mobile Safari/537.36'

    # flow.request.headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8'
    # flow.request.headers['Accept-Encoding'] = 'gzip, deflate'
    # flow.request.headers['Cache-Control'] = 'max-age=0'
    # flow.request.headers['Cookie'] = '_lxsdk_cuid=16c46760461c8-0b7dad8fe0c1ba-3f75065b-1fa400-16c46760461c8; iuuid=696E8210DB7411E99D75E3DD995277BC5E0CA61B5E9C495591E1DAA26C10213B; ci=55%2C%E5%8D%97%E4%BA%AC; __mta=252518070.1564550264183.1575345819156.1575345940846.56; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1586770524; __mta=252518070.1564550264183.1575594197141.1586770557358.79; webp=true; _lxsdk=19749EA07D6A11EA8C9A81FBF6E90933C386E56DAF7B435FA6E8C1646D4F7437; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1586773113; _lxsdk_s=17172e4b7dd-aa5-886-c7e%7C%7C30'

    print("request url = ", flow.request.url)
    print("request method = ", flow.request.method)
    # print("request headers = ", flow.request.headers)
    # if flow.request.url.startswith('https://maoyan.com'):
    #     print("request headers = ", flow.request.headers)
    # if 'bs/yoda-static/file' in flow.request.url:
    #     print('*' * 100)
    #     print(flow.request.url)
    #     flow.response.text = flow.response.text.replace("webdriver", "fuck_that")
    #     flow.response.text = flow.response.text.replace("Webdriver", "fuck_that")
    #     flow.response.text = flow.response.text.replace("WEBDRIVER", "fuck_that")
    # chang_ip()





def response(flow):
    if '爬虫' in flow.response.text:
        print("爬虫==========in==============", flow.request.url)
    print("response = ", flow.response.text)
    # if 'webdriver' in flow.response.text:
    #     print('*' * 100)
    #     print('find web_driver key')
    #     flow.response.text = flow.response.text.replace("webdriver", "fuck_that_1")
    # if 'Webdriver' in flow.response.text:
    #     print('*' * 100)
    #     print('find web_driver key')
    #     flow.response.text = flow.response.text.replace("Webdriver", "fuck_that_2")
    # if 'WEBDRIVER' in flow.response.text:
    #     print('*' * 100)
    #     print('find web_driver key')
    #     flow.response.text = flow.response.text.replace("WEBDRIVER", "fuck_that_3")
    # pass

    # print("response url = ", flow.request.url)
    # print("response url \n\n\n")

    # if flow.request.url == 'https://maoyan.com/films?showType=1':
    #     print(flow.response.text)

    # if 'bs/yoda-static' in flow.request.url:
    # print("response = ", flow.response.text)

    """修改应答数据"""
    # 屏蔽selenium检测
    for webdriver_key in ['webdriver', '__driver_evaluate', '__webdriver_evaluate', '__selenium_evaluate',
                          '__fxdriver_evaluate', '__driver_unwrapped', '__webdriver_unwrapped',
                          '__selenium_unwrapped', '__fxdriver_unwrapped', '_Selenium_IDE_Recorder', '_selenium',
                          'calledSelenium', '_WEBDRIVER_ELEM_CACHE', 'ChromeDriverw', 'driver-evaluate',
                          'webdriver-evaluate', 'selenium-evaluate', 'webdriverCommand',
                          'webdriver-evaluate-response', '__webdriverFunc', '__webdriver_script_fn',
                          '__$webdriverAsyncExecutor', '__lastWatirAlert', '__lastWatirConfirm',
                          '__lastWatirPrompt', '$chrome_asyncScriptInfo', '$cdc_asdjflasutopfhvcZLmcfl_']:
        if webdriver_key in flow.response.text:
            print(webdriver_key, "==========in==============", flow.request.url)
            flow.response.text = flow.response.text.replace(webdriver_key, 'userAgent')
    #     # ctx.log.info('Remove"{}"from{}.'.format(webdriver_key, flow.request.url))
    #     flow.response.text = flow.response.text.replace('"{}"'.format(webdriver_key), '"NO-SUCH-ATTR"')
    #     flow.response.text = flow.response.text.replace('t.webdriver', 'false')
    #     flow.response.text = flow.response.text.replace('ChromeDriver', '')
    #     flow.response.text = flow.response.text.replace('webdriver', 'userAgent')