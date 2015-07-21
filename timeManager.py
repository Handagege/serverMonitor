#!/usr/bin/python

import time

class timeManager():
	def __init__(self):
		self.Period = 0
		self.endPoint = 0

	def __init__(self,period,tempTime):
		self.period = period
		self.endPoint = tempTime-tempTime%(self.period)+self.period

	def setEndPoint(self,tempTime):
		self.endPoint = tempTime-tempTime%(self.period)+self.period

	def setPeriod(self,period):
		self.period = period

	def updateEndPoint(self):
		self.endPoint += self.period


if __name__ == "__main__":
	t = timeManager(5*60,int(time.time()))
	print t.period
	print t.endPoint
	print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(t.endPoint))
	t.updateEndPoint()
	print "after update time end point:"
	print t.endPoint
	print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(t.endPoint))
	t.updateEndPoint()
	print "after update time short end point:"
	print t.endPoint
	print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(t.endPoint))

