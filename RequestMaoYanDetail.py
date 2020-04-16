#!/usr/bin/python
# coding=utf-8
import base64
import json
import os
import re
import time
from pathlib import Path
from urllib import request

import PIL.Image, PIL.ImageFont, PIL.ImageDraw
import requests
from fontTools.ttLib import TTFont
from pytesseract import pytesseract
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from com_zxl_knn_font.knn_font import classifyPerson
from com_zxl_spider_data.MaoYanAwardBean import MaoYanAwardBean
from com_zxl_spider_data.MaoYanCelebrityBean import MaoYanCelebrityBean
from com_zxl_spider_data.MaoYanCommentBean import MaoYanCommentBean
from com_zxl_spider_data.MaoYanDetailBean import MaoYanDetailBean
from com_zxl_spider_data.MaoYanImgCollectionBean import MaoYanImgCollectionBean
from com_zxl_spider_db.MaoYanAwardDB import MaoYanAwardDB
from com_zxl_spider_db.MaoYanCelebrityDB import MaoYanCelebrityDB
from com_zxl_spider_db.MaoYanCommentDB import MaoYanCommentDB
from com_zxl_spider_db.MaoYanDB import MaoYanDB
from com_zxl_spider_db.MaoYanDetailDB import MaoYanDetailDB
from com_zxl_spider_db.MaoYanImgCollectionDB import MaoYanImgCollectionDB
from com_zxl_spider_request.BaseRequest import BaseRequest


