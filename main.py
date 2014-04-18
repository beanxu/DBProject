import sys
import wx
import sqlite3
from hashlib import md5

class LoginDialog(wx.Frame):
    def __init__(self, parent, id=-1, title='Login',
            pos = wx.DefaultPosition,
            size = (300, 160),
            text = 'Please type your username and password:',
            username = ''):

        wx.Frame.__init__(self, parent, id, title, pos, size)
        bkg = wx.Panel(self)
        self.myText = wx.StaticText(bkg, -1, text, pos = (15, 5))
        wx.StaticText(bkg, -1, 'Username:', pos = (50, 30))
        wx.StaticText(bkg, -1, 'Password:', pos = (50, 55))
        self.nameBox = wx.TextCtrl(bkg, -1, '', 
                pos = (120, 30), 
                size = (120, -1))
        self.passwordBox = wx.TextCtrl(bkg, -1, '', 
                pos = (120, 55), 
                size = (120, -1),
                style = wx.TE_PASSWORD)
        wx.Button(bkg, wx.ID_OK, 'OK', 
                pos = (35, 90), 
                size = wx.DefaultSize).SetDefault()
        wx.Button(bkg, wx.ID_CANCEL, 'Cancel',
                pos = (165, 90),
                size = wx.DefaultSize)
        self.status = self.CreateStatusBar()
        #bkg.SetSizer()

    def halt(self, event):
        sys.exit()

    def getV(self, event):
        username = self.nameBox.GetValue()
        password = self.passwordBox.GetValue()
        if username == '':
            self.status.SetStatusText('Username cannot be empty!')
            return
        if password == '':
            self.status.SetStatusText('Password cannot be empty!')
            return
        password = md5(password).hexdigest()
        try:
            curs.execute('SELECT pw FROM admin WHERE name="'
                    + username + '"')
            if password == curs.fetchall()[0][0]:
                global rootID 
                rootID = username
                win_init.SetMenuBar(menubar)
                win_init.Show()
                self.Close()
            else:
                self.status.SetStatusText('Username/password is incorrect!')
        except IndexError:
            self.status.SetStatusText('Username/password is incorrect!')

