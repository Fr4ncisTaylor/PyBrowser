import os
import sys
import config

from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport     import * 
from PyQt5.QtWebEngineWidgets import *

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class MyWindowINIT(QMainWindow): 
	def __init__(self, *args, **kwargs):
		super(MyWindowINIT, self).__init__(*args, **kwargs)

		self.navegador = QWebEngineView()

		self.setWindowIcon(QIcon(os.path.join(basedir, "icons", "python.png")))
		self.navegador.setUrl(QUrl(config.home_url))
		self.navegador.urlChanged.connect(self.update_urlbar)
		self.navegador.loadFinished.connect(self.set_title)
		
		self.resize(config.init_X, config.init_Y)
		
		self.setCentralWidget(self.navegador)
		self.setStatusBar(QStatusBar())
		
		navtb = QToolBar("Navegação")
		navtb.setStyleSheet(open(config.style_arqv).read())

		self.addToolBar(navtb)
		
		# Back Btn
		back_btn = QAction("Retornar", self)
		back_btn.setIcon(QIcon(os.path.join(basedir, "icons", "retornar.png")))
		back_btn.triggered.connect(self.navegador.back)
		navtb.addAction(back_btn)

		# Next btn
		next_btn = QAction("Avançar", self)
		next_btn.setIcon(QIcon(os.path.join(basedir, "icons", "avancar.png")))
		next_btn.triggered.connect(self.navegador.forward)
		navtb.addAction(next_btn)
		
		# refresh
		refresh_btn = QAction("Atualizar página", self)
		refresh_btn.setIcon(QIcon(os.path.join(basedir, "icons", "refresh.png")))
		refresh_btn.triggered.connect(self.navegador.reload)
		navtb.addAction(refresh_btn)

		# home
		home_btn = QAction("Página Inicial", self)
		home_btn.setIcon(QIcon(os.path.join(basedir, "icons", "home.png")))
		home_btn.triggered.connect(self.home)
		navtb.addAction(home_btn)
		navtb.addSeparator()

		# My Git

		git_btn = QAction("Meu GitHub", self)
		#git_btn.setStatusTip("Go to Git")
		git_btn.setIcon(QIcon(os.path.join(basedir, "icons", "git.png")))
		git_btn.triggered.connect(self.git)
		navtb.addAction(git_btn)
		navtb.addSeparator()

		# UrlBar
		self.urlbar = QLineEdit()
		self.urlbar.returnPressed.connect(self.go_to_url)
		self.urlbar.setFixedHeight(config.url_bar_size)
		navtb.addWidget(self.urlbar)
		
		# stop
		stop_btn = QAction("Parar", self)
		stop_btn.setIcon(QIcon(os.path.join(basedir, "icons", "stop.png")))
		stop_btn.setStatusTip("Stop loading current page")
		stop_btn.triggered.connect(self.navegador.stop)
		navtb.addAction(stop_btn)
		self.show()

		# Set home_url in UrlBar
		self.update_urlbar(QUrl(config.home_url))

	# set window title
	def set_title(self): 
		title = self.navegador.page().title()
		self.setWindowTitle("% s " % title)

	# go to url home
	def home(self): 
		self.navegador.setUrl(QUrl(config.home_url))

	# go to my GitHub Url
	def git(self): 
		self.navegador.setUrl(QUrl(config.git_url))

	# go to url 
	def go_to_url(self): 
		qurl = QUrl(self.urlbar.text())
		if qurl.scheme() == "": qurl.setScheme("http")
		self.navegador.setUrl(qurl)

	# update urlbar text
	def update_urlbar(self, qurl): 
		self.urlbar.setText(qurl.toString())
		self.urlbar.setCursorPosition(0)


app = QApplication(sys.argv)
app.setApplicationName("My Simple Browser")
app.setWindowIcon(QIcon(os.path.join(basedir, "icons", "icon.ico")))

window = MyWindowINIT()
app.exec_()