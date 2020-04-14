#!/usr/bin/python
# coding=utf-8

from com_zxl_data.MaoYanCelebrityBean import MaoYanCelebrityBean
from com_zxl_data.MaoYanCommentBean import MaoYanCommentBean
from com_zxl_db.BaseDB import BaseDB


class MaoYanCommentDB(BaseDB):
    TABLE_NAME = 'mao_yan_comment'

    COLUME_ID = 'id'
    COLUME_MOVIE_ID = 'movie_id'
    COLUME_COMMENT_USER_NAME = 'comment_user_name'
    COLUME_COMMENT_USER_HEAD_IMG = 'comment_user_head_img'
    COLUME_COMMENT_CONTENT = 'comment_content'
    COLUME_COMMENT_TIME = 'comment_time'
    COLUME_COMMENT_APPROVE_NUM = 'comment_approve_num'

    CREATE_TABLE_SQL = ''

    INSERT_SQL = ''

    DELETE_SQL = ''

    DELETE_BY_MOVIE_ID = ''

    QUERY_ALL = ''

    def __init__(self):
        print("MaoYanCommentDB::__init__::TABLE_NAME = " + self.TABLE_NAME)

        self.CREATE_TABLE_SQL = (
                "CREATE TABLE IF NOT EXISTS " + self.TABLE_NAME + " ("
                + self.COLUME_ID + " bigint(20) NOT NULL AUTO_INCREMENT,"
                + self.COLUME_MOVIE_ID + "  text,"
                + self.COLUME_COMMENT_USER_NAME + " text,"
                + self.COLUME_COMMENT_USER_HEAD_IMG + " text,"
                + self.COLUME_COMMENT_CONTENT + " text,"
                + self.COLUME_COMMENT_TIME + " text,"
                + self.COLUME_COMMENT_APPROVE_NUM + " text,"
                + "  PRIMARY KEY (" + self.COLUME_ID + ")"
                + ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci")

        self.INSERT_SQL = ("INSERT INTO " + self.TABLE_NAME + " ("
                           + self.COLUME_MOVIE_ID + ","
                           + self.COLUME_COMMENT_USER_NAME + ","
                           + self.COLUME_COMMENT_USER_HEAD_IMG + ","
                           + self.COLUME_COMMENT_CONTENT + ","
                           + self.COLUME_COMMENT_TIME + ","
                           + self.COLUME_COMMENT_APPROVE_NUM
                           + ") "
                           + "VALUES (%s, %s, %s, %s, %s, %s)")

        self.DELETE_SQL = ("DELETE FROM " + self.TABLE_NAME)

        self.DELETE_BY_MOVIE_ID = ("DELETE FROM  "
                                   + self.TABLE_NAME
                                   + " WHERE " + self.COLUME_MOVIE_ID + " = '%s'")

        self.QUERY_ALL = ("SELECT "
                          + self.COLUME_ID + ","
                          + self.COLUME_MOVIE_ID + ","
                          + self.COLUME_COMMENT_USER_NAME + ","
                          + self.COLUME_COMMENT_USER_HEAD_IMG + ","
                          + self.COLUME_COMMENT_CONTENT + ","
                          + self.COLUME_COMMENT_TIME + ","
                          + self.COLUME_COMMENT_APPROVE_NUM
                          + " FROM " + self.TABLE_NAME)

        super(MaoYanCommentDB, self).__init__()

    def create_insert_data(self, mao_yan_comment_bean):
        return (
            mao_yan_comment_bean['movie_id'],
            mao_yan_comment_bean['comment_user_name'],
            mao_yan_comment_bean['comment_user_head_img'],
            mao_yan_comment_bean['comment_content'],
            mao_yan_comment_bean['comment_time'],
            mao_yan_comment_bean['comment_approve_num']
        )

    def insert_bean(self, mao_yan_comment_bean):
        self.insert(self.INSERT_SQL, self.create_insert_data(mao_yan_comment_bean))

    def delete_all(self):
        self.delete(self.DELETE_SQL)

    def delete_by_movie_id(self, movie_id):
        self.delete(self.DELETE_BY_MOVIE_ID % (movie_id,))

    def query_all(self):
        cursor = self.query(self.QUERY_ALL)

        mao_yan_comment_list = []

        for (COLUME_ID,
             COLUME_MOVIE_ID,
             COLUME_COMMENT_USER_NAME,
             COLUME_COMMENT_USER_HEAD_IMG,
             COLUME_COMMENT_CONTENT,
             COLUME_COMMENT_TIME,
             COLUME_COMMENT_APPROVE_NUM) in cursor:
            mao_yan_comment_bean = MaoYanCommentBean()
            mao_yan_comment_bean = mao_yan_comment_bean.create_bean(COLUME_ID,
                                                                        COLUME_MOVIE_ID,
                                                                        COLUME_COMMENT_USER_NAME,
                                                                        COLUME_COMMENT_USER_HEAD_IMG,
                                                                        COLUME_COMMENT_CONTENT,
                                                                        COLUME_COMMENT_TIME,
                                                                        COLUME_COMMENT_APPROVE_NUM)
            mao_yan_comment_list.append(mao_yan_comment_bean)
        return mao_yan_comment_list
