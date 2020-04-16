#!/usr/bin/python
# coding=utf-8
import platform

from selenium import webdriver


class BaseRequest:

    @staticmethod
    def get_web_content(url):
        print("get_web_content::", url)
        #chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        chrome_driver = "/Users/zxl/Downloads/chromedriver"
        sys_str = platform.system()
        print("get_web_content::", sys_str)
        if sys_str == 'Darwin':
            chrome_driver = "/Users/zxl/Downloads/chromedriver"
        elif sys_str == 'Windows':
            chrome_driver = "D:\\my_github_workspace\\chromedriver.exe"
        elif sys_str == 'Linux':
            # chrome_driver = "/Users/zxl/Downloads/chromedriver"
            chrome_driver = "/home/mi/下载/chromedriver"

        # 创建chrome参数对象
        opt = webdriver.ChromeOptions()

        # opt.add_experimental_option('excludeSwitches', ['enable-automation'])

        # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
        # opt.set_headless()
        # opt.add_argument('--headless')
        opt.add_argument('--proxy-server=http://127.0.0.1:8080')

        opt.add_experimental_option('excludeSwitches', ['enable-automation'])

        pre_fs = {"profile.managed_default_content_settings.images": 2}
        opt.add_experimental_option("prefs", pre_fs)

        # 创建chrome无界面对象
        driver = webdriver.Chrome(executable_path=chrome_driver, options=opt)

        driver.maximize_window()

        driver.get(url)

        # while True:
        #     continue
        return driver