class AddUserFrame(wx.Frame):
    def __init__(self, parent, id=-1, title='Add User',
            pos = wx.DefaultPosition,
            size = (320, 250),
            text = 'Create a super user:'):
        wx.Frame.__init__(self, parent, id, title, pos, size)
        bkg = wx.Panel(self)
        hint = wx.StaticText(bkg, -1, text)
        userHint = wx.StaticText(bkg, -1, 'Username:')
        pwHint =  wx.StaticText(bkg, -1 ,'Password:')
        nameHint = wx.StaticText(bkg, -1, 'Real name:')
        telHint = wx.StaticText(bkg, -1, 'Telephone:')
        self.username = wx.TextCtrl(bkg)
        self.password = wx.TextCtrl(bkg, style = wx.TE_PASSWORD)
        self.realname = wx.TextCtrl(bkg)
        self.tel = wx.TextCtrl(bkg)
        self.okBtn = wx.Button(bkg, wx.ID_OK, label = 'OK')
        self.okBtn.SetDefault()
        self.cancelBtn = wx.Button(bkg, wx.ID_CANCEL, label = 'Cancel')
        self.status = wx.StatusBar(bkg)
        hbox1 = wx.BoxSizer()
        hbox1.Add(userHint, flag = wx.EXPAND)
        hbox1.Add(self.username, flag = wx.ALIGN_CENTER | wx.LEFT, border = 2)
        hbox2 = wx.BoxSizer()
        hbox2.Add(pwHint, flag = wx.EXPAND)
        hbox2.Add(self.password, flag = wx.ALIGN_CENTER | wx.LEFT, border = 2)
        hbox3 = wx.BoxSizer()
        hbox3.Add(nameHint, flag = wx.EXPAND)
        hbox3.Add(self.realname, flag = wx.ALIGN_CENTER | wx.LEFT, border = 2)
        hbox4 = wx.BoxSizer()
        hbox4.Add(telHint, flag = wx.EXPAND)
        hbox4.Add(self.tel, flag = wx.ALIGN_CENTER | wx.LEFT, border = 2)
        hbox5 = wx.BoxSizer()
        hbox5.Add(self.okBtn)
        hbox5.Add(self.cancelBtn)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hint, flag = wx.EXPAND | wx.ALL, border = 5)
        vbox.Add(hbox1, flag = wx.ALIGN_CENTER | wx.ALL, border = 5)
        vbox.Add(hbox2, flag = wx.ALIGN_CENTER | wx.ALL, border = 5)
        vbox.Add(hbox3, flag = wx.ALIGN_CENTER | wx.ALL, border = 5)
        vbox.Add(hbox4, flag = wx.ALIGN_CENTER | wx.ALL, border = 5)
        vbox.Add(hbox5, flag = wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.ALL,
                border = 15)
        vbox.Add(self.status, flag = wx.EXPAND, border = 5)
        bkg.SetSizer(vbox)

    def onOK(self, event):
        if not self.username.GetValue():
            self.status.SetStatusText('Username cannot be empty!')
        elif not self.password.GetValue():
            self.status.SetStatusText('Password cannot be empty!')
        else:
            curs.execute('SELECT name FROM admin')
            flag = True
            for i in curs.fetchall():
                if i[0] == self.username.GetValue():
                    flag = False
                    break
            if flag:
                self.status.SetStatusText('Adding...')
                curs.execute('INSERT INTO admin VALUES (?, ?, ?, ?)',
                            [   self.username.GetValue(),
                                md5(self.password.GetValue()).hexdigest(),
                                self.realname.GetValue(),
                                self.tel.GetValue()  ])
                conn.commit()
                success = wx.MessageDialog(self, 'Done!', 'Success', wx.OK)
                success.ShowModal()
                success.Destroy()
                self.Close()
            else:
                self.status.SetStatusText('Username has already existed!')

    def onCancel(self, event):
        self.Close()

class AddCardFrame(wx.Frame):
    def __init__(self, parent, id=-1, title='Add Card',
            pos = wx.DefaultPosition,
            size = (320, 250),
            text = 'Create a new card:'):
        wx.Frame.__init__(self, parent, id, title, pos, size)
        bkg = wx.Panel(self)
        hint = wx.StaticText(bkg, -1, text)
        idHint = wx.StaticText(bkg, -1, 'Card ID:      ')
        nameHint = wx.StaticText(bkg, -1, 'Username:   ')
        dptmHint = wx.StaticText(bkg, -1, 'Department:')
        typeHint = wx.StaticText(bkg, -1, 'Type:           ')
        self.cardid = wx.TextCtrl(bkg)
        self.username = wx.TextCtrl(bkg)
        self.dptm = wx.TextCtrl(bkg)
        self.cardtype = wx.ComboBox(bkg, -1, choices = ['Teacher', 'Student'],
                style = wx.CB_READONLY)
        self.okBtn = wx.Button(bkg, wx.ID_OK, label = 'OK')
        self.okBtn.SetDefault()
        self.cancelBtn = wx.Button(bkg, wx.ID_CANCEL, label = 'Cancel')
        self.status = wx.StatusBar(bkg)
        hbox1 = wx.BoxSizer()
        hbox1.Add(idHint, flag = wx.EXPAND)
        hbox1.Add(self.cardid, flag = wx.ALIGN_CENTER | wx.LEFT, border = 2)
        hbox2 = wx.BoxSizer()
        hbox2.Add(nameHint, flag = wx.EXPAND)
        hbox2.Add(self.username, flag = wx.ALIGN_CENTER | wx.LEFT, border = 2)
        hbox3 = wx.BoxSizer()
        hbox3.Add(dptmHint, flag = wx.EXPAND)
        hbox3.Add(self.dptm, flag = wx.ALIGN_CENTER | wx.LEFT, border = 2)
        hbox4 = wx.BoxSizer()
        hbox4.Add(typeHint, flag = wx.EXPAND)
        hbox4.Add(self.cardtype, flag = wx.ALIGN_CENTER | wx.LEFT, border = 2)
        hbox5 = wx.BoxSizer()
        hbox5.Add(self.okBtn)
        hbox5.Add(self.cancelBtn)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hint, flag = wx.EXPAND | wx.ALL, border = 5)
        vbox.Add(hbox1, flag = wx.ALIGN_CENTER | wx.ALL, border = 5)
        vbox.Add(hbox2, flag = wx.ALIGN_CENTER | wx.ALL, border = 5)
        vbox.Add(hbox3, flag = wx.ALIGN_CENTER | wx.ALL, border = 5)
        vbox.Add(hbox4, flag = wx.ALIGN_CENTER | wx.ALL, border = 5)
        vbox.Add(hbox5, flag = wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.ALL,
                 border = 15)
        vbox.Add(self.status, flag = wx.EXPAND, border = 5)
        bkg.SetSizer(vbox)

    def onOK(self, event):
        if not self.cardid.GetValue():
            self.status.SetStatusText('Card ID cannot be empty!')
        elif not self.username.GetValue():
            self.status.SetStatusText('Username cannot be empty!')
        else:
            ID = self.cardid.GetValue()
            curs.execute('SELECT cid FROM card WHERE cid="'+ID+'"')
            try:
                if curs.fetchall()[0][0] == ID:
                    self.status.SetStatusText('Card has already existed!')
            except IndexError:
                self.status.SetStatusText('Adding...')
                curs.execute('INSERT INTO card VALUES (?,?,?,?)',
                        [   ID,
                            self.username.GetValue(),
                            self.dptm.GetValue(),
                            self.cardtype.GetValue()    ])
                conn.commit()
                msg = wx.MessageDialog(self, 'Done!', 'Success', wx.OK)
                msg.ShowModal()
                msg.Destroy()
                self.Close()

    def onCancel(self, event):
        self.Close()

