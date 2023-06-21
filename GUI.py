import sys


from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap, QColor, QImage
from PyQt5.QtGui import QTransform
import sql.takeout_sqlite3_make
import test
from seleniumbase import SB
import time
import os
import find
import folium
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import codecs
import mapMake
from PyQt5.QtWidgets import QPushButton
import hashlib
from PIL import Image

global path, name, size, extenstion, lon, lat, m, se
#첫 번째 창
class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.loginbutton.clicked.connect(self.loginFunction)
        self.PW.setEchoMode(QtWidgets.QLineEdit.Password)

    def loginFunction(self):
        global path, name, size, extenstion, lon, lat, m, se
        collectviewWindow = CollectView()
        widget.addWidget(collectviewWindow)
        widget.setWindowTitle("Capstone Design Ⅱ_Collect View")  # 프로그램 이름
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedWidth(480)
        widget.setFixedHeight(420)


        '''with SB(uc=True) as sb:
            sb.open(
                "https://takeout.google.com/settings/takeout/custom/photos?utm_medium=organic-nav&utm_source=google-photos&hl=ko")
            sb.type("//input[@name='identifier']", self.ID.text())
            sb.click("//div[@id='identifierNext']")
            sb.sleep(2)  #
            sb.type('input[type="password"]', self.PW.text())
            sb.click('button:contains("다음")')
            sb.sleep(1)
            sb.click('button:contains("다음 단계")')
            sb.sleep(1)
            sb.click('//div[@class="MocG8c YECFcc LMgvRb KKjvXb"]')
            sb.sleep(1)
            sb.click(
                '// *[ @ id = "i10"] / div / div[1] / div / div[2] / div[1] / div / div[2] / div[2]')
            sb.sleep(1)
            sb.click('button:contains("내보내기 생성")')
            while (True):
                print(sb.is_element_visible(
                    '//*[@id="yDmH0d"]/c-wiz/c-wiz/div/div[2]/div[2]/c-wiz/div/div[4]/div[1]/div/div[2]/div[2]/div/div/div/button/div[1]'))
                if (sb.is_element_visible(
                        '//*[@id="yDmH0d"]/c-wiz/c-wiz/div/div[2]/div[2]/c-wiz/div/div[4]/div[1]/div/div[2]/div[2]/div/div/div/button/div[1]') == False):
                    break

            sb.click(
                '//*[@id="yDmH0d"]/c-wiz/c-wiz/div/div[2]/div[2]/c-wiz/div/div[4]/div/table/tbody[1]/tr[1]/td[6]/div/div/a')
            sb.sleep(3)
            sb.click(
                'body > div.ndfHFb-c4YZDc.ndfHFb-c4YZDc-AHmuwe-Hr88gd-OWB6Me.dif24c.vhoiae.LgGVmb.bvmRsc.ndfHFb-c4YZDc-vyDMJf-aZ2wEe.ndfHFb-c4YZDc-i5oIFb.ndfHFb-c4YZDc-uoC0bf.ndfHFb-c4YZDc-TSZdd > div.ndfHFb-c4YZDc-Wrql6b > div > div.ndfHFb-c4YZDc-Wrql6b-AeOLfc-b0t70b.ndfHFb-c4YZDc-Wrql6b-AeOLfc-b0t70b-SfQLQb-Woal0c-jcJzye-n1UuX > div.ndfHFb-c4YZDc-Wrql6b-LQLjdd > div.ndfHFb-c4YZDc-Wrql6b-C7uZwb-b0t70b > div:nth-child(3)')

            time.sleep(3)
            try:
                sb.click('#uc-download-link')
            except:
                pass
            else:
                pass
            finally:
                pass

            fileEx = r'.zip'
            bool = True

            while (bool):
                filepath = (os.listdir('./downloaded_files'))

                for file in filepath:
                    if file.endswith(fileEx):
                        bool = False
                        break'''

        check = find.findFile()
        path, name, size, extenstion, lon, lat, se = sql.takeout_sqlite3_make.db_process(check)

        mapCombined = list(zip(name, lon, lat, path))
        m = mapMake.mapMake(mapCombined)



