# Python program For
# Birthday and Holidays in India Reminder Application
from tkinter import *
from tkinter import filedialog
import tkinter as tk
import tkinter.messagebox
import sqlite3
import datetime
from time import *	
from icalendar import *
import calendar
import os
# file import
import notify

# Birthdays and Holidays should be stored in this SQl file 
db = sqlite3.connect("my_db.sql")
conn = db.cursor()


''' GUI Calendar'''
class calend:
    def __init__(self, parent, values):
        self.values = values
        self.parent = parent
        self.cal = calendar.TextCalendar(calendar.SUNDAY)
        self.year = datetime.date.today().year
        self.month = datetime.date.today().month
        self.wid = []
        self.day_selected = 1
        self.month_selected = self.month
        self.year_selected = self.year
        self.day_name = ''
        self.setup(self.year, self.month)
         
    def clear(self):
        for w in self.wid[:]:
            w.grid_forget()
            self.wid.remove(w)
     
    def go_prev(self):
        if self.month > 1:
            self.month -= 1
        else:
            self.month = 12
            self.year -= 1        
        self.clear()
        self.setup(self.year, self.month)
 
    def go_next(self):
        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.year += 1
        self.clear()
        self.setup(self.year, self.month)
         
    def selection(self, day, name):
        self.day_selected = day
        self.month_selected = self.month
        self.year_selected = self.year
        self.day_name = name
        self.values['day_selected'] = day
        self.values['month_selected'] = self.month
        self.values['year_selected'] = self.year
        self.values['day_name'] = name
        self.values['month_name'] = calendar.month_name[self.month_selected]
        self.clear()
        self.setup(self.year, self.month)
         
    def setup(self, y, m):
    	# go_prev
        left = tk.Button(self.parent, text='<', command=self.go_prev)
        self.wid.append(left)
        left.grid(row=0, column=1)
         
        # page_title 
        header = tk.Label(self.parent, height=2, text='{}   {}'.format(calendar.month_abbr[m], str(y)))
        self.wid.append(header)
        header.grid(row=0, column=2, columnspan=3)
        
        # go_next 
        right = tk.Button(self.parent, text='>', command=self.go_next)
        self.wid.append(right)
        right.grid(row=0, column=5)
         
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        for num, name in enumerate(days):
            t = tk.Label(self.parent, text=name[:3])
            self.wid.append(t)
            t.grid(row=1, column=num)
         
        for w, week in enumerate(self.cal.monthdayscalendar(y, m), 2):
            for d, day in enumerate(week):
                if day:
                    #print(calendar.day_name[day])
                    b = tk.Button(self.parent, width=1, text=day, command=lambda day=day:self.selection(day, calendar.day_name[(day-1) % 7]))
                    self.wid.append(b)
                    b.grid(row=w, column=d)
        
        # display the date with respective attributes              
        sel = tk.Label(self.parent, height=2, text='{} {} {} {}'.format(
            self.day_name, calendar.month_name[self.month_selected], self.day_selected, self.year_selected))
        self.wid.append(sel)
        sel.grid(row=8, column=0, columnspan=7)
        
        # selection process
        ok = tk.Button(self.parent, width=5, text='OK', command=self.kill_and_save)
        self.wid.append(ok)
        ok.grid(row=9, column=2, columnspan=3, pady=10)
    # To quit the tab     
    def kill_and_save(self):
        self.parent.destroy()
 




