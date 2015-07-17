#!/usr/bin/python

import Queue

class statsItem():
	def __init__(self,windowLength=12):
		self.reqCostStatusQueue = [0.0]*windowLength
		self.reqSuccessNumStatusQueue = [0]*windowLength
		self.reqNumNoErrorStatusQueue = [0]*windowLength
		self.reqNumStatusQueue = [0]*windowLength

	def updateRCStatsQueue(self,reqCost,pos=-1):
		self.reqCostStatusQueue[pos] += reqCost

	def updateRSNStatsQueue(self,pos=-1):
		self.reqSuccessNumStatusQueue[pos] += 1

	def updateRNNEStatsQueue(self,pos=-1):
		self.reqNumNoErrorStatusQueue[pos] += 1

	def updateRNStatsQueue(self,pos=-1):
		self.reqNumStatusQueue[pos] += 1
		
	def proStats(self):
		avgReqCost = 0.0
		reqSuccessRatio = 0.0
		reqNum = 0
		if self.reqNumStatusQueue[0] != 0:
			reqSuccessRatio = float(self.reqSuccessNumStatusQueue[0])/float(self.reqNumStatusQueue[0])
			reqNum = self.reqNumStatusQueue[0]
		else:	
			print "[waring] total req Num is 0"
		if self.reqNumNoErrorStatusQueue[0] != 0:
			avgReqCost = self.reqCostStatusQueue[0]/float(self.reqNumNoErrorStatusQueue[0])
		else:
			print "[waring] all log is error type"
		del self.reqCostStatusQueue[0]
		del self.reqNumNoErrorStatusQueue[0]
		del self.reqSuccessNumStatusQueue[0]
		del self.reqNumStatusQueue[0]
		self.reqCostStatusQueue.append(0.0)
		self.reqNumNoErrorStatusQueue.append(0)
		self.reqSuccessNumStatusQueue.append(0)
		self.reqNumStatusQueue.append(0)
		return avgReqCost,reqSuccessRatio,reqNum

	def printMsg(self):
		print "request cost time status queue: ",self.reqCostStatusQueue
		print "request success number status queue: ",self.reqSuccessNumStatusQueue
		print "request number no error status queue: ",self.reqNumNoErrorStatusQueue
		print "request number status queue: ",self.reqNumStatusQueue
		
	def printMsgToLog(self,logger):
		pass
		
if __name__ == "__main__":
	import random
	myStatsItem = statsItem(3)
	for i in range(1,120):
		print "---------------- get %d data -------------"%(i)
		#post time
		if i%34 == 0:
			avgReqCost,reqSuccessRatio,reqNum = myStatsItem.proStats()
			print "--- ARCValue: %.3f | RSRValue: %.3f | RNValue: %d ---"%(avgReqCost,reqSuccessRatio,reqNum)
		myStatsItem.updateRNStatsQueue()
		#error log
		if i%20 == 0:
			myStatsItem.printMsg()
		#fail log
		elif i%11 == 0:
			myStatsItem.updateRNNEStatsQueue()
			myStatsItem.updateRCStatsQueue(random.uniform(1,10))
			myStatsItem.printMsg()
		#success log
		else :
			myStatsItem.updateRNNEStatsQueue()
			myStatsItem.updateRCStatsQueue(random.uniform(1,10))
			myStatsItem.updateRSNStatsQueue()
			myStatsItem.printMsg()
		print "------------------ end --------------------"
