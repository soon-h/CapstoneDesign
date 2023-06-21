import os
import logging

import sql.takeout_analyze
from sql.sqlite_takeout import SQLite3
import sql.process
logger = logging.getLogger("takeout_analyze")

GOOGLE_PHOTO = 'Google 포토'

class Case:
    def __init__(self, input_dir, output_dir):
        self.preprocess_db_path = None
        self.input_dir_path = input_dir
        self.output_dir_path = output_dir

    def get_preprocess_db_path(self):
        return self.preprocess_db_path

    def set_file_path(self):
        if self.input_dir_path[-1] == os.sep:
            self.input_dir_path = self.input_dir_path[:-1]
        if self.output_dir_path[-1] == os.sep:
            self.output_dir_path = self.output_dir_path[:-1]

        self.takeout_path = self.input_dir_path + os.sep + 'Takeout'
        if os.path.exists(self.takeout_path) == False:
            logger.error("takeout data not exist")
            return False

        self.takeout_google_photo_path = self.takeout_path + os.sep + GOOGLE_PHOTO


        self.output_dir_path = self.output_dir_path + os.sep + os.path.basename(self.input_dir_path)
        self.preprocess_db_path = self.output_dir_path + os.sep + 'preprocess_' + os.path.basename(self.input_dir_path) + '_takeout.db'

        if os.path.exists(self.output_dir_path) == False:
            os.makedirs(self.output_dir_path)



    def create_db(self):
        query_create_google_photo = "CREATE TABLE IF NOT EXISTS parse_google_photo \
         (parentpath TEXT, album_name TEXT, filename TEXT, extension TEXT, bytes INTEGER, \
         album_created_time INTEGER, photo_taken_time INTEGER, photo_created_time INTEGER, photo_modified_time INTEGER, file_modified_time INTEGER, \
         latitude TEXT, longitude TEXT, latitude_span TEXT, longitude_span TEXT, \
         exif_latitude TEXT, exif_longitude TEXT, exif_latitude_span TEXT, exif_longitude_span TEXT, filepath TEXT)"


        SQLite3.execute_commit_query(query_create_google_photo,str(self.preprocess_db_path))


    def create_exists_db(self):
        query_create_exists_table = """ CREATE TABLE IF NOT EXISTS jpg_files
                                        AS 
                                        SELECT 
                                            parentpath, album_name, filename, extension, bytes,
                                            album_created_time, photo_taken_time, photo_created_time, photo_modified_time, file_modified_time,
                                            latitude, longitude, latitude_span, longitude_span,
                                            exif_latitude, exif_longitude, exif_latitude_span, exif_longitude_span, filepath,
                                            "" AS suspicious_extension
                                        FROM parse_google_photo
                                        WHERE filepath LIKE '%.jpg' OR filepath LIKE '%.JPG' OR filepath LIKE '%.png' OR filepath LIKE '%.PNG';"""


        SQLite3.execute_commit_query(query_create_exists_table,str(self.preprocess_db_path))


def db_process(check):
    input_dir = "./" + check

    output_dir = './'
    case = Case(input_dir, output_dir)
    case.set_file_path()
    case.create_db()
    sql.takeout_analyze.GooglePhoto.parse_google_photo(case)
    case.create_exists_db()
    path = SQLite3.get_all_filepaths(Case.get_preprocess_db_path(case))

    sql.process.extcheck(path,Case.get_preprocess_db_path(case))

    name = SQLite3.get_all_filenames(Case.get_preprocess_db_path(case))
    size = SQLite3.get_all_fileSize(Case.get_preprocess_db_path(case))
    extension = SQLite3.get_all_extension(Case.get_preprocess_db_path(case))
    lon = SQLite3.get_all_lon(Case.get_preprocess_db_path(case))
    lat = SQLite3.get_all_lat(Case.get_preprocess_db_path(case))
    suspicious_extension = SQLite3.get_all_suspicious_extension(Case.get_preprocess_db_path(case))
    return path,name,size,extension,lon,lat,suspicious_extension