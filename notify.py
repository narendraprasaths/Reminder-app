# Python program For
# Birthday and Holidays in India Reminder Application
import os
import sqlite3
import datetime

# Birthdays and Holidays should be stored in this SQl file 
db= sqlite3.connect("my_db.sql")
conn=db.cursor()

class remind:
	def __init__(self):
			self.Birthday()
			self.Holiday()

	# To retrive birthday notification
	def Birthday(self):
		now=str(datetime.datetime.now())
		year,month,day=now[:11].strip().split("-")
		dayt=day+"-"+month
		try:
			conn.execute("select * from BirthdayEvent where day=?",(dayt,))
			rows=conn.fetchall()
			print(rows)
		except:
			return
		for row in rows:
			age=int(year)-int(row[2])
			if(row[3]!=""):
				os.system('notify-send " Today is '+str(row[0])+"'s "+str(age)+" birthday\n Note: "+row[3]+'"')

			else:
				os.system('notify-send " Today is '+str(row[0])+"'s birthday he is turning"+str(age)+'"')

	# To retrive holiday notification
	def Holiday(self):
		now=str(datetime.datetime.now())
		dater=now[:11].strip()
		try:
			conn.execute("select * from HolidayEvent where day=?",(dater,))
			rows=conn.fetchall()
			print(rows)
		except:
			return
		for row in rows:
			os.system('notify-send "Today is '+str(row[0]+'"'))

remind()