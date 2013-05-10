# -*- coding: utf-8 -*-
import threading
from scada.models import GlobalConfig
from scada.clients import ModbusMaster

class DataAcquisition():
	def __init__(self):
		# time in seconds between the measurement
		self.s = GlobalConfig.objects.get(key='stepsize').value			
		# number of repeatings, 0 run as service
		self.n = GlobalConfig.objects.get(key='repeatings').value 
		self.status = "stop"	# status of the service
		self.i = 1				# 
		self.ModMaster = ModbusMaster()
		self.silentMode = GlobalConfig.objects.get(key='silentMode').value
	
	def reinit(self):
		self.status = "stop"	# status of the service
		self.i = 1				# 
		self.ModMaster = ModbusMaster()
	
	def config(self):
		""" configuration of the service
		
		
		"""
		x = None
		limit = 0
		while not x and limit < 3:
			x = raw_input('run as background service yes/no:')
			if x == "yes" or x == "no":
				if x == "yes":
					self.n = 0
				else:
					self.n = input('repeatings [{0:.1f}s]:') .format(self.n)
			else:
				x = None
				limit = limit+1
				print 'please say "yes" or "no"'
		limit = 0
		while self.s <=0 and limit < 3:
			self.s = input('time in seconds between the measurement [{0:.1f}s]:') .format(self.s)
			if self.s <=0 :
				limit = limit+1
				print 'the time hast to be greater then 0'
				
	def service(self):
		if (self.i<=self.n and self.status == "runnig"):
			try:
				self.ModMaster.request()
				if (self.silentMode == 0):
					print "%d/%d" % (self.i,self.n)
			except:
				print "error"

			self.logThread = threading.Timer(float(self.s),self.service)
			self.logThread.start()
			if (self.n > 0):
				self.i = self.i+1
		else:
			print "stoped Logging"

	def start(self):
		""" start the DataAcquisition service
		
		"""
		self.status = "runnig"
		print "start logging"
		self.service()
		
	def stop(self):
		""" stop the DataAcquisition service
		
		"""
		self.status = "stop"


		
	
	