class RequestMaoYanDetail(BaseRequest):

    fontdict = {'uniE997': '0', 'uniEE22': '8', 'uniE526': '9', 'uniF652': '2', 'uniE811': '6', 'uniE635': '3', 'uniF85A': '1', 'uniE6D4': '4', 'uniE9C8': '5', 'uniEA6D': '7'}


    parent_path = ''

    font_dict = {}

    def __init__(self):
        pass

    def request(self, movie_id, movie_detail_url):
        print("request::movie_id = %s " % movie_id)
        print("request::movie_detail_url = %s " % movie_detail_url)

        driver = self.get_web_content(movie_detail_url)

        # driver = self.login_mao_yan()
        # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')  # 触发ctrl + t
        # time.sleep(5)
        # driver.get(movie_detail_url)

        try:
            box_wrapper_path = "//div[@class='box-wrapper ']"
            box_wrapper_object = WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, box_wrapper_path)))
            print("box_wrapper_object = ", box_wrapper_object)

            if box_wrapper_object is not None:
                # print("box_wrapper_object.get_attribute = ", box_wrapper_object.get_attribute('outerHTML'))
                boxStatic_path = "//div[@class='boxStatic ']"
                boxStatic_object = box_wrapper_object.find_element_by_xpath(boxStatic_path)

                moveingBar_path = "//div[@class='moveingBar ']"
                moveingBar_object = box_wrapper_object.find_element_by_xpath(moveingBar_path)

                ActionChains(driver).click_and_hold(boxStatic_object).perform()
                while True:
                        ActionChains(driver).move_by_offset(50, 0).perform()
                        # print("boxStatic_object.get_attribute = ", boxStatic_object.get_attribute('style'))
                        # print("moveingBar_object.get_attribute = ", moveingBar_object.get_attribute('style'))
                        print("box_wrapper_object.get_attribute = ", box_wrapper_object.get_attribute('outerHTML'))
        except Exception as no_box_wrapper_exception:
            print("no_box_wrapper_exception = ", no_box_wrapper_exception)

        page_content = driver.page_source
        print(page_content)

        try:
            movie_detail_path = "//div[@class='banner']"

            # banner_object = WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located((By.XPATH, movie_detail_path)))
            # print("banner_object = ", banner_object)

            movie_detail_object = driver.find_element_by_xpath(movie_detail_path)
            # print("movie_detail_object = ", movie_detail_object)

            find_result = re.findall(r'.*?url\(\'(.*?)\'\).*?', page_content)
            if len(find_result) > 0:
                for woff_url in find_result:
                    if 'woff' in woff_url:
                        woff_url = "http:" + woff_url
                        # print("woff_url--->", woff_url)
                        font_request = request.Request(woff_url)
                        font_res = request.urlopen(font_request)
                        font_respoen = font_res.read()
                        font_file = open(self.parent_path + 'mao_yan_font.woff', 'wb')
                        font_file.write(font_respoen)
                        font_file.close()
                        woff_font = TTFont(self.parent_path + "mao_yan_font.woff")
                        woff_font.saveXML(self.parent_path + "mao_yan_font.xml")

                        base_font = TTFont(self.parent_path + 'mao_yan_font.woff')
                        base_list = base_font.getGlyphOrder()[2:]

                        for font in base_list:
                            coordinate = base_font['glyf'][font].coordinates
                            font_0 = [i for item in coordinate for i in item]
                            # print(font_0)
                            self.font_dict[font] = classifyPerson(font_0)
                        print("font_dict = ", self.font_dict)

            movie_avatar_url = ''
            try:
                movie_avatar_path = ".//img[@class='avatar']"
                movie_avatar_object = movie_detail_object.find_element_by_xpath(movie_avatar_path)
                movie_avatar_url = movie_avatar_object.get_attribute("src")
                if '@' in movie_avatar_url:
                    movie_avatar_url = movie_avatar_url.split('@')[0]
            except NoSuchElementException as no_avatar_url_exception:
                print("no_avatar_url_exception = ", no_avatar_url_exception)

            movie_introduce_path = ".//div[@class='celeInfo-right clearfix']"
            movie_introduce_object = movie_detail_object.find_element_by_xpath(movie_introduce_path)

            movie_brief_path = ".//div[@class='movie-brief-container']"
            movie_brief_object = movie_introduce_object.find_element_by_xpath(movie_brief_path)

            movie_name = ''
            try:
                movie_name_path = ".//h3[@class='name']"
                movie_name_object = movie_brief_object.find_element_by_xpath(movie_name_path)
                movie_name = movie_name_object.text
            except NoSuchElementException as no_movie_name_exception:
                print("no_movie_name_exception = ", no_movie_name_exception)

            movie_en_name = ''
            try:
                movie_en_name_path = ".//div[@class='ename ellipsis']"
                movie_en_name_object = movie_brief_object.find_element_by_xpath(movie_en_name_path)
                movie_en_name = movie_en_name_object.text
            except NoSuchElementException as no_movie_en_name_exception:
                print("no_movie_en_name_exception = ", no_movie_en_name_exception)

            movie_category = ''
            movie_country = ''
            movie_duration = ''
            movie_release_info = ''

            try:
                movie_brief_info_list_path = ".//li"
                movie_brief_info_list_object = movie_brief_object.find_elements_by_xpath(movie_brief_info_list_path)

                if len(movie_brief_info_list_object) > 0:
                    movie_category = movie_brief_info_list_object[0].text
                if len(movie_brief_info_list_object) > 1:
                    temp_str = movie_brief_info_list_object[1].text
                    movie_country = temp_str
                    if "/" in temp_str:
                        temp_str = temp_str.replace(" ", "")
                        temp_str = temp_str.split("/")
                        if len(temp_str) > 1:
                            movie_country = temp_str[0]
                            movie_duration = temp_str[1]
                movie_release_time = ''
                movie_release_area = ''
                if len(movie_brief_info_list_object) > 2:
                    movie_release_info = movie_brief_info_list_object[2].text
                    movie_release_info_find_result = re.findall('(\\d+.*?\\d+.*?\\d+.*?\\d+.*?\\d+)(.+)',
                                                                movie_release_info, re.S)
                    # print("movie_release_info_find_result = ", movie_release_info_find_result)
                    if len(movie_release_info_find_result) > 0 and len(movie_release_info_find_result[0]) > 1:
                        movie_release_time = movie_release_info_find_result[0][0]
                        movie_release_area = movie_release_info_find_result[0][1]
            except NoSuchElementException as no_release_exception:
                print("no_release_exception = ", no_release_exception)

            movie_stats_path = ".//div[@class='movie-stats-container']"
            movie_stats_object = movie_introduce_object.find_element_by_xpath(movie_stats_path)

            movie_want_to_see_count = ''
            try:
                movie_want_to_see_content_path = ".//span[@class='index-left info-num one-line']"
                movie_want_to_see_content_object = movie_stats_object.find_element_by_xpath(movie_want_to_see_content_path)
                movie_want_to_see_count_path = ".//span"
                movie_want_to_see_count_object = movie_want_to_see_content_object.find_element_by_xpath(movie_want_to_see_count_path)
                movie_want_to_see_count = self.get_mao_yan_num_by_object(movie_want_to_see_count_object, 'mao_yan_font.woff', self.parent_path + "want_to_see.png")
                for font_content_item in movie_want_to_see_count_object:
                    print("zxl--->font_content_item--->"+font_content_item)
                    print("zxl--->font_dict.get--->"+self.font_dict.get(font_content_item))
            except NoSuchElementException as no_movie_want_to_see_content_exception:
                print("no_movie_want_to_see_content_exception = ", no_movie_want_to_see_content_exception)
                pass

            movie_score_content = ''
            try:
                movie_score_path = ".//span[@class='index-left info-num ']"
                movie_score_object = movie_stats_object.find_element_by_xpath(movie_score_path)
                print("movie_score_object.innerHTML = ", movie_score_object.get_attribute('innerHTML'))
                movie_score_content_path = ".//span"
                movie_score_content_object = movie_score_object.find_element_by_xpath(movie_score_content_path)
                # movie_score_content = self.get_mao_yan_num(woff_url, movie_score_content_object.text, self.parent_path + "score.png")
                movie_score_content = self.get_mao_yan_num_by_object(movie_score_content_object, 'mao_yan_font.woff', self.parent_path + "score.png")
            except NoSuchElementException as no_movie_score_content_exception:
                print("no_movie_score_content_exception = ", no_movie_score_content_exception)

            if movie_score_content == '-1':
                print("exit movie_score_content = ", movie_score_content)
                driver.close()
                return '-1'

            movie_stats_people_count_content = ''
            movie_stats_people_count_unit_content = ''
            try:
                movie_stats_people_count_parent_path = ".//span[@class='score-num']"
                movie_stats_people_count_parent_object = movie_stats_object.find_element_by_xpath(
                    movie_stats_people_count_parent_path)
                movie_stats_people_count_path = ".//span"
                movie_stats_people_count_object = movie_stats_people_count_parent_object.find_element_by_xpath(
                    movie_stats_people_count_path)
                # movie_stats_people_count_content = self.get_mao_yan_num(woff_url, movie_stats_people_count_object.text, self.parent_path + "stats_people_count.png")
                movie_stats_people_count_content = self.get_mao_yan_num_by_object(movie_stats_people_count_object, 'mao_yan_font.woff', self.parent_path + "stats_people_count.png")
                temp_movie_stats_people_count_unit_content = movie_stats_people_count_object.text
                # print("movie_stats_people_count_content = ", movie_stats_people_count_content,
                #       len(movie_stats_people_count_content))
                # print("temp_movie_stats_people_count_unit_content = ", temp_movie_stats_people_count_unit_content,
                #       len(temp_movie_stats_people_count_unit_content))
                if len(movie_stats_people_count_content) == len(temp_movie_stats_people_count_unit_content):
                    movie_stats_people_count_unit_content = ''
                else:
                    movie_stats_people_count_unit_content = temp_movie_stats_people_count_unit_content[
                                                            len(temp_movie_stats_people_count_unit_content) - 1:len(
                                                                temp_movie_stats_people_count_unit_content)]
            except NoSuchElementException as no_movie_stats_people_count_content_exception:
                print("no_movie_stats_people_count_content_exception = ", no_movie_stats_people_count_content_exception)

            if movie_stats_people_count_content == '-1':
                print("exit movie_stats_people_count_content = ", movie_score_content)
                driver.close()
                return '-1'

            movie_box_value_content = ''
            movie_box_unit_content = ''
            try:
                movie_box_path = ".//div[@class='movie-index-content box']"
                movie_box_object = movie_stats_object.find_element_by_xpath(movie_box_path)

                movie_box_value_path = ".//span[@class='stonefont']"
                movie_box_value_object = movie_box_object.find_element_by_xpath(movie_box_value_path)
                # movie_box_value_content = self.get_mao_yan_num(woff_url, movie_box_value_object.text, self.parent_path + "box.png")
                movie_box_value_content = self.get_mao_yan_num_by_object(movie_box_value_object, 'mao_yan_font.woff', self.parent_path + "box.png")

                movie_box_unit_path = ".//span[@class='unit']"
                movie_box_unit_object = movie_box_object.find_element_by_xpath(movie_box_unit_path)
                movie_box_unit_content = movie_box_unit_object.text
            except NoSuchElementException as no_movie_box_value_content_exception:
                print("no_movie_box_value_content_exception = ", no_movie_box_value_content_exception)

            if movie_box_value_content == '-1':
                print("exit movie_box_value_content = ", movie_score_content)
                driver.close()
                return '-1'

            # ================tab==================
            tab_content_path = "//div[@class='tab-content-container']"
            tab_content_object = driver.find_element_by_xpath(tab_content_path)

            # ================简介 评论============
            introduce_content = ''
            comment_list_object = None
            tab_celebrity_list_object = None
            tab_award_list_object = None
            tab_img_list_object = None

            tab_content_detail_path = ".//div[@class='tab-desc tab-content active']"
            tab_content_detail_object = tab_content_object.find_element_by_xpath(tab_content_detail_path)

            tab_content_detail_list_path = ".//div[@class='module']"
            tab_content_detail_list_object = tab_content_detail_object.find_elements_by_xpath(
                tab_content_detail_list_path)
            # print("tab_content_detail_list_object = ", len(tab_content_detail_list_object),
            #       tab_content_detail_list_object)
            if len(tab_content_detail_list_object) > 0:
                introduce_content = ''
                try:
                    introduce_object = tab_content_detail_list_object[0].find_element_by_xpath(".//span[@class='dra']")
                    introduce_content = introduce_object.text
                except NoSuchElementException as no_introduce_content_exception:
                    print("no_introduce_content_exception = ", no_introduce_content_exception)

                try:
                    comment_list_object = tab_content_detail_list_object[
                        len(tab_content_detail_list_object) - 1].find_element_by_xpath(
                        ".//div[@class='comment-list-container']").find_elements_by_xpath(
                        ".//li[@class='comment-container ']")
                except NoSuchElementException as no_comment_list_object_exception:
                    print("no_comment_list_object_exception = ", no_comment_list_object_exception)

            # ================演职人员==============
            try:
                tab_celebrity_path = ".//div[@class='tab-celebrity tab-content']"
                tab_celebrity_object = tab_content_object.find_element_by_xpath(tab_celebrity_path)
                tab_celebrity_list_object = tab_celebrity_object.find_elements_by_xpath(
                    ".//div[@class='celebrity-group']")
            except NoSuchElementException as no_tab_celebrity_list_object_exception:
                print("no_tab_celebrity_list_object_exception = ", no_tab_celebrity_list_object_exception)

            # ================奖项=================
            try:
                tab_award_path = ".//div[@class='tab-award tab-content']"
                tab_award_object = tab_content_object.find_element_by_xpath(tab_award_path)
                tab_award_list_object = tab_award_object.find_elements_by_xpath(".//li[@class='award-item ']")
            except NoSuchElementException as no_tab_award_list_object_exception:
                print("no_tab_award_list_object_exception = ", no_tab_award_list_object_exception)

            # ================图集=================
            try:
                tab_img_path = ".//div[@class='tab-img tab-content']"
                tab_img_object = tab_content_object.find_element_by_xpath(tab_img_path)
                tab_img_list_object = tab_img_object.find_elements_by_xpath(".//li")
                # print("tab_img_list_object = ", len(tab_img_list_object), tab_img_list_object)
            except NoSuchElementException as no_tab_img_list_object_exception:
                print("no_tab_img_list_object_exception = ", no_tab_img_list_object_exception)

            print("movie_avatar_url = ", movie_avatar_url)
            print("movie_name = ", movie_name)
            print("movie_en_name ", movie_en_name)
            print("movie_category ", movie_category)
            print("movie_country = ", movie_country)
            print("movie_duration = ", movie_duration)
            print("movie_release_info = ", movie_release_info)
            print("movie_release_time = ", movie_release_time)
            print("movie_release_area = ", movie_release_area)
            print("movie_score_content = ", movie_score_content)
            print("movie_want_to_see_count = ", movie_want_to_see_count)
            print("movie_stats_people_count_content = ", movie_stats_people_count_content)
            print("movie_stats_people_count_unit_content = ", movie_stats_people_count_unit_content)
            print("movie_box_value_content = ", movie_box_value_content)
            print("movie_box_unit_content = ", movie_box_unit_content)

            print("introduce_content = ", introduce_content)

            print('\n')

            mao_yan_detail_bean = MaoYanDetailBean()
            mao_yan_detail_bean = mao_yan_detail_bean.create_bean(
                '-1',
                movie_id,
                movie_avatar_url,
                movie_name,
                movie_en_name,
                movie_category,
                movie_country,
                movie_duration,
                movie_release_info,
                movie_release_time,
                movie_release_area,
                movie_score_content,
                movie_want_to_see_count,
                movie_stats_people_count_content,
                movie_stats_people_count_unit_content,
                movie_box_value_content,
                movie_box_unit_content,
                introduce_content
            )
            mao_yan_detail_db = MaoYanDetailDB()
            temp_detail_bean = mao_yan_detail_db.query_by_movie_id(movie_id)
            if temp_detail_bean is not None:
                mao_yan_detail_db.update_by_movie_id(mao_yan_detail_bean)
            else:
                mao_yan_detail_db.insert_bean(mao_yan_detail_bean)
            mao_yan_detail_db.close_db()

            self.parse_tab_celebrity_list(movie_id, tab_celebrity_list_object)

            self.parse_tab_award_list(movie_id, tab_award_list_object)

            self.parse_tab_img_list(movie_id, tab_img_list_object)

            self.parse_comment_list(movie_id, comment_list_object)

        except Exception as exception:
            print("exception = ", exception)

        driver.close()

    # def get_mao_yan_num(self, woff_url, num_content, img_save_name):
    #     # print("get_mao_yan_num::num_content = ", num_content)
    #     # print("get_mao_yan_num::woff_url = ", woff_url)
    #
    #     request_baidu_count_lines = []
    #     if Path(self.parent_path + "request_baidu_count.txt").is_file():
    #         print("request_baidu_count file exist")
    #         request_baidu_count_file = open(self.parent_path + "request_baidu_count.txt", "r")
    #         request_baidu_count_lines = request_baidu_count_file.readlines()
    #         request_baidu_count_file.close()
    #     print("get_mao_yan_num::request_baidu_count_lines = ", request_baidu_count_lines)
    #
    #     temp_current_time = time.strftime("%Y-%m-%d", time.localtime()) + '\n'
    #     print("get_mao_yan_num::temp_current_time = ", temp_current_time)
    #
    #     count = 1
    #     if len(request_baidu_count_lines) == 2:
    #         last_time = request_baidu_count_lines[0]
    #         print("get_mao_yan_num::last_time = ", last_time, "---isSame---", (last_time == temp_current_time))
    #         count = int(request_baidu_count_lines[1])
    #         count = count + 1
    #         print("get_mao_yan_num::count = ", count)
    #         if count > 500:
    #             if last_time == temp_current_time:
    #                 return "-1"
    #             else:
    #                 count = 1
    #
    #     request_baidu_count_file = open(self.parent_path + "request_baidu_count.txt", "w")
    #     request_baidu_count_file.write(time.strftime("%Y-%m-%d", time.localtime()))
    #     request_baidu_count_file.write('\n')
    #     request_baidu_count_file.write(str(count))
    #     request_baidu_count_file.close()
    #
    #     replace_woff_url = '------'
    #     replace_num_content = '======'
    #
    #     temp_file = open(self.parent_path + 'base_maoyan_detail.html', 'r', encoding='utf-8')
    #     new_file = open(self.parent_path + 'new_maoyan_detail.html', 'wb')
    #
    #     line = temp_file.readline()
    #     while len(line) > 0:
    #         if replace_woff_url in line:
    #             line = line.replace(replace_woff_url, woff_url)
    #         if replace_num_content in line:
    #             line = line.replace(replace_num_content, num_content)
    #         line = line.replace("\n", "")
    #         new_file.write(line.encode())
    #         line = temp_file.readline()
    #         # print("get_mao_yan_num::line = ", line)
    #         # print("get_mao_yan_num::len(line) = ", len(line))
    #
    #     new_file.close()
    #     temp_file.close()
    #
    #     new_file_path = 'file://' + os.path.abspath(self.parent_path + 'new_maoyan_detail.html')
    #     # print("get_mao_yan_num::new_file_path = ", new_file_path)
    #     new_driver = self.get_web_content(new_file_path)
    #     new_driver.get_screenshot_as_file(self.parent_path +img_save_name)
    #     # print("get_mao_yan_num::page_source = ", new_driver.page_source)
    #     num_pic_base64 = new_driver.get_screenshot_as_base64()
    #     # print("get_mao_yan_num::num_pic_base64 = ", num_pic_base64)
    #     new_driver.close()
    #
    #     baidu_token_result = requests.get(
    #         'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Wk03dOF1kRG1SnajCmyKELNx&client_secret=XAqRaMFFCUY2ZUGNSvtGsL8ZYbYRkERp&')
    #     # print('baidu_token_result_json = ', baidu_token_result.text)
    #     baidu_token_result_json = json.loads(baidu_token_result.text)
    #     # print('baidu_token = ', baidu_token_result_json['access_token'])
    #
    #     postdata = {'access_token': baidu_token_result_json['access_token'], 'image': num_pic_base64}
    #     # result = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic', data=postdata)
    #     result = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic', data=postdata)
    #     # result = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/webimage', data=postdata)
    #     # result =  {"log_id": 2337563219107430326, "words_result_num": 1, "words_result": [{"words": "9.4"}]}
    #     print("result = ", result.text, "\n")
    #     result_json_object = json.loads(result.text)
    #
    #     words = ''
    #     if 'words_result' in result_json_object:
    #         words_result = result_json_object['words_result']
    #         if len(words_result) > 0:
    #             words = words_result[0]['words']
    #             words_find_result = re.findall('(\\d+.?\\d+).*?', words, re.S)
    #             if len(words_find_result) > 0:
    #                 words = words_find_result[0]
    #
    #     # print("words = ", words)
    #
    #     return words

    def get_mao_yan_num_by_object(self, element_object, woff_font_file, img_save_name):
        print("get_mao_yan_num_by_object::element_object = ", element_object)
        print("get_mao_yan_num_by_object::woff_font_file = ", woff_font_file)
        print("get_mao_yan_num_by_object::img_save_name = ", img_save_name)

        num_content = element_object.text

        has_wan = False
        if num_content.endswith("万"):
            num_content = num_content.replace("万", "")
            has_wan = True

        num_content = num_content.encode("unicode-escape").decode()
        print("zxl--->num_content--->", num_content)

        num_content_array = num_content.split('\\u')
        print("zxl--->num_content_array--->", num_content_array)

        num_content_str = ''
        for font_content_item in num_content_array:
            if font_content_item != '':
                has_point = False
                if font_content_item.endswith("."):
                    font_content_item = font_content_item.replace(".", "")
                    has_point = True

                print("zxl--->font_content_item--->", font_content_item)

                temp_key = 'uni' + font_content_item.upper()
                print("zxl--->temp_key--->", temp_key)
                print("zxl--->font_dict.get--->", self.font_dict.get(temp_key))

                num_content_str = num_content_str + str(self.font_dict.get(temp_key))
                if has_point:
                    num_content_str = num_content_str + "."

        if has_wan:
            num_content_str = num_content_str + "万"

        return num_content_str
        # if '万' in num_content:
        #     num_content = num_content[:len(num_content) - 1]
        #
        # if '.' in num_content:
        #     num_content_find_result = num_content.split('.')
        #     print("get_mao_yan_num_by_object::len(num_content_find_result) = ", len(num_content_find_result))
        #     print("get_mao_yan_num_by_object::num_content_find_result[0] = ", (num_content_find_result[0] == ''))
        #     while num_content_find_result[0] == '':
        #         num_content = element_object.text
        #         if '万' in num_content:
        #             num_content = num_content[:len(num_content) - 1]
        #
        #         num_content_find_result = num_content.split('.')
        #         print("get_mao_yan_num_by_object::num_content_find_result = ", num_content_find_result)
        # else:
        #     num_content_find_result = num_content.split('.')
        #
        # num_result = ''
        # index = len(num_content_find_result)
        # for num_content_item_find_result in num_content_find_result:
        #     text = num_content_item_find_result
        #     print("get_mao_yan_num_by_object::text =",text,"---")
        #
        #     im = PIL.Image.new("RGB", (300, 60), (255, 255, 255))
        #     print("start draw text img 0")
        #     dr = PIL.ImageDraw.Draw(im)
        #     print("start draw text img 1")
        #     font = PIL.ImageFont.truetype(os.path.join(woff_font_file), 30)
        #
        #     print("start draw text img")
        #     dr.text((10, 15), text + text, font=font, fill="#000000")
        #     print("end draw text img")
        #
        #     # im.show()
        #     im.save(img_save_name)
        #
        #     # image2 = PIL.Image.open(img_save_name)
        #     # code = pytesseract.image_to_string(image2, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
        #     # print("get_mao_yan_num_by_object::code = ", code)
        #
        #     baidu_token_result = requests.get(
        #         'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Wk03dOF1kRG1SnajCmyKELNx&client_secret=XAqRaMFFCUY2ZUGNSvtGsL8ZYbYRkERp&')
        #     # print('baidu_token_result_json = ', baidu_token_result.text)
        #     baidu_token_result_json = json.loads(baidu_token_result.text)
        #     # print('baidu_token = ', baidu_token_result_json['access_token'])
        #
        #     with open(img_save_name, 'rb') as f:
        #         num_pic_base64 = base64.b64encode(f.read())
        #
        #     postdata = {'access_token': baidu_token_result_json['access_token'], 'image': num_pic_base64}
        #     # result = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic', data=postdata)
        #     result = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic', data=postdata)
        #     # result = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/webimage', data=postdata)
        #     # result =  {"log_id": 2337563219107430326, "words_result_num": 1, "words_result": [{"words": "9.4"}]}
        #     print("result = ", result.text, "\n")
        #     result_json_object = json.loads(result.text)
        #
        #     code = ''
        #     if 'words_result' in result_json_object:
        #         words_result = result_json_object['words_result']
        #         if len(words_result) > 0:
        #             code = words_result[0]['words']
        #
        #     # print("words = ", words)
        #
        #     num_result = num_result + code[0:int(len(code) / 2)]
        #     if index == 2:
        #         num_result = num_result + "."
        #     index = 0
        #
        #     time.sleep(2)

        # print("get_mao_yan_num_by_object::num_result = ", num_result)
        # print("\n\n")
        return ""

    def parse_tab_celebrity_list(self, movie_id, tab_celebrity_list_object):
        if tab_celebrity_list_object is not None:
            # print("tab_celebrity_list_object = ", len(tab_celebrity_list_object), tab_celebrity_list_object)

            mao_yan_celebrity_db = MaoYanCelebrityDB()
            mao_yan_celebrity_db.delete_by_movie_id(movie_id)

            for tab_celebrity_item_object in tab_celebrity_list_object:
                # print('tab_celebrity_item_object==================>')
                # print(tab_celebrity_item_object.get_attribute('innerHTML'))
                celebrity_type_path = ".//div[@class='celebrity-type']"
                celebrity_type_object = tab_celebrity_item_object.find_element_by_xpath(celebrity_type_path)
                # print(celebrity_type_object.get_attribute('innerHTML'), "--1--", celebrity_type_object.text, "--2--", celebrity_type_object.get_attribute('textContent'))
                celebrity_type_name = celebrity_type_object.get_attribute('outerHTML')
                find_celebrity_type_name_result = re.findall(
                    '<div class="celebrity-type">(.*?)<span class="num">(.*?)</span>.*?</div>', celebrity_type_name,
                    re.S)
                # print(find_celebrity_type_name_result)

                # celebrity_type_value = ''
                if len(find_celebrity_type_name_result) > 0:
                    celebrity_type_name = find_celebrity_type_name_result[0][0]
                    celebrity_type_name = celebrity_type_name.replace('\n', "")
                    celebrity_type_name = celebrity_type_name.replace(' ', "")

                    # celebrity_type_value = find_celebrity_type_name_result[0][1]

                # celebrity_type_value_object = celebrity_type_object.find_element_by_xpath(".//span[@class='num']")
                # # print(celebrity_type_value_object.get_attribute('innerHTML'))
                # celebrity_type_value = celebrity_type_value_object.get_attribute('innerHTML')
                # find_celebrity_type_value_result = re.findall("(\\d+)", celebrity_type_value)
                # if len(find_celebrity_type_value_result) > 0:
                #     celebrity_type_value = find_celebrity_type_value_result[0]

                # print("celebrity_type_name = ", celebrity_type_name)
                # print("celebrity_type_value = ", celebrity_type_value)
                # print('\n')

                celebrity_list_path = ".//ul[@class='celebrity-list clearfix']"
                celebrity_list_object = tab_celebrity_item_object.find_elements_by_xpath(celebrity_list_path)
                celebrity_list_object = tab_celebrity_item_object.find_elements_by_xpath(".//li")
                # print("celebrity_list_object = ", len(celebrity_list_object), tab_celebrity_list_object)
                for celebrity_item_object in celebrity_list_object:
                    # print('celebrity_item_object==================>')
                    celebrity_detail_path = ".//a[@class='portrait']"
                    celebrity_detail_object = celebrity_item_object.find_element_by_xpath(celebrity_detail_path)
                    celebrity_detail_url = celebrity_detail_object.get_attribute("href")
                    celebrity_head_img = celebrity_detail_object.find_element_by_xpath(
                        ".//img[@class='default-img']").get_attribute('data-src')
                    if '@' in celebrity_head_img:
                        celebrity_head_img = celebrity_head_img.split('@')[0]
                    celebrity_name = celebrity_item_object.find_element_by_xpath(".//a[@class='name']").get_attribute(
                        'innerHTML')
                    celebrity_name = celebrity_name.replace('\n', "")
                    celebrity_name = celebrity_name.replace(' ', "")

                    celebrity_role_name = ''
                    celebrity_role_path = ".//span[@class='role']"
                    try:
                        celebrity_role_object = celebrity_item_object.find_element_by_xpath(celebrity_role_path)
                        if celebrity_role_object is not None:
                            celebrity_role_name = celebrity_role_object.get_attribute('innerHTML')
                    except NoSuchElementException as no_celebrity_role_exception:
                        # print("no_celebrity_role_exception = ", no_celebrity_role_exception)
                        pass

                    # print("celebrity_name = ", celebrity_name)
                    # print("celebrity_role_name = ", celebrity_role_name)
                    # print("celebrity_head_img = ", celebrity_head_img)
                    # print("celebrity_detail_url = ", celebrity_detail_url)
                    # print('\n')

                    mao_yan_celebrity_bean = MaoYanCelebrityBean()
                    mao_yan_celebrity_bean = mao_yan_celebrity_bean.create_bean('-1',
                                                                                movie_id,
                                                                                celebrity_type_name,
                                                                                celebrity_name,
                                                                                celebrity_role_name,
                                                                                celebrity_head_img,
                                                                                celebrity_detail_url)
                    mao_yan_celebrity_db.insert_bean(mao_yan_celebrity_bean)

            mao_yan_celebrity_db.close_db()

    def parse_tab_award_list(self, movie_id, tab_award_list_object):
        if tab_award_list_object is not None:
            # print("tab_award_list_object = ", len(tab_award_list_object), tab_award_list_object)

            mao_yan_award_db = MaoYanAwardDB()
            mao_yan_award_db.delete_by_movie_id(movie_id)

            for tab_award_item_object in tab_award_list_object:
                find_award_head_result = re.findall(
                    '<li class="award-item ">.*?<div>.*?<div class="portrait">.*?<img src="(.*?)" alt="">.*?</div>(.*?)</div>.*?<div class="content">.* ?</div>.*?</li>',
                    tab_award_item_object.get_attribute('outerHTML'), re.S)
                award_img = ''
                award_title = ''
                if len(find_award_head_result) > 0:
                    award_img = find_award_head_result[0][0]
                    award_title = find_award_head_result[0][1]

                    if '@' in award_img:
                        award_img = award_img.split('@')[0]
                    award_title = award_title.replace('\n', "")
                    award_title = award_title.replace(' ', "")

                award_content = ''
                award_content_parent_path = ".//div[@class='content']"
                award_content_parent_object = tab_award_item_object.find_element_by_xpath(award_content_parent_path)
                award_content_list_object = award_content_parent_object.find_elements_by_xpath(".//div")
                for award_content_item_object in award_content_list_object:
                    award_content = award_content + award_content_item_object.get_attribute('innerHTML') + "\n"
                award_content = award_content.replace(' ', "")

                # print("award_title = ", award_title)
                # print("award_content = ")
                # print(award_content)
                # print("award_img = ", award_img)
                # print('\n')

                mao_yan_award_bean = MaoYanAwardBean()
                mao_yan_award_bean = mao_yan_award_bean.create_bean('-1',
                                                                    movie_id,
                                                                    award_title,
                                                                    award_content,
                                                                    award_img)
                mao_yan_award_db.insert_bean(mao_yan_award_bean)

            mao_yan_award_db.close_db()

    def parse_tab_img_list(self, movie_id, tab_img_list_object):
        if tab_img_list_object is not None:
            # print("tab_img_list_object = ", len(tab_img_list_object), tab_img_list_object)

            mao_yan_img_collection_db = MaoYanImgCollectionDB()
            mao_yan_img_collection_db.delete_by_movie_id(movie_id)

            for tab_img_item_object in tab_img_list_object:
                tab_img = ''
                try:
                    tab_img = tab_img_item_object.find_element_by_xpath(".//img[@class='default-img']").get_attribute(
                        "data-src")
                except NoSuchElementException as no_tab_img_exception:
                    print("no_tab_img_exception = ", no_tab_img_exception)

                if '@' in tab_img:
                    tab_img = tab_img.split('@')[0]
                # print("tab_img = ", tab_img)

                mao_yan_img_collection_bean = MaoYanImgCollectionBean()
                mao_yan_img_collection_bean = mao_yan_img_collection_bean.create_bean('-1',
                                                                                      movie_id,
                                                                                      tab_img)
                mao_yan_img_collection_db.insert_bean(mao_yan_img_collection_bean)

            mao_yan_img_collection_db.close_db()

    def parse_comment_list(self, movie_id, comment_list_object):
        if comment_list_object is not None:
            # print("comment_list_object = ", len(comment_list_object), comment_list_object)

            mao_yan_comment_db = MaoYanCommentDB()
            mao_yan_comment_db.delete_by_movie_id(movie_id)

            for comment_item_object in comment_list_object:
                # print('comment_item_object==================>')
                # print(comment_item_object.get_attribute('innerHTML'))
                comment_user_head_path = ".//div[@class='portrait-container']"
                comment_user_head_object = comment_item_object.find_element_by_xpath(comment_user_head_path)
                comment_user_head_img = comment_user_head_object.find_element_by_xpath(".//img").get_attribute("src")
                if '@' in comment_user_head_img:
                    comment_user_head_img = comment_user_head_img.split('@')[0]

                comment_user_path = ".//div[@class='user']"
                comment_user_object = comment_item_object.find_element_by_xpath(comment_user_path)
                comment_user_name = comment_user_object.find_element_by_xpath(".//span[@class='name']").text

                comment_time_path = ".//div[@class='time']"
                comment_time_object = comment_item_object.find_element_by_xpath(comment_time_path)
                comment_time = comment_time_object.get_attribute("title")

                # 点赞
                comment_approve_path = ".//div[@class='approve ']"
                comment_approve_object = comment_item_object.find_element_by_xpath(comment_approve_path)
                comment_approve_num = comment_approve_object.find_element_by_xpath(".//span[@class='num']").text

                comment_content_path = ".//div[@class='comment-content']"
                comment_content_object = comment_item_object.find_element_by_xpath(comment_content_path)
                comment_content = comment_content_object.text

                # print("comment_user_name = ", comment_user_name)
                # print("comment_user_head_img = ", comment_user_head_img)
                # print("comment_content = ", comment_content)
                # print("comment_time = ", comment_time)
                # print("comment_approve_num = ", comment_approve_num)
                # print('\n')

                mao_yan_comment_bean = MaoYanCommentBean()
                mao_yan_comment_bean = mao_yan_comment_bean.create_bean('-1',
                                                                        movie_id,
                                                                        comment_user_name,
                                                                        comment_user_head_img,
                                                                        comment_content,
                                                                        comment_time,
                                                                        comment_approve_num)
                mao_yan_comment_db.insert_bean(mao_yan_comment_bean)

            mao_yan_comment_db.close_db()

    def login_mao_yan(self):
        driver = self.get_web_content(
            "https://passport.meituan.com/account/unitivelogin?service=maoyan&continue=https%3A%2F%2Fmaoyan.com%2Fpassport%2Flogin%3Fredirect%3D%252F")
        user_name_input = driver.find_element_by_xpath("//input[@class='f-text phone-input']")
        pass_word_input = driver.find_element_by_xpath("//input[@class='f-text pw-input']")
        login_input = driver.find_element_by_xpath("//input[@value='登录']")
        user_name_input.send_keys('15850687360')
        pass_word_input.send_keys('working')
        login_input.click()
        time.sleep(10)
        print("login success")
        # while True:
        #     pass
        return driver

    def request_now_mao_yan_detail(self):
        mao_yan_now_db = MaoYanDB(MaoYanDB.NOW_TABLE_NAME)
        mao_yan_bean_list = mao_yan_now_db.query_all()
        mao_yan_now_db.close_db()
        # i = 0
        for mao_yan_bean in mao_yan_bean_list:
            print("request_now_mao_yan_detail::movie_id = ", mao_yan_bean['movie_id'])
            result = self.request(mao_yan_bean['movie_id'], mao_yan_bean['movie_detail_url'])
            print("request_now_mao_yan_detail::result = ", result)
            # i = i + 1
            # if i == 1:
            #     break
            if result == '-1':
                break

        # self.request("1218029", "https://maoyan.com/films/1218029")



