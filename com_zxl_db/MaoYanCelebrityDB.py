#!/usr/bin/python
# coding=utf-8

from com_zxl_data.MaoYanCelebrityBean import MaoYanCelebrityBean
from com_zxl_db.BaseDB import BaseDB


class MaoYanCelebrityDB(BaseDB):
    TABLE_NAME = 'mao_yan_celebrity'

    COLUME_ID = 'id'
    COLUME_MOVIE_ID = 'movie_id'
    COLUME_CELEBRITY_TYPE_NAME = 'celebrity_type_name'
    COLUME_CELEBRITY_NAME = 'celebrity_name'
    COLUME_CELEBRITY_ROLE_NAME = 'celebrity_role_name'
    COLUME_CELEBRITY_HEAD_IMG = 'celebrity_head_img'
    COLUME_CELEBRITY_DETAIL_URL = 'celebrity_detail_url'

    CREATE_TABLE_SQL = ''

    INSERT_SQL = ''

    DELETE_SQL = ''

    DELETE_BY_MOVIE_ID = ''

    QUERY_ALL = ''

    def __init__(self):
        print("MaoYanCelebrityDB::__init__::TABLE_NAME = " + self.TABLE_NAME)

        self.CREATE_TABLE_SQL = (
                "CREATE TABLE IF NOT EXISTS " + self.TABLE_NAME + " ("
                + self.COLUME_ID + " bigint(20) NOT NULL AUTO_INCREMENT,"
                + self.COLUME_MOVIE_ID + "  text,"
                + self.COLUME_CELEBRITY_TYPE_NAME + " text,"
                + self.COLUME_CELEBRITY_NAME + " text,"
                + self.COLUME_CELEBRITY_ROLE_NAME + " text,"
                + self.COLUME_CELEBRITY_HEAD_IMG + " text,"
                + self.COLUME_CELEBRITY_DETAIL_URL + " text,"
                + "  PRIMARY KEY (" + self.COLUME_ID + ")"
                + ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci")

        self.INSERT_SQL = ("INSERT INTO " + self.TABLE_NAME + " ("
                           + self.COLUME_MOVIE_ID + ","
                           + self.COLUME_CELEBRITY_TYPE_NAME + ","
                           + self.COLUME_CELEBRITY_NAME + ","
                           + self.COLUME_CELEBRITY_ROLE_NAME + ","
                           + self.COLUME_CELEBRITY_HEAD_IMG + ","
                           + self.COLUME_CELEBRITY_DETAIL_URL
                           + ") "
                           + "VALUES (%s, %s, %s, %s, %s, %s)")

        self.DELETE_SQL = ("DELETE FROM " + self.TABLE_NAME)

        self.DELETE_BY_MOVIE_ID = ("DELETE FROM  "
                                   + self.TABLE_NAME
                                   + " WHERE " + self.COLUME_MOVIE_ID + " = '%s'")

        self.QUERY_ALL = ("SELECT "
                          + self.COLUME_ID + ","
                          + self.COLUME_MOVIE_ID + ","
                          + self.COLUME_CELEBRITY_TYPE_NAME + ","
                          + self.COLUME_CELEBRITY_NAME + ","
                          + self.COLUME_CELEBRITY_ROLE_NAME + ","
                          + self.COLUME_CELEBRITY_HEAD_IMG + ","
                          + self.COLUME_CELEBRITY_DETAIL_URL
                          + " FROM " + self.TABLE_NAME)

        super(MaoYanCelebrityDB, self).__init__()

    def create_insert_data(self, mao_yan_celebrity_bean):
        return (
            mao_yan_celebrity_bean['movie_id'],
            mao_yan_celebrity_bean['celebrity_type_name'],
            mao_yan_celebrity_bean['celebrity_name'],
            mao_yan_celebrity_bean['celebrity_role_name'],
            mao_yan_celebrity_bean['celebrity_head_img'],
            mao_yan_celebrity_bean['celebrity_detail_url']
        )

    def insert_bean(self, mao_yan_celebrity_bean):
        self.insert(self.INSERT_SQL, self.create_insert_data(mao_yan_celebrity_bean))

    def delete_all(self):
        self.delete(self.DELETE_SQL)

    def delete_by_movie_id(self, movie_id):
        self.delete(self.DELETE_BY_MOVIE_ID % (movie_id,))

    def query_all(self):
        cursor = self.query(self.QUERY_ALL)

        mao_yan_celebrity_bean_list = []

        for (COLUME_ID,
             COLUME_MOVIE_ID,
             COLUME_CELEBRITY_TYPE_NAME,
             COLUME_CELEBRITY_NAME,
             COLUME_CELEBRITY_ROLE_NAME,
             COLUME_CELEBRITY_HEAD_IMG,
             COLUME_CELEBRITY_DETAIL_URL) in cursor:
            mao_yan_celebrity_bean = MaoYanCelebrityBean()
            mao_yan_celebrity_bean = mao_yan_celebrity_bean.create_bean(COLUME_ID,
                                                                        COLUME_MOVIE_ID,
                                                                        COLUME_CELEBRITY_TYPE_NAME,
                                                                        COLUME_CELEBRITY_NAME,
                                                                        COLUME_CELEBRITY_ROLE_NAME,
                                                                        COLUME_CELEBRITY_HEAD_IMG,
                                                                        COLUME_CELEBRITY_DETAIL_URL)
            mao_yan_celebrity_bean_list.append(mao_yan_celebrity_bean)
        return mao_yan_celebrity_bean_list
