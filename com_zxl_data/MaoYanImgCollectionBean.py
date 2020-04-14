# /usr/bin/python
# coding=utf-8


class MaoYanImgCollectionBean:

    def create_bean(self,
                    id,
                    movie_id,
                    img_url):
        bean = {'id': id,
                'movie_id': movie_id,
                'img_url': img_url}
        return bean
