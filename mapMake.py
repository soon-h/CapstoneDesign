import folium
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import codecs
from folium import IFrame
from folium.features import DivIcon
import base64
import os
from PIL import Image

current_dir = os.path.dirname(os.path.abspath(__file__))

def resize_image(image_path, output_path, max_size):
    img = Image.open(image_path)
    img.thumbnail((max_size, max_size), Image.ANTIALIAS)
    img.save(output_path)

def mapMake(mapCombined):
    indices_to_delete = [i for i, (_, lon, lat,_) in enumerate(mapCombined) if lon == '0.0' or lat == '0.0']
    for index in sorted(indices_to_delete, reverse=True):
        del mapCombined[index]

    print(mapCombined)
    name, lon, lat, path = zip(*mapCombined)

    center_lat = sum(map(float, lat)) / len(lat)
    center_lon = sum(map(float, lon)) / len(lon)

    # OpenStreetMap 기반의 지도 생성
    m = folium.Map(location=[center_lat, center_lon], zoom_start=10, tiles='OpenStreetMap')

    for i in range(len(name)):
        # Check if the image path exists
        if path[i] != '':
            # Resize the image
            max_image_size = 200
            resized_image_path = os.path.join(current_dir, f'./tmp/resized_image_{i}.jpg')
            resize_image(path[i], resized_image_path, max_image_size)

            new_image_dir = os.path.join(current_dir, 'resized_images')
            os.makedirs(new_image_dir, exist_ok=True)
            new_image_path = os.path.join(new_image_dir, f'resized_image_{i}_{os.path.basename(path[i])}')

            # Check if the image file already exists
            if not os.path.exists(new_image_path):
                os.rename(resized_image_path, new_image_path)

            # Read the resized image file
            with open(new_image_path, 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                image_tag = f'<img src="data:image/jpeg;base64,{encoded_image}">'
                popup_content = f'<center><strong>{name[i]}</strong></center><br>{image_tag}'
                iframe = folium.IFrame(popup_content, width=210, height=220)
                popup = folium.Popup(iframe, max_width=450)
                folium.Marker(location=[float(lat[i]), float(lon[i])], popup=popup, tooltip=name[i]).add_to(m)

        else:
            # If image path is empty, add a default marker
            folium.Marker(location=[float(lat[i]), float(lon[i])], popup=name[i]).add_to(m)

    # html 파일로 저장
    m.save('map.html')

    return m