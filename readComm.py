import requests
from bs4 import BeautifulSoup
from tkinter import *
import tkinter.messagebox as messagebox
import os

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.nameInput = Entry(self)
        self.nameInput.grid(row=0,column=1,padx=10,pady=10)
        self.nameInput2 = Entry(self, show="*")
        self.nameInput2.grid(row=1,column=1,padx=10,pady=10)
        self.label = Label(self, text="LoginID:")
        self.label.grid(row=0,sticky=E)
        self.label2 = Label(self,text="Password:")
        self.label2.grid(row=1,sticky=E)
        self.button =Button(self, text='提交',command=self.login)
        self.button.grid(row=1,column=2, padx=7,pady=7)

    def login(self):
        loginID = self.nameInput.get()
        password = self.nameInput2.get()
        data = {'destination': '/ccms-bin/loading.pl?location=%2Findex.html', 
            'credential_0': loginID, 
            'credential_1': password}
        read(data)

def read(data):
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
    login_url = 'https://www.wblt.ccms.teleperformance.com/auth/LOGIN'
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
    list = soup.find(id='priority').tbody.find_all('tr')
    for  item in list:
        if item:
                ident = item.find(class_='ident').string
                itemType = item.find(class_='comm_type').string
                subject = item.find(class_='subject').string
                date = item.find(class_='date_issued').string
                url_ident = 'https://www.wblt.ccms.teleperformance.com/ccms-bin/employee/communication.pl?frmTarget=NEW_COMMUNICATION&employee_ident='+ccms+'&ident='+ident
                msglist = []
                if session.get(url_ident):
                    msglist.append('Ident: '+ident+' | Type: '+itemType+' | Subject: '+subject+' | Date: '+date)
    try:
        msgbox = ''
        for msg in msglist:
            msgbox = msgbox + msg + '/n'

        messagebox.showinfo('已读传讯', msgbox)
        os._exit(0)
    except:
        messagebox.showinfo('CCMS', '无未读传讯！')
        os._exit(0)


app = Application()
app.master.title('CCMS Login')
app.master.iconbitmap('readComm.ico')
app.mainloop()
