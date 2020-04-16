#!/usr/bin/python
# coding=utf-8
import re
import sys
from urllib import request

from fontTools.ttLib import TTFont
from selenium.common.exceptions import NoSuchElementException

from com_zxl_data.MaoYanAwardBean import MaoYanAwardBean
from com_zxl_data.MaoYanCelebrityBean import MaoYanCelebrityBean
from com_zxl_data.MaoYanCommentBean import MaoYanCommentBean
from com_zxl_data.MaoYanDetailBean import MaoYanDetailBean
from com_zxl_data.MaoYanImgCollectionBean import MaoYanImgCollectionBean
from com_zxl_db.MaoYanAwardDB import MaoYanAwardDB
from com_zxl_db.MaoYanCelebrityDB import MaoYanCelebrityDB
from com_zxl_db.MaoYanCommentDB import MaoYanCommentDB
from com_zxl_db.MaoYanDetailDB import MaoYanDetailDB
from com_zxl_db.MaoYanImgCollectionDB import MaoYanImgCollectionDB
from com_zxl_knn_font.knn_font import classifyPerson
from com_zxl_request.BaseRequest import BaseRequest


class RequestMaoYanDetail(BaseRequest):

    parent_path = sys.path[0]
    woff_font_file_name = 'mao_yan_font.woff'
    woff_font_file_path = parent_path + '/' + 'mao_yan_font.woff'

    font_dict = {}

    def __init__(self):
        pass

    def request(self, movie_id, movie_detail_url):
        print("request::movie_id = %s " % movie_id)
        print("request::movie_detail_url = %s " % movie_detail_url)

        driver = self.get_web_content(movie_detail_url)

        page_content = driver.page_source
        print(page_content)

        try:
            movie_detail_path = "//div[@class='banner']"

            movie_detail_object = driver.find_element_by_xpath(movie_detail_path)
            print("movie_detail_object = ", movie_detail_object)

            movie_detail_path = "//div[@class='banner']"

            # banner_object = WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located((By.XPATH, movie_detail_path)))
            # print("banner_object = ", banner_object)

            movie_detail_object = driver.find_element_by_xpath(movie_detail_path)
            # print("movie_detail_object = ", movie_detail_object)

            woff_url_result = re.findall(r'.*?url\(\'(.*?)\'\).*?', page_content)
            if len(woff_url_result) > 0:
                for woff_url in woff_url_result:
                    if 'woff' in woff_url:
                        woff_url = "http:" + woff_url
                        # print("woff_url--->", woff_url)
                        print("woff_font_file_path--->", self.woff_font_file_path)
                        font_request = request.Request(woff_url)
                        font_res = request.urlopen(font_request)
                        font_respoen = font_res.read()
                        font_file = open(self.woff_font_file_path, 'wb')
                        font_file.write(font_respoen)
                        font_file.close()

                        base_font = TTFont(self.woff_font_file_path)
                        base_list = base_font.getGlyphOrder()[2:]

                        for font in base_list:
                            coordinate = base_font['glyf'][font].coordinates
                            font_0 = [i for item in coordinate for i in item]
                            # print(font_0)
                            self.font_dict[font] = classifyPerson(font_0)
                        print("font_dict = ", self.font_dict)

            mao_yan_detail_bean = MaoYanDetailBean()

            mao_yan_detail_bean.movie_id = movie_id

            self.parse_avatar_url(movie_detail_object, mao_yan_detail_bean)
            self.parse_movie_name(movie_detail_object, mao_yan_detail_bean)
            self.parse_movie_header(movie_detail_object, mao_yan_detail_bean)
            self.parse_movie_want_content(movie_detail_object, mao_yan_detail_bean)
            self.parse_movie_score_content(movie_detail_object, mao_yan_detail_bean)
            self.parse_movie_stats_people_content(movie_detail_object, mao_yan_detail_bean)
            self.parse_movie_box_content(movie_detail_object, mao_yan_detail_bean)

            self.parse_movie_detail(movie_id, driver, mao_yan_detail_bean)

            dict = mao_yan_detail_bean.create_bean_dict()
            print("mao_yan_detail_bean = ", dict)

            mao_yan_detail_db = MaoYanDetailDB()
            temp_detail_bean = mao_yan_detail_db.query_by_movie_id(movie_id)
            if temp_detail_bean is not None:
                mao_yan_detail_db.update_by_movie_id(mao_yan_detail_bean.create_bean_dict())
            else:
                mao_yan_detail_db.insert_bean(mao_yan_detail_bean.create_bean_dict())
            mao_yan_detail_db.close_db()

        except Exception as exception:
            print("exception = ", exception)

        driver.close()

    # 电影海报
    def parse_avatar_url(self, movie_detail_object, mao_yan_detail_bean):
        movie_avatar_url = ''
        try:
            movie_avatar_path = ".//img[@class='avatar']"
            movie_avatar_object = movie_detail_object.find_element_by_xpath(movie_avatar_path)
            movie_avatar_url = movie_avatar_object.get_attribute("src")
            if '@' in movie_avatar_url:
                movie_avatar_url = movie_avatar_url.split('@')[0]
        except NoSuchElementException as no_avatar_url_exception:
            print("no_avatar_url_exception = ", no_avatar_url_exception)
        mao_yan_detail_bean.movie_avatar_url = movie_avatar_url

    # 电影名称
    def parse_movie_name(self, movie_detail_object, mao_yan_detail_bean):
        movie_introduce_path = ".//div[@class='celeInfo-right clearfix']"
        movie_introduce_object = movie_detail_object.find_element_by_xpath(movie_introduce_path)

        movie_brief_path = ".//div[@class='movie-brief-container']"
        movie_brief_object = movie_introduce_object.find_element_by_xpath(movie_brief_path)

        movie_name = ''
        try:
            movie_name_path = ".//h1[@class='name']"
            movie_name_object = movie_brief_object.find_element_by_xpath(movie_name_path)
            movie_name = movie_name_object.text
        except NoSuchElementException as no_movie_name_exception:
            print("no_movie_name_exception = ", no_movie_name_exception)
        mao_yan_detail_bean.movie_name = movie_name

        movie_en_name = ''
        try:
            movie_en_name_path = ".//div[@class='ename ellipsis']"
            movie_en_name_object = movie_brief_object.find_element_by_xpath(movie_en_name_path)
            movie_en_name = movie_en_name_object.text
        except NoSuchElementException as no_movie_en_name_exception:
            print("no_movie_en_name_exception = ", no_movie_en_name_exception)
        mao_yan_detail_bean.movie_en_name = movie_en_name

    # 电影发布信息
    def parse_movie_header(self, movie_detail_object, mao_yan_detail_bean):
        movie_category = ''
        movie_country = ''
        movie_duration = ''
        movie_release_info = ''
        movie_release_time = ''
        movie_release_area = ''

        movie_introduce_path = ".//div[@class='celeInfo-right clearfix']"
        movie_introduce_object = movie_detail_object.find_element_by_xpath(movie_introduce_path)

        movie_brief_path = ".//div[@class='movie-brief-container']"
        movie_brief_object = movie_introduce_object.find_element_by_xpath(movie_brief_path)

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
        mao_yan_detail_bean.movie_category = movie_category
        mao_yan_detail_bean.movie_country = movie_country
        mao_yan_detail_bean.movie_duration = movie_duration
        mao_yan_detail_bean.movie_release_info = movie_release_info
        mao_yan_detail_bean.movie_release_time = movie_release_time
        mao_yan_detail_bean.movie_release_area = movie_release_area

    # 想看电影的
    def parse_movie_want_content(self, movie_detail_object, mao_yan_detail_bean):
        movie_introduce_path = ".//div[@class='celeInfo-right clearfix']"
        movie_introduce_object = movie_detail_object.find_element_by_xpath(movie_introduce_path)
        movie_stats_path = ".//div[@class='movie-stats-container']"
        movie_stats_object = movie_introduce_object.find_element_by_xpath(movie_stats_path)

        movie_want_to_see_count = ''
        try:
            movie_want_to_see_content_path = ".//span[@class='index-left info-num one-line']"
            movie_want_to_see_content_object = movie_stats_object.find_element_by_xpath(movie_want_to_see_content_path)
            movie_want_to_see_count_path = ".//span"
            movie_want_to_see_count_object = movie_want_to_see_content_object.find_element_by_xpath(
                movie_want_to_see_count_path)
            movie_want_to_see_count = self.get_mao_yan_num_by_object(movie_want_to_see_count_object)
        except NoSuchElementException as no_movie_want_to_see_content_exception:
            print("no_movie_want_to_see_content_exception = ", no_movie_want_to_see_content_exception)
            pass
        mao_yan_detail_bean.movie_want_to_see_count = movie_want_to_see_count

    # 电影评分
    def parse_movie_score_content(self, movie_detail_object, mao_yan_detail_bean):
        movie_introduce_path = ".//div[@class='celeInfo-right clearfix']"
        movie_introduce_object = movie_detail_object.find_element_by_xpath(movie_introduce_path)
        movie_stats_path = ".//div[@class='movie-stats-container']"
        movie_stats_object = movie_introduce_object.find_element_by_xpath(movie_stats_path)

        movie_score_content = ''
        try:
            movie_score_path = ".//span[@class='index-left info-num ']"
            movie_score_object = movie_stats_object.find_element_by_xpath(movie_score_path)
            print("movie_score_object.innerHTML = ", movie_score_object.get_attribute('innerHTML'))
            movie_score_content_path = ".//span"
            movie_score_content_object = movie_score_object.find_element_by_xpath(movie_score_content_path)
            movie_score_content = self.get_mao_yan_num_by_object(movie_score_content_object)
        except NoSuchElementException as no_movie_score_content_exception:
            print("no_movie_score_content_exception = ", no_movie_score_content_exception)
        mao_yan_detail_bean.movie_score_content = movie_score_content

    # 电影评论人数
    def parse_movie_stats_people_content(self, movie_detail_object, mao_yan_detail_bean):
        movie_introduce_path = ".//div[@class='celeInfo-right clearfix']"
        movie_introduce_object = movie_detail_object.find_element_by_xpath(movie_introduce_path)
        movie_stats_path = ".//div[@class='movie-stats-container']"
        movie_stats_object = movie_introduce_object.find_element_by_xpath(movie_stats_path)

        movie_stats_people_count_content = ''
        movie_stats_people_count_unit_content = ''
        try:
            movie_stats_people_count_parent_path = ".//span[@class='score-num']"
            movie_stats_people_count_parent_object = movie_stats_object.find_element_by_xpath(
                movie_stats_people_count_parent_path)
            movie_stats_people_count_path = ".//span"
            movie_stats_people_count_object = movie_stats_people_count_parent_object.find_element_by_xpath(
                movie_stats_people_count_path)

            movie_stats_people_count_content = self.get_mao_yan_num_by_object(movie_stats_people_count_object)
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
        mao_yan_detail_bean.movie_stats_people_count_content = movie_stats_people_count_content
        mao_yan_detail_bean.movie_stats_people_count_unit_content = movie_stats_people_count_unit_content

    # 电影票房
    def parse_movie_box_content(self, movie_detail_object, mao_yan_detail_bean):
        movie_introduce_path = ".//div[@class='celeInfo-right clearfix']"
        movie_introduce_object = movie_detail_object.find_element_by_xpath(movie_introduce_path)
        movie_stats_path = ".//div[@class='movie-stats-container']"
        movie_stats_object = movie_introduce_object.find_element_by_xpath(movie_stats_path)

        movie_box_value_content = ''
        movie_box_unit_content = ''
        try:
            movie_box_path = ".//div[@class='movie-index-content box']"
            movie_box_object = movie_stats_object.find_element_by_xpath(movie_box_path)

            movie_box_value_path = ".//span[@class='stonefont']"
            movie_box_value_object = movie_box_object.find_element_by_xpath(movie_box_value_path)
            # movie_box_value_content = self.get_mao_yan_num(woff_url, movie_box_value_object.text, self.parent_path + "box.png")
            movie_box_value_content = self.get_mao_yan_num_by_object(movie_box_value_object)

            movie_box_unit_path = ".//span[@class='unit']"
            movie_box_unit_object = movie_box_object.find_element_by_xpath(movie_box_unit_path)
            movie_box_unit_content = movie_box_unit_object.text
        except NoSuchElementException as no_movie_box_value_content_exception:
            print("no_movie_box_value_content_exception = ", no_movie_box_value_content_exception)
        mao_yan_detail_bean.movie_box_value_content = movie_box_value_content
        mao_yan_detail_bean.movie_box_unit_content = movie_box_unit_content

    def get_mao_yan_num_by_object(self, element_object):
        num_content = element_object.text

        has_wan = False
        if num_content.endswith("万"):
            num_content = num_content.replace("万", "")
            has_wan = True

        num_content = num_content.encode("unicode-escape").decode()
        # print("get_mao_yan_num_by_object--->num_content--->", num_content)

        num_content_array = num_content.split('\\u')
        # print("get_mao_yan_num_by_object--->num_content_array--->", num_content_array)

        num_content_str = ''
        for font_content_item in num_content_array:
            if font_content_item != '':
                has_point = False
                if font_content_item.endswith("."):
                    font_content_item = font_content_item.replace(".", "")
                    has_point = True

                # print("get_mao_yan_num_by_object--->font_content_item--->", font_content_item)

                temp_key = 'uni' + font_content_item.upper()
                # print("get_mao_yan_num_by_object--->temp_key--->", temp_key)
                # print("get_mao_yan_num_by_object--->font_dict.get--->", self.font_dict.get(temp_key))

                num_content_str = num_content_str + str(self.font_dict.get(temp_key))
                if has_point:
                    num_content_str = num_content_str + "."

        if has_wan:
            num_content_str = num_content_str + "万"

        return num_content_str

    def parse_movie_detail(self, movie_id, driver, mao_yan_detail_bean):
        # ================tab==================
        tab_content_path = "//div[@class='tab-content-container']"
        tab_content_object = driver.find_element_by_xpath(tab_content_path)

        # ================简介 评论============
        mao_yan_detail_bean.introduce_content = ''
        comment_list_object = None
        tab_celebrity_list_object = None
        tab_award_list_object = None
        tab_img_list_object = None

        tab_content_detail_path = ".//div[@class='tab-desc tab-content active']"
        tab_content_detail_object = tab_content_object.find_element_by_xpath(tab_content_detail_path)

        tab_content_detail_list_path = ".//div[@class='module']"
        tab_content_detail_list_object = tab_content_detail_object.find_elements_by_xpath(tab_content_detail_list_path)
        print("tab_content_detail_list_object = ", tab_content_detail_list_object)
        if len(tab_content_detail_list_object) > 0:
            try:
                introduce_object = tab_content_detail_list_object[0].find_element_by_xpath(".//span[@class='dra']")
                mao_yan_detail_bean.introduce_content = introduce_object.text
            except NoSuchElementException as no_introduce_content_exception:
                print("no_introduce_content_exception = ", no_introduce_content_exception)

            try:
                comment_list_object = tab_content_detail_list_object[4].\
                    find_element_by_xpath(".//div[@class='comment-list-container']").\
                    find_elements_by_xpath(".//li[starts-with(@class,'comment-container ')]")
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
        self.parse_tab_celebrity_list(movie_id, tab_celebrity_list_object)
        self.parse_tab_award_list(movie_id, tab_award_list_object)
        self.parse_tab_img_list(movie_id, tab_img_list_object)
        self.parse_comment_list(movie_id, comment_list_object)

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
        print("comment_list_object = ", comment_list_object)
        if comment_list_object is not None:
            print("comment_list_object len = ", len(comment_list_object))

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

if __name__ == "__main__":
    requestMaoYanDetail = RequestMaoYanDetail()

    # feature
    # requestMaoYanDetail.request("1217023", "https://maoyan.com/films/1217023")
    # now
    requestMaoYanDetail.request("1258163", "http://maoyan.com/films/1258163")