class BookAddFrame(wx.Frame):
    def __init__(self, parent, id=-1, title='Add Book',
            pos = wx.DefaultPosition,
            size = (410, 335)):
        wx.Frame.__init__(self, parent, id, title, pos, size)
        bkg = wx.Panel(self)
        self.openBtn = wx.Button(bkg, -1, 'Open')
        self.openBtn.SetDefault()
        self.addBtn = wx.Button(bkg, -1, 'Add')
        self.filename = wx.TextCtrl(bkg)
        self.contents = wx.TextCtrl(bkg)
        hbox = wx.BoxSizer()
        hbox.Add(self.filename, proportion = 1, flag = wx.EXPAND)
        hbox.Add(self.openBtn, proportion = 0, flag = wx.LEFT, border = 5)
        hbox.Add(self.addBtn, proportion = 0, flag = wx.LEFT, border = 5)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox, proportion = 0, flag = wx.EXPAND | wx.ALL, border = 5)
        vbox.Add(self.contents, proportion = 1,
                flag = wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border = 5)
        bkg.SetSizer(vbox)
        
    def openFile(self, event):
        try:
            f = open(self.filename.GetValue())
            self.contents.SetValue(f.read())
            f.close()
        except:
            pass
    
    def loadBook(self, event):
        totalClash = 0
        for line in self.contents.GetValue().splitlines():
            a = line.strip(' ()').split(', ')
            curs.execute('SELECT * FROM book WHERE isbn="'+a[0]+'"')
            result = curs.fetchall()
            try:
                if result[0][0] == a[0]:
                    #TODO
                    if  a[1]!=result[0][1] or \
                        a[2]!=result[0][2] or \
                        a[3]!=result[0][3] :
                            totalClash = totalClash + 1
                            msg = wx.MessageDialog(self, 
                                    'Error: '+a[0]+' has a clash!',
                                    'Error', wx.OK)
                            msg.ShowModal()
                            msg.Destroy()
                    else:
                        curs.execute('UPDATE book SET total=total+'+
                                a[7]+' WHERE isbn="'+a[0]+'"')
                        curs.execute('UPDATE book SET remain=remain+'+
                                a[7]+' WHERE isbn="'+a[0]+'"')
            except (TypeError, IndexError):
                curs.execute('INSERT INTO book VALUES (?,?,?,?,?,?,?,?,?)', 
                    [   a[0], a[1], a[2], a[3], 
                        int(a[4]), 
                        a[5], 
                        float(a[6]), 
                        int(a[7]), int(a[7])    ])
        conn.commit()
        msg = wx.MessageDialog(self, 'Done! ('+str(totalClash)+' clash(es))',
                'Success', wx.OK)
        msg.ShowModal()
        msg.Destroy()
        self.Close()

