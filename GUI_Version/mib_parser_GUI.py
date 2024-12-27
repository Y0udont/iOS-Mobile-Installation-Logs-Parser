#Script to extract to process the mobile installation logs. Normalize output and import to sqlite database for report generation.
import sys, os, re, sqlite3, glob
import easygui as gui
from pathlib import Path

#initialize counters
counter = 0
filescounter = 0

#Month to numeric with leading zero when month < 10 function
#Function call: month = month_converter(month)
def month_converter(month):
	months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	month = months.index(month) + 1
	if (month < 10):
		month = f"{month:02d}"
	return month

#Day with leading zero if day < 10 function
#Functtion call: day = day_converter(day)
def day_converter(day):	
	day = int(day)
	if (day < 10):
		day = f"{day:02d}"
	return day

sp = os.path.abspath(os.path.dirname(sys.argv[0]))
choices = ("Ok","Cancel")

buttonoption = gui.buttonbox("iOS Mobile Installation Logs Parser\nTwitter: @AlexisBrignoni\nWeb: abrignoni.com\n\nSelect the directory that contains the log files.\nReports will be generated in the following directory: "+sp+"\n\nPress OK to select the directory that contains the log files.", "iOS Mobile Installation Logs Parser", choices)

if buttonoption is None:
	exit()
if buttonoption == "Cancel":
	exit()
	
#Create sqlite databases
db = sqlite3.connect('mib.db')

cursor = db.cursor()

#Create table fileds for destroyed, installed, moved and made identifiers.

cursor.execute('''

    CREATE TABLE dimm(time_stamp TEXT, action TEXT, bundle_id TEXT, 

					  path TEXT)

''')

db.commit()



#Search for Installed applications
#for filename in glob.glob('*.log*'):
#file = open('mobile_installation.log.1', 'r', encoding="utf8")



input_path = gui.diropenbox()
if input_path is None:
	exit()
