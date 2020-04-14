#!/usr/bin/python
# coding=utf-8
import mysql
from mysql.connector import errorcode

from com_zxl_data.MaoYanBean import MaoYanBean
from com_zxl_db.BaseDB import BaseDB


class MaoYanDB(BaseDB):

    NOW_TABLE_NAME = 'mao_yan_now'
    FUTURE_TABLE_NAME = 'mao_yan_future'
    HISTORY_TABLE_NAME = 'mao_yan_history'

    TABLE_NAME = ''

    COLUME_ID = 'id'
    COLUME_MOVIE_ID = 'movie_id'
    COLUME_MOVIE_TITLE = 'movie_title'
    COLUME_MOVIE_POSTER_URL = 'movie_poster_url'
    COLUME_MOVIE_DETAIL_URL = 'movie_detail_url'
    COLUME_MOVIE_TYPE = 'movie_type'

    CREATE_TABLE_SQL = ''

    INSERT_SQL = ''

    DELETE_SQL = ''

    QUERY_BY_MOVIE_ID = ''
    QUERY_ALL = ''

    def __init__(self, table_name):
        self.TABLE_NAME = table_name
        print("MaoYanDB::__init__::TABLE_NAME = " + table_name)

        self.CREATE_TABLE_SQL = (
                "CREATE TABLE IF NOT EXISTS " + self.TABLE_NAME + " ("
                                              + self.COLUME_ID + " bigint(20) NOT NULL AUTO_INCREMENT,"
                                              + self.COLUME_MOVIE_ID + "  text,"
                                              + self.COLUME_MOVIE_TITLE + " text,"
                                              + self.COLUME_MOVIE_POSTER_URL + " text,"
                                              + self.COLUME_MOVIE_DETAIL_URL + " text,"
                                              + self.COLUME_MOVIE_TYPE + " text,"
                                              + "  PRIMARY KEY (" + self.COLUME_ID + ")"
                                              + ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci")

        self.INSERT_SQL = ("INSERT INTO " + self.TABLE_NAME + " ("
                      + self.COLUME_MOVIE_ID + ","
                      + self.COLUME_MOVIE_TITLE + ","
                      + self.COLUME_MOVIE_POSTER_URL + ","
                      + self.COLUME_MOVIE_DETAIL_URL + ","
                      + self.COLUME_MOVIE_TYPE
                      + ") "
                      + "VALUES (%s, %s, %s, %s, %s)")

        self.DELETE_SQL = ("DELETE FROM " + self.TABLE_NAME)

        self.QUERY_BY_MOVIE_ID = ("SELECT "
                             + self.COLUME_ID + ","
                             + self.COLUME_MOVIE_ID + ","
                             + self.COLUME_MOVIE_TITLE + ","
                             + self.COLUME_MOVIE_POSTER_URL + ","
                             + self.COLUME_MOVIE_DETAIL_URL + ","
                             + self.COLUME_MOVIE_TYPE
                             + " FROM " + self.TABLE_NAME
                             + " WHERE " + self.COLUME_MOVIE_ID + " = '%s'")

        self.QUERY_ALL = ("SELECT "
                             + self.COLUME_ID + ","
                             + self.COLUME_MOVIE_ID + ","
                             + self.COLUME_MOVIE_TITLE + ","
                             + self.COLUME_MOVIE_POSTER_URL + ","
                             + self.COLUME_MOVIE_DETAIL_URL + ","
                             + self.COLUME_MOVIE_TYPE
                             + " FROM " + self.TABLE_NAME)

        super(MaoYanDB, self).__init__()

    def create_insert_data(self, mao_yan_bean):
        return (
            mao_yan_bean['movie_id'],
            mao_yan_bean['movie_title'],
            mao_yan_bean['movie_poster_url'],
            mao_yan_bean['movie_detail_url'],
            mao_yan_bean['movie_type']
        )

    def insert_bean(self, mao_yan_bean):
        self.insert(self.INSERT_SQL, self.create_insert_data(mao_yan_bean))

    def delete_all(self):
        self.delete(self.DELETE_SQL)

    def query_by_movie_id(self, movie_id):
        cursor = self.query(self.QUERY_BY_MOVIE_ID % (movie_id,))

        for (COLUME_ID,
             COLUME_MOVIE_ID,
             COLUME_MOVIE_TITLE,
             COLUME_MOVIE_POSTER_URL,
             COLUME_MOVIE_DETAIL_URL,
             COLUME_MOVIE_TYPE) in cursor:
            mao_yan_bean = MaoYanBean()
            return mao_yan_bean.create_bean(COLUME_ID,
                                             COLUME_MOVIE_ID,
                                             COLUME_MOVIE_TITLE,
                                             COLUME_MOVIE_POSTER_URL,
                                             COLUME_MOVIE_DETAIL_URL,
                                             COLUME_MOVIE_TYPE)
        return None

    def query_all(self):
        cursor = self.query(self.QUERY_ALL)

        mao_yan_bean_list = []

        for (COLUME_ID,
             COLUME_MOVIE_ID,
             COLUME_MOVIE_TITLE,
             COLUME_MOVIE_POSTER_URL,
             COLUME_MOVIE_DETAIL_URL,
             COLUME_MOVIE_TYPE) in cursor:
            mao_yan_bean = MaoYanBean()
            mao_yan_bean = mao_yan_bean.create_bean(COLUME_ID,
                                             COLUME_MOVIE_ID,
                                             COLUME_MOVIE_TITLE,
                                             COLUME_MOVIE_POSTER_URL,
                                             COLUME_MOVIE_DETAIL_URL,
                                             COLUME_MOVIE_TYPE)
            mao_yan_bean_list.append(mao_yan_bean)
        return mao_yan_bean_list
