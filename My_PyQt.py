
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox, QLineEdit


def getSmallFont() -> int:

    return QFont('Arial', 16)


def getNormalFont() -> int:

    return QFont('Arial', 18)


def notify(message: str, title: str = 'Notification'):

    msgBox = QMessageBox()

    msgBox.setIcon(QMessageBox.Information)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.setWindowTitle(title)
    msgBox.setText(message)

    msgBox.exec()


def error(message: str, title: str = 'Critical Error'):

    msgBox = QMessageBox()

    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.setWindowTitle(title)
    msgBox.setText(message)

    msgBox.exec()


class MyQLineEdit(QLineEdit):

    def __init__(self):

        super().__init__()

        self.__focusOutHandle = None
        self.setFont(getNormalFont())

    def setFocusOutHandle(self, focusOutHandle):

        if callable(focusOutHandle):
            self.__focusOutHandle = focusOutHandle


    def focusOutEvent(self, e):

        super().focusOutEvent(e)

        if self.__focusOutHandle != None:
            self.__focusOutHandle()

