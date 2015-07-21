#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import copy
import time
import logging
import logging.config
from chartConfProducer import *
from statsItem import *

class effectMonitor():
	def __init__(self,configData,timeManager):
		#时间管理器，用于储存更新时间数据
		self.timeManager = timeManager
		#配置信息
		self.configData = configData
		#配置logger
		logging.config.fileConfig(self.configData.loggerConfPath)
		self.logger = logging.getLogger(self.configData.loggerName)
		#最近一段时间的数据窗口长度
		self.windowLength = int(configData.windowLength)
		#所有的统计状态
		self.totalStatusKey = "total"
		self.allInOneDic = {}
		self.allInOneDic[self.totalStatusKey] = statsItem(self.windowLength)
		#用于标记新的key值
		self.newKeyFlag = False
		#标准标记符
		self.stdIndex = ":"
		#不同数据类型key尾缀
		self.keySuffixList = [":avgReqCost",":reqSuccessRatio",":reqNum"]
		#前缀
		self.keyPrefix = "eros:server:"
		#日志类型
		self.logTypeList = ["ERROR","INFO","WARNING"]
		self.ccProducer = chartConfProducer(self.configData.keyTablePath,self.keyPrefix,self.keySuffixList)

	def deal(self,dataDic):
		dataIntegrityFlag = True
		dataCorrectFlag = True
		#得到数据
		reqCost = dataDic.get(self.configData.costTimeKey,None)
		logType = dataDic.get(self.configData.logTypeKey,None)
		#reqTime已经被转换成int时间戳
		reqTime = dataDic.get(self.configData.reqTimeKey,None)
		retCode = dataDic.get(self.configData.retCodeKey,None)
		serverNodeName = dataDic.get(self.configData.serverNodeNameKey,None)
		
		#judge data integrity
		if (reqCost == None or logType == None or reqTime == None or\
			retCode == None or serverNodeName == None) \
			or (reqCost == "" or logType == "" or reqTime == "" \
			or retCode == "" or serverNodeName == ""):
			dataIntegrityFlag = False
		#judge data correct
		try:
			reqCost = int(reqCost)
			retCode = int(retCode)	
		except ValueError:
			self.logger.error("have some data error(reqCost or retCode) can't tansfer to int")
			dataCorrectFlag = False
		
		if dataIntegrityFlag and dataCorrectFlag:	
			endPoint = self.timeManager.endPoint
			period = self.timeManager.period
			startPoint = endPoint-period*self.windowLength
			#check the key exist
			self.addNewStatsItem(serverNodeName)
			#update key table
			if self.newKeyFlag:
				self.logger.debug("-----------|update key table|-----------")
				self.updateChartKeyTable()
			self.logger.debug("......................start.....................")
			#self.logger.debug(dataDic)
			self.logger.debug("end time point is %d"%(endPoint))
			keyTime = reqTime
			if keyTime >= startPoint and keyTime < endPoint:
				pos = int((keyTime-startPoint)/period)
				##update data
				self.updateStats(serverNodeName,pos,logType,reqCost,retCode)
			elif keyTime >= endPoint:
				self.logger.debug(".................post window stats................")
				self.postStats()
				self.timeManager.updateEndPoint()
				self.logger.debug("after update end time point is %d"%(self.timeManager.endPoint))
				self.deal(dataDic)

	def postStats(self):
		keyTime = self.timeManager.endPoint-self.timeManager.period*self.windowLength
		postFlag = True
		for key in self.allInOneDic.keys():
			(avgReqCost,reqSuccessRatio,reqNum,delFlag) = self.allInOneDic[key].proStats()
			postAvgReqCostKey = self.keyPrefix + key + self.keySuffixList[0]
			postReqSuccessRatioKey = self.keyPrefix + key + self.keySuffixList[1]
			postReqNumKey = self.keyPrefix + key + self.keySuffixList[2]
			if delFlag:
				del self.allInOneDic[key]
			elif postFlag:
				response = urllib.urlopen(self.configData.postUrlPath,\
				self.constructUrlData(postAvgReqCostKey,int(avgReqCost),keyTime))
				self.logger.debug("[%s] avgReqCost post success or fail:%s"\
				%(postAvgReqCostKey,response.read()))
				response = urllib.urlopen(self.configData.postUrlPath,\
				self.constructUrlData(postReqSuccessRatioKey,int(reqSuccessRatio),keyTime))
				self.logger.debug("[%s] reqSuccessRatio post success or fail:%s"\
				%(postAvgReqCostKey,response.read()))
				response = urllib.urlopen(self.configData.postUrlPath,\
				self.constructUrlData(postReqNumKey,int(reqNum),keyTime))
				self.logger.debug("[%s] reqNum post success or fail:%s"%(postAvgReqCostKey,response.read()))
			self.logger.debug("[%s] stats----time:%s avgReqCost:%d reqSuccessRatio:%0.3f reqNum:%d"\
			%(key,time.strftime('%Y%m%d%H%M%S',time.localtime(keyTime)),int(avgReqCost),reqSuccessRatio,reqNum))

	def updateStats(self,key,pos,logType,reqCost,retCode):
		#total内容一并更新
		self.allInOneDic[self.totalStatusKey].updateRNStatsQueue(pos)
		self.allInOneDic[key].updateRNStatsQueue(pos)
		if logType != self.logTypeList[0]:
			self.allInOneDic[self.totalStatusKey].updateRCStatsQueue(reqCost,pos)
			self.allInOneDic[self.totalStatusKey].updateRNNEStatsQueue(pos)
			self.allInOneDic[key].updateRCStatsQueue(reqCost,pos)
			self.allInOneDic[key].updateRNNEStatsQueue(pos)
			if retCode >= 0:
				self.allInOneDic[self.totalStatusKey].updateRSNStatsQueue(pos)
				self.allInOneDic[key].updateRSNStatsQueue(pos)
		
	
	def constructUrlData(self,key,rank,time):
		para_dic = {}
		para_dic["key"] = key
		para_dic["rank"] = rank
		para_dic["time"] = time
		return urllib.urlencode(para_dic)

	def addNewStatsItem(self,key):
		if key not in self.allInOneDic:
			self.allInOneDic[key] = statsItem(self.windowLength)
			self.newKeyFlag = True

	def updateChartKeyTable(self):
		self.newKeyFlag = False
		#self.ccProducer.deal(self.allInOneDic.keys())

	def writeKeyToFile(self,file,keys,suffix):
		for d in keys:
			for keySuffix in self.keySuffixList:
				file.write(self.keyPrefix+d+keySuffix+"\n")

	def printStatsItemMsg(self):
		for key in self.allInOneDic:
			print "***...[%s] itemStatsMsg...***"%(key)
			self.allInOneDic[key].printMsg()
	
	def printStatsItemMsgToLog(self):
		for key in self.allInOneDic:
			self.logger.debug("***...[%s] itemStatsMsg...***"%(key))
			self.allInOneDic[key].printMsgToLog(self.logger)
		self.logger.debug("......................end.....................\n")
		
