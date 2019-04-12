import pytesseract
import cv2
from ShowVideo import *
from ImageViewer import *
from main_window import *
from sub_window import *

#===================================================
# MainWindow에서 실행할 함수 리스트
#===================================================

def openWindow(self):
    self.window=QtWidgets.QMainWindow()
    self.ui=Ui_SubWindow()
    self.ui.setupUi(self.window)
    self.window.show()

def addWidget(self, widget):
    self.horizontalLayout.addWidget(widget)

def onSig(self):
    self.onoffBtn.clicked.connect(vid.startVideo)

def capSig(self):
    self.capBtn.clicked.connect(vid.capPic)

def exitSig(self):
    self.exitBtn.clicked.connect(sys.exit)

#===================================================
# sShowVideo에서 실행할 함수 리스트
#===================================================

def capPic(self):
    cv2.imwrite("img1.png",self.image, params=[cv2.IMWRITE_PNG_COMPRESSION,0])
    config = ('-l eng --oem 1 --psm 3')
    text = pytesseract.image_to_string(self.image, config=config)

#===================================================
# 클래스에 함수 추가
#===================================================

Ui_MainWindow.addWidget = addWidget
Ui_MainWindow.onSig = onSig
Ui_MainWindow.capSig = capSig
Ui_MainWindow.exitSig = exitSig

ShowVideo.capPic = capPic

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # 비디오 촬영 스레드 생성
    thread = QtCore.QThread()
    thread.start()
    vid = ShowVideo()
    vid.moveToThread(thread)

    # 이미지 뷰어 위젯 객체 생성
    image_viewer1 = ImageViewer()

    # 시그널 연결
    vid.VideoSignal.connect(image_viewer1.setImage)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.addWidget(image_viewer1)
    ui.onSig()
    ui.capSig()
    ui.exitSig()
    MainWindow.show()
    sys.exit(app.exec_())
