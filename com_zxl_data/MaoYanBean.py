# /usr/bin/python
# coding=utf-8


class MaoYanBean:

    def create_bean(self,
                         id,
                         movie_id,
                         movie_title,
                         movie_poster_url,
                         movie_detail_url,
                         movie_type):
        bean = {'id': id,
                'movie_id': movie_id,
                'movie_title': movie_title,
                'movie_poster_url': movie_poster_url,
                'movie_detail_url': movie_detail_url,
                'movie_type': movie_type}
        return bean
