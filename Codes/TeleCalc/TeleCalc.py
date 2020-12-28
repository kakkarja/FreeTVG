# -*- coding: utf-8 -*-
#Copyright (c) 2020, KarjaKAK
#All rights reserved.
#CALCULATOR is built also from the ideas of ❤Yohanes❤

from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog
import datetime as dt
import calendar as cal
from Fixerio import Fixio
from CreatePassword import CreatePassword as cp
from FileFind import filen
import string
import os
import re

class ChoCal:
    """Creating a calendar class"""
    def __init__(self, year = dt.date.today().year , 
                 month =  dt.date.today().month):
        self.year = year
        self.month = month
    
    def createcal(self):
        cld = cal.TextCalendar(firstweekday = 6)
        cld = cld.formatmonth(self.year, self.month, 5).split('\n')[:-1]
        tx = ''
        for i in range(len(cld)):
            if i == 0:
                gemp = re.match(r'\W+', cld[i])
                tx += ''.join(f'{cld[i][gemp.span()[1]:]}\n')
            elif i < len(cld)-1:
                tx += ''.join(f'{cld[i]}\n')
            else:
                tx += ''.join(f'{cld[i]}{" "*(len(cld[1])-len(cld[i]))}')
        return tx

class Calculator():
    LOCK = False
    MAINST = None
    DEST = None
    def __init__(self, root):
        """
        Calculator base on python programming.
           Take Note:
               - For to the power '**'.
               - For divide with no decimal point '//'.
               - The '%' will divide the last number by 100
               - There a saving function for saving calculation as a text file.
               - Load function to load back a calculation file.
               - Edit function, for edit calculated values and also adding note.
               - There a calendar function, 'CAL' key.
               (If you look for interctive calendar, you can see CalGui in
                https//: github.com/kakkarja/CAL)
        """
        self.root = root
        self.mem = ''
        self.ans = 0
        self.cn = ''
        self.idx = 0
        self.ctc = {}
        self.run = True
        self.ops = True
        self.bt = {}
        self.tpl = None
        self.ic = None
        self.rate = None
        self.base = None
        self.root.config(background = 'black')
        self.root.title("TeleCalc")
        self.root.resizable(False,False)
        self.root.protocol('WM_DELETE_WINDOW', self.bye)
        self.wwidth = 630
        self.wheight = 650
        self.pwidth = int(self.root.winfo_screenwidth()/2 - self.wwidth/2)
        self.pheight = int(self.root.winfo_screenheight()/4 - self.wheight/4)
        self.root.geometry(f"{self.wwidth}x{self.wheight}+{self.pwidth}+{self.pheight}")
        self.root.bind_all('<Control-Left>', self.typ)
        self.root.bind_all('<Control-Right>', self.typ)
        self.root.bind_all('<Control-Up>',self.typ)
        self.root.bind_all('<Control-Down>', self.typ)
        self.root.bind_all('<Control-z>', self.edtlr)
        self.root.bind_all('<Control-s>', self.movc)
        self.root.bind_all('<Control-m>', self.maxim)
        self.root.bind('<Control-q>', self.bye)
        self.lt = StringVar()
        self.label = ttk.Label(self.root, textvariable = self.lt, font = 'verdana 9 bold', 
                               background = 'black', foreground = 'white')
        self.label.pack(pady = 2)
        self.frt = Frame(self.root)
        self.frt.pack()
        self.text = Text(self.frt, background = 'black', foreground = 'white', font = 'verdana 11',
                         width=56, height =12, borderwidth = 4, padx = 5, pady = 3)
        self.scroll = Scrollbar(self.frt, background = 'gold')
        self.text.bind_all('<Up>', self.scru)
        self.text.bind_all('<Down>', self.scrd)
        self.text.tag_config('thg', background = 'yellow', foreground = 'black')
        self.text.pack(side = 'left', padx = (3,0), pady = 5)
        self.scroll.pack(side = 'right', fill = 'y', padx = 2, pady = 5)
        self.scroll.config(command = self.text.yview)
        self.text.config(yscrollcommand = self.scroll.set)
        self.text.tag_add('js', '1.0', END)
        self.text.tag_configure('js', foreground = 'khaki')
        self.text.config(state = 'disable')
        self.entry = Entry(self.root, width = 32, font = 'verdana 17', justify = 'right', 
                      disabledbackground = 'black', disabledforeground = 'white',
                      borderwidth = 2, relief = RAISED)
        self.entry.pack(pady = 5, ipadx = 10)
        self.entry.config(state = 'disable')
        self.symbols = None
        with open(filen('curiso'), 'rb') as symfile:
            self.symbols = eval(symfile.readlines()[1].decode('utf-8'))
        self.frex = Frame(self.root, background = 'black', width = 76)
        self.frex.pack()
        self.cbc1 = ttk.Combobox(self.frex, width = 37)
        self.cbc1.pack(side = LEFT, padx =(0,5), pady = (0,5)) 
        self.cbc1['values'] = self.symbols
        self.cbc1.bind('<KeyRelease>', self.tynam)
        self.cbc1.bind_all('<r>', self.typ)
        self.cbc2 = ttk.Combobox(self.frex, width = 37)
        self.cbc2.pack(side = RIGHT, padx = (5,0), pady = (0,5)) 
        self.cbc2['values'] = self.symbols
        self.cbc2.bind_all('<e>', self.typ)
        self.cbc2.bind('<KeyRelease>', self.tynam)
        self.cbc2.bind('<FocusIn>', self.retrat)
        self.frex2 = Frame(self.root, background = 'black', width = 76)
        self.frex2.pack()
        self.btrat = Button(self.frex2, text = 'RATES', background = 'teal',
                            foreground = 'gold', width = 30, font = 'verdna 10 bold',
                            command = self.getrate)
        self.btrat.pack(side = LEFT)
        self.btrat.bind_all('<Control-r>', self.getrate)
        self.bt['btrat'] = self.btrat
        self.btcon = Button(self.frex2, text = 'CONVERT', background = 'teal',
                            foreground = 'gold', width = 30, font = 'verdna 10 bold',
                            command = self.conv)
        self.btcon.pack(side = RIGHT)
        self.btcon.bind_all('<Control-e>', self.conv)
        self.bt['btcon'] = self.btcon
        self.frm = Frame(self.root, background = 'black')
        self.frm.pack()
        r = 1
        c = 0
        lck = 1
        lc = ['1','2','3','(','-','BACK','4','5','6',')','+','%',
              '7','8','9','MOVE','/','M','0','.','C','ANS','*','+/-']
        nck = ['0','1','2','3','4','5','6','7','8','9', '/','.']
        while r <= len(lc):
            if lck:
                self.bt[lc[r-1]] = Button(self.frm, text = lc[r-1], font = 'verdana 15', width = 5, 
                                        background = 'teal', foreground = 'gold') 
            self.bt[lc[r-1]].configure(command = lambda obj=self.bt[lc[r-1]]: self.calculation(obj))
            if c < 6:
                self.bt[lc[r-1]].grid(row = r-c, column = c+1, pady = 5, padx = 5) 
                if lc[r-1] in nck:
                    self.bt[lc[r-1]].bind_all(f'{lc[r-1]}', self.typ)
                elif lc[r-1] == '-':
                    self.bt[lc[r-1]].bind_all('<minus>', self.typ)
                elif lc[r-1] == '%':
                    self.bt[lc[r-1]].bind_all('<percent>', self.typ)
                elif lc[r-1] == '+':
                    self.bt[lc[r-1]].bind_all('<plus>', self.typ)
                elif lc[r-1] == '(':
                    self.bt[lc[r-1]].bind_all('<parenleft>', self.typ)
                elif lc[r-1] == ')':
                    self.bt[lc[r-1]].bind_all('<parenright>', self.typ)
                elif lc[r-1] == '*':
                    self.bt[lc[r-1]].bind_all('<asterisk>', self.typ)
                elif lc[r-1] == 'BACK':
                    self.bt[lc[r-1]].bind_all('<BackSpace>', self.typ)
                elif lc[r-1] == 'MOVE':
                    self.bt[lc[r-1]].config(command = self.movc)
                elif lc[r-1] == 'M':
                    self.bt[lc[r-1]].bind_all('<m>', self.typ)
                elif lc[r-1] == '+/-':
                    self.bt[lc[r-1]].bind_all('<p>', self.typ)
                elif lc[r-1] == 'ANS':
                    self.bt[lc[r-1]].bind_all('<equal>', self.typ)
                elif lc[r-1] == 'C':
                    self.bt[lc[r-1]].bind_all('<c>', self.typ)
                c += 1
                r += 1
                lck = 1
            else:
                lck = 0
                c = 0
        del nck
        del lc
        del lck
        del c
        del r
        
        # Change places of the button. You can chage the button order placement as you like!
        # Make sure you understand the placement order.
        self.bt['BACK'].grid(row=20, column = 4, pady = 6, padx = 5)
        self.bt['M'].grid(row=20, column = 2, pady = 6, padx = 5)
        self.bt['MOVE'].grid(row=20, column = 1, pady = 6, padx = 5)
        self.bt['ANS'].grid(row=20, column = 3, pady = 6, padx = 5)
        self.bt['+/-'].grid(row=13, column = 5, pady = 6, padx = 5)
        self.bt['%'].grid(row=19, column = 5, pady = 6, padx = 5)
        self.bt['/'].grid(row=13, column = 4, pady = 6, padx = 5)
        self.bt['*'].grid(row=19, column = 4, pady = 6, padx = 5)
        self.bt[')'].grid(row=7, column = 5, pady = 6, padx = 5)
        self.bt['('].grid(row=1, column = 5, pady = 6, padx = 5)
        self.bt['-'].grid(row=1, column = 4, pady = 6, padx = 5)
        self.bt['+'].grid(row=7, column = 4, pady = 6, padx = 5)
        self.bt['C'].grid(row=19, column = 1, pady = 6, padx = 5)
        self.bt['0'].grid(row=19, column = 2, pady = 6, padx = 5)
        self.bt['.'].grid(row=19, column = 3, pady = 6, padx = 5)
        ##########################################################
        
        self.delb = Button(self.frm, text = 'DEL', font = 'verdana 15', width = 5, 
                      background = 'teal', foreground = 'gold', command = self.tdel)
        self.delb.bind_all('D', self.typ)
        self.delb.grid(row =1, column =0 , pady = 5, padx = 5)
        self.bt['delb'] = self.delb
        self.savb = Button(self.frm, text = 'SAVE', font = 'verdana 15', width = 5, 
                     background = 'teal', foreground = 'gold', command = self.savef)
        self.savb.bind_all('S', self.typ)
        self.savb.grid(row =7, column =0 , pady = 6, padx = 5)
        self.bt['savb'] = self.savb
        self.loab = Button(self.frm, text = 'LOAD', font = 'verdana 15', width = 5, 
                      background = 'teal', foreground = 'gold', command = self.loadcalc)
        self.loab.bind_all('L', self.typ)
        self.loab.grid(row =13, column =0 , pady = 6, padx = 5)
        self.bt['loab'] = self.loab
        self.edb = Button(self.frm, text = 'EDIT', font = 'verdana 15', width = 5, 
                     background = 'teal', foreground = 'gold', command = self.edt)
        self.edb.bind_all('E', self.typ)
        self.edb.grid(row =19, column =0 , pady = 6, padx = 5)
        self.bt['edb'] = self.edb
        self.copb = Button(self.frm, text = 'COPY', font = 'verdana 15', width = 5, 
                     background = 'teal', foreground = 'gold', command = self.copc)
        self.copb.bind_all('C', self.typ)
        self.copb.grid(row =20, column =0 , pady = 6, padx = 5)
        self.bt['copb'] = self.copb
        self.calb = Button(self.frm, text = 'CAL', font = 'verdana 15', width = 5, 
                     background = 'teal', foreground = 'gold', command = self.runcal)
        self.calb.bind_all('A', self.typ)
        self.calb.grid(row =20, column =5 , pady = 6, padx = 5)
        self.bt['calb'] = self.calb
        self.root.bind_all('<Key>', self.inspect)
    
    def inspect(self, event = None):
        if event.state == 2:
            kc = [20, 13]
            if event.keycode not in kc:
                messagebox.showinfo('Calculator', 'Please off the caps lock!', parent = self.root)
            
    def tynam(self, event = None):
        #To predict the key-in typing in comboboxes.
        try:
            if event.char in string.ascii_letters:
                pos = str(self.root.focus_get()) 
                if pos[-8:] == 'combobox':
                    if self.cbc1.get():
                        idx = self.cbc1.index(INSERT)
                        gt = self.cbc1.get()
                        self.cbc1.delete(0, END)
                        self.cbc1.insert(0, gt[:idx])
                        if self.cbc1.get():
                            for sym in self.symbols:
                                if self.cbc1.get().lower() in sym.lower()[:3] and sym.lower()[:3].startswith(self.cbc1.get().lower()[0]):
                                    self.cbc1.current(self.symbols.index(sym))
                        self.cbc1.icursor(index = idx)
                elif pos[-9:] == 'combobox2':
                    if self.cbc2.get():
                        idx = self.cbc2.index(INSERT)
                        gt = self.cbc2.get()
                        self.cbc2.delete(0, END)
                        self.cbc2.insert(0, gt[:idx])
                        if self.cbc2.get():
                            for sym in self.symbols:
                                if self.cbc2.get().lower() in sym.lower()[:3] and sym.lower()[:3].startswith(self.cbc2.get().lower()[0]):
                                    self.cbc2.current(self.symbols.index(sym))
                                    self.retrat()
                        self.cbc2.icursor(index = idx)                    
        except Exception as e:
            messagebox.showwarning('ReminderTel', f'{e}', parent = self.root)
    
    def maxim(self, event = None):
        #Maximize window without bar, and back to normal again.
        varct = ['<Control-Left>', '<Control-Right>', '<Control-Up>', '<Control-Down>']
        if self.root.winfo_width() != self.root.winfo_screenwidth():
            self.root.overrideredirect(True)
            self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()-20}+0+0")
            for i in varct:
                self.root.unbind_all(i)            
        else:
            self.root.overrideredirect(False)
            self.root.state('normal')
            self.wwidth = self.root.winfo_reqwidth()
            self.wheight = self.root.winfo_reqheight()
            self.pwidth = int(self.root.winfo_screenwidth()/3 - self.wwidth/3)+140
            self.pheight = int(self.root.winfo_screenheight()/10 - self.wheight/10)+20
            self.root.geometry(f"630x650+{self.pwidth}+{self.pheight}")
            for i in varct:
                self.root.bind_all(i, self.typ)
                
    def bye(self, event= None):
        #Stop application event.
        if Calculator.LOCK is False:
            os.chdir(Calculator.DEST)
            Calculator.MAINST.free()
            Calculator.MAINST.root.deiconify()
            if Calculator.MAINST.store:
                Calculator.MAINST.editor()
            Calculator.DEST = None
            Calculator.MAINST = None
            self.root.destroy()
        else:
            messagebox.showinfo('Calculator', 'Please deactivate Calendar first!', parent = self.root)
        
    def typ(self, event = None):
        #Keyboard binding event.
        try:
            fcom = str(self.root.focus_get())
        except:
            fcom = 'combobox'
        if self.tpl is None:
            nck = ['0','1','2','3','4','5','6','7','8','9','-', '/','.']
            if event.char in nck:
                self.calculation(self.bt[event.char])
            else:
                if event.keysym == 'BackSpace':
                    self.calculation(self.bt['BACK'])
                elif event.keysym == 'equal':
                    self.calculation(self.bt['ANS'])
                elif event.keysym == 'asterisk':
                    self.calculation(self.bt['*'])
                elif event.keysym == 'plus':
                    self.calculation(self.bt['+'])
                elif event.keysym == 'c':
                    self.calculation(self.bt['C'])
                elif event.keysym == 'parenleft':
                    self.calculation(self.bt['('])
                elif event.keysym == 'parenright':
                    self.calculation(self.bt[')']) 
                elif event.keysym == 'percent':
                    self.calculation(self.bt['%'])
                elif event.keysym == 'p':
                    self.calculation(self.bt['+/-'])
                elif event.keysym == 'm':
                    self.calculation(self.bt['M'])                
                elif event.keysym == 'Left' and 'combobox' not in fcom:
                    self.pwidth = self.pwidth - 10
                    self.root.geometry(f"+{self.pwidth}+{self.pheight}")
                elif event.keysym == 'Right' and 'combobox' not in fcom:
                    self.pwidth = self.pwidth + 10
                    self.root.geometry(f"+{self.pwidth}+{self.pheight}")
                elif event.keysym == 'Down' and 'combobox' not in fcom:
                    self.pheight = self.pheight + 10
                    self.root.geometry(f"+{self.pwidth}+{self.pheight}")
                elif event.keysym == 'Up' and 'combobox' not in fcom:
                    self.pheight = self.pheight - 10
                    self.root.geometry(f"+{self.pwidth}+{self.pheight}")
                elif event.keysym == 'A' and 'combobox' not in fcom:
                    self.runcal()
                elif event.keysym == 'C' and 'combobox' not in fcom:
                    self.copc()          
                elif event.keysym == 'E' and 'combobox' not in fcom:
                    self.edt()
                elif event.keysym == 'L' and 'combobox' not in fcom:
                    self.loadcalc()
                elif event.keysym == 'S' and 'combobox' not in fcom:
                    self.savef()
                elif event.keysym == 'D' and 'combobox' not in fcom:
                    self.tdel()
                elif event.keysym == 'r':
                    if 'combobox' not in fcom:
                        self.cbc1.focus()
                elif event.keysym == 'e':
                    if 'combobox' not in fcom:
                        self.cbc2.focus()
                
    def retrat(self, event = None):
        #Tracking currency symbol in 2nd combo,
        #to get the rate.
        if not self.lt.get() and self.ops:
            if self.rate:
                ck = list(self.rate)
                if 'result' not in ck:
                    if self.cbc1.get()[:3] == self.base and self.cbc2.get()[:3]:
                        tmp = dt.datetime.isoformat(dt.datetime.fromtimestamp(int(self.rate['timestamp']))).replace('T', ' ')
                        drt = float(self.rate["rates"][self.cbc2.get()[:3]])
                        disp = f'From: {self.rate["base"]}\nTo: {self.cbc2.get()[:3]}\nRate: {drt:,}\nDate-Time: {tmp}'
                        self.text.config(state = 'normal')
                        self.text.delete('1.0', END)
                        self.text.insert(END, disp)
                        self.text.config(state = 'disable')
                    
    def getrate(self, event = None):
        #Getting rates.
        if self.ops:
            if not self.lt.get():
                try:
                    if self.cbc1.get()[:3] and self.cbc2.get()[:3]:
                        self.ic = 1
                        key = cp.readcpd('fixio')
                        rtb = Fixio(base = self.cbc1.get()[:3], apik = key)
                        self.rate = rtb.converlatest()
                        self.base = self.cbc1.get()[:3]
                        tmp = dt.datetime.isoformat(dt.datetime.fromtimestamp(int(self.rate['timestamp']))).replace('T', ' ')
                        drt = float(self.rate["rates"][self.cbc2.get()[:3]])
                        disp = f'From: {self.rate["base"]}\nTo: {self.cbc2.get()[:3]}\nRate: {drt:,}\nDate-Time: {tmp}'
                        self.text.config(state = 'normal')
                        self.text.delete('1.0', END)
                        self.text.insert(END, disp)
                        self.text.config(state = 'disable')
                except Exception as e:
                    messagebox.showwarning('Calculator', f'{e}', parent = self.root)
            else:
                messagebox.showwarning('Calculator', 'Cannot get rate while in working file mode!!!', parent = self.root)
        else:
            messagebox.showwarning('Calculator', 'Unable to save, because Calendar or Rate is active!!!', parent = self.root)
        self.root.focus_set()
            
    def conv(self, event = None):
        #Getting amount convert.
        if self.ops:
            if not self.lt.get() and self.entry.get():
                try:
                    if self.cbc1.get()[:3] and self.cbc2.get()[:3]:
                        self.ic = 1
                        key = cp.readcpd('fixio')
                        enn = eval(self.entry.get().replace(',',''))
                        rtb = Fixio(base = self.cbc1.get()[:3], symbols = self.cbc2.get()[:3], amount = enn, apik = key)
                        self.rate = rtb.converconv()
                        tmp = dt.datetime.isoformat(dt.datetime.fromtimestamp(int(self.rate["info"]["timestamp"]))).replace('T', ' ')
                        drt = float(self.rate["info"]["rate"])
                        rst = float(self.rate["result"])
                        disp = f'From: {self.rate["query"]["from"]}\nTo: {self.rate["query"]["to"]}\nRate: {drt:,}\nResult: {rst:,}\nDate-Time: {tmp}'
                        self.text.config(state = 'normal')
                        self.text.delete('1.0', END)
                        self.text.insert(END, disp)
                        self.text.config(state = 'disable')
                except Exception as e:
                    messagebox.showwarning('Calculator', f'{e}', parent = self.root)
            else:
                messagebox.showwarning('Calculator', 'Cannot get conversion while in working file mode or maybe no amount yet!!!', parent = self.root)
        else:
            messagebox.showwarning('Calculator', 'Unable to save, because Calendar or Rate is active!!!', parent = self.root)
        self.root.focus_set()
            
    def scrd(self, event = None):
        #Scroll to the bottom on keyboard, down arrow button.
        if self.tpl is None:
            a = self.text.yview()[0]
            a = eval(f'{a}')+0.01
            self.text.yview_moveto(str(a))
        
    def scru(self, event = None):
        #Scroll to the first position on keyboard, up arrow button.
        if self.tpl is None:
            a = self.text.yview()[0]
            a = eval(f'{a}')-0.01
            self.text.yview_moveto(str(a))
        
    def calculation(self, obj):
        #Engine of the calculator.
        if not self.entry.get():
            self.ctc = {}    
        nck = ['0','1','2','3','4','5','6','7','8','9','e']
        ock = ['-', '+', '*', '/', '(', ')','.']
        bck = ['ANS','M','C','BACK','%','+/-']
        if not self.entry.get() == 'ERR':
            if obj['text'] in nck:
                self.entry.config(state = 'normal')
                go = self.entry.get()
                try:
                    if self.ctc:
                        ls = list(self.ctc)[-1]
                        if go[ls-1] == self.ctc[ls] :
                            go = go[ls:] 
                        self.cn = go.replace(',','')
                        self.entry.delete(ls,END)
                        self.cn = self.cn + ''.join(obj['text'])
                        if not self.ctc[ls] == '.':
                            ecn = f'{eval(self.cn):,}'
                        else:
                            ecn = self.cn
                        if not self.idx:
                            self.idx = len(self.entry.get())+1
                        self.entry.delete(self.idx-1,END)
                        self.entry.insert(END,ecn)
                        self.entry.config(state = 'disable')
                    else:
                        self.cn = go.replace(',','')
                        self.cn = self.cn + ''.join(obj['text'])
                        ecn = f'{eval(self.cn):,}'
                        self.entry.delete(0,END)
                        self.entry.insert(END,ecn)
                        self.entry.config(state = 'disable')
                except:
                    self.entry.delete(0,END)
                    self.entry.insert(END,'ERR')
                    self.entry.config(state = 'disable')
            elif obj['text'] in ock:
                self.entry.config(state = 'normal')
                self.idx = 0
                self.cn = ''
                reg = re.compile(r'\W')
                self.entry.insert(END,obj['text'])
                self.ctc = {i.span()[1]: i.group() for i in reg.finditer(self.entry.get()) if i.group()!=','}
                self.entry.config(state = 'disable')
            else:
                if obj['text'] == bck[0]:
                    self.idx = 0
                    self.cn = ''
                    self.ctc = {}
                    self.ans = 0
                    try:
                        self.ans = eval(self.entry.get().replace(',',''))
                        if isinstance(self.ans, float):
                            if self.ans.is_integer():
                                self.ans = int(self.ans)
                        
                        bans = {i.group(): i.span()[0] for i in re.finditer(r'\W', self.entry.get()) if i.group()!=','}
                        if bans:
                            lbans = list(bans) 
                            if len(lbans) == 1:
                                if '-' in lbans:
                                    if bans['-'] != 0: 
                                        self.prcalc(f'CAL: {self.entry.get()}')
                                        self.prcalc(f'ANS: {self.ans:,}')
                                elif not '.' in lbans:
                                    self.prcalc(f'CAL: {self.entry.get()}')
                                    self.prcalc(f'ANS: {self.ans:,}')
                            elif len(lbans) == 2: 
                                if '-' in lbans and '.' in lbans:
                                    if bans['-'] != 0:  
                                        self.prcalc(f'CAL: {self.entry.get()}')
                                        self.prcalc(f'ANS: {self.ans:,}')
                                else:
                                    self.prcalc(f'CAL: {self.entry.get()}')
                                    self.prcalc(f'ANS: {self.ans:,}')
                            else:
                                self.prcalc(f'CAL: {self.entry.get()}')
                                self.prcalc(f'ANS: {self.ans:,}')
                        bans = None
                        lbans = None
                        reg = re.compile(r'\W')
                        self.entry.config(state = 'normal')
                        self.entry.delete(0,END)
                        self.entry.insert(END,f'{self.ans:,}')
                        self.ctc = {i.span()[1]: i.group() for i in reg.finditer(self.entry.get()) if i.group()!=','}
                        self.entry.config(state = 'disable')
                    except:
                        import sys
                        print(sys.exc_info())
                        self.entry.config(state = 'normal')
                        self.entry.delete(0,END)
                        self.entry.insert(END,'ERR')
                        self.entry.config(state = 'disable')
                elif obj['text'] == bck[1]:
                    self.ctc = {}
                    self.idx = 0
                    self.cn = ''
                    if not self.mem:
                        self.mem = self.entry.get()
                        self.entry.config(state = 'normal')
                        self.entry.delete(0,END)
                        self.entry.config(state = 'disable')
                    else:
                        reg = re.compile(r'\W')
                        self.entry.config(state = 'normal')
                        self.entry.insert(END,self.mem)
                        self.mem = ''
                        self.ctc = {i.span()[1]: i.group() for i in reg.finditer(self.entry.get()) if i.group()!=','}
                        self.entry.config(state = 'disable')     
                elif obj['text'] == bck[2]:
                    self.idx = 0
                    self.cn = ''
                    self.ctc = {}
                    self.ans = 0
                    self.entry.config(state = 'normal')
                    self.entry.delete(0,END)
                    self.entry.config(state = 'disable')
                elif obj['text'] == bck[3]:
                    self.idx = 0
                    self.cn = ''
                    self.entry.config(state = 'normal')
                    ge = self.entry.get()[:-1]
                    if self.ctc:
                        if list(self.ctc)[-1] > len(ge):
                            del self.ctc[list(self.ctc)[-1]]
                        try:
                            ge = eval(ge[list(self.ctc)[-1]:].replace(',',''))
                            self.entry.delete(list(self.ctc)[-1], END)
                            if self.ctc[list(self.ctc)[-1]] == '.' and len(self.ctc) == 1:
                                self.entry.insert(END, ge)
                            else:
                                self.entry.insert(END, f'{ge:,}')
                            self.entry.config(state = 'disable')
                        except:
                            self.entry.delete(0, END)
                            self.entry.insert(END, ge)
                            self.entry.config(state = 'disable')
                    else:
                        try:
                            ge = eval(ge.replace(',',''))            
                            self.entry.delete(0,END)
                            self.entry.insert(END,f'{ge:,}')
                            self.entry.config(state = 'disable')
                        except:
                            self.entry.delete(0, END)
                            self.entry.insert(END, ge)
                            self.entry.config(state = 'disable')
                elif obj['text'] == bck[4]:
                    self.entry.config(state = 'normal')
                    self.idx = 0
                    self.cn = ''
                    reg = re.compile(r'\W')
                    try:
                        if self.ctc:
                            self.ctc = {i.span()[1]: i.group() for i in reg.finditer(self.entry.get()) if i.group() != ',' and i.group() != '.'}
                            if self.ctc:
                                gn = eval(self.entry.get()[list(self.ctc)[-1]:].replace(',',''))/100
                                self.entry.delete(list(self.ctc)[-1],END)
                                self.entry.insert(END,f'{gn:,}')
                        self.ctc = {i.span()[1]: i.group() for i in reg.finditer(self.entry.get()) if i.group() != ','}
                        self.entry.config(state = 'disable')
                    except:
                        self.entry.config(state = 'disable')                        
                elif obj['text'] == bck[5]:
                    self.entry.config(state = 'normal')
                    self.idx = 0
                    self.cn = ''
                    reg = re.compile(r'\W')
                    if self.entry.get():
                        if self.entry.get()[0] == '-':
                            pm = self.entry.get()[1:]
                        else:
                            pm = f'-{self.entry.get()}'
                        self.entry.delete(0,END)
                        self.entry.insert(END,pm)
                        self.ctc = {i.span()[1]: i.group() for i in reg.finditer(self.entry.get()) if i.group() != ','}
                    self.entry.config(state = 'disable')
        else:
            if obj['text'] == bck[2]:
                self.idx = 0
                self.cn = ''
                self.ctc = {}
                self.ans = 0
                self.entry.config(state = 'normal')
                self.entry.delete(0,END)
                self.entry.config(state = 'disable')
        self.entry.xview_moveto('1.0')
        
    def prcalc(self, calc: str):
        #Helping the calculator to print out on the text screen.
        if self.ic is None:
            self.text.config(state = 'normal')
            self.text.insert(END, f'{calc}\n','js')
            self.text.config(state = 'disable')
            self.text.yview_moveto('1.0')
            
    def tdel(self, event = None):
        #To delete text screen and stop the active calendar.
        #Also delete rates.
        std = os.getcwd()
        os.chdir('CalculatorData')
        self.tpl = 1
        ask = messagebox.askyesno('Calculator', 'Want delete screen record?', parent = self.root)
        if ask:
            if self.run and not self.ops:
                self.run = False
                self.entry.config(state = 'normal', justify = 'right')
                self.entry.delete(0,END)
                self.entry.config(state = 'disable')
            
            if self.rate:
                dr = messagebox.askyesno('Calculator', 'Delete Rate?', parent = self.root)
                if dr:
                    self.ic = None
                    self.rate = None
                    self.base = None
                    self.text.config(state = 'normal', font = 'verdana 11')
                    self.text.delete('1.0', END)
                    self.text.config(state ='disable')
                    self.lt.set('')
                else:
                    messagebox.showinfo('Calculator', 'Exchange Rate is still active!', parent = self.root)
            else:
                self.text.config(state = 'normal', font = 'verdana 11')
                self.text.delete('1.0', END)
                self.text.config(state ='disable')
                self.lt.set('')                
        else:
            ldc = os.listdir()
            if ldc:
                class MyDialog(simpledialog.Dialog):
                        
                        def body(self, master):
                            self.title('Choose File')
                            Label(master, text="File: ").grid(row=0, column = 0, sticky = E)
                            self.e1 = ttk.Combobox(master, state = 'readonly')
                            self.e1['values'] = ldc
                            self.e1.current(0)
                            self.e1.grid(row=0, column=1)
                            return self.e1
                    
                        def apply(self):
                            self.result = self.e1.get()
                                        
                d = MyDialog(self.root)
                if d.result:
                    os.remove(d.result)
                    if self.lt.get():
                        if self.lt.get() == d.result.rpartition('.')[0]:
                            self.lt.set('')
                            self.text.config(state = 'normal')
                            self.text.delete('1.0', END)
                            self.text.config(state = 'disable')
                    messagebox.showinfo('Calculator', f'File {d.result} has been deleted!', parent = self.root)
                else:                   
                    messagebox.showinfo('Calculator', 'Deletion file aborted!!!', parent = self.root)
        self.tpl = None
        os.chdir(std)
        
    def savef(self, event = None):
        #To save the calculation on a file.
        std = os.getcwd()
        os.chdir('CalculatorData')
        self.tpl = 1
        if self.ops and self.ic is None:
            if self.text.get('1.0',END)[:-1]:
                if not self.lt.get():
                    filename = simpledialog.askstring('Calculator', 'Create save file?', parent = self.root)
                else:
                    filename = self.lt.get()
                if filename:
                    owt = None
                    if f'{filename}.txt' in os.listdir():
                        owt = messagebox.askyesno('Calculator', 'Do you wan overwrite existing file?', parent = self.root)
                    if owt or not f'{filename}.txt' in os.listdir():
                        with open(f'{filename}.txt', 'w') as cdt:
                            dt =[i for i in self.text.get('1.0', END).split('\n')[:-1] if i]
                            dd = {}
                            n = 1
                            while dt:
                                if len(dt)>2:
                                    if 'Note:' in dt[2]:
                                        dd[n] = (dt[0], dt[1], dt[2])
                                        del dt[0]
                                        del dt[0]
                                        del dt[0]
                                        n += 1
                                    else:
                                        dd[n] = (dt[0], dt[1])
                                        del dt[0]
                                        del dt[0]
                                        n += 1
                                elif dt:
                                    dd[n] = (dt[0], dt[1])
                                    del dt[0]
                                    del dt[0]
                                    n += 1
                            cdt.write(f'{dd}')
                        self.lt.set(f'{filename}')
                else:
                    messagebox.showinfo('Calculator', 'Saving a file is aborted!!!', parent = self.root)
            else:
                messagebox.showinfo('Calculator', 'Nothing to be saved!!!', parent = self.root)
        else:
            messagebox.showwarning('Calculator', 'Unable to save, because Calendar or Rate is active!!!', parent = self.root)
        self.tpl = None
        os.chdir(std)
        
    def loadcalc(self, event = None):
        #To load a calculation file back to screen.
        
        if self.ops and self.ic is None :
            std = os.getcwd()
            os.chdir('CalculatorData')
            if not self.lt.get():
                ldc = os.listdir()
                self.tpl = 1
                if ldc:
                    class MyDialog(simpledialog.Dialog):
                        
                        def body(self, master):
                            self.title('Choose File')
                            Label(master, text="File: ").grid(row=0, column = 0, sticky = E)
                            self.e1 = ttk.Combobox(master, state = 'readonly')
                            self.e1['values'] = ldc
                            self.e1.current(0)
                            self.e1.grid(row=0, column=1)
                            return self.e1
                    
                        def apply(self):
                            self.result = self.e1.get()
                                        
                    d = MyDialog(self.root)
                    if d.result:
                        with open(f'{d.result}') as rd:
                            ex = eval(rd.read())
                            self.text.config(state = 'normal')
                            self.text.delete('1.0', END)
                            for _, t in ex.items():
                                if len(t) == 2:
                                    self.text.insert(END, f'{t[0]}\n{t[1]}\n')
                                else:
                                    self.text.insert(END, f'{t[0]}\n{t[1]}\n{t[2]}\n\n')
                            self.text.config(state = 'disable')
                        self.lt.set(f'{d.result[:-4]}')    
                    else:
                        messagebox.showinfo('Calculator', 'Load file aborted!!!', parent = self.root)
                else:
                    messagebox.showinfo('Calculator', 'No Files yet!!!', parent = self.root)
            else:
                with open(f'{self.lt.get()}.txt') as rd:
                    ex = eval(rd.read())
                    self.text.config(state = 'normal')
                    self.text.delete('1.0', END)
                    for _, t in ex.items():
                        if len(t) == 2:
                            self.text.insert(END, f'{t[0]}\n{t[1]}\n')
                        else:
                            self.text.insert(END, f'{t[0]}\n{t[1]}\n{t[2]}\n\n')
                    self.text.config(state = 'disable')
            self.tpl = None
            os.chdir(std)
        else:
            messagebox.showwarning('Calculator', 'Unable to load, because Calendar or Rate is active!!!', parent = self.root)     
            
    def edt(self, event = None):
        #Edit calculation for changing value in a file and add note as well.
        if self.ops and self.ic is None:
            if self.lt.get():
                std = os.getcwd()
                os.chdir('CalculatorData')
                self.tpl = 1
                with open(f'{self.lt.get()}.txt') as rd:
                    cdt = eval(rd.read())
                    ldc = []
                    for i in cdt:
                        ldc.append(f'{i}:{cdt[i]}\n')
                
                class MyDialog(simpledialog.Dialog):
                    
                    def body(self, master):
                        self.title('Choose Data')
                        Label(master, text="Data: ").grid(row=0, column = 0, sticky = E)
                        self.e1 = ttk.Combobox(master, state = 'readonly', width = 35)
                        self.e1['values'] = ldc
                        self.e1.current(0)
                        self.e1.grid(row=0, column=1)
                        return self.e1
                
                    def apply(self):
                        self.result = int(self.e1.get().partition(':')[0])
                                    
                d = MyDialog(self.root)
                ask = None
                if d.result:
                    ask = d.result
                    chg = messagebox.askyesno('Calculator', 'Change values"Yes", Delete row "No"', parent = self.root)
                    if chg:
                        vn = messagebox.askyesno('Calculator', 'Add note "Yes", Add values "No"', parent = self.root)
                        if vn:
                            adno = simpledialog.askstring('Calculator', 'Adding Note:', parent = self.root)
                            if adno:
                                if len(cdt[ask]) == 2:
                                    cdt[ask] = cdt[ask] + (f'Note: {adno}',)
                                else:
                                    cdt[ask] = cdt[ask][:-1] + (f'Note: {adno}',)
                                with open(f'{self.lt.get()}.txt', 'w') as rd:
                                    rd.write(f'{cdt}')
                                messagebox.showinfo('Updated', 
                                f'File {self.lt.get()} has been updated!!!', parent = self.root)    
                            else:
                                den = messagebox.askyesno('Calculator', 'Delete Note?', parent = self.root)
                                if den:
                                    if len(cdt[ask]) == 3:
                                        cdt[ask] = cdt[ask][:-1]
                                        with open(f'{self.lt.get()}.txt', 'w') as rd:
                                            rd.write(f'{cdt}')
                                        messagebox.showinfo('Updated', 
                                        f'File {self.lt.get()} has been updated!!!', parent = self.root)
                                    else:
                                        messagebox.showinfo('Calculator', 'No Note!!!', parent = self.root)
                                else:                    
                                    messagebox.showwarning('Calculator', 'Adding note aborted!!!', parent = self.root)
                        else:            
                            if self.entry.get():
                                val = self.entry.get().replace(',','')
                                try:
                                    cval = eval(val)
                                    tx = self.entry.get()
                                    if isinstance(cval, float):
                                        if cval.is_integer():
                                            cval = int(cval)
                                    if len(cdt[ask]) == 2: 
                                        rchg = (f'CAL: {tx}', f'ANS: {cval:,}')
                                        cdt[ask] = rchg
                                    else:
                                        rchg = (f'CAL: {tx}', f'ANS: {cval:,}')
                                        rchg = rchg + (cdt[ask][-1],)
                                        cdt[ask] = rchg
                                    with open(f'{self.lt.get()}.txt', 'w') as rd:
                                        rd.write(f'{cdt}')
                                    messagebox.showinfo('Updated', 
                                    f'File {self.lt.get()} has been updated!!!', parent = self.root)
                                except:
                                    import sys
                                    print(sys.exc_info())
                                    messagebox.showwarning('Calcultor', 'Please change the formula!!!', parent = self.root)
                            else:
                                messagebox.showwarning('Calculator', 'Please set formula first', parent = self.root)
                    else:
                        dq = messagebox.askyesno('Deletion Row', f'Delete row {ask}?\n{cdt[ask]}', parent = self.root)
                        if dq:
                            if ask < len(cdt):
                                cot = cdt[ask+1]
                                cdt[ask] = cot
                                del cdt[ask+1]
                            else:
                                del cdt[ask] 
                            with open(f'{self.lt.get()}.txt', 'w') as rd:
                                rd.write(f'{cdt}')
                            messagebox.showinfo('Updated', 
                            f'File {self.lt.get()} has been updated!!!', parent = self.root)
                        else:
                            messagebox.showwarning('Calculator', 'Deletion row aborted!!!', parent = self.root)
                else:
                    messagebox.showwarning('Calculator', 'Editing is aborted!!!', parent = self.root)
                self.tpl = None
                os.chdir(std)
                self.loadcalc()
                if ask:
                    with open(f'CalculatorData\{self.lt.get()}.txt') as rd:
                        cdt = eval(rd.read()) 
                    tot = 0
                    if ask < len(cdt):
                        for i in range(ask):
                            if len(cdt[i+1])==2:
                                tot += 2
                            else:
                                tot += 4                    
                        self.text.see(float(tot-1))
                    else:
                        for i in range(ask-1):
                            if len(cdt[i+1])==2:
                                tot += 2
                            else:
                                tot += 4                    
                        self.text.see(float(tot-1))                        
            else:
                messagebox.showinfo('Calculator', 'Please load a file first!!!', parent = self.root)
        else:
            messagebox.showwarning('Calculator', 'Unable to edit, because Calendar or Rate is active!!!', parent = self.root)
    
    def movc(self, event = None):
        #Moving a calculation to other row. [In saved mode only]
        if self.ops and self.ic is None:
            if self.lt.get():
                self.tpl = 1
                std = os.getcwd()
                os.chdir('CalculatorData') 
                with open(f'{self.lt.get()}.txt') as rd:
                    cdt = eval(rd.read())
                    ldc = []
                    for i in cdt:
                        ldc.append(f'{i}:{cdt[i]}\n')
                
                class MyDialog(simpledialog.Dialog):
                    
                    def body(self, master):
                        self.title('Move Data to?')
                        Label(master, text="Move: ").grid(row=0, column = 0, sticky = E)
                        self.e1 = ttk.Combobox(master, state = 'readonly', width = 35)
                        self.e1['values'] = ldc
                        self.e1.current(0)
                        self.e1.grid(row=0, column=1)
                        Label(master, text="To: ").grid(row=1, column = 0, sticky = E)
                        self.e2 = ttk.Combobox(master, state = 'readonly', width = 35)
                        self.e2['values'] = ldc
                        self.e2.current(0)
                        self.e2.grid(row=1, column=1)                        
                        return self.e1
                
                    def apply(self):
                        self.result = int(self.e1.get().partition(':')[0])
                        self.to = int(self.e2.get().partition(':')[0])
                d = MyDialog(self.root)
                mvt =  None
                if d.result and d.to:
                    ask = d.result
                    mvt = d.to
                    if mvt and mvt <= len(cdt):
                        lcm = list(cdt)
                        mc = lcm[ask-1]
                        if mvt == len(lcm):
                            lcm.append(mc)
                        else:
                            lcm.insert(mvt-1, mc)
                        if mvt > ask:
                            del lcm[ask-1]
                        else:
                            del lcm[ask]
                        cdt = {i+1:cdt[lcm[i]] for i in range(len(lcm))}
                        with open(f'{self.lt.get()}.txt', 'w') as wd:
                            wd.writelines(str(cdt))
                    else:
                        messagebox.showinfo('Calculator', 'Moving Calculation aborted!!!', parent = self.root)
                else:
                    messagebox.showinfo('Calculator', 'Moving Calculation aborted!!!', parent = self.root)
                self.tpl = None
                os.chdir(std)
                self.loadcalc()
                with open(f'CalculatorData\{self.lt.get()}.txt') as rd:
                    cdt = eval(rd.read()) 
                tot = 0
                if mvt:
                    if mvt < len(cdt):
                        for i in range(mvt):
                            if len(cdt[i+1])==2:
                                tot += 2
                            else:
                                tot += 4
                        self.text.see(float(tot-1))
                    else:
                        for i in range(mvt-1):
                            if len(cdt[i+1])==2:
                                tot += 2
                            else:
                                tot += 4
                        self.text.see(float(tot-1))
        else:
            messagebox.showwarning('Calculator', 'Unable to edit, because Calendar or Rate is active!!!', parent = self.root)
    
    def edtlr(self, event = None):
        #Edit the calculation entry box directly.
        #[All function will be freeze to avoid errors]
        if self.tpl is None and self.ops is True:
            self.entry.config(state = 'normal')
            self.entry.focus()
            self.tpl = 1
            self.ops = False
            lbtn = list(self.bt)
            for i in lbtn:
                self.bt[i].config(state = 'disable')
        else:
            self.tpl = None
            self.ops = True
            lbtn = list(self.bt)
            for i in lbtn:
                self.bt[i].config(state = 'normal')
            nck = ['0','1','2','3','4','5','6','7','8','9']
            ock = ['-', '+', '*', '/', '(', ')','.']         
            inp = self.entry.get().replace(',','')
            self.entry.delete(0, END)
            for i in inp:
                if i in nck+ock:
                    self.calculation(self.bt[i])
                else:
                    break
            self.entry.config(state = 'disable')

    def copc(self, event = None):
        #Copy function that collect the screen calculation to clipboard. Paste to any chat :).
        self.tpl = 1
        if self.ops:
            if self.ic is None:
                if self.text.get('1.0', END)[:-1]:
                    gpt = self.text.get('1.0', END)[:-1].split('\n')
                    gpt = [i for i in gpt if i and 'CAL:' in i]
                    gpn = [f'{i+1}:{j}' for i, j in enumerate(gpt)]
                    class MyDialog(simpledialog.Dialog):
                        
                        def body(self, master):
                            self.title('Choose Data')
                            Label(master, text="Data: ").grid(row=0, column = 0, sticky = E)
                            self.e1 = ttk.Combobox(master, state = 'readonly', width = 35)
                            self.e1['values'] = gpn
                            self.e1.current(0)
                            self.e1.grid(row=0, column=1)
                            return self.e1
                    
                        def apply(self):
                            self.result = int(self.e1.get().partition(':')[0])
                                        
                    d = MyDialog(self.root)
                    if d.result:
                        pas = d.result
                        self.entry.config(state = 'normal')
                        self.entry.delete(0,END)
                        self.entry.insert(END, gpt[pas-1][5:])
                        self.entry.config(state = 'disable')
                        reg = re.compile(r'\W')
                        ean = eval(gpt[pas-1][5:].replace(",",""))
                        if isinstance(ean, float) and ean.is_integer():
                            ean = int(ean)
                        cp = f'{gpt[pas-1]}\nANS: {ean:,}\n'
                        self.root.clipboard_clear()
                        self.root.clipboard_append(cp)
                        messagebox.showinfo('Calculator', f'Pasted and\n{cp}copied!', parent = self.root)
                        self.ctc = {i.span()[1]: i.group() for i in reg.finditer(gpt[pas-1][5:]) if i.group()!=','}
                    else:
                        txt = 'p:Calculations\n'
                        frt = [i for i in self.text.get('1.0', END)[:-2].split('\n')]
                        wrd = ''
                        for w in range(len(frt)):
                            if frt[w]:
                                wrd += ''.join(f'c1:{frt[w]}\n')
                            else:
                                if w != len(frt)-1:
                                    wrd += ''.join(f'c1: \n')
                        
                        Calculator.MAINST.store = txt + wrd
                        messagebox.showinfo('Calculator', 'Pasting skipped and screen copied for editor!', parent = self.root)
                else:
                    messagebox.showinfo('Calculator', 'Copy aborted!', parent = self.root)
            else:
                gtr = [i for i in self.text.get('1.0', END)[:-1].split('\n') if 'Rate:' in i]
                pas = messagebox.askyesno('Calculator', 'Want to paste Rate?', parent = self.root)
                if pas:
                    self.entry.config(state = 'normal')
                    self.entry.delete(0,END)
                    self.entry.insert(END, gtr[0][6:])
                    self.entry.config(state = 'disable')                    
                    messagebox.showinfo('Calculator', f'Pasted {gtr[0]}!', parent = self.root)
                else:
                    txt = 'p:Exchange Rate\n'
                    if 'Result:' in self.text.get('1.0', END)[:-1]:
                        txt += f'c1:{self.cbc1.get().partition("-")[0]}{self.entry.get()}\n'
                    frt = [i for i in self.text.get('1.0', END)[:-1].split('\n') if i]
                    wrd = ''
                    for w in frt:
                        wrd += ''.join(f'c1:{w}\n')
                    Calculator.MAINST.store = txt + wrd
                    messagebox.showinfo('Calculator', 'Pasting skipped and screen copied for editor!', parent = self.root)
        else:
            messagebox.showwarning('Calculator', 'Unable to copy, because Calendar or Rate is active!!!', parent = self.root)
        self.tpl = None
        
    def runcal(self, event = None):
        if Calculator.LOCK is False:
            self.calcal()
    
    def calcal(self, event = None):
        #Calendar Function that show the today's date and also display hours.
        if self.run:
            self.ops = False
            if not self.text.get('1.0', END)[:-1]:
                cald = ChoCal(dt.date.today().year, dt.date.today().month).createcal()
                self.text.tag_add('jt', '1.0', END)
                self.text.tag_config('jt', justify = 'center')
                self.text.config(state = 'normal')
                self.text.config(font = 'courier 12 bold')
                self.text.insert('1.0', f'\n\n{cald}', ('js','jt'))
                sch1 = self.text.search(str(dt.datetime.today().day),'5.0',END)
                sch2 = f'{sch1}+{len(str(dt.datetime.today().day))}c'
                gt = self.text.get(sch1,sch2)
                self.text.delete(sch1, sch2)
                self.text.insert(sch1,gt, ('thg'))                
                self.text.config(state = 'disable')
                self.entry.config(state = 'normal', justify = 'center')
                self.entry.delete(0,END)
                self.entry.insert(END, dt.datetime.now().replace(microsecond=0))
                self.entry.config(state = 'disable')
                Calculator.LOCK = self.root.after(1000, self.calcal)
            else:
                self.entry.config(state = 'normal', justify = 'center')
                self.entry.delete(0,END)
                self.entry.insert(END, dt.datetime.now().replace(microsecond=0))
                self.entry.config(state = 'disable')
                Calculator.LOCK = self.root.after(1000, self.calcal)
        else:
            self.run = True
            self.ops = True
            Calculator.LOCK = False

def main(stat, ori):
    #Get start and making "CalculatorData" dir.
    cdt = os.listdir(os.getcwd())
    if 'CalculatorData' not in cdt:
        os.mkdir('CalculatorData')
    root = Tk()
    Calculator.MAINST = stat
    Calculator.DEST = ori
    Calculator.MAINST.root.withdraw()
    begin = Calculator(root)
    begin.MAINST.root.withdraw()
    begin.root.focus_force()
    begin.root.mainloop()