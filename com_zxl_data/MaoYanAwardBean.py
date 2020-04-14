# /usr/bin/python
# coding=utf-8


class MaoYanAwardBean:

    def create_bean(self,
                    id,
                    movie_id,
                    award_title,
                    award_content,
                    award_img):
        bean = {'id': id,
                'movie_id': movie_id,
                'award_title': award_title,
                'award_content': award_content,
                'award_img': award_img}
        return bean
