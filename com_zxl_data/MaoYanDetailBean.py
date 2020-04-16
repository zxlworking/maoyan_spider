# /usr/bin/python
# coding=utf-8


class MaoYanDetailBean:
    id = ''
    movie_id = ''
    movie_avatar_url = ''
    movie_name = ''
    movie_en_name = ''
    movie_category = ''
    movie_country = ''
    movie_duration = ''
    movie_release_info = ''
    movie_release_time = ''
    movie_release_area = ''
    movie_score_content = ''
    movie_want_to_see_count = ''
    movie_stats_people_count_content = ''
    movie_stats_people_count_unit_content = ''
    movie_box_value_content = ''
    movie_box_unit_content = ''
    introduce_content = ''

    def create_bean_dict(self):
        bean_dict = {'id': self.id,
                'movie_id': self.movie_id,
                "movie_avatar_url": self.movie_avatar_url,
                "movie_name": self.movie_name,
                "movie_en_name": self.movie_en_name,
                "movie_category": self.movie_category,
                "movie_country": self.movie_country,
                "movie_duration": self.movie_duration,
                "movie_release_info": self.movie_release_info,
                "movie_release_time": self.movie_release_time,
                "movie_release_area": self.movie_release_area,
                "movie_score_content": self.movie_score_content,
                "movie_want_to_see_count": self.movie_want_to_see_count,
                "movie_stats_people_count_content": self.movie_stats_people_count_content,
                "movie_stats_people_count_unit_content": self.movie_stats_people_count_unit_content,
                "movie_box_value_content": self.movie_box_value_content,
                "movie_box_unit_content": self.movie_box_unit_content,
                "introduce_content": self.introduce_content}
        return bean_dict
