
import sys
from datetime import datetime
from time import sleep
from threading import Thread
import pysftp
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QFormLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap
from My_PyQt import *


class RemoteLogin(QMainWindow):

    def __init__(self, parent = None):

        super().__init__(parent)

        self.lineEdit_hostname = MyQLineEdit()
        self.lineEdit_hostname.setText('192.168.1.101')

        self.lineEdit_username = MyQLineEdit()
        self.lineEdit_username.setText('user')

        self.lineEdit_projectRoot = MyQLineEdit()
        self.lineEdit_projectRoot.setText('/home/user/Workspace/project/')
        self.lineEdit_projectRoot.setFocusOutHandle(self.checkProjectRoot)

        self.pushButton_ok = QPushButton()
        self.pushButton_ok.setText('OK')
        self.pushButton_ok.clicked.connect(self.connectRemote)

        self.formLayout_mainSection = QFormLayout()
        self.formLayout_mainSection.addRow('Hostname', self.lineEdit_hostname)
        self.formLayout_mainSection.addRow('Username', self.lineEdit_username)
        self.formLayout_mainSection.addRow('Project Root', self.lineEdit_projectRoot)
        self.formLayout_mainSection.addRow(self.pushButton_ok)
        self.formLayout_mainSection.labelForField(self.lineEdit_hostname).setFont(getSmallFont())
        self.formLayout_mainSection.labelForField(self.lineEdit_username).setFont(getSmallFont())
        self.formLayout_mainSection.labelForField(self.lineEdit_projectRoot).setFont(getSmallFont())

        self.widget_mainSection = QWidget()
        self.widget_mainSection.setLayout(self.formLayout_mainSection)

        self.setCentralWidget(self.widget_mainSection)
        self.setMinimumWidth(600)
        self.setWindowTitle("Login to remote")

    
    def lockInput(self) -> None:

        self.lineEdit_hostname.setReadOnly(True)
        self.lineEdit_username.setReadOnly(True)
        self.lineEdit_projectRoot.setReadOnly(True)


    def unlockInput(self) -> None:

        self.lineEdit_hostname.setReadOnly(False)
        self.lineEdit_username.setReadOnly(False)
        self.lineEdit_projectRoot.setReadOnly(False)


    def checkProjectRoot(self) -> None:

        if not self.lineEdit_projectRoot.text().endswith('/'):
            self.lineEdit_projectRoot.setText(self.lineEdit_projectRoot.text() + '/')


    def connectRemote(self) -> None:

        self.lockInput()

        try:
            with pysftp.Connection(host = self.lineEdit_hostname.text(), username = self.lineEdit_username.text()) as sftpCon:
                try:
                    names = sftpCon.listdir(self.lineEdit_projectRoot.text() + '/output/')
                except FileNotFoundError:
                    error('Remote path "{}" NOT found.'.format(self.lineEdit_projectRoot.text() + '/output/'))
                else:
                    if len(names) == 0:
                        notify('No output directory to fetch.')

                    else:
                        names.reverse()

                        for name in names:
                            if sftpCon.isdir(self.lineEdit_projectRoot.text() + '/output/' + name):
                                self.hide()

                                sftpLoginInfo = {'hostname': self.lineEdit_hostname.text(), 'username': self.lineEdit_username.text()}
                                FollowOutput(self, sftpLoginInfo, self.lineEdit_projectRoot.text() + '/output/' + name + '/', name)

                                return

                        notify('No output directory to fetch.')

        except Exception as e:
            error('Failed to establish ssh connection in connectRemote() .')

        self.unlockInput()


