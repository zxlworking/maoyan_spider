#!/usr/bin/python
# coding=utf-8

from com_zxl_data.MaoYanDetailBean import MaoYanDetailBean
from com_zxl_db.BaseDB import BaseDB


class MaoYanDetailDB(BaseDB):
    TABLE_NAME = 'mao_yan_detail'

    COLUME_ID = 'id'
    COLUME_MOVIE_ID = 'movie_id'
    COLUME_MOVIE_AVATAR = 'movie_avatar_url'
    COLUME_MOVIE_NAME = 'movie_name'
    COLUME_MOVIE_EN_NAME = 'movie_en_name'
    COLUME_MOVIE_CATEGORY = 'movie_category'
    COLUME_MOVIE_COUNTRY = 'movie_country'
    COLUME_MOVIE_DURATION = 'movie_duration'
    COLUME_MOVIE_RELEASE_INFO = 'movie_release_info'
    COLUME_MOVIE_RELEASE_TIME = 'movie_release_time'
    COLUME_MOVIE_RELEASE_AREA = 'movie_release_area'
    COLUME_MOVIE_SCORE_CONTENT = 'movie_score_content'
    COLUME_MOVIE_WANT_TO_SEE_COUNT = 'movie_want_to_see_count'
    COLUME_MOVIE_STATS_PEOPLE_COUNT_CONTENT = 'movie_stats_people_count_content'
    COLUME_MOVIE_STATS_PEOPLE_COUNT_UNIT_CONTENT = 'movie_stats_people_count_unit_content'
    COLUME_MOVIE_BOX_VALUE_CONTENT = 'movie_box_value_content'
    COLUME_MOVIE_BOX_UNIT_CONTENT = 'movie_box_unit_content'
    COLUME_MOVIE_INTRODUCE_CONTENT = 'introduce_content'

    CREATE_TABLE_SQL = ''

    INSERT_SQL = ''

    DELETE_SQL = ''

    UPDATE_BY_MOVIE_ID = ''

    QUERY_BY_MOVIE_ID = ''

    def __init__(self):
        print("MaoYanDetailDB::__init__::TABLE_NAME = " + self.TABLE_NAME)

        self.CREATE_TABLE_SQL = (
                "CREATE TABLE IF NOT EXISTS " + self.TABLE_NAME + " ("
                + self.COLUME_ID + " bigint(20) NOT NULL AUTO_INCREMENT,"
                + self.COLUME_MOVIE_ID + "  text,"
                + self.COLUME_MOVIE_AVATAR + "  text,"
                + self.COLUME_MOVIE_NAME + "  text,"
                + self.COLUME_MOVIE_EN_NAME + "  text,"
                + self.COLUME_MOVIE_CATEGORY + "  text,"
                + self.COLUME_MOVIE_COUNTRY + "  text,"
                + self.COLUME_MOVIE_DURATION + "  text,"
                + self.COLUME_MOVIE_RELEASE_INFO + "  text,"
                + self.COLUME_MOVIE_RELEASE_TIME + "  text,"
                + self.COLUME_MOVIE_RELEASE_AREA + "  text,"
                + self.COLUME_MOVIE_SCORE_CONTENT + "  text,"
                + self.COLUME_MOVIE_WANT_TO_SEE_COUNT + "  text,"
                + self.COLUME_MOVIE_STATS_PEOPLE_COUNT_CONTENT + "  text,"
                + self.COLUME_MOVIE_STATS_PEOPLE_COUNT_UNIT_CONTENT + "  text,"
                + self.COLUME_MOVIE_BOX_VALUE_CONTENT + "  text,"
                + self.COLUME_MOVIE_BOX_UNIT_CONTENT + "  text,"
                + self.COLUME_MOVIE_INTRODUCE_CONTENT + "  text,"
                + "  PRIMARY KEY (" + self.COLUME_ID + ")"
                + ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci")

        self.INSERT_SQL = ("INSERT INTO " + self.TABLE_NAME + " ("
                           + self.COLUME_MOVIE_ID + ","
                           + self.COLUME_MOVIE_AVATAR + ","
                           + self.COLUME_MOVIE_NAME + ","
                           + self.COLUME_MOVIE_EN_NAME + ","
                           + self.COLUME_MOVIE_CATEGORY + ","
                           + self.COLUME_MOVIE_COUNTRY + ","
                           + self.COLUME_MOVIE_DURATION + ","
                           + self.COLUME_MOVIE_RELEASE_INFO + ","
                           + self.COLUME_MOVIE_RELEASE_TIME + ","
                           + self.COLUME_MOVIE_RELEASE_AREA + ","
                           + self.COLUME_MOVIE_SCORE_CONTENT + ","
                           + self.COLUME_MOVIE_WANT_TO_SEE_COUNT + ","
                           + self.COLUME_MOVIE_STATS_PEOPLE_COUNT_CONTENT + ","
                           + self.COLUME_MOVIE_STATS_PEOPLE_COUNT_UNIT_CONTENT + ","
                           + self.COLUME_MOVIE_BOX_VALUE_CONTENT + ","
                           + self.COLUME_MOVIE_BOX_UNIT_CONTENT + ","
                           + self.COLUME_MOVIE_INTRODUCE_CONTENT
                           + ") "
                           + "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        self.DELETE_SQL = ("DELETE FROM " + self.TABLE_NAME)

        self.UPDATE_BY_MOVIE_ID = ("UPDATE " + self.TABLE_NAME + " SET "
                                   + self.COLUME_MOVIE_AVATAR + " = '%s', "
                                   + self.COLUME_MOVIE_NAME + " = '%s', "
                                   + self.COLUME_MOVIE_EN_NAME + " = '%s', "
                                   + self.COLUME_MOVIE_CATEGORY + " = '%s', "
                                   + self.COLUME_MOVIE_COUNTRY + " = '%s', "
                                   + self.COLUME_MOVIE_DURATION + " = '%s', "
                                   + self.COLUME_MOVIE_RELEASE_INFO + " = '%s', "
                                   + self.COLUME_MOVIE_RELEASE_TIME + " = '%s', "
                                   + self.COLUME_MOVIE_RELEASE_AREA + " = '%s', "
                                   + self.COLUME_MOVIE_SCORE_CONTENT + " = '%s', "
                                   + self.COLUME_MOVIE_WANT_TO_SEE_COUNT + " = '%s', "
                                   + self.COLUME_MOVIE_STATS_PEOPLE_COUNT_CONTENT + " = '%s', "
                                   + self.COLUME_MOVIE_STATS_PEOPLE_COUNT_UNIT_CONTENT + " = '%s', "
                                   + self.COLUME_MOVIE_BOX_VALUE_CONTENT + " = '%s', "
                                   + self.COLUME_MOVIE_BOX_UNIT_CONTENT + " = '%s', "
                                   + self.COLUME_MOVIE_INTRODUCE_CONTENT + " = '%s' "
                                   + " WHERE " + self.COLUME_MOVIE_ID + " = '%s'")

        self.QUERY_BY_MOVIE_ID = ("SELECT "
                                  + self.COLUME_ID + ","
                                  + self.COLUME_MOVIE_ID + ","
                                  + self.COLUME_MOVIE_AVATAR + ","
                                  + self.COLUME_MOVIE_NAME + ","
                                  + self.COLUME_MOVIE_EN_NAME + ","
                                  + self.COLUME_MOVIE_CATEGORY + ","
                                  + self.COLUME_MOVIE_COUNTRY + ","
                                  + self.COLUME_MOVIE_DURATION + ","
                                  + self.COLUME_MOVIE_RELEASE_INFO + ","
                                  + self.COLUME_MOVIE_RELEASE_TIME + ","
                                  + self.COLUME_MOVIE_RELEASE_AREA + ","
                                  + self.COLUME_MOVIE_SCORE_CONTENT + ","
                                  + self.COLUME_MOVIE_WANT_TO_SEE_COUNT + ","
                                  + self.COLUME_MOVIE_STATS_PEOPLE_COUNT_CONTENT + ","
                                  + self.COLUME_MOVIE_STATS_PEOPLE_COUNT_UNIT_CONTENT + ","
                                  + self.COLUME_MOVIE_BOX_VALUE_CONTENT + ","
                                  + self.COLUME_MOVIE_BOX_UNIT_CONTENT + ","
                                  + self.COLUME_MOVIE_INTRODUCE_CONTENT
                                  + " FROM " + self.TABLE_NAME
                                  + " WHERE " + self.COLUME_MOVIE_ID + " = '%s'")

        self.QUERY_ALL = ("SELECT "
                          + self.COLUME_ID + ","
                          + self.COLUME_MOVIE_ID + ","
                          + self.COLUME_MOVIE_AVATAR + ","
                          + self.COLUME_MOVIE_NAME + ","
                          + self.COLUME_MOVIE_EN_NAME + ","
                          + self.COLUME_MOVIE_CATEGORY + ","
                          + self.COLUME_MOVIE_COUNTRY + ","
                          + self.COLUME_MOVIE_DURATION + ","
                          + self.COLUME_MOVIE_RELEASE_INFO + ","
                          + self.COLUME_MOVIE_RELEASE_TIME + ","
                          + self.COLUME_MOVIE_RELEASE_AREA + ","
                          + self.COLUME_MOVIE_SCORE_CONTENT + ","
                          + self.COLUME_MOVIE_WANT_TO_SEE_COUNT + ","
                          + self.COLUME_MOVIE_STATS_PEOPLE_COUNT_CONTENT + ","
                          + self.COLUME_MOVIE_STATS_PEOPLE_COUNT_UNIT_CONTENT + ","
                          + self.COLUME_MOVIE_BOX_VALUE_CONTENT + ","
                          + self.COLUME_MOVIE_BOX_UNIT_CONTENT + ","
                          + self.COLUME_MOVIE_INTRODUCE_CONTENT
                          + " FROM " + self.TABLE_NAME)

        super(MaoYanDetailDB, self).__init__()

    def create_insert_data(self, mao_yan_detail_bean):
        return (
            mao_yan_detail_bean['movie_id'],
            mao_yan_detail_bean['movie_avatar_url'],
            mao_yan_detail_bean['movie_name'],
            mao_yan_detail_bean['movie_en_name'],
            mao_yan_detail_bean['movie_category'],
            mao_yan_detail_bean['movie_country'],
            mao_yan_detail_bean['movie_duration'],
            mao_yan_detail_bean['movie_release_info'],
            mao_yan_detail_bean['movie_release_time'],
            mao_yan_detail_bean['movie_release_area'],
            mao_yan_detail_bean['movie_score_content'],
            mao_yan_detail_bean['movie_want_to_see_count'],
            mao_yan_detail_bean['movie_stats_people_count_content'],
            mao_yan_detail_bean['movie_stats_people_count_unit_content'],
            mao_yan_detail_bean['movie_box_value_content'],
            mao_yan_detail_bean['movie_box_unit_content'],
            mao_yan_detail_bean['introduce_content']
        )

    def create_update_data(self, mao_yan_detail_bean):
        return (
            mao_yan_detail_bean['movie_avatar_url'],
            mao_yan_detail_bean['movie_name'],
            mao_yan_detail_bean['movie_en_name'],
            mao_yan_detail_bean['movie_category'],
            mao_yan_detail_bean['movie_country'],
            mao_yan_detail_bean['movie_duration'],
            mao_yan_detail_bean['movie_release_info'],
            mao_yan_detail_bean['movie_release_time'],
            mao_yan_detail_bean['movie_release_area'],
            mao_yan_detail_bean['movie_score_content'],
            mao_yan_detail_bean['movie_want_to_see_count'],
            mao_yan_detail_bean['movie_stats_people_count_content'],
            mao_yan_detail_bean['movie_stats_people_count_unit_content'],
            mao_yan_detail_bean['movie_box_value_content'],
            mao_yan_detail_bean['movie_box_unit_content'],
            mao_yan_detail_bean['introduce_content'],
            mao_yan_detail_bean['movie_id']
        )

    def insert_bean(self, mao_yan_detail_bean):
        self.insert(self.INSERT_SQL, self.create_insert_data(mao_yan_detail_bean))

    def delete_all(self):
        self.delete(self.DELETE_SQL)

    def update_by_movie_id(self, mao_yan_detail_bean):
        self.update(self.UPDATE_BY_MOVIE_ID % self.create_update_data(mao_yan_detail_bean))

    def query_by_movie_id(self, movie_id):
        cursor = self.query(self.QUERY_BY_MOVIE_ID % (movie_id,))

        for (COLUME_ID,
             COLUME_MOVIE_ID,
             COLUME_MOVIE_AVATAR,
             COLUME_MOVIE_NAME,
             COLUME_MOVIE_EN_NAME,
             COLUME_MOVIE_CATEGORY,
             COLUME_MOVIE_COUNTRY,
             COLUME_MOVIE_DURATION,
             COLUME_MOVIE_RELEASE_INFO,
             COLUME_MOVIE_RELEASE_TIME,
             COLUME_MOVIE_RELEASE_AREA,
             COLUME_MOVIE_SCORE_CONTENT,
             COLUME_MOVIE_WANT_TO_SEE_COUNT,
             COLUME_MOVIE_STATS_PEOPLE_COUNT_CONTENT,
             COLUME_MOVIE_STATS_PEOPLE_COUNT_UNIT_CONTENT,
             COLUME_MOVIE_BOX_VALUE_CONTENT,
             COLUME_MOVIE_BOX_UNIT_CONTENT,
             COLUME_MOVIE_INTRODUCE_CONTENT) in cursor:
            mao_yan_detail_bean = MaoYanDetailBean()
            return mao_yan_detail_bean.create_bean(COLUME_ID,
                                                   COLUME_MOVIE_ID,
                                                   COLUME_MOVIE_AVATAR,
                                                   COLUME_MOVIE_NAME,
                                                   COLUME_MOVIE_EN_NAME,
                                                   COLUME_MOVIE_CATEGORY,
                                                   COLUME_MOVIE_COUNTRY,
                                                   COLUME_MOVIE_DURATION,
                                                   COLUME_MOVIE_RELEASE_INFO,
                                                   COLUME_MOVIE_RELEASE_TIME,
                                                   COLUME_MOVIE_RELEASE_AREA,
                                                   COLUME_MOVIE_SCORE_CONTENT,
                                                   COLUME_MOVIE_WANT_TO_SEE_COUNT,
                                                   COLUME_MOVIE_STATS_PEOPLE_COUNT_CONTENT,
                                                   COLUME_MOVIE_STATS_PEOPLE_COUNT_UNIT_CONTENT,
                                                   COLUME_MOVIE_BOX_VALUE_CONTENT,
                                                   COLUME_MOVIE_BOX_UNIT_CONTENT,
                                                   COLUME_MOVIE_INTRODUCE_CONTENT)
        return None

    def query_all(self):
        cursor = self.query(self.QUERY_ALL)

        mao_yan_detail_bean_list = []

        for (COLUME_ID,
             COLUME_MOVIE_ID,
             COLUME_MOVIE_AVATAR,
             COLUME_MOVIE_NAME,
             COLUME_MOVIE_EN_NAME,
             COLUME_MOVIE_CATEGORY,
             COLUME_MOVIE_COUNTRY,
             COLUME_MOVIE_DURATION,
             COLUME_MOVIE_RELEASE_INFO,
             COLUME_MOVIE_RELEASE_TIME,
             COLUME_MOVIE_RELEASE_AREA,
             COLUME_MOVIE_SCORE_CONTENT,
             COLUME_MOVIE_WANT_TO_SEE_COUNT,
             COLUME_MOVIE_STATS_PEOPLE_COUNT_CONTENT,
             COLUME_MOVIE_STATS_PEOPLE_COUNT_UNIT_CONTENT,
             COLUME_MOVIE_BOX_VALUE_CONTENT,
             COLUME_MOVIE_BOX_UNIT_CONTENT,
             COLUME_MOVIE_INTRODUCE_CONTENT) in cursor:
            mao_yan_detail_bean = MaoYanDetailBean()
            mao_yan_detail_bean = mao_yan_detail_bean.create_bean(COLUME_ID,
                                                                  COLUME_MOVIE_ID,
                                                                  COLUME_MOVIE_AVATAR,
                                                                  COLUME_MOVIE_NAME,
                                                                  COLUME_MOVIE_EN_NAME,
                                                                  COLUME_MOVIE_CATEGORY,
                                                                  COLUME_MOVIE_COUNTRY,
                                                                  COLUME_MOVIE_DURATION,
                                                                  COLUME_MOVIE_RELEASE_INFO,
                                                                  COLUME_MOVIE_RELEASE_TIME,
                                                                  COLUME_MOVIE_RELEASE_AREA,
                                                                  COLUME_MOVIE_SCORE_CONTENT,
                                                                  COLUME_MOVIE_WANT_TO_SEE_COUNT,
                                                                  COLUME_MOVIE_STATS_PEOPLE_COUNT_CONTENT,
                                                                  COLUME_MOVIE_STATS_PEOPLE_COUNT_UNIT_CONTENT,
                                                                  COLUME_MOVIE_BOX_VALUE_CONTENT,
                                                                  COLUME_MOVIE_BOX_UNIT_CONTENT,
                                                                  COLUME_MOVIE_INTRODUCE_CONTENT)
            mao_yan_detail_bean_list.append(mao_yan_detail_bean)
        return mao_yan_detail_bean_list