for filename in Path(input_path).rglob('mobile_installation.log.*'):
	file = open(filename, 'r', encoding='utf8' )
	filescounter = filescounter + 1
	for line in file:
		counter = counter+1
		matchObj = re.search( r"(Install Successful for)", line) #Regex for installed applications
		''' Old code
		if matchObj:
			actiondesc = "Install successful"
			#print(actiondesc)
			matchObj = re.search( r"(?<=for \()(.*)(?=\))", line) #Regex for bundle id
			if matchObj:
				bundleid = matchObj.group(1)
				#print ("Bundle ID: ", bundleid )
		'''
		if matchObj:
			actiondesc = "Install successful"
			matchObj1 = re.search( r"(?<= for \(Placeholder:)(.*)(?=\))", line) #Regex for bundle id
			matchObj2 = re.search( r"(?<= for \(Customer:)(.*)(?=\))", line) #Regex for bundle id	
			matchObj3 = re.search( r"(?<= for \(System:)(.*)(?=\))", line) #Regex for bundle id	
			matchObj4 = re.search( r"(?<= for \()(.*)(?=\))", line) #Regex for bundle id			
			if matchObj1:
				bundleid = matchObj1.group(1)
			elif matchObj2:
				bundleid = matchObj2.group(1)
			elif matchObj3:
				bundleid = matchObj3.group(1)
			elif matchObj4:
				bundleid = matchObj4.group(1)
			matchObj = re.search( r"(?<=^)(.*)(?= \[)", line) #Regex for timestamp
			if matchObj:
				timestamp = matchObj.group(1)
				weekday, month, day, time, year = (str.split(timestamp))
				day = day_converter(day)
				month = month_converter(month)
				inserttime = str(year)+ '-'+ str(month) + '-' + str(day) + ' ' + str(time)
				#print(inserttime)
				#print(month)
				#print(day)
				#print(year)
				#print(time)
				#print ("Timestamp: ", timestamp)
			
			#print(inserttime, actiondesc, bundleid)
			
			#insert to database
			cursor = db.cursor()
			datainsert = (inserttime, actiondesc, bundleid, '' ,)
			cursor.execute('INSERT INTO dimm (time_stamp, action, bundle_id, path)  VALUES(?,?,?,?)', datainsert)
			db.commit()
			
			#print()
				
		
		matchObj = re.search( r"(Destroying container with identifier)", line) #Regex for destroyed containers
		if matchObj:
			actiondesc = "Destroying container"
			#print(actiondesc)
			#print("Destroyed containers:")
			matchObj = re.search( r"(?<=identifier )(.*)(?= at )", line) #Regex for bundle id
			if matchObj:
				bundleid = matchObj.group(1)
				#print ("Bundle ID: ", bundleid )
		
			matchObj = re.search( r"(?<=^)(.*)(?= \[)", line) #Regex for timestamp
			if matchObj:
				timestamp = matchObj.group(1)
				weekday, month, day, time, year = (str.split(timestamp))
				day = day_converter(day)
				month = month_converter(month)
				inserttime = str(year)+ '-'+ str(month) + '-' + str(day) + ' ' + str(time)
				#print(inserttime)
				#print(month)
				#print(day)
				#print(year)
				#print(time)
				#print ("Timestamp: ", timestamp)
			
			matchObj = re.search( r"(?<= at )(.*)(?=$)", line) #Regex for path
			if matchObj:
				path = matchObj.group(1)
				#print ("Path: ", matchObj.group(1))
			
		
			#print(inserttime, actiondesc, bundleid, path)			
			
			#insert to database
			cursor = db.cursor()
			datainsert = (inserttime, actiondesc, bundleid, path ,)
			cursor.execute('INSERT INTO dimm (time_stamp, action, bundle_id, path)  VALUES(?,?,?,?)', datainsert)
			db.commit()
			
			#print()
			

		matchObj = re.search( r"(Data container for)", line) #Regex Moved data containers
		if matchObj:
			actiondesc = "Data container moved"
			#print(actiondesc)
			#print("Data container moved:")
			matchObj = re.search( r"(?<=for )(.*)(?= is now )", line) #Regex for bundle id
			if matchObj:
				bundleid = matchObj.group(1)
				#print ("Bundle ID: ", bundleid )
		
			matchObj = re.search( r"(?<=^)(.*)(?= \[)", line) #Regex for timestamp
			if matchObj:
				timestamp = matchObj.group(1)
				weekday, month, day, time, year = (str.split(timestamp))
				day = day_converter(day)
				month = month_converter(month)
				inserttime = str(year)+ '-'+ str(month) + '-' + str(day) + ' ' + str(time)
				#print(inserttime)
				#print(month)
				#print(day)
				#print(year)
				#print(time)
				#print ("Timestamp: ", timestamp)
			
			matchObj = re.search( r"(?<= at )(.*)(?=$)", line) #Regex for path
			if matchObj:
				path = matchObj.group(1)
				#print ("Path: ", matchObj.group(1))
				
			#print(inserttime, actiondesc, bundleid, path)			
			
			#insert to database
			cursor = db.cursor()
			datainsert = (inserttime, actiondesc, bundleid, path ,)
			cursor.execute('INSERT INTO dimm (time_stamp, action, bundle_id, path)  VALUES(?,?,?,?)', datainsert)
			db.commit()
			
			#print()
			
		matchObj = re.search( r"(Made container live for)", line) #Regex for made container
		if matchObj:
			actiondesc = "Made container live"
			#print(actiondesc)
			#print("Made container:")
			matchObj = re.search( r"(?<=for )(.*)(?= at)", line) #Regex for bundle id
			if matchObj:
				bundleid = matchObj.group(1)
				#print ("Bundle ID: ", bundleid )
		
			matchObj = re.search( r"(?<=^)(.*)(?= \[)", line) #Regex for timestamp
			if matchObj:
				timestamp = matchObj.group(1)
				weekday, month, day, time, year = (str.split(timestamp))
				day = day_converter(day)
				month = month_converter(month)
				inserttime = str(year)+ '-'+ str(month) + '-' + str(day) + ' ' + str(time)
				#print(inserttime)
				#print(month)
				#print(day)
				#print(year)
				#print(time)
				#print ("Timestamp: ", timestamp)
			
			matchObj = re.search( r"(?<= at )(.*)(?=$)", line) #Regex for path
			if matchObj:
				path = matchObj.group(1)
				#print ("Path: ", matchObj.group(1))
			#print(inserttime, actiondesc, bundleid, path)			
			
			#insert to database
			cursor = db.cursor()
			datainsert = (inserttime, actiondesc, bundleid, path ,)
			cursor.execute('INSERT INTO dimm (time_stamp, action, bundle_id, path)  VALUES(?,?,?,?)', datainsert)
			db.commit()
			
		matchObj = re.search( r"(Uninstalling identifier )", line) #Regex for made container
		if matchObj:
			actiondesc = "Uninstalling identifier"
			#print(actiondesc)
			#print("Uninstalling identifier")
			matchObj = re.search( r"(?<=Uninstalling identifier )(.*)", line) #Regex for bundle id
			if matchObj:
				bundleid = matchObj.group(1)
				#print ("Bundle ID: ", bundleid )
		
			matchObj = re.search( r"(?<=^)(.*)(?= \[)", line) #Regex for timestamp
			if matchObj:
				timestamp = matchObj.group(1)
				weekday, month, day, time, year = (str.split(timestamp))
				day = day_converter(day)
				month = month_converter(month)
				inserttime = str(year)+ '-'+ str(month) + '-' + str(day) + ' ' + str(time)
				#print(inserttime)
				#print(month)
				#print(day)
				#print(year)
				#print(time)
				#print ("Timestamp: ", timestamp)
			
			#insert to database
			cursor = db.cursor()
			datainsert = (inserttime, actiondesc, bundleid, '' ,)
			cursor.execute('INSERT INTO dimm (time_stamp, action, bundle_id, path)  VALUES(?,?,?,?)', datainsert)
			db.commit()

		matchObj = re.search( r"(main: Reboot detected)", line) #Regex for reboots
		if matchObj:
			actiondesc = "Reboot detected"
			#print(actiondesc)		
			matchObj = re.search( r"(?<=^)(.*)(?= \[)", line) #Regex for timestamp
			if matchObj:
				timestamp = matchObj.group(1)
				weekday, month, day, time, year = (str.split(timestamp))
				day = day_converter(day)
				month = month_converter(month)
				inserttime = str(year)+ '-'+ str(month) + '-' + str(day) + ' ' + str(time)
				#print(inserttime)
				#print(month)
				#print(day)
				#print(year)
				#print(time)
				#print ("Timestamp: ", timestamp)
			
			#insert to database
			cursor = db.cursor()
			datainsert = (inserttime, actiondesc, '', '' ,)
			cursor.execute('INSERT INTO dimm (time_stamp, action, bundle_id, path)  VALUES(?,?,?,?)', datainsert)
			db.commit()			
			
		matchObj = re.search( r"(Attempting Delta patch update of )", line) #Regex for Delta patch
		if matchObj:
			actiondesc = "Attempting Delta patch"
			#print(actiondesc)
			#print("Made container:")
			matchObj = re.search( r"(?<=Attempting Delta patch update of )(.*)(?= from)", line) #Regex for bundle id
			if matchObj:
				bundleid = matchObj.group(1)
				#print ("Bundle ID: ", bundleid )
		
			matchObj = re.search( r"(?<=^)(.*)(?= \[)", line) #Regex for timestamp
			if matchObj:
				timestamp = matchObj.group(1)
				weekday, month, day, time, year = (str.split(timestamp))
				day = day_converter(day)
				month = month_converter(month)
				inserttime = str(year)+ '-'+ str(month) + '-' + str(day) + ' ' + str(time)
				#print(inserttime)
				#print(month)
				#print(day)
				#print(year)
				#print(time)
				#print ("Timestamp: ", timestamp)
			
			matchObj = re.search( r"(?<= from )(.*)", line) #Regex for path
			if matchObj:
				path = matchObj.group(1)
				#print ("Path: ", matchObj.group(1))
			#print(inserttime, actiondesc, bundleid, path)			
			
			#insert to database
			cursor = db.cursor()
			datainsert = (inserttime, actiondesc, bundleid, path ,)
			cursor.execute('INSERT INTO dimm (time_stamp, action, bundle_id, path)  VALUES(?,?,?,?)', datainsert)
			db.commit()
			
			#print()