class FollowOutput(QMainWindow):

    def __init__(self, parent: QMainWindow, sftpLoginInfo: dict, outputDirPath: str, outputDirName: str):

        super().__init__(parent)

        self.parent = parent
        self.sftpLoginInfo = sftpLoginInfo
        self.outputDirPath = outputDirPath
        self.outputDirName = outputDirName

        self.label_outputDirPath = QLabel()
        self.label_outputDirPath.setText('Working Directory : ' + outputDirPath)
        self.label_outputDirPath.setFont(getNormalFont())

        self.label_depthImage = QLabel()
        self.label_depthImage.setAlignment(Qt.AlignCenter)

        self.label_rgbImage = QLabel()
        self.label_rgbImage.setAlignment(Qt.AlignCenter)

        self.label_yoloImage = QLabel()
        self.label_yoloImage.setAlignment(Qt.AlignCenter)

        self.hboxLayout_imageSection = QHBoxLayout()
        self.hboxLayout_imageSection.addWidget(self.label_depthImage)
        self.hboxLayout_imageSection.addWidget(self.label_rgbImage)
        self.hboxLayout_imageSection.addWidget(self.label_yoloImage)

        self.label_depthFilename = QLabel()
        self.label_depthFilename.setText('(Empty)')
        self.label_depthFilename.setFont(getNormalFont())
        self.label_depthFilename.setAlignment(Qt.AlignCenter)

        self.label_rgbFilename = QLabel()
        self.label_rgbFilename.setText('(Empty)')
        self.label_rgbFilename.setFont(getNormalFont())
        self.label_rgbFilename.setAlignment(Qt.AlignCenter)

        self.label_yoloFilename = QLabel()
        self.label_yoloFilename.setText('(Empty)')
        self.label_yoloFilename.setFont(getNormalFont())
        self.label_yoloFilename.setAlignment(Qt.AlignCenter)

        self.hboxLayout_filenameSection = QHBoxLayout()
        self.hboxLayout_filenameSection.addWidget(self.label_depthFilename)
        self.hboxLayout_filenameSection.addWidget(self.label_rgbFilename)
        self.hboxLayout_filenameSection.addWidget(self.label_yoloFilename)

        self.label_slamImage = QLabel()
        self.label_slamImage.setAlignment(Qt.AlignCenter)

        self.hboxLayout_imageSection2 = QHBoxLayout()
        self.hboxLayout_imageSection2.addWidget(self.label_slamImage)

        self.label_slamFilename = QLabel()
        self.label_slamFilename.setText('(Empty)')
        self.label_slamFilename.setFont(getNormalFont())
        self.label_slamFilename.setAlignment(Qt.AlignCenter)

        self.hboxLayout_filenameSection2 = QHBoxLayout()
        self.hboxLayout_filenameSection2.addWidget(self.label_slamFilename)

        self.vboxLayout_mainSection = QVBoxLayout()
        self.vboxLayout_mainSection.addWidget(self.label_outputDirPath)
        self.vboxLayout_mainSection.addLayout(self.hboxLayout_imageSection)
        self.vboxLayout_mainSection.addLayout(self.hboxLayout_filenameSection)
        self.vboxLayout_mainSection.addLayout(self.hboxLayout_imageSection2)
        self.vboxLayout_mainSection.addLayout(self.hboxLayout_filenameSection2)

        self.widget_mainSection = QWidget()
        self.widget_mainSection.setLayout(self.vboxLayout_mainSection)

        self.setCentralWidget(self.widget_mainSection)
        self.setWindowTitle('Follow Output')

        self.isTerminated = False

        self.traceOutputThread = Thread(target = self.traceOutput)
        self.traceOutputThread.start()

        self.show()


    def isOutputExist(self, id: int) -> bool:

        if id >= 1:
            idStr = ('%010d') % (id)

            with pysftp.Connection(host = self.sftpLoginInfo['hostname'], username = self.sftpLoginInfo['username']) as sftpCon:
                depthExists = sftpCon.isfile(self.outputDirPath + 'depth_' + idStr + '.jpg')
                rgbExists = sftpCon.isfile(self.outputDirPath + 'color_' + idStr + '.jpg')
                yoloExists = sftpCon.isfile(self.outputDirPath + 'yolov4_' + idStr + '.jpg')

            return (depthExists and rgbExists and yoloExists)

        else:
            return False


    def getLatestOutput(self) -> int:

        with pysftp.Connection(host = self.sftpLoginInfo['hostname'], username = self.sftpLoginInfo['username']) as sftpCon:
            depthFile = sftpCon.execute("ls '{}' | grep 'depth_' | tail -n 1".format(self.outputDirPath))
            rgbFile = sftpCon.execute("ls '{}' | grep 'color_' | tail -n 1".format(self.outputDirPath))
            yoloFile = sftpCon.execute("ls '{}' | grep 'yolov4_' | tail -n 1".format(self.outputDirPath))
            slamFile = sftpCon.execute("ls '{}' | grep 'slam_' | tail -n 1".format(self.outputDirPath))
            
            if len(depthFile) > 0 and len(rgbFile) > 0 and len(yoloFile) > 0 and len(slamFile) > 0:
                depthId = int(depthFile[0].decode('utf-8').replace('depth_', '').replace('.jpg', '').replace('\n', ''))
                rgbId = int(rgbFile[0].decode('utf-8').replace('color_', '').replace('.jpg', '').replace('\n', ''))
                yoloId = int(yoloFile[0].decode('utf-8').replace('yolov4_', '').replace('.jpg', '').replace('\n', ''))
                slamId = int(slamFile[0].decode('utf-8').replace('slam_', '').replace('.jpg', '').replace('\n', ''))

                return min(depthId, rgbId, yoloId, slamId)

        return 0


    def traceOutput(self) -> None:

        while not self.isTerminated:
            with pysftp.Connection(host = self.sftpLoginInfo['hostname'], username = self.sftpLoginInfo['username']) as sftpCon:
                id = self.getLatestOutput()
                idStr = ('%010d') % (id)

                if id >= 1:
                    sftpCon.get(self.outputDirPath + 'depth_' + idStr + '.jpg', 'download/depth.jpg')
                    sftpCon.get(self.outputDirPath + 'color_' + idStr + '.jpg', 'download/rgb.jpg')
                    sftpCon.get(self.outputDirPath + 'yolov4_' + idStr + '.jpg', 'download/yolo.jpg')
                    sftpCon.get(self.outputDirPath + 'slam_' + idStr + '.jpg', 'download/slam.jpg')

                    self.label_depthImage.setPixmap(QPixmap('download/depth.jpg'))
                    self.label_rgbImage.setPixmap(QPixmap('download/rgb.jpg'))
                    self.label_yoloImage.setPixmap(QPixmap('download/yolo.jpg'))

                    slamImage = QPixmap('download/slam.jpg')

                    if slamImage.width() > 1920:
                        slamImage = slamImage.scaledToWidth(1920)

                    self.label_slamImage.setPixmap(slamImage)

                    self.label_depthFilename.setText('depth_({}).jpg'.format(idStr))
                    self.label_rgbFilename.setText('color_({}).jpg'.format(idStr))
                    self.label_yoloFilename.setText('yolov4_({}).jpg'.format(idStr))
                    self.label_slamFilename.setText('slam_({}).jpg'.format(idStr))


    def closeEvent(self, event):

        self.isTerminated = True
        self.parent.unlockInput()
        self.parent.show()


app = QApplication(sys.argv)

window = RemoteLogin()
window.show()

sys.exit(app.exec_())

