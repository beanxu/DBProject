import wx
import sqlite3
import os
import sys
from hashlib import md5

def exit(event):
    sys.exit()

def setup(event):

    #testframe = wx.Frame(None, -1, 'test')
    #testframe.Show()

    if (not username.GetValue()):
        status.SetStatusText('Username cannot be empty!')
        return
    if (not password.GetValue()):
        status.SetStatusText('Password cannot be empty!')
        return
    try:
        os.remove('lib.db')
    except OSError:
        pass
    status.SetStatusText('Initializing...')

    conn = sqlite3.connect('lib.db')
    curs = conn.cursor()

    curs.execute('''
    CREATE TABLE book (
        isbn    TEXT    PRIMARY KEY,
        type    TEXT,
        title   TEXT,
        pub     TEXT,
        year    INT,
        author  TEXT,
        price   FLOAT,
        total   INT,
        remain  INT
    )
    ''')
    curs.execute('''
    CREATE TABLE card (
        cid     TEXT    PRIMARY KEY,
        name    TEXT,
        dptm    TEXT,
        type    TEXT
    )
    ''')
    curs.execute('''
    CREATE TABLE admin (
        name    TEXT    PRIMARY KEY,
        pw      TEXT,
        rName   TEXT,
        tel     TEXT
    )
    ''')
    curs.execute('''
    CREATE TABLE borrow (
        cid     TEXT,
        isbn    TEXT,
        dateb   TEXT    PRIMARY KEY,
        ddl     TEXT,
        dater   TEXT,
        aid     TEXT
    )
    ''')
    
    curs.execute('INSERT INTO admin VALUES (?, ?, ?, ?)', 
                [   username.GetValue(),
                    md5(password.GetValue()).hexdigest(), 
                    realname.GetValue(), tel.GetValue() ])

    conn.commit()
    conn.close()

    win_done = wx.Dialog(None, -1, 'Success', size = (280, 120))
    doneText = wx.StaticText(win_done, -1, 'Done!', pos = (120, 40))
    okBtn = wx.Button(win_done, wx.ID_OK, label = 'OK', pos = (180, 60))
    okBtn.SetDefault()
    okBtn.Bind(wx.EVT_BUTTON, exit)
    win_done.ShowModal()
    win_done.Destroy()

init = wx.App()
win_init = wx.Frame(None, title = 'Library System: Setup   By Ketian XU', 
        size = (320, 250))
bkg = wx.Panel(win_init)

hint = wx.StaticText(bkg, -1, 'Create a super user and initialize the database:')
userHint = wx.StaticText(bkg, -1, 'Username:')
pswdHint = wx.StaticText(bkg, -1, 'Password:')
nameHint = wx.StaticText(bkg, -1, 'Real name:')
telHint = wx.StaticText(bkg, -1, 'Telephone:')

username = wx.TextCtrl(bkg)
password = wx.TextCtrl(bkg, style = wx.TE_PASSWORD)
realname = wx.TextCtrl(bkg)
tel = wx.TextCtrl(bkg)

nextBtn = wx.Button(bkg, label = 'Next')
nextBtn.SetDefault()

status = wx.StatusBar(bkg)

hbox1 = wx.BoxSizer()
hbox1.Add(userHint, flag = wx.EXPAND)
hbox1.Add(username, flag = wx.ALIGN_CENTER | wx.EXPAND | wx.LEFT, border = 2)
hbox2 = wx.BoxSizer()
hbox2.Add(pswdHint, flag = wx.EXPAND)
hbox2.Add(password, flag = wx.ALIGN_CENTER | wx.EXPAND | wx.LEFT, border = 2)
hbox3 = wx.BoxSizer()
hbox3.Add(nameHint, flag = wx.EXPAND)
hbox3.Add(realname, flag = wx.ALIGN_CENTER | wx.EXPAND | wx.LEFT, border = 2)
hbox4 = wx.BoxSizer()
hbox4.Add(telHint, flag = wx.EXPAND)
hbox4.Add(tel, flag = wx.ALIGN_CENTER | wx.EXPAND | wx.LEFT, border = 2)

vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(hint, flag = wx.EXPAND | wx.ALL, border = 5)
vbox.Add(hbox1, flag = wx.ALIGN_CENTER | wx.ALL, border = 5)
vbox.Add(hbox2, flag = wx.ALIGN_CENTER | wx.ALL, border = 5)
vbox.Add(hbox3, flag = wx.ALIGN_CENTER | wx.ALL, border = 5)
vbox.Add(hbox4, flag = wx.ALIGN_CENTER | wx.ALL, border = 5)
vbox.Add(nextBtn, flag =  wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.ALL, border = 15)
vbox.Add(status, flag = wx.EXPAND, border = 5)

bkg.SetSizer(vbox)
win_init.Show()

nextBtn.Bind(wx.EVT_BUTTON, setup)

init.MainLoop()

