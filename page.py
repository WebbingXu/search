# -*- coding:utf-8 -*- ＃

import requests
from bs4 import BeautifulSoup
import re
from urllib import parse
import sys
import jieba
from PyQt5.QtWidgets import QProgressBar
from collections import Counter

targetList = ["学院", "专业", "邮箱", "性别"]
instiuteContainer = ["机械工程", "电子信息", "通信工程", 
"自动化", "计算机", "材料与环境工程", "生命信息与仪器工程",
"软件工程","理", "经济","管理","数字媒体和艺术设计","人文与法",
"卓越","网络空间安全","马克思主义","信息工程","浙江保密","外国语",
"继续教育","国际教育","电子", "通信"]


#获取一个连接内网页的内容
def getLinkContent(url):
	print ("in getLinkContent......")
	user_agent = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
	headers = {'User_Agent':user_agent}
	try:
		print ("in getLinkContent try......")
		response = requests.get(url, headers = headers, timeout = 5)
		html = response.text
		print ("in getLinkContent try exiting......")
		return html
	except:
		print ("in getLinkContent except exiting......")
		return None
	



#获取第一页内容
def getFirstPageContent(url):
	return getLinkContent(url)



def getPageUsefulLink(page):
	usefulLink = [] 
	soup_1 = BeautifulSoup(page, 'html.parser')
	allLinkWraper = soup_1.find_all(id='content_left')
	soup_2 = BeautifulSoup(str(allLinkWraper), 'html.parser')
	everyLinkWraper = soup_2.find_all(class_=re.compile('result(.*?)c-container'))
	for i in everyLinkWraper:
		soup_3 = BeautifulSoup(str(i), 'html.parser')
		usefulLink.append(soup_3.a["href"])
	return usefulLink


def getInputCountPagesLink(firstPage, count):
	nextPagesLink = []
	soup_1 = BeautifulSoup(firstPage, 'html.parser')
	nextPagesWraper = soup_1.find_all(id="page")
	soup_2 = BeautifulSoup(str(nextPagesWraper), 'html.parser')
	try:
		i = 0
		for child in soup_2.div.children:
			string = str(child)
			if "href" in string and i < count - 1:
				soup_3 = BeautifulSoup(str(string), 'html.parser')
				nextPagesLink.append("https://www.baidu.com"+soup_3.a["href"])
				i = i + 1
		return nextPagesLink
	except:
		return []

		


def getAllLinks(pagesLinkList):
	allLinklist = []
	for pageLink in pagesLinkList:
		page = getLinkContent(pageLink)
		list_ = getPageUsefulLink(page)
		for l in list_:
			allLinklist.append(l)
	return allLinklist

 
def getHtmlBody(page):
	p = re.compile("<body.*>[\s\S]*</body>", re.I)
	if page == None:
		return None
	r = p.findall(page)
	print ("in getHtmlBody", r)
	if len(r) == 1:
		return r[0]
	else:
		return None

def searchPhone(pageContent):
	pattern = re.compile("1[3578]{1}[0-9]{9}")
	body = getHtmlBody(pageContent)
	if body == None:
		return None
	phoneList = pattern.findall(body)

	if len(phoneList) >= 6:
		return None
	return phoneList

def searchEmail(pageContent):
	pattern = re.compile("[a-zA-Z0-9_.]+@[a-zA-Z0-9_]+\.[a-zA-Z0-9_\.]*")
	body = getHtmlBody(pageContent)
	if body == None:
		return None
	emailList = pattern.findall(body)
	if len (emailList) >= 5:
		return None
	else:
		return emailList

def searchInstiute(pageContent):
	pattern = re.compile("[。，；.,;]{1}[^。，；.,;]*学院")
	body = getHtmlBody(pageContent)
	instiuteResult = []
	if body != None:
		instiuteList = pattern.findall(body)
		#如果数目太多，那么说明网页相关性不大，直接去除
		if len(instiuteList) >= 5:
			return None
		for instiute in instiuteList:
			seg_list = jieba.cut(instiute, cut_all=False)
			for seg in seg_list:
				if seg in instiuteContainer:
					instiuteResult.append(seg)
		return instiuteResult
	else:
		return None

#每页找到的关键字“男”，“女”个数进行比较，哪个多，以这个关键字作为该页的性别关键字
def searchGender(pageContent):
	maleCount = pageContent.count("男")
	femaleCount = pageContent.count("女")
	if maleCount > femaleCount:
		return "男"
	elif maleCount < femaleCount:
		return "女"
	else:
		return "未知"

# def searchPrize(pageContent):
# 	pattern = re.compile("[。，；].*?奖.*[。，；]?")
# 	instiuteList = pattern.findall(pageContent)
# 	print (instiuteList)



#处理所有页面的链接
def processAllLinks(linkList, parent):
	email = []
	phone = []
	institute = []
	gender = []
	gender_result = ""
	linkListLen = len(linkList)
	progress= QProgressBar(parent)
	progress.move(250,200)
	step = 0
	if linkListLen != 0:
		step = 100 / linkListLen
	else:
		print ("no page link")
		return {}
	progress.show()
	pValue = 0

	for link in linkList:
		pValue = pValue + step
		print (pValue,"%")
		progress.setValue(pValue)
		linkContent = getLinkContent(link)
		if linkContent == None:
			continue
		tmp = searchPhone(linkContent)
		if tmp != None:
			for p in tmp:
				phone.append(p)
		tmp = searchEmail(linkContent)
		if tmp != None:
			for e in tmp:
				email.append(e)
		tmp = searchInstiute(linkContent)
		if tmp != None:
			for i in tmp:
				institute.append(i)
		gender.append(searchGender(linkContent))
	if gender.count("男") > gender.count("女"):
		gender_result = "男"
	elif gender.count("男") < gender.count("女"):
		gender_result = "女"
	else:
		gender_result = "未知"
	progress.close()
	map_result = {}
	if (gender_result.count("男") == 0 and gender_result.count("女") == 0):
		map_result["gender"] = "未知"
	elif (gender_result.count("男") >= gender_result.count("女")):
		map_result["gender"] = "男"
	else:
		map_result["gender"] = "女"
	

	#由于第一页的内容最相关，第一页的邮箱被确定，然后后面的根据出现次数来选
	emailResultList = []
	if (len(email) == 0):
		emailResultList.append("未知")
	else:
		emailResultList.append(email[0])
	#选择剩余出现次数最多的
		if (len(email) > 1):
			most_email = Counter(email).most_common(1)[0][0]
			if most_email != emailResultList[0]:
				emailResultList.append(most_email)
	map_result["email"] = emailResultList


	#由于第一页的内容最相关，第一页的手机被确定，然后后面的根据出现次数来选
	phoneResultList = []
	if (len(phone) == 0):
		phoneResultList.append("未知")
	#选择剩余出现次数最多的
	else:
		phoneResultList.append(phone[0])
		if (len(phone) > 1):
			most_phone = Counter(phone).most_common(1)[0][0]
			if most_phone != phoneResultList[0]:
				phoneResultList.append(most_phone)

	map_result["phone"] = phoneResultList
	
	#学院，选择出现次数最多的
	if (len(institute) >= 1):
		most_institute = Counter(institute).most_common(1)[0][0]
	else:
		most_institute = "未知"
	map_result["institute"] = most_institute
	return map_result
	
