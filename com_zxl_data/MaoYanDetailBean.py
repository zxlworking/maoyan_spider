# /usr/bin/python
# coding=utf-8


class MaoYanDetailBean:

    def create_bean(self,
                    id,
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
                    introduce_content):
        bean = {'id': id,
                'movie_id': movie_id,
                "movie_avatar_url": movie_avatar_url,
                "movie_name": movie_name,
                "movie_en_name": movie_en_name,
                "movie_category": movie_category,
                "movie_country": movie_country,
                "movie_duration": movie_duration,
                "movie_release_info": movie_release_info,
                "movie_release_time": movie_release_time,
                "movie_release_area": movie_release_area,
                "movie_score_content": movie_score_content,
                "movie_want_to_see_count": movie_want_to_see_count,
                "movie_stats_people_count_content": movie_stats_people_count_content,
                "movie_stats_people_count_unit_content": movie_stats_people_count_unit_content,
                "movie_box_value_content": movie_box_value_content,
                "movie_box_unit_content": movie_box_unit_content,
                "introduce_content": introduce_content}
        return bean