if __name__ == "__main__":
    requestMaoYanDetail = RequestMaoYanDetail()
    # requestMaoYanDetail.parent_path = '../'
    # 267,1250952
    # requestMaoYanDetail.request("1211270", "https://maoyan.com/films/1211270")
    requestMaoYanDetail.request("1258163", "https://maoyan.com/films/1258163")
    # requestMaoYanDetail.request("1211270", "https://passport.meituan.com/account/unitivelogin?service=maoyan&continue=https%3A%2F%2Fmaoyan.com%2Fpassport%2Flogin%3Fredirect%3D%252F")

    # new_driver = requestNowMaoYan.get_web_content("file:///home/mi/zxl/workspace/my_github/joke_spider/com_zxl_spider_request/new_maoyan_detail.html")
    # time.sleep(10)
    # new_driver.get_screenshot_as_file(self.parent_path + 'new_maoyan_detail.png')
    # print("get_mao_yan_num::page_source = ", new_driver.page_source)
    # new_driver.close()
    # while True:
    #     pass

    # num_pic_base64 = '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ACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAACq+j+Gse57AvcRUgAAAABJRU5ErkJggg=='
    # baidu_token_result = requests.get(
    #     'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Wk03dOF1kRG1SnajCmyKELNx&client_secret=XAqRaMFFCUY2ZUGNSvtGsL8ZYbYRkERp&')
    # print('baidu_token_result_json = ', baidu_token_result.text)
    # baidu_token_result_json = json.loads(baidu_token_result.text)
    # print('baidu_token = ', baidu_token_result_json['access_token'])
    #
    # postdata = {'access_token': baidu_token_result_json['access_token'], 'image': num_pic_base64}
    # result = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic', data=postdata)
    # print("result = ", result.text)
