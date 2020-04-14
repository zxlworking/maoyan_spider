#!/usr/bin/python
# coding=utf-8
import re

from selenium.common.exceptions import NoSuchElementException

from com_zxl_data.MaoYanBean import MaoYanBean
from com_zxl_db.MaoYanDB import MaoYanDB
from com_zxl_request.BaseRequest import BaseRequest


class RequestMaoYan(BaseRequest):

    mao_yan_now_db = None
    mao_yan_future_db = None
    mao_yan_history_db = None

    def __init__(self):
        self.mao_yan_now_db = MaoYanDB(MaoYanDB.NOW_TABLE_NAME)
        self.mao_yan_future_db = MaoYanDB(MaoYanDB.FUTURE_TABLE_NAME)
        self.mao_yan_history_db = MaoYanDB(MaoYanDB.HISTORY_TABLE_NAME)

    def request(self, type, url):
        print("request::type = %d " % type)
        print("request::url = %s " % url)
        driver = self.get_web_content(url)
        print(driver.page_source)

        movies_list_path = "//div[@class='movies-list']"
        movies_list_obj = driver.find_element_by_xpath(movies_list_path)

        movie_items_path = ".//dd"
        movie_items_obj = movies_list_obj.find_elements_by_xpath(movie_items_path)

        for movie_item in movie_items_obj:
            print("----------start-----------")
            movie_item_path = ".//div[@class='movie-item film-channel']"
            movie_item_obj = movie_item.find_element_by_xpath(movie_item_path)

            movie_poster_path = ".//div[@class='movie-poster']"
            movie_poster_obj = movie_item_obj.find_element_by_xpath(movie_poster_path)

            movie_poster_img_list_obj = movie_poster_obj.find_elements_by_xpath(".//img")
            movie_poster_url = ''
            movie_poster_default_url = ''
            for movie_poster_img in movie_poster_img_list_obj:
                if movie_poster_img.get_attribute('data-src') is None:
                    movie_poster_default_url = movie_poster_img.get_attribute('src')
                else:
                    movie_poster_url = movie_poster_img.get_attribute('data-src')

            if movie_poster_url == '':
                movie_poster_url = movie_poster_default_url

            if '@' in movie_poster_url:
                movie_poster_url = movie_poster_url.split('@')[0]

            movie_item_detail_path = ".//div[@class='channel-detail movie-item-title']"
            movie_item_detail_obj = movie_item.find_element_by_xpath(movie_item_detail_path)
            movie_item_detail_obj = movie_item_detail_obj.find_element_by_xpath(".//a")
            movie_id = movie_item_detail_obj.get_attribute('data-val')
            movie_title = movie_item_detail_obj.text
            movie_detail_url = movie_item_detail_obj.get_attribute('href')

            movie_id_result = re.findall(".*?(\\d+).*?", movie_id)
            if len(movie_id_result) > 0:
                movie_id = movie_id_result[0]

            print("movie_id = %s" % movie_id)
            print("movie_title = %s" % movie_title)
            # print("movie_poster_url = %s" % movie_poster_url)
            print("movie_detail_url = %s" % movie_detail_url)

            mao_yan_bean = MaoYanBean()
            mao_yan_bean = mao_yan_bean.create_bean('', movie_id, movie_title, movie_poster_url, movie_detail_url, type)

            mao_yan_db = self.mao_yan_now_db
            if type == 1:
                mao_yan_db = self.mao_yan_now_db
            elif type == 2:
                mao_yan_db = self.mao_yan_future_db
            elif type == 3:
                mao_yan_db = self.mao_yan_history_db

            mao_yan_temp_bean = mao_yan_db.query_by_movie_id(movie_id)
            if mao_yan_temp_bean is None:
                mao_yan_db.insert_bean(mao_yan_bean)
            else:
                print("----------exist break-----------\n")
                break

            print("----------end-----------\n")

        try:
            page_list_path = '//ul[@class="list-pager"]'
            page_list_obj = driver.find_element_by_xpath(page_list_path)

            page_items = page_list_obj.find_elements_by_xpath(".//a")
            for page_item in page_items:
                page_item_text = page_item.text
                if page_item_text == '下一页':
                    self.request(type, page_item.get_attribute("href"))
        except NoSuchElementException as e:
            print(e)

        driver.close()

    def close_db(self):
        self.mao_yan_now_db.close_db()
        self.mao_yan_future_db.close_db()
        self.mao_yan_history_db.close_db()

    def start_now_mao_yan(self):
        self.mao_yan_now_db.delete_all()
        self.request(1, "https://maoyan.com/films?showType=1")
        # self.request(2, "https://maoyan.com/films?showType=2")
        # self.request(3, "https://maoyan.com/films?showType=3")
        self.close_db()


if __name__ == "__main__":
    request = RequestMaoYan()
    # 正在热映
    # request.request(1, "https://maoyan.com/films?showType=1")
    # 即将
    # request.request(2, "https://maoyan.com/films?showType=2")
    # 历史
    # request.request(3, "https://maoyan.com/films?showType=3")
    # request.close_db()

    request.start_now_mao_yan()

