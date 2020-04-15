#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# def request(flow):
#     print("request host = ", flow.request.pretty_host)
#    if flow.request.pretty_host == 'www.baidu.com':
#        flow.request.host = '192.168.29.128'
#        flow.request.port = 8080
import platform


def request(flow):
    sys_str = platform.system()
    if sys_str == 'Darwin':
        flow.request.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    elif sys_str == 'Windows':
        pass
    elif sys_str == 'Linux':
        flow.request.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

    # flow.request.headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8'
    # flow.request.headers['Accept-Encoding'] = 'gzip, deflate'
    # flow.request.headers['Cache-Control'] = 'max-age=0'
    # flow.request.headers['Cookie'] = '_lxsdk_cuid=16c46760461c8-0b7dad8fe0c1ba-3f75065b-1fa400-16c46760461c8; iuuid=696E8210DB7411E99D75E3DD995277BC5E0CA61B5E9C495591E1DAA26C10213B; ci=55%2C%E5%8D%97%E4%BA%AC; __mta=252518070.1564550264183.1575345819156.1575345940846.56; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1586770524; __mta=252518070.1564550264183.1575594197141.1586770557358.79; webp=true; _lxsdk=19749EA07D6A11EA8C9A81FBF6E90933C386E56DAF7B435FA6E8C1646D4F7437; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1586773113; _lxsdk_s=17172e4b7dd-aa5-886-c7e%7C%7C30'

    #print("request url = ", flow.request.url)
    #print("request method = ", flow.request.method)

    print("\n\nrequest-------------------start------------------------------")
    print("request--->flow.request.url = ", flow.request.url)
    print("request--->flow.request.method = ", flow.request.method)
    print("request--->flow.request.headers = ", flow.request.headers)
    print("request--->flow.request.get_text = ", flow.request.get_text())
    print("request-------------------end------------------------------\n\n")
    # if flow.request.url.startswith('https://passport.meituan.com/account'):
    #     cookie = flow.request.headers['Cookie']
    #     cookie_file = open('mao_yan_cookie.txt', 'wb')
    #     cookie_file.write(cookie.encode())
    #     cookie_file.close()
    # if flow.request.url.startswith('https://maoyan.com/films'):
    #     cookie_file = open('mao_yan_cookie.txt', 'wb')
    #     flow.request.headers['Cookie'] = cookie_file.read()
    #     cookie_file.close()



def response(flow):
    print("\n\nresponse*******************start*******************")
    print("response--->flow.request.url = ", flow.request.url)
    print("response--->flow.response.headers = ", flow.response.headers)
    print("response--->flow.response.text = ", flow.response.text)
    print("response*******************end*******************\n\n")
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
        # print("webdriver_key==============", webdriver_key)
        if webdriver_key in flow.response.text:
            print(webdriver_key, "==========in==============", flow.request.url)
    #         # flow.response.text = flow.response.text.replace(webdriver_key, 'userAgent')
    #     # ctx.log.info('Remove"{}"from{}.'.format(webdriver_key, flow.request.url))
    #     # flow.response.text = flow.response.text.replace('"{}"'.format(webdriver_key), '"NO-SUCH-ATTR"')
    #     # flow.response.text = flow.response.text.replace('t.webdriver', 'false')
    #     # flow.response.text = flow.response.text.replace('ChromeDriver', '')
    #     # flow.response.text = flow.response.text.replace('webdriver', 'userAgent')

    if flow.request.url.startswith('https://verify.meituan.com/v2/ext_api/spiderindefence/verify'):
        flow.response.text = '{"status":1,"data":{"response_code":"9c8cbc4b68a848d5970ca3ee8c10c549"},"error":null}'

    if flow.request.url.startswith('http://maoyan.com/films?showType=1'):
        flow.response.text = flow.response.text.replace("('Location', '*')", "('Location', 'http://maoyan.com/films?showType=1')")

    print("\n\n")
    if flow.request.url.startswith('https://static.meituan.net/bs/yoda-static/file:file/d/js/slider.91b17a4b2b.js'):
        print("__webdriver_script_fn--->in--->", "__webdriver_script_fn" in flow.response.text)
        if "__webdriver_script_fn" in flow.response.text:
            print("==========__webdriver_script_fn in==============", flow.request.url)
            flow.response.text = flow.response.text.replace("__webdriver_script_fn", 'zxl')
            print("==========__webdriver_script_fn in==============", "__webdriver_script_fn" in flow.response.text)
            print("\n\n")

        print("__$webdriverAsyncExecutor--->in--->", "__$webdriverAsyncExecutor" in flow.response.text)
        if "__$webdriverAsyncExecutor" in flow.response.text:
            print("==========__$webdriverAsyncExecutor in==============", flow.request.url)
            flow.response.text = flow.response.text.replace("__$webdriverAsyncExecutor", 'zxl')
            print("==========__$webdriverAsyncExecutor in==============", "__$webdriverAsyncExecutor" in flow.response.text)
            print("\n\n")

        print("webdriver,_Selenium_IDE_Recorder,_selenium,calledSelenium--->in--->", "webdriver,_Selenium_IDE_Recorder,_selenium,calledSelenium" in flow.response.text)
        if "webdriver,_Selenium_IDE_Recorder,_selenium,calledSelenium" in flow.response.text:
            print("==========webdriver,_Selenium_IDE_Recorder,_selenium,calledSelenium in==============", flow.request.url)
            flow.response.text = flow.response.text.replace("webdriver,_Selenium_IDE_Recorder,_selenium,calledSelenium", 'zxl')
            print("==========webdriver,_Selenium_IDE_Recorder,_selenium,calledSelenium in==============", "webdriver,_Selenium_IDE_Recorder,_selenium,calledSelenium" in flow.response.text)
            print("\n\n")

        print("ChromeDriverwjers908fljsdf37459fsdfgdfwru--->in--->", "ChromeDriverwjers908fljsdf37459fsdfgdfwru" in flow.response.text)
        if "ChromeDriverwjers908fljsdf37459fsdfgdfwru" in flow.response.text:
            print("==========ChromeDriverwjers908fljsdf37459fsdfgdfwru in==============", flow.request.url)
            flow.response.text = flow.response.text.replace("ChromeDriverwjers908fljsdf37459fsdfgdfwru", 'zxl')
            print("==========ChromeDriverwjers908fljsdf37459fsdfgdfwru in==============", "ChromeDriverwjers908fljsdf37459fsdfgdfwru" in flow.response.text)
            print("\n\n")

        print("__lastWatirAlert--->in--->", "__lastWatirAlert" in flow.response.text)
        if "__lastWatirAlert" in flow.response.text:
            print("==========__lastWatirAlert in==============", flow.request.url)
            flow.response.text = flow.response.text.replace("__lastWatirAlert", 'zxl')
            print("==========__lastWatirAlert in==============", "ChromeDriverwjers908fljsdf37459fsdfgdfwru" in flow.response.text)
            print("\n\n")

        print("navigator.webdriver--->in--->", "navigator.webdriver" in flow.response.text)
        print('navigator.webdriver ? "gw" : ""', 'navigator.webdriver ? "gw" : ""' in flow.response.text)
        if 'navigator.webdriver ? "gw" : ""' in flow.response.text:
            print("==========navigator in==============", flow.request.url)
            flow.response.text = flow.response.text.replace('navigator.webdriver ? "gw" : ""', '')
            print("==========navigator in==============" in flow.response.text)
            print("\n\n")
