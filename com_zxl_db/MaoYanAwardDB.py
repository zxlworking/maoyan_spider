#!/usr/bin/python
# coding=utf-8
from com_zxl_data.MaoYanAwardBean import MaoYanAwardBean
from com_zxl_data.MaoYanCelebrityBean import MaoYanCelebrityBean
from com_zxl_db.BaseDB import BaseDB


class MaoYanAwardDB(BaseDB):
    TABLE_NAME = 'mao_yan_award'

    COLUME_ID = 'id'
    COLUME_MOVIE_ID = 'movie_id'
    COLUME_AWARD_TITLE = 'award_title'
    COLUME_AWARD_CONTENT = 'award_content'
    COLUME_AWARD_IMG = 'award_img'

    CREATE_TABLE_SQL = ''

    INSERT_SQL = ''

    DELETE_SQL = ''

    DELETE_BY_MOVIE_ID = ''

    QUERY_ALL = ''

    def __init__(self):
        print("MaoYanAwardDB::__init__::TABLE_NAME = " + self.TABLE_NAME)

        self.CREATE_TABLE_SQL = (
                "CREATE TABLE IF NOT EXISTS " + self.TABLE_NAME + " ("
                + self.COLUME_ID + " bigint(20) NOT NULL AUTO_INCREMENT,"
                + self.COLUME_MOVIE_ID + "  text,"
                + self.COLUME_AWARD_TITLE + " text,"
                + self.COLUME_AWARD_CONTENT + " text,"
                + self.COLUME_AWARD_IMG + " text,"
                + "  PRIMARY KEY (" + self.COLUME_ID + ")"
                + ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci")

        self.INSERT_SQL = ("INSERT INTO " + self.TABLE_NAME + " ("
                           + self.COLUME_MOVIE_ID + ","
                           + self.COLUME_AWARD_TITLE + ","
                           + self.COLUME_AWARD_CONTENT + ","
                           + self.COLUME_AWARD_IMG
                           + ") "
                           + "VALUES (%s, %s, %s, %s)")

        self.DELETE_SQL = ("DELETE FROM " + self.TABLE_NAME)

        self.DELETE_BY_MOVIE_ID = ("DELETE FROM  "
                                   + self.TABLE_NAME
                                   + " WHERE " + self.COLUME_MOVIE_ID + " = '%s'")

        self.QUERY_ALL = ("SELECT "
                          + self.COLUME_ID + ","
                          + self.COLUME_MOVIE_ID + ","
                          + self.COLUME_AWARD_TITLE + ","
                          + self.COLUME_AWARD_CONTENT + ","
                          + self.COLUME_AWARD_IMG
                          + " FROM " + self.TABLE_NAME)

        super(MaoYanAwardDB, self).__init__()

    def create_insert_data(self, mao_yan_award_bean):
        return (
            mao_yan_award_bean['movie_id'],
            mao_yan_award_bean['award_title'],
            mao_yan_award_bean['award_content'],
            mao_yan_award_bean['award_img']
        )

    def insert_bean(self, mao_yan_award_bean):
        self.insert(self.INSERT_SQL, self.create_insert_data(mao_yan_award_bean))

    def delete_all(self):
        self.delete(self.DELETE_SQL)

    def delete_by_movie_id(self, movie_id):
        self.delete(self.DELETE_BY_MOVIE_ID % (movie_id,))

    def query_all(self):
        cursor = self.query(self.QUERY_ALL)

        mao_yan_award_bean_list = []

        for (COLUME_ID,
             COLUME_MOVIE_ID,
             COLUME_AWARD_TITLE,
             COLUME_AWARD_CONTENT,
             COLUME_AWARD_IMG) in cursor:
            mao_yan_award_bean = MaoYanAwardBean()
            mao_yan_award_bean = mao_yan_award_bean.create_bean(COLUME_ID,
                                                                        COLUME_MOVIE_ID,
                                                                        COLUME_AWARD_TITLE,
                                                                        COLUME_AWARD_CONTENT,
                                                                        COLUME_AWARD_IMG)
            mao_yan_award_bean_list.append(mao_yan_award_bean)
        return mao_yan_award_bean_list
