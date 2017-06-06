#!/usr/bin/python3
#coding:utf-8

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPainter
from PyQt5 import QtWidgets
import sys
import page
import string
import rx


#专业 学院 邮箱 获奖

class MainWindow(QtWidgets.QWidget):

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.resize(600, 500)

		self.pageCount = 0
		self.keyWord=""
		self.name=""
		self.school=""

		topLabel = QLabel("同学搜寻与邀请系统")
		topLabel.setParent(self)
		topLabel.move(250, 20)

		self.keywordLabel = QLabel("检索关键字")
		self.keywordLabel.setParent(self)
		self.keywordLabel.move(130, 65)

		self.keywordLineEdit = QLineEdit("")
		self.keywordLineEdit.setParent(self)
		self.keywordLineEdit.move(200, 60)

		self.pageCountLabel = QLabel("  网页数")
		self.pageCountLabel.setParent(self)
		self.pageCountLabel.move(130, 105)

		self.pageCountLineEdit = QLineEdit("")
		self.pageCountLineEdit.setParent(self)
		self.pageCountLineEdit.move(200, 100)

		confirmButton = QPushButton("确认")
		confirmButton.setParent(self)
		confirmButton.move(160, 170)

		clearButton = QPushButton("清除")
		clearButton.setParent(self)
		clearButton.move(280, 170)

		topLabel = QLabel("结果显示")
		topLabel.setParent(self)
		topLabel.move(250, 230)


		academyLabel = QLabel("   学院")
		academyLabel.setParent(self)
		academyLabel.move(130, 260)

		self.academyResultLabel = QLabel("")
		self.academyResultLabel.setParent(self)
		self.academyResultLabel.resize(200, 20)
		self.academyResultLabel.move(200, 255)


		phoneLabel = QLabel("   手机")
		phoneLabel.setParent(self)
		phoneLabel.move(130, 310)

		self.phoneResultLabel = QLabel("")
		self.phoneResultLabel.setParent(self)
		self.phoneResultLabel.resize(400, 20)
		self.phoneResultLabel.move(200, 310)


		emailLabel = QLabel("   邮箱")
		emailLabel.setParent(self)
		emailLabel.move(130, 360)

		self.emailResultLabel = QLabel("")
		self.emailResultLabel.setParent(self)
		self.emailResultLabel.resize(400, 20)
		self.emailResultLabel.move(200, 360)


		genderLabel = QLabel("   性别")
		genderLabel.setParent(self)
		genderLabel.move(130, 410)

		self.genderResultLabel = QLabel("")
		self.genderResultLabel.setParent(self)
		self.genderResultLabel.resize(200, 20)
		self.genderResultLabel.move(200, 410)

		confirmButton.clicked.connect(self.confirmHandler)
		clearButton.clicked.connect(self.clearHandler)

	def init(self):
		self.pageCount = 0
		self.keyWord=""
		self.name=""
		self.school=""

	def confirmHandler(self):
		self.init()

		keyword = self.keywordLineEdit.text()
		print ("***************关键字 = ",keyword)
		if keyword == "":
			QMessageBox.critical(self,"Critical", self.tr("请输入关键字!"))  
			return
		self.keyWord = keyword
		pageCounts = self.pageCountLineEdit.text()
		if pageCounts == "":
			QMessageBox.critical(self,"Critical", self.tr("请输入网页数!"))  
			return
		if pageCounts.isdigit() == False:
			QMessageBox.critical(self,"Critical", self.tr("网页数为数字!"))  
			return
		self.pageCount = int(pageCounts)
		print ("***************网页数 = ",pageCounts)
		schoolEnd = False
		school = ""
		name = ""
		for i in keyword:
			if not i.isspace():
				if schoolEnd == False:
					self.school += i
				else:
					self.name += i
			else:
				schoolEnd = True
		
		allPagesLinks = []
		inputCountPagesLink = []
		firstPageUrl = 'http://www.baidu.com/s?wd=%s&rsv_bp=0&rsv_spt=3&rsv_n=2&inputT=6391'%keyword
		firstPageContent = page.getFirstPageContent(firstPageUrl)  #获取第一页内容，这一页包含了关键信息。
		tmp = page.getInputCountPagesLink(firstPageContent, self.pageCount)
		#将获取到的每个页面的连接中的https改成http否则无法访问
		for link in tmp:
			inputCountPagesLink.append(link.replace("https://", "http://"))
		

		#第一页Url插入头部
		inputCountPagesLink.insert(0, firstPageUrl)

		#allPagesLinks包含了所有要分析的链接
		allPagesLinks = page.getAllLinks(inputCountPagesLink)
		#分析所有链接：返回值为一个map,键值有major(专业)，email(邮箱)，institute(学院)，(gender)性别
		map_result = page.processAllLinks(allPagesLinks, self)
		if len(map_result) == 0:
			self.phoneResultLabel.setText("未知")
			self.emailResultLabel.setText("未知")
			self.genderResultLabel.setText("未知")
			self.academyResultLabel.setText("未知")
		#print (map_result)
		else:
			string = ""
			for elem in map_result["phone"]:
				string += elem + "  "
			self.phoneResultLabel.setText(string)
			string = ""
			for elem in map_result["email"]:
				string += elem + "  "
			self.emailResultLabel.setText(string)
			self.genderResultLabel.setText(map_result["gender"])
			self.academyResultLabel.setText(map_result["institute"])

	def clearHandler(self):
		self.keywordLineEdit.clear()
		self.pageCountLineEdit.clear()
		self.academyResultLabel.clear()
		self.phoneResultLabel.clear()
		self.emailResultLabel.clear()
		self.genderResultLabel.clear()


if __name__ == "__main__":

	app = QApplication(sys.argv)
	w = MainWindow()
	w.show()
	sys.exit(app.exec_())
	
	


