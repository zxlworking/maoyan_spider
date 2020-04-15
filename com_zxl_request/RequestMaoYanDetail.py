#!/usr/bin/python
# coding=utf-8

from com_zxl_request.BaseRequest import BaseRequest


class RequestMaoYanDetail(BaseRequest):

    parent_path = ''

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

        except Exception as exception:
            print("exception = ", exception)

        driver.close()

if __name__ == "__main__":
    requestMaoYanDetail = RequestMaoYanDetail()

    # requestMaoYanDetail.request("1211270", "https://maoyan.com/films/1211270")
    requestMaoYanDetail.request("1258163", "https://maoyan.com/films/1258163")