class CollectView(QDialog):
    def __init__(self):
        super(CollectView,self).__init__()
        loadUi("collectview.ui",self)
        self.mapbutton.clicked.connect(self.mapfunction)
        self.imagebutton.clicked.connect(self.imageFunction)

    #Mapview로 이동
    def mapfunction(self):
        mapviewWindow = MapView()
        widget.addWidget(mapviewWindow)
        widget.setWindowTitle("Capstone Design Ⅱ_MAP View")
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedWidth(1500)
        widget.setFixedHeight(1000)


    #functions 기능 코드 넣기
    def imageFunction(self):
        imageWindow = ImageView()
        widget.addWidget(imageWindow)
        widget.setWindowTitle("Capstone Design Ⅱ_Image View")
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedWidth(1500)
        widget.setFixedHeight(1000)


class MapView(QWidget):
    def __init__(self):
        super(MapView,self).__init__()
        global m
        # Create a folium map
        # m = folium.Map(location=[latitude, longitude], zoom_start=zoom, tiles='OpenStreetMap')

        # Convert the map to HTML string
        map_html = m._repr_html_()

        # Create a QWebEngineView widget
        self.browser = QWebEngineView()
        self.browser.setHtml(map_html)

        # Set the layout of the widget
        layout = QVBoxLayout(self)
        layout.addWidget(self.browser)

        # Set the fixed size of the widget
        self.setFixedWidth(1500)
        self.setFixedHeight(1000)

        # Add back button to the layout
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.backFunction)
        layout.addWidget(back_button)

        # Load the HTML file and show the widget
        with codecs.open('map.html', 'r', 'utf-8') as f:
            html = f.read()

        self.browser.setHtml(html)
        self.browser.show()

        # Go back to CollectView

    def backFunction(self):
        collectviewWindow = CollectView()
        widget.addWidget(collectviewWindow)
        widget.setWindowTitle("Capstone Design Ⅱ_Collect View")
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedWidth(480)
        widget.setFixedHeight(420)


