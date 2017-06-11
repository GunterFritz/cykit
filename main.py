import sys
from gui.draw import MyView
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
	app = QApplication(sys.argv)
	view = MyView()
	view.show()
	sys.exit(app.exec_())


