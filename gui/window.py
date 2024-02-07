import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow
from PyQt5.QtCore import pyqtSlot

class App(QMainWindow):

	def __init__(self):
		super().__init__()
		self.title = 'PyQt5 status bar example - pythonspot.com'
		self.left = 350
		self.top = 200
		self.width = 640
		self.height = 480
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.statusBar().showMessage('Message in statusbar.')

		button = QPushButton('PyQt5 button', self)
		button.setToolTip('This is an example button')
		button.move(300,270)
		button.clicked.connect(self.on_click)
		# self.show()

	@pyqtSlot()
	def on_click(self):
		print('PyQt5 button click')


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	ex.show()
	sys.exit(app.exec_())
