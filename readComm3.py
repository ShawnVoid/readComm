from tkinter import *
import tkinter as tk
import time
import threading
import base64
import os
import requests
from bs4 import BeautifulSoup
import tkinter.messagebox as messagebox


class Application(tk.Tk):
	def __init__(self):
		super().__init__()		
		self.createUI()

	# 生成界面
	def createUI(self):
		self.text = tk.Text(self,font=('微软雅黑', 9, 'normal'))
		self.text.place(x=1,y=1)
		tk.Label(self, text="Login ID:").place(x=9,y=328)
		tk.Label(self, text="Password:").place(x=210,y=328)
		self.idInput = tk.Entry(self,width=17)
		self.idInput.place(x=69,y=329)
		self.passInput = tk.Entry(self,width=17, show="*")
		self.passInput.place(x=278,y=329)
		self.buttonSub = tk.Button(self, text='Submit',width=6, borderwidth=1,relief=RIDGE, command=lambda :self.thread_it(self.login))
		self.buttonSub.place(x=428,y=325)
		tk.Button(self, text='Cancel',width=6, borderwidth=1, relief=RIDGE, command=lambda :self.thread_it(self.quit)).place(x=505,y=325)


	# 逻辑：登录
	def login(self):
		self.buttonSub['state'] = DISABLED
		self.text.focus()
		loginID = self.idInput.get()
		password = self.passInput.get()
		data = {'destination': '/ccms-bin/loading.pl?location=%2Findex.html', 
			'credential_0': loginID, 
			'credential_1': password}
		session = requests.Session()
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
		login_url = 'https://www.wblt.ccms.teleperformance.com/auth/LOGIN'
		self.text.insert(tk.END,'登录中...\n')
		resp = session.post(login_url, data, headers)
		try:
			ccms = BeautifulSoup(session.get('https://www.wblt.ccms.teleperformance.com/ccms-bin/home.pl').content.decode('utf-8'),'lxml').find(class_='pmc').find(class_='ident').string
		except:
			messagebox.showinfo('CCMS', 'LoginID或密码错误！')
			os._exit(0)
		url = 'https://www.wblt.ccms.teleperformance.com/ccms-bin/employee/communication.pl?employee_ident='+ccms
		resp = session.get(url)
		html = resp.content.decode('utf-8')
		soup = BeautifulSoup(html, 'lxml')
		if not soup.find(id = 'priority').tbody.find(class_='subject'):
			messagebox.showinfo('CCMS','无未读传讯！')
			os._exit(0)
		list = soup.find(id='priority').tbody.find_all('tr')
		count = 1
		for  item in list:
			if item:
				ident = item.find(class_='ident').string
				itemType = item.find(class_='comm_type').string
				subject = item.find(class_='subject').string
				acknowledge = item.find(class_='ack_by').string
				date = item.find(class_='date_issued').string
				url_ident = 'https://www.wblt.ccms.teleperformance.com/ccms-bin/employee/communication.pl?frmTarget=NEW_COMMUNICATION&employee_ident='+ccms+'&ident='+ident
				url_ident_ack = 'https://www.wblt.ccms.teleperformance.com/ccms-bin/employee/communication.pl?frmTarget=NEW_COMMUNICATION&new_communication=1&employee_ident='+ccms+'&ident='+ident+'&frmOption=ACK'
				if acknowledge == 'N/A':
					session.get(url_ident)
				else:
					session.get(url_ident_ack)
				msgbox = '%d'%count + '.' +subject+'\n'
				self.text.delete(0.0,tk.END)
				self.text.insert(tk.END,msgbox)
				count += 1
		messagebox.showinfo('已读传讯','已读'+'%d'%(count-1)+'条传讯!')


	# 打包进线程（耗时的操作）
	@staticmethod
	def thread_it(func, *args):
		t = threading.Thread(target=func, args=args) 
		t.setDaemon(True)   # 守护--主界面关闭，线程会立刻退出
		t.start()		   # 启动
		# t.join()		  # 阻塞--会卡死界面！
		
		
app = Application()
app.title('CCMS Login')
app.geometry('567x363+%d+%d'%((app.winfo_screenwidth()-567)/2,(app.winfo_screenheight()-363)/2))
app.resizable(False,False)
app.idInput.focus()
img = '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'
tmp = open("tmp.ico","wb+")
tmp.write(base64.b64decode(img))
tmp.close()
app.iconbitmap('tmp.ico')  
os.remove("tmp.ico")  
app.mainloop()