class SearchFrame(wx.Frame):
    def __init__(self, parent, id=-1, title='Search Books',
            pos = wx.DefaultPosition,
            size = (730, 500)):
        wx.Frame.__init__(self, parent, id, title, pos, size)
        bkg = wx.Panel(self)
        typeHint = wx.StaticText(bkg, -1, 'Type:')
        titleHint = wx.StaticText(bkg, -1, 'Title:')
        pubHint = wx.StaticText(bkg, -1, 'Publisher:')
        yearHint = wx.StaticText(bkg, -1, 'Year:')
        authorHint = wx.StaticText(bkg, -1, 'Author:')
        priceHint = wx.StaticText(bkg, -1, 'Price:')
        toHint0 = wx.StaticText(bkg, -1, '--')
        toHint = wx.StaticText(bkg, -1, '--')
        self.typ = wx.TextCtrl(bkg)
        self.tit = wx.TextCtrl(bkg)
        self.pub = wx.TextCtrl(bkg)
        self.yearB = wx.TextCtrl(bkg)
        self.yearE = wx.TextCtrl(bkg)
        self.aut = wx.TextCtrl(bkg) 
        self.priceB = wx.TextCtrl(bkg)
        self.priceE = wx.TextCtrl(bkg)
        hbox1 = wx.BoxSizer()
        hbox1.Add(typeHint, proportion = 2)
        hbox1.Add(self.typ, proportion = 2, flag = wx.EXPAND, border = 5)
        hbox1.Add(titleHint, proportion = 2, flag = wx.LEFT, border = 50)
        hbox1.Add(self.tit, proportion = 2, flag = wx.EXPAND, border = 5)
        hbox1.Add(yearHint, proportion = 2, flag = wx.LEFT, border = 50)
        hbox1.Add(self.yearB, proportion = 1, flag = wx.EXPAND, border = 5)
        hbox1.Add(toHint0, proportion = 0)
        hbox1.Add(self.yearE, proportion = 1, flag = wx.EXPAND, border = 5)
        hbox2 = wx.BoxSizer()
        hbox2.Add(pubHint, proportion = 2)
        hbox2.Add(self.pub, proportion = 2, flag = wx.EXPAND, border = 5)
        hbox2.Add(authorHint, proportion = 2, flag = wx.LEFT, border = 50)
        hbox2.Add(self.aut, proportion = 2, flag = wx.EXPAND, border = 5)
        hbox2.Add(priceHint, proportion = 2, flag = wx.LEFT, border = 50)
        hbox2.Add(self.priceB, proportion = 1, flag = wx.EXPAND, border = 5)
        hbox2.Add(toHint, proportion = 0)
        hbox2.Add(self.priceE, proportion = 1, flag = wx.EXPAND, border = 5)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox1, proportion = 0, flag = wx.EXPAND | wx.ALL, border = 5)
        vbox.Add(hbox2, proportion = 0, flag = wx.EXPAND | wx.ALL, border = 5)
        self.l = wx.ListCtrl(bkg, -1, style = wx.LC_REPORT)
        self.l.InsertColumn(0, 'ISBN')
        self.l.InsertColumn(1, 'Type')
        self.l.InsertColumn(2, 'Title')
        self.l.InsertColumn(3, 'Publisher')
        self.l.InsertColumn(4, 'Year')
        self.l.InsertColumn(5, 'Author')
        self.l.InsertColumn(6, 'Price')
        self.l.InsertColumn(7, 'Total')
        self.l.InsertColumn(8, 'Remain')
        vbox.Add(self.l, proportion = 1, flag = wx.EXPAND | wx.ALL, border = 5)
        self.searchBtn = wx.Button(bkg, -1, 'Search')
        self.searchBtn.SetDefault()
        vbox.Add(self.searchBtn, proportion = 0, flag = wx.ALIGN_RIGHT | wx.ALL,
                border = 5)
        bkg.SetSizer(vbox)

    def work(self, event):
        self.l.DeleteAllItems()

        kind = self.typ.GetValue()
        title = self.tit.GetValue()
        publisher = self.pub.GetValue()
        author = self.aut.GetValue()
        yFrom = self.yearB.GetValue()
        yTo = self.yearE.GetValue()
        pFrom = self.priceB.GetValue()
        pTo = self.priceE.GetValue()
        
        query = 'SELECT * FROM book '
        where = ''
        if kind:
            where = 'WHERE type="'+kind+'"'
        if title:
            if where:
                where = where + ' AND '
            else:
                where = 'WHERE '
            where = where+'title="'+title+'"'
        if publisher:
            if where:
                where = where + ' AND '
            else:
                where = 'WHERE '
            where = where+'pub="'+publisher+'"'
        if author:
            if where:
                where = where + ' AND '
            else:
                where = 'WHERE '
            where = where+'author="'+author+'"'
        if yFrom:
            if where:
                where = where + ' AND '
            else:
                where = 'WHERE '
            where = where+'year>='+yFrom
        if yTo:
            if where:
                where = where + ' AND '
            else:
                where = 'WHERE '
            where = where+'year<='+yTo
        if pFrom:
            if where:
                where = where + ' AND '
            else:
                where = 'WHERE '
            where = where+'price>='+pFrom
        if pTo:
            if where:
                where = where + ' AND '
            else:
                where = 'WHERE '
            where = where+'price<='+pTo

        curs.execute(query+where+' LIMIT 50')
        for line in curs.fetchall():
            num = self.l.GetItemCount()
            self.l.InsertStringItem(num, line[0])
            for (no, i) in zip(range(9), line):
                self.l.SetStringItem(num, no, str(i))


