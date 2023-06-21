import io
import sqlite3
import logging
import sys

logger = logging.getLogger("takeout_analyze")

class SQLite3(object):
    def is_exist_table(table_name,db):
        print('db:',db)
        try:
            con = sqlite3.connect(db)
            print("db connect")
        except sqlite3.Error as e:
            print("db connect error")
            logger.error("sqlite open error. it is an invalid file : %s"% db)
            con.close()
        return False

        cursor = con.consur()
        query = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='%s'" % table_name
        print('query: ',query)

        try:
            cursor.excute(query)
        except sqlite3.Error as e:
            logger.error("sqlite query execution error. query: %s"% query)
            return False
        try:
            ret = cursor.fetchone()
        except sqlite3.Error as e:
            logger.error("sqlite query execution error. query: %s"% query)
            return False

        con.close()
        return ret

    def execute_fetch_query(query, db):
        try:
            con = sqlite3.connect(db)
        except sqlite3.Error as e:
            logger.error("SQLite open error. it is an invalid file: %s" % db)
            return False
        cursor = con.cursor()
        try:
            cursor.execute(query)
        except sqlite3.Error as e:
            logger.error("SQLite query execution error. query: %s" % query)
            return False
        try:
            ret = cursor.fetchone()
        except sqlite3.Error as e:
            logger.error("SQLite query execution error. query: %s" % query)
            return False
        con.close()
        return ret

    def execute_commit_query(queries, db):

        try:
            con = sqlite3.connect(db)
        except sqlite3.Error as e:
            logger.error("SQLite open error. it is an invalid file: %s" % db)
            return False
        cursor = con.cursor()

        query_type = type(queries)

        if query_type == list:
            for query in queries:
                # print('query: %s' % query)
                try:
                    cursor.execute(query)
                except sqlite3.Error as e:
                    logger.error("SQLite query execution error. query: %s" % query)
                    return False
        elif query_type == str:
            try:
                cursor.execute(queries)
            except sqlite3.Error as e:
                logger.error("SQLite query execution error. query: %s" % queries)
                return False
        else:
            print(query_type)

        con.commit()
        con.close()
        return

    def execute_commit_query(query, db, data=None):
        try:
            con = sqlite3.connect(db)
        except sqlite3.Error as e:
            print("SQLite open error. Invalid file:", db)
            return False
        cursor = con.cursor()

        try:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
        except sqlite3.Error as e:
            print("SQLite query execution error. Query:", query)
            return False

        con.commit()
        con.close()
        return True
    def get_all_filepaths(db):

        try:
            con = sqlite3.connect(db)
        except sqlite3.Error as e:
            logger.error("SQLite open error. it is an invalid file: %s" % db)
            return False
        cursor = con.cursor()

        cursor.execute("SELECT filepath FROM jpg_files")
        filepaths = [row[0] for row in cursor.fetchall()]
        con.close()

        return filepaths

    def get_all_filenames(db):

        try:
            con = sqlite3.connect(db)
        except sqlite3.Error as e:
            logger.error("SQLite open error. it is an invalid file: %s" % db)
            return False
        cursor = con.cursor()

        cursor.execute("SELECT filename FROM jpg_files")
        filenames = [row[0] for row in cursor.fetchall()]
        con.close()

        return filenames


    def get_all_fileSize(db):
        try:
            con = sqlite3.connect(db)
        except sqlite3.Error as e:
            logger.error("SQLite open error. it is an invalid file: %s" % db)
            return False
        cursor = con.cursor()

        cursor.execute("SELECT bytes FROM jpg_files")
        filebytes = [row[0] for row in cursor.fetchall()]
        con.close()

        return filebytes

    def get_all_extension(db):
        try:
            con = sqlite3.connect(db)
        except sqlite3.Error as e:
            logger.error("SQLite open error. it is an invalid file: %s" % db)
            return False
        cursor = con.cursor()

        cursor.execute("SELECT extension FROM jpg_files")
        extension = [row[0] for row in cursor.fetchall()]
        con.close()

        return extension

    def get_all_lon(db):
        try:
            con = sqlite3.connect(db)
        except sqlite3.Error as e:
            logger.error("SQLite open error. it is an invalid file: %s" % db)
            return False
        cursor = con.cursor()

        cursor.execute("SELECT longitude FROM jpg_files")
        lon = [row[0] for row in cursor.fetchall()]
        con.close()

        return lon


    def get_all_lat(db):
        try:
            con = sqlite3.connect(db)
        except sqlite3.Error as e:
            logger.error("SQLite open error. it is an invalid file: %s" % db)
            return False
        cursor = con.cursor()

        cursor.execute("SELECT latitude FROM jpg_files")
        lat = [row[0] for row in cursor.fetchall()]
        con.close()

        return lat

    def get_all_suspicious_extension(db):
        try:
            con = sqlite3.connect(db)
        except sqlite3.Error as e:
            logger.error("SQLite open error. it is an invalid file: %s" % db)
            return False
        cursor = con.cursor()

        cursor.execute("SELECT suspicious_extension FROM jpg_files")
        suspicious_extension = [row[0] for row in cursor.fetchall()]
        con.close()

        return suspicious_extension
