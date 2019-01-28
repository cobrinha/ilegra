#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob, os, re, time, shutil

class ImportDatFiles:
	def __init__(self, homedir = os.path.expanduser("~")):		
		self._homedir_in  = homedir + "/data/in"  
		self._homedir_out = homedir + "/data/out"

	def getFileList(self):
		self.__dat_files = []
		if os.path.isdir(self._homedir_in):
			os.chdir(self._homedir_in)
			self.__dat_files = ['%s/%s' % (self._homedir_in, file) for file in glob.glob("*.dat")]
			if self.__dat_files:
				return self.__dat_files
			else:
				return self.setError("DAT_NOT_FOUND", self._homedir_in)	
		else:
			return self.setError("DIR_NOT_FOUND", self._homedir_in)

	def setFileList(self, files):
		self.clearOutput()	
		if files:
			self.__dat_files = [file for file in files if os.path.isfile(file)]
			if self.__dat_files:
				self.readFiles()
			else:
				return self.setError("SET_FILES_ERROR", files)	
		else:
			return self.setError("SET_FILES_INVALID_PARAMETER", files)	

	def clearOutput(self):	
		print('%s %s' % ("Removing old output files in", self._homedir_out))
		files = glob.glob(self._homedir_out+'/*')		
		for file_remove in files:
			try:
				os.remove(file_remove)
			except:
				print('%s %s' % ("Cannot remove file:", file_remove))
				pass

	def readFiles(self):
		for file in self.__dat_files:
			self.readData(file)

	def readData(self, file):
		print('%s %s' % ("Reading file:", file))
		line_list = []
		self.worst_salesman_ever	= {}
		self.amount_customers = 0
		self.amount_salesman = 0
		self.most_expensive_id = 0
		self.most_expensive = 0
		with open(file) as input_file:
			while True:
				line = input_file.readline()
				if not line:
					break
				self.formatData(line, file)
			self.saveOutput(file)

	def formatData(self, line, file):
		line_re = re.compile("(?<!^)\s+(?=[0000])(?!.\s)").split(line)	
		for line_aux in line_re:
			line_split = line_aux.split('ç')
			if str(line_split[0].strip())=='001': #if salesman
				self.amount_salesman += 1
			elif str(line_split[0].strip())=='002': #elif customer
				self.amount_customers += 1
			elif str(line_split[0].strip())=='003': #elif sales data
				sale = line_split[2].replace('[','').replace(']','')
				sale_list = sale.strip().split(',')
				for sale_items in sale_list:
					sale_items_list = sale_items.split('-')
					sale_value = float(sale_items_list[2])
					sale_id = str(sale_items_list[0])
					self.most_expensive_id = sale_id if sale_value > self.most_expensive else self.most_expensive_id
					self.most_expensive = sale_value if sale_value > self.most_expensive else self.most_expensive
					if line_split[3].strip() in self.worst_salesman_ever:
						self.worst_salesman_ever[line_split[3].strip()] += sale_value
					else:
						self.worst_salesman_ever[line_split[3].strip()] = sale_value

	def saveOutput(self, file):						
		output_filename = os.path.basename(file).replace('.dat','.done.dat')
		print('%s %s/%s' % ("Writing file: ", self._homedir_out, output_filename))
		with open(self._homedir_out+'/'+output_filename, 'w+') as output_file:			
			worst = min(self.worst_salesman_ever, key=self.worst_salesman_ever.get)
			output_data  = '%s %s \n' % ("Amount of customers: ", str(self.amount_customers))
			output_data += '%s %s \n' % ("Amount of salesman: ", str(self.amount_salesman))
			output_data += '%s %s \n' % ("Most expensive ID: ", str(self.most_expensive_id))
			output_data += '%s %s \n' % ("Worst salesman ever: ", str(worst))
			output_file.write(output_data)
			output_file.close()

	def setError(self, error_code, error_arg = ""):
		if error_code:
			error_dict =	{
			  "DIR_NOT_FOUND": "Invalid or inexistent path",
			  "DAT_NOT_FOUND": "No DAT files found",
			  "SET_FILES_ERROR": "Error setting DAT files",
			  "SET_FILES_INVALID_PARAMETER": "Invalid parameter setting DAT files",
			}
			error_msg = error_dict[error_code]
			if error_msg:
				print('%s : %s' % (error_msg, error_arg))
		return False

if __name__ == "__main__":
	objImport = ImportDatFiles()
	while True:
		dat_files = objImport.getFileList()
		objImport.setFileList(dat_files)
		print('%s' % "Sleeping 10 seconds...")
		time.sleep(10)