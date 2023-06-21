from PIL import Image

from sql.sqlite_takeout import SQLite3


def get_image_size(paths,db_path):

    update_width_query = "UPDATE jpg_files SET width = ? WHERE filepath = ?"
    update_height_query = "UPDATE jpg_files SET height = ? WHERE filepath = ?"

    for path in paths:
        with Image.open(path) as img:
            width, height = img.size
            SQLite3.execute_commit_query(update_width_query, db_path, (width,path))
            SQLite3.execute_commit_query(update_height_query, db_path, (width,path))


def search_signature(file_path, signature):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
        if isinstance(signature, list):
            for sig in signature:
                if bytes.fromhex(str(sig)) in binary_data:
                    return True
            return False
        else:
            if bytes.fromhex(str(signature)) in binary_data:
                return True
            return False


def extcheck(paths, db_path):
    # 데이터베이스에 값을 추가하는 쿼리 생성
    update_query = "UPDATE jpg_files SET suspicious_extension = ? WHERE filepath = ?"

    extensions = {
        'hwp': '48575020',
        'jpg': ['FFD8FF', 'FFD8FFE8'],
        'mp3': '49443303',
        'mp4': '0000001866747970',
        'jar': '4A4152435300',
        'docx': '504B030414000600',
        'pptx': '504B030414000600',
        'zip': '504B0304',
        'png': '89504E470D0A1A0A',
        'pdf': '255044462D312E',
        'alzip': '414C5A01',
        'ppt': 'D0CF11E0A1B11AE1'
        # 다른 확장자에 대한 시그니처도 추가할 수 있습니다
    }

    for path in paths:
        file_path = path
        print(file_path)
        suspicious_extensions = []

        for extension, signature in extensions.items():
            if search_signature(file_path, signature):
                suspicious_extensions.append(extension)

        # 데이터베이스에 값을 추가
        if suspicious_extensions:
            extensions_str = ','.join(suspicious_extensions)
            data = (extensions_str, file_path)
            SQLite3.execute_commit_query(update_query, db_path, data)