class ImageView(QDialog):
    def __init__(self,startnum = 0):
        super(ImageView,self).__init__()
        loadUi("imageview.ui",self)
        self.backbutton.clicked.connect(self.backFunction)
        self.imageButton1.clicked.connect(self.clickImage1)
        self.imageButton2.clicked.connect(self.clickImage2)
        self.imageButton3.clicked.connect(self.clickImage3)
        self.imageButton4.clicked.connect(self.clickImage4)
        self.nextButton.clicked.connect(self.nextImage)
        self.beforeButton.clicked.connect(self.beforeImage)

        self.pic, self.mPage = test.imageProcess(path)
        if startnum == 0:
            self.num = 0
            self.beforeButton.setEnabled(False)
        else:
            self.num = startnum
            self.beforeButton.setEnabled(True)

        if startnum == 0:
            self.pCount = 1
        else:
            self.pCount = int(startnum // 4) + 1
            if self.pCount == self.mPage:
                self.nextButton.setEnabled(False)

        self.b1List = []
        self.b2List = []
        self.b3List = []
        self.b4List = []
        self.pList = []

        pixmap = QPixmap(self.pic[self.num])
        pixmap = pixmap.scaled(self.imageButton1.size())
        self.imageButton1.setIcon(QIcon(pixmap))
        self.imageButton1.setIconSize(pixmap.size())
        if self.pic[self.num] == 'null.jpg':
            self.imageButton1.setEnabled(False)
        self.b1List.append(self.num)

        self.num += 1
        pixmap = QPixmap(self.pic[self.num])
        pixmap = pixmap.scaled(self.imageButton2.size())
        self.imageButton2.setIcon(QIcon(pixmap))
        self.imageButton2.setIconSize(pixmap.size())
        if self.pic[self.num] == 'null.jpg':
            self.imageButton2.setEnabled(False)
        self.b2List.append(self.num)

        self.num += 1
        pixmap = QPixmap(self.pic[self.num])
        pixmap = pixmap.scaled(self.imageButton3.size())
        self.imageButton3.setIcon(QIcon(pixmap))
        self.imageButton3.setIconSize(pixmap.size())
        if self.pic[self.num] == 'null.jpg':
            self.imageButton3.setEnabled(False)
        self.b3List.append(self.num)

        self.num += 1
        pixmap = QPixmap(self.pic[self.num])
        pixmap = pixmap.scaled(self.imageButton4.size())
        self.imageButton4.setIcon(QIcon(pixmap))
        self.imageButton4.setIconSize(pixmap.size())
        if self.pic[self.num] == 'null.jpg':
            self.imageButton4.setEnabled(False)
        self.b4List.append(self.num)

    def backFunction(self):
        collectviewWindow = CollectView()
        widget.addWidget(collectviewWindow)
        widget.setWindowTitle("Capstone Design Ⅱ_Collect View")
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedWidth(480)
        widget.setFixedHeight(420)

    def clickImage1(self): # 이 코드는 이미지를 눌렀을 때 버튼이 작동하는 코드 입니다.
        informationviewWindow = InformationView(self.b1List[-1], self.num - 3)
        widget.addWidget(informationviewWindow)
        widget.setWindowTitle("Capstone Design Ⅱ_Information View")
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedWidth(1500)
        widget.setFixedHeight(1000)

    def clickImage2(self): # 이 코드는 이미지를 눌렀을 때 버튼이 작동하는 코드 입니다.
        informationviewWindow = InformationView(self.b2List[-1], self.num - 3)
        widget.addWidget(informationviewWindow)
        widget.setWindowTitle("Capstone Design Ⅱ_Information View")
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedWidth(1500)
        widget.setFixedHeight(1000)

    def clickImage3(self): # 이 코드는 이미지를 눌렀을 때 버튼이 작동하는 코드 입니다.
        informationviewWindow = InformationView(self.b3List[-1], self.num - 3)
        widget.addWidget(informationviewWindow)
        widget.setWindowTitle("Capstone Design Ⅱ_Information View")
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedWidth(1500)
        widget.setFixedHeight(1000)

    def clickImage4(self): # 이 코드는 이미지를 눌렀을 때 버튼이 작동하는 코드 입니다.
        informationviewWindow = InformationView(self.b4List[-1], self.num - 3)
        widget.addWidget(informationviewWindow)
        widget.setWindowTitle("Capstone Design Ⅱ_Information View")
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedWidth(1500)
        widget.setFixedHeight(1000)


    def nextImage(self):
        self.pCount += 1
        self.pList.append(self.pCount)
        if self.pCount == self.mPage:
            self.nextButton.setEnabled(False)

        self.beforeButton.setEnabled(True)
        self.num += 1
        pixmap = QPixmap(self.pic[self.num])
        pixmap = pixmap.scaled(self.imageButton1.size())
        self.imageButton1.setIcon(QIcon(pixmap))
        self.imageButton1.setIconSize(pixmap.size())
        if self.pic[self.num] == 'null.jpg':
            self.imageButton1.setEnabled(False)
        self.b1List.append(self.num)

        self.num += 1
        pixmap = QPixmap(self.pic[self.num])
        pixmap = pixmap.scaled(self.imageButton2.size())
        self.imageButton2.setIcon(QIcon(pixmap))
        self.imageButton2.setIconSize(pixmap.size())
        if self.pic[self.num] == 'null.jpg':
            self.imageButton2.setEnabled(False)
        self.b2List.append(self.num)

        self.num += 1
        pixmap = QPixmap(self.pic[self.num])
        pixmap = pixmap.scaled(self.imageButton3.size())
        self.imageButton3.setIcon(QIcon(pixmap))
        self.imageButton3.setIconSize(pixmap.size())
        if self.pic[self.num] == 'null.jpg':
            self.imageButton3.setEnabled(False)
        self.b3List.append(self.num)

        self.num += 1
        pixmap = QPixmap(self.pic[self.num])
        pixmap = pixmap.scaled(self.imageButton4.size())
        self.imageButton4.setIcon(QIcon(pixmap))
        self.imageButton4.setIconSize(pixmap.size())
        if self.pic[self.num] == 'null.jpg':
            self.imageButton4.setEnabled(False)
        self.b4List.append(self.num)


    def beforeImage(self):
        self.pCount -= 1
        self.imageButton1.setEnabled(True)
        self.imageButton2.setEnabled(True)
        self.imageButton3.setEnabled(True)
        self.imageButton4.setEnabled(True)
        self.pList.append(self.pCount)
        self.nextButton.setEnabled(True)
        if self.pCount == 1:
            self.beforeButton.setEnabled(False)
        self.num -= 7
        pixmap = QPixmap(self.pic[self.num])
        pixmap = pixmap.scaled(self.imageButton1.size())
        self.imageButton1.setIcon(QIcon(pixmap))
        self.imageButton1.setIconSize(pixmap.size())
        self.b1List.append(self.num)

        self.num += 1
        pixmap = QPixmap(self.pic[self.num])
        pixmap = pixmap.scaled(self.imageButton2.size())
        self.imageButton2.setIcon(QIcon(pixmap))
        self.imageButton2.setIconSize(pixmap.size())
        self.b2List.append(self.num)

        self.num += 1
        pixmap = QPixmap(self.pic[self.num])
        pixmap = pixmap.scaled(self.imageButton3.size())
        self.imageButton3.setIcon(QIcon(pixmap))
        self.imageButton3.setIconSize(pixmap.size())
        self.b3List.append(self.num)

        self.num += 1
        pixmap = QPixmap(self.pic[self.num])
        pixmap = pixmap.scaled(self.imageButton4.size())
        self.imageButton4.setIcon(QIcon(pixmap))
        self.imageButton4.setIconSize(pixmap.size())
        self.b4List.append(self.num)


class InformationView(QDialog):
    def __init__(self, number, n):
        super(InformationView,self).__init__()
        loadUi("informationview.ui",self)
        global name, size, extenstion, path
        self.backbutton.clicked.connect(self.backFunction)
        self.analysisbutton.clicked.connect(self.analysis)
        self.number = number
        self.n = n
        self.picc, self.mPagee = test.imageProcess(path)
        pixmap = QPixmap(self.picc[self.number])
        pixmap = pixmap.scaled(self.showimageButton.size())
        self.showimageButton.setIcon(QIcon(pixmap))
        self.showimageButton.setIconSize(pixmap.size())
        self.imagename.setText(str(name[self.number]))
        self.imagesize.setText(str(size[self.number])+" bytes")
        self.imageextension.setText(str(extenstion[self.number]))

        # MD5 해시 생성
        md5_hash = self.generate_hash(str(path[self.number]), 'md5')
        # SHA-1 해시 생성
        sha1_hash = self.generate_hash(str(path[self.number]), 'sha1')

        self.md5.setText(str(md5_hash))
        self.sha1.setText(str(sha1_hash))

    def backFunction(self):
        imageviewWindow = ImageView(self.n)
        widget.addWidget(imageviewWindow)
        widget.setWindowTitle("Capstone Design Ⅱ_Image View")
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedWidth(1500)
        widget.setFixedHeight(1000)
    def analysis(self):
        analysisviewWindow = AnalysisView(self.number,self.n)
        widget.addWidget(analysisviewWindow)
        widget.setWindowTitle("Capstone Design Ⅱ_Analysis View")
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedWidth(1500)
        widget.setFixedHeight(1000)

    def generate_hash(self,file_path, algorithm):
        try:
            with open(file_path, 'rb') as file:
                contents = file.read()
                hash_object = hashlib.new(algorithm)
                hash_object.update(contents)
                return hash_object.hexdigest()
        except IOError:
            print("파일을 읽는 중 오류가 발생했습니다.")
class AnalysisView(QDialog):
    def __init__(self, number,n):
        super(AnalysisView,self).__init__()
        loadUi("analysis.ui",self)
        global name, size, extenstion, se
        self.number = number
        self.n = n
        self.bit_number = 0
        # 추출한 픽셀을 저장할 리스트를 초기화합니다.
        self.extracted_pixels = []
        self.picc, self.mPagee = test.imageProcess(path)
        pixmap = QPixmap(self.picc[self.number])
        pixmap = pixmap.scaled(self.imagelabel.size())
        self.imagelabel.setPixmap(pixmap)
        self.spinbutton.clicked.connect(self.spinFunction)
        self.backbutton.clicked.connect(self.backFunction)
        self.selabel.setText(str(se[self.number]))
        self.pushButton.clicked.connect(self.chageFunction)
        self.nButton.clicked.connect(self.extract_secret_image_next)
        self.pButton.clicked.connect(self.extract_secret_image_prev)
        self.label_2.setText(str(f"원본 이미지"))
        self.pButton.setEnabled(False)
        # 현재 이미지를 가져옴
        pixmap = self.imagelabel.pixmap()
        image = pixmap.toImage()

        # 첫 번째 픽셀의 RGB 값을 가져옴
        color = image.pixel(0, 0)
        r, g, b, _ = QColor(color).getRgb()

        # RGB 값을 텍스트 상자에 설정
        self.rlineEdit.setText(str(r))
        self.glineEdit.setText(str(g))
        self.blineEdit.setText(str(b))
    def spinFunction(self):
        pixmap = self.imagelabel.pixmap()

        # 이미지를 회전시킴
        transform = QTransform().rotate(90)
        rotated_pixmap = pixmap.transformed(transform)

        # 회전된 QPixmap을 Label에 맞게 조정
        rotated_pixmap = rotated_pixmap.scaled(self.imagelabel.size())

        # 회전된 QPixmap을 Label에 설정
        self.imagelabel.setPixmap(rotated_pixmap)

    def backFunction(self):
        informationviewWindow = InformationView(self.number,self.n)

        directory = './tmp'  # 삭제할 파일들이 있는 디렉토리 경로

        # 디렉토리 내의 모든 파일과 디렉토리 목록을 가져옵니다.
        file_list = os.listdir(directory)

        # 파일 목록을 순회하면서 확장자가 '.jpg'인 파일을 삭제합니다.
        for file_name in file_list:
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path) and file_name.endswith('.jpg'):
                os.remove(file_path)
            elif os.path.isfile(file_path) and file_name.endswith('.png'):
                os.remove(file_path)

        widget.addWidget(informationviewWindow)
        widget.setWindowTitle("Capstone Design Ⅱ_Information View")
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedWidth(1500)
        widget.setFixedHeight(1000)

    def chageFunction(self):
        # 현재 이미지를 가져옴
        pixmap = self.imagelabel.pixmap()
        image = pixmap.toImage()

        # RGB 값을 가져옴
        r = int(self.rlineEdit.text())
        g = int(self.glineEdit.text())
        b = int(self.blineEdit.text())

        # 이미지 색상 변경
        for i in range(image.width()):
            for j in range(image.height()):
                color = image.pixel(i, j)
                current_r, current_g, current_b, _ = QColor(color).getRgb()
                new_r = min(r, current_r)
                new_g = min(g, current_g)
                new_b = min(b, current_b)
                new_color = QColor(new_r, new_g, new_b)
                image.setPixelColor(i, j, new_color)

        # 변경된 이미지를 QPixmap으로 변환
        new_pixmap = QPixmap.fromImage(image)

        # 변경된 QPixmap을 Label에 맞게 조정
        new_pixmap = new_pixmap.scaled(self.imagelabel.size())

        # 변경된 QPixmap을 Label에 설정
        self.imagelabel.setPixmap(new_pixmap)


    def extract_secret_image_next(self):
        self.bit_number += 1

        if self.bit_number > 7:
            self.nButton.setEnabled(False)
        else:
            self.pButton.setEnabled(True)


        image = Image.open(self.picc[self.number])


        if image.mode != "RGB":
            image = image.convert("RGB")

        # 이미지의 크기를 가져옵니다.
        width, height = image.size

        # 이미지의 픽셀을 가져옵니다.
        pixels = list(image.getdata())
        # 픽셀에서 비트를 추출하여 시크릿 픽셀을 생성합니다.
        self.extracted_pixels = []  # 추출한 픽셀을 저장할 리스트를 초기화합니다.

        # 픽셀에서 비트를 추출하여 시크릿 픽셀을 생성합니다.
        for pixel in pixels:
            r, g, b = pixel

            # R, G, B 각각의 채널에서 비트를 추출하고 시크릿 픽셀을 생성합니다.
            r_bit_value = (r >> (8 - self.bit_number)) & 1
            g_bit_value = (g >> (8 - self.bit_number)) & 1
            b_bit_value = (b >> (8 - self.bit_number)) & 1

            # 추출한 비트를 이용하여 시크릿 픽셀을 생성합니다.
            secret_pixel = (r_bit_value * 255, g_bit_value * 255, b_bit_value * 255)

            # 추출한 시크릿 픽셀을 리스트에 추가합니다.
            self.extracted_pixels.append(secret_pixel)

        # 시크릿 이미지를 생성하고 저장합니다.
        secret_image = Image.new("RGB", (width, height))
        secret_image.putdata(self.extracted_pixels)
        secret_image.save(f"./tmp/secret_image_bit_{self.bit_number}.png")

        # 변경된 이미지를 QPixmap으로 변환
        new_pixmap = QPixmap.fromImage(QImage(f"./tmp/secret_image_bit_{self.bit_number}.png"))

        # 변경된 QPixmap을 Label에 맞게 조정
        new_pixmap = new_pixmap.scaled(self.imagelabel.size())

        # 변경된 QPixmap을 Label에 설정
        self.imagelabel.setPixmap(new_pixmap)
        self.label_2.setText(str(f"LSB 기법을 통한 {self.bit_number}비트 변환 이미지."))

    def extract_secret_image_prev(self):
        if self.bit_number == 1:
            self.pButton.setEnabled(False)
            self.bit_number -= 1
            # 변경된 이미지를 QPixmap으로 변환
            new_pixmap = QPixmap.fromImage(QImage(str(self.picc[self.number])))

            # 변경된 QPixmap을 Label에 맞게 조정
            new_pixmap = new_pixmap.scaled(self.imagelabel.size())

            # 변경된 QPixmap을 Label에 설정
            self.imagelabel.setPixmap(new_pixmap)
            self.label_2.setText(str(f"원본 이미지"))
        else:
            self.nButton.setEnabled(True)
            self.bit_number -= 1
            # 변경된 이미지를 QPixmap으로 변환
            new_pixmap = QPixmap.fromImage(QImage(f"./tmp/secret_image_bit_{self.bit_number}.png"))

            # 변경된 QPixmap을 Label에 맞게 조정
            new_pixmap = new_pixmap.scaled(self.imagelabel.size())

            # 변경된 QPixmap을 Label에 설정
            self.imagelabel.setPixmap(new_pixmap)
            self.label_2.setText(str(f"LSB 기법을 통한 {self.bit_number}비트 변환 이미지."))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Login()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainWindow)
    widget.setWindowTitle("Capstone Design Ⅱ")
    widget.setFixedWidth(480)
    widget.setFixedHeight(420)
    widget.show()
    app.exec_()