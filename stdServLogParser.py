#!/usr/bin/python

import time

class stdServLogParser():
	def __init__(self,configData):
		self.dic_data = {}
		self.configData = configData

	def parse(self,data):
		logClassList = data.split("|")
		temp_dic_data = {}
		frameLog = logClassList[0]
		frameLog.strip()
		servLog = logClassList[1]
		servLog.strip()
		frameLogItemList = frameLog.split(" ")
		temp_dic_data[self.configData.logTypeKey] = frameLogItemList[0]
		timeStr = frameLogItemList[1] + " " + frameLogItemList[2]
		timeStr = timeStr[1:timeStr.find(".")]
		temp_dic_data[self.configData.reqTimeKey] = timeStr
		logID = frameLogItemList[3]
		temp_dic_data[self.configData.logIDKey] = logID[1:-1]
		temp_dic_data[self.configData.positionKey] = frameLogItemList[4][1:-1]
		for i in servLog.split(";"):
			dataNodeList = i.split(":")
			temp_dic_data[dataNodeList[0]] = dataNodeList[-1]
		costTimeKey = temp_dic_data.get(self.configData.costTimeKey,None)
		if costTimeKey != None:
			temp_dic_data[self.configData.costTimeKey] = costTimeKey[:costTimeKey.find("(")]
		self.dic_data = temp_dic_data
		return temp_dic_data

	#def get(self,=""):
		#return self.dic_data.get(,None)

	def getDicData(self):
		return self.dic_data

	def clear(self):
		self.dic_data.clear()

if __name__ == "__main__":
	import configData
	import ConfigParser
	cf = ConfigParser.ConfigParser()
	cf.readfp(open('./conf/rinMethod.ini','r'))
	c = configData.configData(cf)
	s = stdServLogParser(c)
	data = "WARN [2015-05-03 11:13:46.998] [logid:0] [src/userrecomtest_work_interface.cpp:247] | REQ_ID:10758252990061920973;SERV:RecomServ;CMD:recom;RET_CODE:0;FEAT_ROUTE:b_id_01->ct_id_01->pt_id_01->st_id_03;COST:3449(9-3421-3-13-1-2);"
	print s.parse(data)
	data = "ERROR [2015-04-01 15:34:30.657] [logid:0] [tcpserver.cpp:152] | REQ_ID:10758252990973006192;SERV:Ranker;CMD:rank;RET_CODE:-3;"
	print s.parse(data)
	data = "INFO [2015-05-03 11:13:46.998] [logid:0] [src/userrecomtest_work_interface.cpp:312] | REQ_ID:10751920973825299006;SERV:RecomServ;CMD:recom;RET_CODE:24;FEAT_ROUTE:b_id_01->ct_id_01->pt_id_01->st_id_02;COST:37299(1154-2493-9257-3414-19115-1866);"
	print s.parse(data)
