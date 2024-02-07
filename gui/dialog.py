import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout


class Dialog(QDialog):

	def __init__(self):
		super(Dialog, self).__init__()

		button = QPushButton("Click me!")
		button.clicked.connect(self.slot_method)

		self.left = 640
		self.top = 280
		self.width = 300
		self.height = 200

		main_layout = QVBoxLayout()
		main_layout.addWidget(button)

		self.setGeometry(self.left, self.top, self.width, self.height)
		self.setWindowTitle("Button Example - pythonspot.com")
		self.setLayout(main_layout)
		# self.show()

	@pyqtSlot()
	def slot_method(self):
		print('slot method called.')


if __name__ == '__main__':
	app = QApplication(sys.argv)
	dialog = Dialog()
	dialog.show()
	sys.exit(app.exec_())