class BookBorrowed(wx.Frame):
    def __init__(self, card, parent, id=-1, title='Borrowed',
            pos = wx.DefaultPosition,
            size = (550,355),
            text = 'This user has borrowed:'):
        wx.Frame.__init__(self, parent, id, title+'('+card+')', pos, size)
        bkg = wx.Panel(self)
        hint = wx.StaticText(bkg, -1, text)
        l = wx.ListCtrl(bkg, -1, style = wx.LC_REPORT)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hint, proportion = 0, flag = wx.ALL, border = 5)
        vbox.Add(l, proportion = 1, flag = wx.EXPAND | wx.ALL, border = 5)
        l.InsertColumn(0, 'ISBN')
        l.InsertColumn(1, 'Title')
        l.InsertColumn(2, 'Borrowed Date')
        l.InsertColumn(3, 'Return before')
        l.InsertColumn(4, 'Administrator')
        l.SetColumnWidth(2, 150)
        l.SetColumnWidth(3, 150)
        curs.execute('''SELECT isbn, dateb, ddl, aid FROM borrow 
                        WHERE cid="'''+card+'" AND dater="NR"')
        records = curs.fetchall()
        for record in records:
            curs.execute('SELECT title FROM book WHERE isbn="'+record[0]+'"')
            num = l.GetItemCount()
            l.InsertStringItem(num, record[0])
            l.SetStringItem(num, 1, curs.fetchone()[0])
            l.SetStringItem(num, 2, record[1])
            l.SetStringItem(num, 3, record[2])
            l.SetStringItem(num, 4, record[3])

        bkg.SetSizer(vbox)


