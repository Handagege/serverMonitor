#!/usr/bin/python
import logging
import logging.config


class configData():
	def __init__(self,ConfigParser):
		self.logTypeKey = ConfigParser.get("info","log_type_key")
		self.reqTimeKey = ConfigParser.get("info","req_time_key")
		self.logIDKey = ConfigParser.get("info","logID_key")
		self.positionKey = ConfigParser.get("info","position_key")
		self.reqIDKey = ConfigParser.get("info","reqID_key")
		self.serverKey = ConfigParser.get("info","server_key")
		self.commodKey = ConfigParser.get("info","commod_key")
		self.retCodeKey = ConfigParser.get("info","ret_code_key")
		self.featRouteKey = ConfigParser.get("info","feat_route_key")
		self.costTimeKey = ConfigParser.get("info","cost_time_key")
		self.extKey = ConfigParser.get("info","ext_key")

		self.windowLength = ConfigParser.get("time","window_length")
		self.timePeriod = ConfigParser.get("time","time_period")

		self.keyTablePath = ConfigParser.get("path","key_table_path")
		self.postUrlPath = ConfigParser.get("path","post_url_path")
		self.delUrlPath = ConfigParser.get("path","del_url_path")

		self.loggerConfPath = ConfigParser.get("logger","file_path")
		self.loggerName = ConfigParser.get("logger","logger_name")

if __name__=="__main__":
	import ConfigParser
	cf = ConfigParser.ConfigParser()
	cf.readfp(open('./conf/rinMethod.ini','r'))
	c = configData(cf)
	print c.logTypeKey
	print c.reqTimeKey
	print c.logIDKey
	print c.positionKey
	print c.reqIDKey
	print c.serverKey
	print c.commodKey
	print c.retCodeKey
	print c.featRouteKey
	print c.costTimeKey
	print c.extKey
	print c.windowLength
	print c.timePeriod
	print c.keyTablePath
	print c.postUrlPath
	print c.postUrlPath
	print c.loggerConfPath
	print c.loggerName

	logging.config.fileConfig(c.loggerConfPath)
	mylogger = logging.getLogger(c.loggerName)

	mylogger.info("This is info message")
	

