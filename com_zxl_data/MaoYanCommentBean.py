# /usr/bin/python
# coding=utf-8


class MaoYanCommentBean:

    def create_bean(self,
                    id,
                    movie_id,
                    comment_user_name,
                    comment_user_head_img,
                    comment_content,
                    comment_time,
                    comment_approve_num):
        bean = {'id': id,
                'movie_id': movie_id,
                'comment_user_name': comment_user_name,
                'comment_user_head_img': comment_user_head_img,
                'comment_content': comment_content,
                'comment_time': comment_time,
                'comment_approve_num': comment_approve_num}
        return bean