try:
	print ()
	print ('iOS Mobile Installation Logs Parser')
	print ('By: @AlexisBrignoni')
	print ('Web: abrignoni.com')
	print ()
	print ('Logs processed: ', filescounter)
	print ('Lines processed: ', counter)
	print ()
	file.close


	
	#Initialize counters
	totalapps = 0
	installedcount = 0
	uninstallcount = 0
	historicalcount = 0
	sysstatecount = 0
	
	#created folders for reports and sub folders for App history, App state
	os.makedirs("./Apps_State/")
	os.makedirs("./Apps_Historical/")
	os.makedirs("./System_State/")
	
	#Initialize text file reports for installed and unistalled apps
	f1=open('./Apps_State/UninstalledApps.txt', 'w+', encoding="utf8")
	f2=open('./Apps_State/InstalledApps.txt', 'w+', encoding="utf8")
	f4=open('./System_State/SystemState.txt', 'w+', encoding="utf8")
	
	
	#Initialize database connection
	db = sqlite3.connect('mib.db')
	
	cursor = db.cursor()
	
	#Query to create installed and uninstalled app reports
	cursor.execute('''SELECT distinct bundle_id from dimm''')
	all_rows = cursor.fetchall()
	for row in all_rows:
		#print(row[0])
		distinctbundle = row[0]
		cursor.execute('''SELECT * from dimm where bundle_id=? order by time_stamp desc limit 1''', (distinctbundle,))
		all_rows_iu = cursor.fetchall()
		for row in all_rows_iu:
			#print(row[0], row[1], row[2], row[3])
			if row[2] == '':
				continue
			elif row[1] == 'Destroying container':
				#print(row[0], row[1], row[2], row[3])
				uninstallcount = uninstallcount + 1
				totalapps = totalapps + 1
				#tofile1 = row[0] + ' ' + row[1] + ' ' + row[2] + ' ' + row[3] + '\n'
				tofile1 = row[2] +  '\n'
				f1.write(tofile1)
				#print()
			elif row[1] == 'Uninstalling identifier':
				#print(row[0], row[1], row[2], row[3])
				uninstallcount = uninstallcount + 1
				totalapps = totalapps + 1
				#tofile1 = row[0] + ' ' + row[1] + ' ' + row[2] + ' ' + row[3] + '\n'
				tofile1 = row[2] +  '\n'
				f1.write(tofile1)
				#print()
			else:
				#print(row[0], row[1], row[2], row[3])
				tofile2 = row[2] + '\n'
				
				f2.write(tofile2)
				installedcount = installedcount + 1	
				totalapps = totalapps + 1
	
	f1.close()
	f2.close()
	
	#Query to create historical report per app
				
	cursor.execute('''SELECT distinct bundle_id from dimm''')
	all_rows = cursor.fetchall()
	for row in all_rows:
		#print(row[0])
		distinctbundle = row[0]
		if row[0] == '':
			continue
		else:
			f3=open('./Apps_Historical/' + distinctbundle + '.txt', 'w+', encoding="utf8") #Create historical app report per app
			cursor.execute('''SELECT * from dimm where bundle_id=? order by time_stamp DESC''', (distinctbundle,)) #Query to create app history per bundle_id
			all_rows_hist = cursor.fetchall()
			for row in all_rows_hist:
				#print(row[0], row[1], row[2], row[3])
				tofile3 = row[0] + ' ' + row[1] + ' ' + row[2] + ' ' + row[3] + '\n'
				f3.write(tofile3)			
		f3.close()
		historicalcount = historicalcount + 1
	
	#Query to create system events
				
	cursor.execute('''SELECT * from dimm where action ='Reboot detected' order by time_stamp DESC''')
	all_rows = cursor.fetchall()
	for row in all_rows:
		#print(row[0])
		#print(row[0], row[1], row[2], row[3])
		tofile4 = row[0] + ' ' + row[1] + ' ' + row[2] + ' ' + row[3] + '\n'
		f4.write(tofile4)
		sysstatecount = sysstatecount + 1		
		
	
		
				
	print ('Total apps: ', totalapps)
	print ('Total installed apps: ', installedcount)
	print ('Total uninstalled apps: ', uninstallcount)
	print ('Total historical app reports: ', historicalcount)
	print ('Total system state events: ', sysstatecount)
	f1.close()
	f2.close()
	f4.close()

except:
	print("Log files not found in "+input_path)

gui.msgbox("Processing completed.\nReports located at "+os.path.abspath(os.path.dirname(sys.argv[0]))+"\n\nLogs processed: "+str(filescounter)+"\nLines processed: "+str(counter)+"\n\nTotal apps: "+str(totalapps)+"\nTotal installed apps: "+str(installedcount)+"\nTotal uninstalled apps: "+str(uninstallcount)+"\nTotal historical app reports: "+str(historicalcount)+"\nTotal system state events: "+str(sysstatecount),"iOS Mobile Installaion Logs Parser", "Ok" )
