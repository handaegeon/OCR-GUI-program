# OCR 동작 부분

from ocr_main_window import *
from ocr_cam_window import *
import pytesseract
import cv2
from PyQt5.QtGui import QPixmap
from show_video import *

#===========================================
# Main Window 에서 실행할 함수 리스트
#===========================================

# Cam Window 실행
def openWindow(self):
    self.window=QtWidgets.QMainWindow()
    self.ui=Ui_CamWindow()
    self.ui.setupUi(self.window)
    self.ui.setConfig(self.langSel.currentText(), self.engSel.currentText())
    self.ui.captureSig()
    self.window.show()

# OpenCV 실행
def showVideo(self):
    thread = QtCore.QThread()
    thread.start()
    vid = ShowVideo()
    vid.moveToThread(thread)

# camera 버튼 시그널
def cameraSig(self):
    self.camBtn.clicked.connect(self.openWindow)
    self.camBtn.clicked.connect(self.showVideo)

#===========================================
# Cam Window에서 실행할 함수 리스트
#===========================================

# 찍기만 함
def capture(self):
    self.imPath = "ocr1.png"

    self.ret, self.image = self.cam.read()
    if self.image is None:
        print ('image is not exist')
        return None
    
    # png로 압축 없이 영상 저장 
    cv2.imwrite(self.imPath, self.imgae, params=[cv2.IMWRITE_PNG_COMPRESSION,0])
    self.cam.release()

# 현재 Cam Label에서 보여주는 이미지 read 후 tesseract 를 사용해서 텍스트로 변환
def readImage(self):
    self.capture()
    self.im = cv2.imread(self.imPath, cv2.IMREAD_COLOR)
    self.config = ('-l %s --oem 1 --psm 3' % self.lang)
    self.text = pytesseract.image_to_string(self.im, config=self.config)
    self.camLabel.setText(self.text)

# capture 버튼 시그널
def captureSig(self):
    self.capBtn.clicked.connect(self.readImage)

# tesseract를 이용할 때 필요한 설정을 세팅하는 함수
# lang: 인식할 언어
# engn: 설정할 엔진
def setConfig(self, lang, engn):
    self.lang = lang
    self.engn = engn

# =====================================
# 적용
#======================================

# 클래스에 함수 추가
Ui_MainWindow.cameraSig = cameraSig
Ui_MainWindow.openWindow = openWindow
Ui_MainWindow.showVideo = showVideo

Ui_CamWindow.captureSig = captureSig
Ui_CamWindow.capture = capture
Ui_CamWindow.readImage = readImage
Ui_CamWindow.setConfig = setConfig

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.cameraSig()
    MainWindow.show()
    sys.exit(app.exec_())