def test2():
	import random
	import time
	import ConfigParser
	import timeManager
	import configData
	import stdServLogParser
	##my data prepare
	##------------------------START-----------------------------------
	#configure message
	cf = ConfigParser.ConfigParser()
	cf.readfp(open('./conf/rinMethod.ini','r'))
	c = configData.configData(cf)
	#data parser
	parser = stdServLogParser.stdServLogParser(c)
	#init timeManager data
	now = int(time.time())
	t = timeManager.timeManager(int(c.timePeriod),now)
	#key processer
	effectMonitorInstance = effectMonitor(c,t)

	logTypeList = ["ERROR","INFO"]
	retCodeList = [-1,0,1,2,3]
	serverNodeNameList = ["10.33.96.33","10.33.96.32"]
	for i in range(1,200):
		msg = ".................%d stats item data................"%(i)
		effectMonitorInstance.logger.debug(msg)
		effectMonitorInstance.logger.debug("------------------------START------------------------------")
		createTime = random.randint(-4,10)+now
		logType = random.choice(logTypeList)
		retCode = random.choice(retCodeList)
		serverNodeName = random.choice(serverNodeNameList)
		stdTimeStr = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(createTime))
		data = "%s [%s.657] [logid:0] [tcpserver.cpp:152] | REQ_ID:10758252990973006192;SERV:Ranker;CMD:rank;RET_CODE:%d;FEAT_ROUTE:b_id_01->ct_id_01->pt_id_01->st_id_03;COST:3449(9-3421-3-13-1-2);EXT3:%s;"%(logType,stdTimeStr,retCode,serverNodeName)
		effectMonitorInstance.logger.debug(data)
		data = parser.parse(data)
		effectMonitorInstance.deal(data)
		parser.clear()
		effectMonitorInstance.printStatsItemMsgToLog()
		effectMonitorInstance.logger.debug("------------------------END------------------------------\n")

if __name__ == "__main__":
	test2()
