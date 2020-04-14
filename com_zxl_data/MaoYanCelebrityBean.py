# /usr/bin/python
# coding=utf-8


class MaoYanCelebrityBean:

    def create_bean(self,
                    id,
                    movie_id,
                    celebrity_type_name,
                    celebrity_name,
                    celebrity_role_name,
                    celebrity_head_img,
                    celebrity_detail_url):
        bean = {'id': id,
                'movie_id': movie_id,
                'celebrity_type_name': celebrity_type_name,
                'celebrity_name': celebrity_name,
                'celebrity_role_name': celebrity_role_name,
                'celebrity_head_img': celebrity_head_img,
                'celebrity_detail_url': celebrity_detail_url}
        return bean