class BookOutFrame(wx.Frame):
    def __init__(self, parent, id=-1, title='Borrow Books',
            pos = wx.DefaultPosition,
            size = (310, 160),
            text = 'Please type CardID and ISBN to borrow books: ',
            btnText = 'Borrow'):
        wx.Frame.__init__(self, parent, id, title, pos, size)
        bkg = wx.Panel(self)
        wx.StaticText(bkg, -1, text, pos = (5, 5))
        wx.StaticText(bkg, -1, 'Card ID:', pos = (50, 30))
        wx.StaticText(bkg, -1, 'ISBN:', pos = (50, 55))
        self.cardid = wx.TextCtrl(bkg, -1, '',
                pos = (120, 30),
                size = (120, -1))
        self.isbn = wx.TextCtrl(bkg, -1, '',
                pos = (120, 55),
                size = (120, -1))
        self.btn = wx.Button(bkg, -1, btnText, pos = (180, 90))
        self.btn.SetDefault()
        self.status = self.CreateStatusBar()

    def work(self, event):
        cid = self.cardid.GetValue()
        if cid == '':
            self.status.SetStatusText('CardID cannot be empty!')
        else:
            curs.execute('SELECT cid, name FROM card WHERE cid="'+cid+'"')
            try:
                card = curs.fetchone()
                if card[0] == cid:
                    bid = self.isbn.GetValue()
                    if bid == '':
                        borrowed = BookBorrowed(cid, self)
                        borrowed.Show()
                        return
                    else:
                        curs.execute('''SELECT isbn, remain, title
                                        FROM book 
                                        WHERE isbn="'''+bid+'"')
                        book = curs.fetchone()
                        try:
                            if book[0] == bid:
                                curs.execute('''SELECT isbn 
                                FROM borrow
                                WHERE isbn="'''+bid+'" AND dater="NR"'
                                + ' AND cid="'+cid+'"')
                                try:
                                    if curs.fetchone()[0]:
                                        self.status.SetStatusText('You have \
borrowed a same book and have not returned!')
                                        return
                                except (TypeError, IndexError):
                                    pass
                                if book[1] > 0:
                                    curs.execute('''UPDATE book
                                    SET remain=remain-1
                                    WHERE isbn="'''+bid+'"')
                                    
                                    timenow = curs.execute('''SELECT
                                    datetime('now')''').fetchone()[0]
                                    timertn = curs.execute('''SELECT
                                    datetime('now','+1 month')''').fetchone()[0]

                                    curs.execute('''INSERT INTO borrow
                                    VALUES (?,?,?,?,?,?)''',
                                    [   cid, bid, timenow, 
                                        timertn, 'NR', rootID   ])

                                    conn.commit()
                                    msg = wx.MessageDialog(self, 
                                            timenow+': '+card[1]+' borrowed '+
                                            book[2]+' successfully!',
                                            'Success', wx.OK)
                                    msg.ShowModal()
                                    msg.Destroy()
                                    self.Close()
                                else:
                                    curs.execute('''SELECT ddl
                                    FROM borrow
                                    WHERE isbn="'''+bid+'" AND dater="NR"'+
                                    " ORDER BY ddl")
                                    ddl = curs.fetchone()[0]
                                    msg = wx.MessageDialog(self,
                                            book[2]+' is not available until '
                                            +ddl+'!', 'Unsuccess', wx.OK)
                                    msg.ShowModal()
                                    msg.Destroy()

                        except (TypeError, IndexError):# Exception, e:
                            #print e
                            self.status.SetStatusText('ISBN dose not exist!')
            except (TypeError, IndexError):# Exception, e:
                #print e
                self.status.SetStatusText('CardID dose not exist!')