class CreateEvent:
	"""docstring for CreateEvent"""
	def __init__(self):
		super(CreateEvent).__init__()
		self.arg = Tk()
		self.arg.protocol("WM_DELETE_WINDOW",self.on_closing)
		self.arg.geometry('800x800')
		self.arg.title("select")
		self.caldata={}
		self.start()

	def start(self):
		# choose the events
		self.hday_event=Button(self.arg,text='Holiday Event',command=self.Holiday)
		self.bday_event=Button(self.arg,text='Birthday Event',command=self.Birthday)
		self.hday_event.place(x=400,y=200,anchor=CENTER)
		self.bday_event.place(x=400,y=250,anchor=CENTER)
		self.back_event=Button(self.arg,text="Back",command=self.hbBack)
		self.back_event.place(x=400,y=300,anchor=CENTER)

	def hbBack(self):
		self.arg.destroy()
		root.deiconify()

	def Holiday(self):
		# holiday tab
		self.arg.withdraw()
		self.new=Tk()
		self.new.protocol("WM_DELETE_WINDOW",self.on_bclose)
		# window size
		self.new.geometry('800x800')
		self.new.title("select")
		self.name_of_hevent=Label(self.new,text='Name of event')
		self.name_of_hevent.place(x=400,y=200,anchor=CENTER)
		self.hday=Entry(self.new)
		self.hday.place(x=400,y=250,anchor=CENTER)
		self.date_of_hevent=Button(self.new,text='Date',command=self.calen)
		self.date_of_hevent.place(x=400,y=300,anchor=CENTER)
		self.hol_ok=Button(self.new,text="ok",command=self.Holstore)
		self.hol_ok.place(x=300,y=350,anchor=CENTER)
		self.hol_back=Button(self.new,text="Back",comman=self.eventback)
		self.hol_back.place(x=500,y=350,anchor=CENTER)

	def Holstore(self):
		# store the values of holiday in the database
		dater=datetime.date(self.caldata['year_selected'],self.caldata['month_selected'],self.caldata['day_selected'])
		# sql query
		conn.execute("CREATE TABLE IF NOT EXISTS HolidayEvent(name Text,day Date)")
		query="INSERT INTO HolidayEvent(name,day) VALUES(?,?)"
		parm=(self.hday.get(),dater);
		if(conn.execute(query,parm)):
			db.commit()
			tk.messagebox.showinfo("Noted","Event Registered")
			self.new.destroy()
			self.arg.destroy()
			root.deiconify()
	
	def on_closing(self):
		self.arg.destroy()
		root.deiconify()

	def eventback(self):
		self.new.destroy()
		self.arg.deiconify()
	
		
	def calen(self):
		child=Toplevel()
		cal=calend(child,self.caldata)

	def on_bclose(self):
		self.new.destroy()
		self.arg.destroy()
		root.deiconify()

	def Birthday(self):
		# Birthday tab
		self.arg.withdraw()
		self.new=Tk()
		self.new.protocol("WM_DELETE_WINDOW",self.on_bclose)
		# window size
		self.new.geometry('800x800')
		self.new.title("select")
		self.name_of_bevent=Label(self.new,text='Name of your friend')
		self.name_of_bevent.place(x=400,y=200,anchor=CENTER)
		self.bday=Entry(self.new)
		self.bday.place(x=400,y=250,anchor=CENTER)
		self.date_of_bevent=Button(self.new,text='Date',command=self.calen)
		self.date_of_bevent.place(x=400,y=300,anchor=CENTER)
		self.dd=Entry(self.arg)
		self.bir_label=Label(self.new,text="description")
		self.bir_label.place(x=400,y=350,anchor=CENTER)
		self.bir_desc=Text(self.new,height=10)
		self.bir_desc.place(x=400,y=450,anchor=CENTER)
		self.bir_ok=Button(self.new,text="ok",command=self.Birstore)
		self.bir_ok.place(x=300,y=600,anchor=CENTER)
		self.bir_back=Button(self.new,text="Back",command=self.eventback)
		self.bir_back.place(x=600,y=600,anchor=CENTER)

	def Birstore(self):
		# store the values of birthday in the database
		day=str(self.caldata['day_selected'])
		month=str(self.caldata['month_selected'])
		if(len(day)==1):
			day="0"+day
		if(len(month)==1):
			month="0"+month
		dayt=day+"-"+month
		# sql query
		conn.execute("CREATE TABLE IF NOT EXISTS BirthdayEvent(name Text,day Text,year Text,description Text)")
		if(conn.execute("INSERT INTO BirthdayEvent VALUES(?,?,?,?);",(self.bday.get(),dayt,self.caldata['year_selected'],self.bir_desc.get("1.0",END).strip()))):
			db.commit()
			tk.messagebox.showinfo("Noted","Event Registered")
			self.new.destroy()
			self.arg.destroy()
			root.deiconify()
	

if __name__ == '__main__':
	class Base:

		def __init__(self,parent):
			# Main event(front tab)
			self.parent=parent
			self.parent.geometry("600x600")
			self.parent.title("Reminder")
			self.create_event=Button(self.parent,text='Create Event',command=self.Create)
			self.import_event=Button(self.parent,text='Import Event',command=self.ImportEvent)
			self.quit=Button(self.parent,text='Quit',command=self.Quit)
			self.create_event.place(x=300,y=200,anchor=CENTER)
			self.import_event.place(x=300,y=250,anchor=CENTER)
			self.quit.place(x=300,y=300,anchor=CENTER)

		def Create(self):
			self.parent.withdraw()
			crat=CreateEvent()

		def ImportEvent(self):
			self.parent.withdraw()
			filename=filedialog.askopenfilename()
			try:
				# file permission
				g=open(filename,'rb')
				gcal=Calendar.from_ical(g.read())
			except:
				self.parent.deiconify()
				return
			for component in gcal.walk():
				if component.name == "VEVENT":
					cmpr = str(component.get('DTSTART').dt)
					cmpdate = cmpr[:11]
					year,month,day = cmpdate.strip().split("-")
					dayt = day+"-"+month
					dater = datetime.date(int(year),int(month),int(day))
					# 	if(component.get('Name') and component.get('DESCRIPTION')):
					# 		conn.execute("CREATE TABLE IF NOT EXISTS BirthdayEvent(name Text,day Text,year Text,description Text)")
					# 		if(conn.execute("INSERT INTO BirthdayEvent VALUES(?,?,?);",(component.get('name'),dayt,year,component.get('DESCRIPTION')))):
					# 			db.commit()
					if(component.get('DESCRIPTION') and component.get('SUMMARY')):
						conn.execute("CREATE TABLE IF NOT EXISTS HolidayEvent(name Text,day Date)")
						if(conn.execute("INSERT INTO HolidayEvent VALUES(?,?);",(component.get('SUMMARY'),dater))):
							db.commit()
					# 	else:
					# 		pass
					# else:
					# 	if(not component.get('DESCRIPTION')):
					# 		if(component.get('SUMMARY')):
					# 			conn.execute("CREATE TABLE IF NOT EXISTS BirthdayEvent(name Text,day Text,year Text)")
					# 			if(conn.execute("INSERT INTO BirthdayEvent VALUES(?,?,?);",(component.get('SUMMARY'),dayt,year)):
					# 				db.commit()
			tk.messagebox.showinfo("Noted","Event imported")
			self.parent.deiconify()

		def Quit(self):
			self.parent.destroy()


root = Tk()
app = Base(root)
root.mainloop()

	
		