class BookBackFrame(BookOutFrame):
    def __init__(self, parent, id=-1, title='Return Books',
            pos = wx.DefaultPosition,
            size = (300, 160),
            text = 'Please type CardID and ISBN to return books:',
            btnText = 'Return'):
        BookOutFrame.__init__(self, parent, id, 
                title, pos, size, text, btnText)

    def work(self, event):
        cid = self.cardid.GetValue()
        if cid == '':
            self.status.SetStatusText('CardID cannot be empty!')
        else:
            curs.execute('SELECT cid, name FROM card WHERE cid="'+cid+'"')
            try:
                card = curs.fetchone()
                if card[0] == cid:
                    bid = self.isbn.GetValue()
                    if bid == '':
                        borrowed = BookBorrowed(cid, self)
                        borrowed.Show()
                        return
                    curs.execute('''SELECT isbn, title
                                    FROM book
                                    WHERE isbn="'''+bid+'"')
                    book = curs.fetchone()
                    try:
                        if book[0] == bid:
                            pass
                    except (TypeError, IndexError):
                        self.status.SetStatusText('ISBN does not exist!')
                        return

                    curs.execute('''SELECT isbn
                                    FROM borrow
                                    WHERE isbn="'''+bid+'" AND dater="NR"'
                                    +' AND cid="'+cid+'"')
                    try:
                        if curs.fetchone()[0] == bid:
                            timenow = curs.execute('SELECT \
                                    datetime("now")').fetchone()[0]
                            curs.execute('''UPDATE borrow
                            SET dater="'''+timenow+'''"
                            WHERE isbn="'''+bid+'" AND dater="NR"'
                            +' AND cid="'+cid+'"')
                            curs.execute('''UPDATE book
                            SET remain=remain+1
                            WHERE isbn="'''+bid+'"')
                            conn.commit()
                            msg = wx.MessageDialog(self, 
                                    timenow+': '+card[1]+' returned '+book[1]
                                    +' successfully!', 'Success', wx.OK)
                            msg.ShowModal()
                            msg.Destroy()
                            self.Close()
                    except (TypeError, IndexError): #Exception, e:
                        self.status.SetStatusText('You have not borrowed \
(or have returned) this book!')
            except (TypeError, IndexError):
                self.status.SetStatusText('CardID dose not exist!')

class DelCardFrame(wx.Frame):
    def __init__(self, parent, id=-1, title='Delete Card',
            pos = wx.DefaultPosition,
            size = (300, 160),
            text = 'Please type the CardID:'):
        wx.Frame.__init__(self, parent, id, title, pos, size)
        bkg = wx.Panel(self)
        wx.StaticText(bkg, -1, text, pos = (15, 5))
        wx.StaticText(bkg, -1, 'Card ID:', pos = (50, 45))
        self.cardid = wx.TextCtrl(bkg, -1, pos = (120, 45), size = (120, -1))
        self.delBtn = wx.Button(bkg, -1, 'Delete', pos = (165, 85))
        self.delBtn.SetDefault()
        self.status = self.CreateStatusBar()

    def delete(self, event):
        cid = self.cardid.GetValue()
        if cid == '':
            self.status.SetStatusText('CardID cannot be empty!')
        else:
            curs.execute('SELECT cid FROM card WHERE cid="'+cid+'"')
            try:
                if curs.fetchone()[0] == cid:
                    curs.execute('SELECT cid FROM borrow WHERE cid="'+cid+'"'
                            +' AND dater="NR"')
                    try:
                        if curs.fetchone()[0] == cid:
                            self.status.SetStatusText(cid+' still have book(s) not returned!')
                    except (TypeError, IndexError):
                        curs.execute('DELETE FROM card WHERE cid="'+cid+'"')
                        conn.commit()
                        msg = wx.MessageDialog(self, cid+' has been deleted!', 'Success', wx.OK)
                        msg.ShowModal()
                        msg.Destroy()
                        self.Close()
            except (TypeError, IndexError):
                self.status.SetStatusText('CardID dose not exist!')

def bookBack(event):
    #TODO
    back = BookBackFrame(None)
    back.btn.Bind(wx.EVT_BUTTON, back.work)
    back.Show()

def bookOut(event):
    #TODO
    out = BookOutFrame(None)
    out.btn.Bind(wx.EVT_BUTTON, out.work)
    out.Show()

def search(event):
    search = SearchFrame(None)
    search.searchBtn.Bind(wx.EVT_BUTTON, search.work)
    search.Show()

def bookAdd(event):
    add = BookAddFrame(None)
    add.openBtn.Bind(wx.EVT_BUTTON, add.openFile)
    add.addBtn.Bind(wx.EVT_BUTTON, add.loadBook)
    add.Show()

def addUser(event):
    print rootID
    add = AddUserFrame(None)
    add.Bind(wx.EVT_BUTTON, add.onOK, id = wx.ID_OK)
    add.Bind(wx.EVT_BUTTON, add.onCancel, id = wx.ID_CANCEL)
    add.Show()

def addCard(event):
    add = AddCardFrame(None)
    add.Bind(wx.EVT_BUTTON, add.onOK, id = wx.ID_OK)
    add.Bind(wx.EVT_BUTTON, add.onCancel, id = wx.ID_CANCEL)
    add.Show()

def delCard(event):
    delU = DelCardFrame(None)
    delU.delBtn.Bind(wx.EVT_BUTTON, delU.delete)
    delU.Show()

def exit(event):
    conn.close()
    init.Exit()

rootID = 'unknown'

conn = sqlite3.connect('lib.db')
curs = conn.cursor()
#querySelectAdmin = 'SELECT pw FROM admin '

init = wx.App()
win_init = wx.Frame(None, title = 'Library System  By Ketian XU',
        size = (320, 250))

menubar = wx.MenuBar()
advanced = wx.Menu()
advanced.Append(101, '&Add Superuser', 'Add an adiministrator')
advanced.Append(102, '&Delete Card', 'Delete a card')
menubar.Append(advanced, '&Advanced')
win_init.Bind(wx.EVT_MENU, addUser, id=101)
win_init.Bind(wx.EVT_MENU, delCard, id=102)

bkg = wx.Panel(win_init)

bookBackBtn = wx.BitmapButton(bkg, -1, wx.Bitmap('icons/bookback.png'))
bookOutBtn = wx.BitmapButton(bkg, -1, wx.Bitmap('icons/bookout.png'))
searchBtn = wx.BitmapButton(bkg, -1, wx.Bitmap('icons/search.png'))
bookAddBtn = wx.BitmapButton(bkg, -1, wx.Bitmap('icons/bookadd.png'))
addCardBtn = wx.BitmapButton(bkg, -1, wx.Bitmap('icons/addCard.png'))
exitBtn = wx.BitmapButton(bkg, -1, wx.Bitmap('icons/exit.png'))

hbox1 = wx.BoxSizer()
hbox1.Add(bookBackBtn, flag = wx.ALIGN_CENTER | wx.ALL, border = 9)
hbox1.Add(bookOutBtn, flag = wx.ALIGN_CENTER | wx.ALL, border = 9)
hbox1.Add(searchBtn, flag = wx.ALIGN_CENTER | wx.ALL, border = 9)
hbox2 = wx.BoxSizer()
hbox2.Add(bookAddBtn, flag = wx.ALIGN_CENTER | wx.ALL, border = 9)
hbox2.Add(addCardBtn, flag = wx.ALIGN_CENTER | wx.ALL, border = 9)
hbox2.Add(exitBtn, flag = wx.ALIGN_CENTER | wx.ALL, border = 9)
vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox1, flag = wx.ALIGN_CENTER | wx.UP, border = 15)
vbox.Add(hbox2, flag = wx.ALIGN_CENTER | wx.UP, border = 10)
bkg.SetSizer(vbox)
bookBackBtn.Bind(wx.EVT_BUTTON, bookBack)
bookOutBtn.Bind(wx.EVT_BUTTON, bookOut)
searchBtn.Bind(wx.EVT_BUTTON, search)
bookAddBtn.Bind(wx.EVT_BUTTON, bookAdd)
addCardBtn.Bind(wx.EVT_BUTTON, addCard)
exitBtn.Bind(wx.EVT_BUTTON, exit)
win_init.Hide()

login = LoginDialog(win_init)
login.Bind(wx.EVT_BUTTON, login.getV, id=wx.ID_OK)
login.Bind(wx.EVT_BUTTON, login.halt, id=wx.ID_CANCEL)
login.Show()

init.MainLoop()
