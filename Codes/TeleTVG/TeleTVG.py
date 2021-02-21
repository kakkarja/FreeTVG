# -*- coding: utf-8 -*-
#Copyright (c) 2020, KarjaKAK
#All rights reserved.

from CreatePassword import CreatePassword as cp
from telethon import TelegramClient
from telethon import functions
from telethon.tl import types
from tkinter import *
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime as dt, timedelta
from FileFind import filen
import string
import asyncio
import shutil
import emo
import os
import sys
import string
import json

class Reminder:
    """
    Building Reminder Telegram to help remind a friend or yourself.
    """
    STATUS = False
    MAINST = None
    DEST = None
    API = None
    HASH_ = None
    GEO = None
    RESZ = None
    EMOP = None
    STOP_A = False
    def __init__(self, root):
        self.root = root
        self.root.title('TeleTVG')
        self.wid = 705
        self.hei = 650
        self.root.minsize(705, 650)
        self.pwidth = int(self.root.winfo_screenwidth()/2 - self.wid/2)
        self.pheight = int(self.root.winfo_screenheight()/3 - self.hei/3)
        self.root.geometry(f'{self.wid}x{self.hei}+{self.pwidth}+{self.pheight}')
        Reminder.RESZ = f'{self.wid}x{self.hei}+{self.pwidth}+{self.pheight}'
        gpath = os.getcwd().rpartition('\\')[0]
        gem = None
        if 'telgeo.tvg' in os.listdir(gpath):
            with open(os.path.join(gpath, 'telgeo.tvg'), 'rb') as geo:
                gem = geo.read().decode('utf-8')
            if '{' == gem[0] and '}' == gem[-1]:
                gem = eval(gem)
                self.root.geometry(gem['geo'])
                Reminder.RESZ = gem['geo']
        del gpath
        del gem
        self.root.protocol('WM_DELETE_WINDOW', self.winexit)
        self.root.bind_all('<Control-p>', self.paste)
        self.root.bind_all('<Control-c>', self.copc)
        self.root.bind_all('<Control-x>', self.clear)
        self.seconds = None
        self.langs = None
        self.chacc = None
        self.lock = False
        self.afterid = None
        self.api_id = cp.readcpd(Reminder.API)
        self.api_hash = cp.readcpd(Reminder.HASH_)
        self.users = {}
        self.frm1 = ttk.Frame(self.root)
        self.frm1.pack(fill = 'x')
        self.lab1 = ttk.Label(self.frm1, text = 'To:', justify = RIGHT)
        self.lab1.pack(side = LEFT, padx = (2, 7), pady = 5)
        self.entto = ttk.Combobox(self.frm1)
        self.entto.pack(side = LEFT, pady = 5, padx = (0, 5), fill = 'x', expand = 1)
        self.entto.bind('<KeyRelease>', self.tynam)
        self.frm2 = ttk.Frame(self.root)
        self.frm2.pack(fill = 'x')
        self.bem = Button(self.frm2, text = 'EMOJI', font = 'consolas 11 bold', 
                          relief = GROOVE, command = self.emj, width = 4)
        self.bem.pack(side = LEFT, padx = 2, pady = (0, 5), fill = 'x', expand = 1)        
        self.bup = Button(self.frm2, text = 'PASTE', font = 'consolas 11 bold', 
                          relief = GROOVE, command = self.paste, width = 4)
        self.bup.pack(side = LEFT, padx = 2, pady = (0, 5), fill = 'x', expand = 1)
        self.buo = Button(self.frm2, text = 'COPIED', font = 'consolas 11 bold', 
                          relief = GROOVE, command = self.copc, width = 4)
        self.buo.pack(side = LEFT, padx = 2, pady = (0, 5), fill = 'x', expand = 1)        
        self.buc = Button(self.frm2, text = 'CLEAR', font = 'consolas 11 bold', 
                          relief = GROOVE, command = self.clear, width = 4)
        self.buc.pack(side = LEFT, padx = 2, pady = (0, 5), fill = 'x', expand = 1)      
        self.bsel = Button(self.frm2, text = 'MULTI', font = 'consolas 11 bold', 
                          relief = GROOVE, command = self.multiselect, width = 4)
        self.bsel.pack(side = LEFT, padx = 2, pady = (0, 5), fill = 'x', expand = 1)
        self.bedm = Button(self.frm2, text = 'ED MULTI', font = 'consolas 11 bold', 
                          relief = GROOVE, command = self.editmu, width = 4)
        self.bedm.pack(side = LEFT, padx = 2, pady = (0, 5), fill = 'x', expand = 1)
        self.bau = Button(self.frm2, text = 'AUTO SAVE', font = 'consolas 11 bold', 
                          relief = GROOVE, command = self.rectext, width = 4)
        self.bau.pack(side = LEFT, padx = 2, pady = (0, 5), fill = 'x', expand = 1)
        self.bds = Button(self.frm2, text = 'DEL REPLY', font = 'consolas 11 bold', 
                          relief = GROOVE, command = self.delscreen, width = 4)
        self.bds.pack(side = LEFT, padx = 2, pady = (0, 5), fill = 'x', expand = 1)
        self.frll = Frame(self.root)
        self.frll.pack(fill = 'x', padx = 2)
        self.frsp = ttk.Frame(self.root)
        self.frsp.pack(fill = 'x')        
        self.spl1 = ttk.Label(self.frsp, text = 'Days')
        self.spl1.pack(side = LEFT, pady = (0, 5), padx = (2, 0))
        self.sp1 = Spinbox(self.frsp, from_ = 0, to = 365, justify = 'center')
        self.sp1.config(state = 'readonly')
        self.sp1.pack(side = LEFT, pady = (0, 5), padx = (0, 5), fill = 'x', expand = 1)
        self.spl2 = ttk.Label(self.frsp, text = 'Hours')
        self.spl2.pack(side = LEFT, pady = (0, 5), padx = (0, 5))
        self.sp2 = Spinbox(self.frsp, from_ = 0, to = 24, justify = 'center')
        self.sp2.config(state = 'readonly')
        self.sp2.pack(side = LEFT, pady = (0, 5), padx = (0, 5), fill = 'x', expand = 1)
        self.spl3 = ttk.Label(self.frsp, text = 'Minutes')
        self.spl3.pack(side = LEFT, pady = (0, 5), padx = (0, 5))
        self.sp3 = Spinbox(self.frsp, from_ = 0, to = 60, justify = 'center')
        self.sp3.config(state = 'readonly')
        self.sp3.pack(side = LEFT, pady = (0, 5), padx = (0, 5), fill = 'x', expand = 1)
        self.spl4 = ttk.Label(self.frsp, text = 'Seconds')
        self.spl4.pack(side = LEFT, pady = (0, 5), padx = (0, 5))
        self.sp4 = Spinbox(self.frsp, from_ = 5, to = 60, justify = 'center')
        self.sp4.config(state = 'readonly')
        self.sp4.pack(side = LEFT, pady = (0, 5), padx = (0, 3), fill = 'x', expand = 1)        
        self.frms = ttk.Frame(self.root)
        self.frms.pack(fill = 'x')
        self.schb = Button(self.frms, text = 'S C H E D U L E R  S E N D', 
                           command = self.runsend, font = 'consolas 12 bold', relief = GROOVE)
        self.schb.pack(padx = 2, pady = (0, 5), fill = 'x', expand = 1)
        self.frm3 = Frame(self.root)
        self.frm3.pack(fill = 'both')
        self.text = Text(self.frm3, font = '-*-Segoe-UI-Emoji-*--*-153-*', pady = 3, padx = 5, 
                         relief = FLAT, wrap = 'word', height = 12)
        self.text.pack(side = LEFT, padx = (2,0), pady = (0, 5), fill = 'both', expand = 1)
        self.scroll = Scrollbar(self.frm3)
        self.scroll.pack(side = RIGHT, fill = 'y', padx = (0,2), pady = (0, 5))
        self.scroll.config(command = self.text.yview)
        self.text.config(yscrollcommand = self.scroll.set)
        self.frbs = Frame(self.root)
        self.frbs.pack(fill = 'x')
        self.sbut = Button(self.frbs, text = 'S E N D  N O W', command = self.sentem, 
                           font = 'consolas 12 bold', relief = GROOVE, width = 4)
        self.sbut.pack(side =  LEFT, padx = 2, pady = (0, 5), fill = 'x', expand = 1)
        self.busf = Button(self.frbs, text = 'S E N D  F I L E', command = self.sf, 
                           font = 'consolas 12 bold', relief = GROOVE, width = 4)
        self.busf.pack(side =  RIGHT, padx = (0, 2), pady = (0, 5), fill = 'x', expand = 1)
        self.busf = Button(self.frbs, text = 'S E N D  M U L T I', command = self.multisend, 
                           font = 'consolas 12 bold', relief = GROOVE, width = 4)
        self.busf.pack(side =  RIGHT, padx = (0, 2), pady = (0, 5), fill = 'x', expand = 1)        
        self.frm4 = Frame(self.root)
        self.frm4.pack(fill = 'both', expand = 1)
        self.text2 = Text(self.frm4, font = '-*-Segoe-UI-Emoji-*--*-153-*', pady = 3, padx = 5, 
                         relief = FLAT, wrap = 'word', height = 12)
        self.text2.pack(side = LEFT, padx = (2,0), pady = (0, 5), fill = 'both', expand = 1)
        self.scroll2 = Scrollbar(self.frm4)
        self.scroll2.pack(side = RIGHT, fill = 'y', padx = (0,2), pady = (0, 5))
        self.scroll2.config(command = self.text2.yview)
        self.text2.config(yscrollcommand = self.scroll2.set)
        self.text2.config(state = 'disable')
        self.text.bind('<KeyRelease-space>', self.autotext)
        self.text.bind('<Double-Button-1>', self.stopauto)
        self.frgr = Frame(self.root)
        self.frgr.pack(fill = 'both')
        self.bugr = Button(self.frgr, text = 'G E T  R E P L Y', command = self.getrep, 
                           font = 'consolas 12 bold', relief = GROOVE, width = 4)
        self.bugr.pack(side = LEFT, padx = 2, pady = (0, 5), fill = 'both', expand = 1)
        self.bugf = Button(self.frgr, text = 'G E T  F I L E', command = self.gf, 
                           font = 'consolas 12 bold', relief = GROOVE, width = 4)
        self.bugf.pack(side = RIGHT, padx = (0, 2), pady = (0, 5), fill = 'both', expand = 1)        
        self.entto.focus()
        self.auto = {}
        if 'auto.tvg' in os.listdir(os.getcwd().rpartition('\\')[0]):
            with open(os.path.join(os.getcwd().rpartition('\\')[0], 'auto.tvg')) as aur:
                rd = aur.read()
            if '{' in rd[0] and '}' in rd[-1]:
                rd = eval(rd)
                self.auto = rd
            else:
                os.remove(os.path.join(os.getcwd().rpartition('\\')[0], 'auto.tvg'))
                messagebox.showwarning('TeleTVG', 'The file has been corrupted and removed!!!', parent = self.root)
                
    def stopauto(self, event = None):
        # Disable autotext
        
        if Reminder.STOP_A:
            Reminder.STOP_A = False
            self.messages('<<Auto-Text>>\n\nis enabled!', 700)
        else:
            Reminder.STOP_A = True
            self.messages('<<Auto-Text>>\n\nis disabled!', 700)
            
    def messages(self, m: str, t_out: int):
        # Message for informing.
        
        def exit(event = None):
            root.destroy()        
        root = Toplevel(self.root)
        root.after(t_out, exit)
        root.attributes('-topmost', 1)
        wd = int(root.winfo_screenwidth()/2 - 250/2)
        hg = int(root.winfo_screenheight()/3 - 250/3)
        root.geometry(f'300x300+{wd}+{hg}')
        root.overrideredirect(1)
        a = Message(master= root)
        a.pack()
        a.tk_strictMotif(1)
        frm = Frame(a, borderwidth = 7, bg = 'dark blue', width = 250, height = 250)
        frm.pack(fill = 'both', expand = 1)
        tx = m
        lab = Label(frm, text = tx, justify = 'center', anchor = 'center', font = 'verdana 15 bold', width = 250, height = 250, bg = 'gold', fg = 'black')
        lab.pack(fill = 'both', expand = 1)
    
    def rectext(self):
        # Autotext saving with format: 
        # <text>::<text>\n
        # text [space] expanded
        
        if self.text.get('0.1', END)[:-1]:
            ask = messagebox.askyesno('TeleTVG', '"Yes" save autotext or "No" to delete', parent = self.root)
            if ask:
                ck = [i for i in self.text.get('0.1', END).split('\n') if i]
                collect = [tuple([k.partition('::')[0].strip(), k.partition('::')[2].strip()]) for k in ck if '::' in k]
                if len(ck) == len(collect):
                    del ck
                    self.auto = {}
                    if 'auto.tvg' not in os.listdir(os.getcwd().rpartition('\\')[0]):
                        with open(os.path.join(os.getcwd().rpartition('\\')[0], 'auto.tvg'), 'w') as aur:
                            aur.write(str(dict(collect)))
                        self.auto = dict(collect)
                    else:
                        with open(os.path.join(os.getcwd().rpartition('\\')[0], 'auto.tvg')) as aur:
                            rd = aur.read()
                        if '{' in rd[0] and '}' in rd[-1]:
                            rd = eval(rd)
                            with open(os.path.join(os.getcwd().rpartition('\\')[0], 'auto.tvg'), 'w') as aur:
                                aur.write(str(rd | dict(collect)))
                            self.auto = rd | dict(collect)
                        else:
                            with open(os.path.join(os.getcwd().rpartition('\\')[0], 'auto.tvg'), 'w') as aur:
                                aur.write(str(dict(collect)))
                            self.auto = dict(collect)                            
                            messagebox.showwarning('TeleTVG', 'The file has been corrupted and recreated new!!!', parent = self.root)
                    del collect
                    self.text.delete('1.0', END)
                else:
                    del ck
                    del collect
                    messagebox.showinfo('TeleTVG', 'No autotext recorded (please check the format)!', parent = self.root)
            else:
                if 'auto.tvg' in os.listdir(os.getcwd().rpartition('\\')[0]):
                    with open(os.path.join(os.getcwd().rpartition('\\')[0], 'auto.tvg')) as aur:
                        rd = aur.read()
                    if '{' in rd[0] and '}' in rd[-1]:                        
                        rd = eval(rd)
                        def sure(event):
                            try:
                                if event.char in string.ascii_letters:
                                    if event.widget.get():
                                        idx = event.widget.index(INSERT)
                                        gt = event.widget.get()
                                        event.widget.delete(0, END)
                                        event.widget.insert(0, gt[:idx])
                                        if event.widget.get():
                                            for name in rd:
                                                if event.widget.get().title() in name.title() and name.title().startswith(event.widget.get().title()[0]):
                                                    event.widget.delete(0, END)
                                                    event.widget.insert(END, f'{name}: {rd[name]}')
                                                    MyDialog.am.see(list(rd).index(name))
                                        event.widget.icursor(index = idx)
                            except Exception as e:
                                messagebox.showwarning('TeleTVG', f'{e}', parent = self.root)

                        class MyDialog(simpledialog.Dialog):
                            am = None
                            def body(self, master):
                                self.title('Select Autotext')
                                fr1 = ttk.Frame(master)
                                fr1.pack()
                                Label(fr1, text="Text: ").pack(side = LEFT)
                                self.e1 = Listbox(fr1, selectmode = MULTIPLE)
                                for i in rd:
                                    self.e1.insert(END,f'{i}: {rd[i]}')
                                self.e1.pack(side = LEFT)
                                MyDialog.am = self.e1
                                self.sce1 = ttk.Scrollbar(fr1, orient = 'vertical')
                                self.sce1.pack(side = RIGHT, fill = 'y')
                                self.sce1.config(command = self.e1.yview)
                                self.e1.config(yscrollcommand = self.sce1.set)
                                fr2 = ttk.Frame(master)
                                fr2.pack(anchor = W)
                                Label(fr2, text = 'Search:').pack(side = LEFT)
                                self.e3 = Entry(fr2)
                                self.e3.pack(side = RIGHT)
                                self.e3.bind('<KeyRelease>', sure)
                    
                            def apply(self):
                                self.result = [list(rd)[int(i)] for i in self.e1.curselection()]
                    
                        d = MyDialog(self.root)
                        if d.result:
                            for i in d.result:
                                del rd[i]
                            if rd:
                                with open(os.path.join(os.getcwd().rpartition('\\')[0], 'auto.tvg'), 'w') as aur:
                                    aur.write(str(rd))
                            else:
                                os.remove(os.path.join(os.getcwd().rpartition('\\')[0], 'auto.tvg'))
                        else:
                            messagebox.showinfo('TeleTVG', 'Deleteion of autotext aborted!', parent = self.root)
                    else:
                        messagebox.showerror('TeleTVG', 'File has been corrupted!!!', parent = self.root)
        else:
            messagebox.showinfo('TeleTVG', 'No autotext to record!', parent = self.root)
            
    def autotext(self, event = None):
        # Autotext algorithm:
        # text [space] expanded
        
        if Reminder.STOP_A is False:
            if 'text' in str(self.root.focus_get()):
                if self.text.get('0.1', END)[:-1]:
                    if self.auto:
                        vpox = self.text.get(f'{INSERT} linestart', f'{INSERT}-1c').split(' ')[-1]
                        if vpox in list(self.auto):
                            self.text.delete(f'{INSERT}-{len(vpox)+1}c', f'{INSERT}')
                            self.text.insert(f'{INSERT}', self.auto[vpox]+' ')
                        del vpox
                            
    def tynam(self, event = None):
        # To predict the key-in typing in "To" combobox.
        
        try:
            if event.char in string.ascii_letters:
                if self.entto.get():
                    idx = self.entto.index(INSERT)
                    gt = self.entto.get()
                    self.entto.delete(0, END)
                    self.entto.insert(0, gt[:idx])
                    if self.entto.get():
                        for name in self.users:
                            if self.entto.get().title() in name.title() and name.title().startswith(self.entto.get().title()[0]):
                                self.entto.current(sorted(list(self.users)).index(name))
                    self.entto.icursor(index = idx)
        except Exception as e:
            messagebox.showwarning('TeleTVG', f'{e}', parent = self.root)
        
    def emj(self):
        # Emoji window.
        
        emo.main(self, Reminder.EMOP)
        
    def winexit(self):
        # Will close ReminderTel and Emoji window as well.

        ori = os.getcwd().rpartition('\\')[0]
        if str(self.root.winfo_geometry()) == Reminder.RESZ:
            with open(os.path.join(ori, 'telgeo.tvg'), 'wb') as geo:
                geo.write(str({'geo': Reminder.RESZ}).encode())
        else:
            ask = messagebox.askyesno('TeleTVG', "Do you want to set your new window's position?")
            if ask:
                with open(os.path.join(ori, 'telgeo.tvg'), 'wb') as geo:
                    geo.write(str({'geo': str(self.root.winfo_geometry())}).encode())
            else:
                with open(os.path.join(ori, 'telgeo.tvg'), 'wb') as geo:
                    geo.write(str({'geo': Reminder.RESZ}).encode())
        del ori
        if self.afterid:
            self.root.after_cancel(self.afterid)
        if emo.Emo.status is False:
            emo.Emo.status = True
            emo.Emo.paste = None
            emo.Emo.mainon.destroy()
        if 's_error.tvg' in os.listdir(Reminder.DEST.rpartition('\\')[0]):
            Reminder.MAINST.root.destroy()
            self.root.destroy()
        else:
            os.chdir(Reminder.DEST)
            Reminder.STATUS = False
            Reminder.DEST = None
            Reminder.MAINST.free()
            Reminder.MAINST.root.deiconify()
            Reminder.MAINST.root.geometry(Reminder.GEO)
            Reminder.GEO = None
            Reminder.MAINST = None
            self.root.destroy()
        
    def paste(self, event = None):
        # Paste any copied text.

        try:
            p = self.root.clipboard_get()
            if p:
                ask = messagebox.askyesno('TeleTVG', 'Do you want to paste text?', parent = self.root)
                if ask:
                    self.text.delete('1.0', END)
                    self.text.insert(END, p)
                    self.root.clipboard_clear()
        except:
            pass
    
    def copc(self, event = None):
        # Copied text and delete them on screen.

        if self.text.get('1.0', END)[:-1]:
            if self.text.tag_ranges('sel'):
                self.root.clipboard_clear()
                self.root.clipboard_append(self.text.selection_get())
                self.text.tag_remove('sel', 'sel.first', 'sel.last')
                self.text.mark_set('insert', INSERT)
                messagebox.showinfo('TeleTVG', 'Selected text has been copied!', parent = self.root)
            else:
                self.root.clipboard_clear()
                self.root.clipboard_append(self.text.get('1.0', END)[:-1])
                messagebox.showinfo('TeleTVG', 'The text has been copied!', parent = self.root)
    
    def clear(self, event = None):
        # Clear screen.
        
        if self.text.get('1.0', END)[:-1]:
            ask = messagebox.askyesno('TeleTVG', 'Do you want to clear the text?', parent = self.root)
            if ask:
                self.text.delete('1.0', END)
                
    async def runs(self, sch: dict):
        # Run Scheduler to send Telegram
        
        gms = int(len(self.text.get('1.0', END)[:-1])/4096)
        async with TelegramClient('ReminderTel', self.api_id, self.api_hash) as client:
            try:
                await client.connect()
                if gms == 0:
                    await client.send_message(self.users[self.entto.get()], self.text.get('1.0', END)[:-1], 
                                              schedule = timedelta(days = sch['days'], 
                                                                   hours = sch['hours'],
                                                                   minutes = sch['minutes'],
                                                                   seconds = sch['seconds']))
                else:
                    orm = self.text.get('1.0', END)[:-1].split('\n')
                    while orm:
                        getm = ''
                        num = 0
                        for i in range(len(orm)):
                            if len(getm) + (len(orm[i])+1) < 4090:
                                getm += ''.join(orm[i]+'\n')
                            else:
                                num = i
                                break
                        await client.send_message(self.users[self.entto.get()], getm,
                                                      schedule = timedelta(days = sch['days'], 
                                                                           hours = sch['hours'],
                                                                           minutes = sch['minutes'],
                                                                           seconds = sch['seconds']))
                        if num:
                            orm = orm[i:]
                            continue
                        else:
                            break
                await client.disconnect()
                ct = timedelta(days = sch['days'], hours = sch['hours'], minutes = sch['minutes'], seconds = sch['seconds'])
                ct = str(dt.today().replace(microsecond = 0) + ct)
                tms = f'Message schedule sent at {ct}'
                messagebox.showinfo('TeleTVG', tms, parent = self.root)
            except:
                await client.disconnect()
                messagebox.showinfo('TeleTVG', f'\n{sys.exc_info()}\n\n{msg}', parent = self.root) 
            
    def runsend(self):
        # Asyncio method of calling for running schedulers.
        
        if self.entto.get():
            if self.text.get('1.0', END)[:-1]:
                stm = dict(days = eval(self.sp1.get()), 
                           hours = eval(self.sp2.get()), 
                           minutes = eval(self.sp3.get()), 
                           seconds = eval(self.sp4.get()),
                           )        
                asyncio.get_event_loop().run_until_complete(self.runs(stm))
            else:
                messagebox.showinfo('TeleTVG', 'Please write message!', parent = self.root)
        else:
            messagebox.showinfo('TeleTVG', 'Please fill "To"!', parent = self.root)            
                
    async def sent(self, event =  None):
        # Sending Telegram to anyone.
        
        try:
            gms = int(len(self.text.get('1.0', END)[:-1])/4096)
            async with TelegramClient('ReminderTel', self.api_id, self.api_hash) as client:
                await client.connect()
                if gms == 0:
                    await client.send_message(self.users[self.entto.get()], self.text.get('1.0', END)[:-1])
                else:
                    orm = self.text.get('1.0', END)[:-1].split('\n')
                    while orm:
                        getm = ''
                        num = 0
                        for i in range(len(orm)):
                            if len(getm) + (len(orm[i])+1) < 4090:
                                getm += ''.join(orm[i]+'\n')
                            else:
                                num = i
                                break
                        await client.send_message(self.users[self.entto.get()], getm)
                        if num:
                            orm = orm[i:]
                            continue
                        else:
                            break
                await client.disconnect()
            self.text.delete('1.0', END)
        except:
            messagebox.showinfo('TeleTVG', f'\n{sys.exc_info()}', parent = self.root)
            await client.disconnect()
            
    def sentem(self):
        # Asyncio method of calling for sending message at once.
        
        if self.entto.get():
            if self.text.get('1.0', END)[:-1]:
                asyncio.get_event_loop().run_until_complete(self.sent())
                if self.afterid:
                    self.root.after_cancel(self.afterid)
                asyncio.get_event_loop().run_until_complete(self.rep())
            else:
                messagebox.showinfo('TeleTVG', 'Please write message!', parent = self.root)
        else:
            messagebox.showinfo('TeleTVG', 'Please fill "To" first!', parent = self.root)            
            
    async def sentfile(self, filename: str):
        # Sending file to user.
        
        try:
            async with TelegramClient('ReminderTel', self.api_id, self.api_hash) as client:
                await client.connect()
                await client.send_file(self.users[self.entto.get()], filename, caption = 'TreeViewGui')
                await client.disconnect()
            tms = f'Message finished sent at {dt.isoformat(dt.now().replace(microsecond = 0)).replace("T", " ")}'
            messagebox.showinfo('TeleTVG', tms, parent = self.root)
        except:
            messagebox.showinfo('TeleTVG', f'\n{sys.exc_info()}', parent = self.root)
            await client.disconnect()
    
    def sf(self):
        # Sending file using asyncio call
        
        if self.entto.get():
            fpt = os.path.join(os.getcwd().rpartition('\\')[0], 'TVGPro')
            ask = filedialog.askopenfilename(initialdir = fpt, filetypes = [("Encryption file","*_protected.txt")], parent = self.root)
            if ask:
                asyncio.get_event_loop().run_until_complete(self.sentfile(ask))
            else:
                messagebox.showinfo('TeleTVG', 'Send file is aborted!', parent = self.root)            
        else:
            messagebox.showinfo('TeleTVG', 'Please fill "To" first!', parent = self.root)        
    
    async def rep(self):
        # Getting reply from a user [get the last 10 messages]
        
        async with TelegramClient('ReminderTel', self.api_id, self.api_hash) as client:
            await client.connect()
            self.text2.config(state = 'normal')
            self.text2.delete('1.0', END)
            async for message in client.iter_messages(self.users[self.entto.get()], 10):
                if message.out:
                    td = dt.ctime(dt.astimezone(message.date))
                    self.text2.insert(END, f'{td}\n')
                    self.text2.insert(END, f'{message.text}\n\n')
                else:
                    td = dt.ctime(dt.astimezone(message.date))
                    self.text2.insert(END, f'{td} [{self.entto.get()}]\n')
                    self.text2.insert(END, f'{message.text}\n\n')
            self.text2.config(state = 'disable')
            await client.disconnect()
        self.afterid = self.root.after(60000, self.getrep)        
                
    def getrep(self):
        # Asyncio method of calling for getting reply.
        
        if self.entto.get():
            if self.afterid:
                self.root.after_cancel(self.afterid)
            asyncio.get_event_loop().run_until_complete(self.rep())
            self.messages('<<<TeleTVG>>>\n\nGet Reply\n\nhas been updated!', 1200)
        else:
            messagebox.showinfo('TeleTVG', 'Please fill "To" first!', parent = self.root)
            
    def delscreen(self):
        if self.afterid:
            self.root.after_cancel(self.afterid)
        self.text2.config(state = 'normal')
        self.text2.delete('1.0', END)
        self.text2.config(state = 'disabled')
            
    async def getfile(self):
        # Getting file from a user [get all TVG protected text file]
                   
        path = os.path.join(os.getcwd().rpartition('\\')[0],'TVGPro')
        async with TelegramClient('ReminderTel', self.api_id, self.api_hash) as client:
            try:
                await client.connect()
                num = 0
                async for message in client.iter_messages(self.users[self.entto.get()], None):
                    if message.media:
                        if isinstance(message.media, types.MessageMediaDocument) and isinstance(message.media.document.attributes[0], types.DocumentAttributeFilename):
                            num += 1
                            await client.download_media(message, path)
                            await client.delete_messages(entity = None, message_ids = message)
                await client.disconnect()
            except:
                await client.disconnect()
                messagebox.showerror('TeleTVG', f'{sys.exc_info()[1]}', parent = self.root)
            finally:
                if num:
                    ask = messagebox.askyesno('TeleTVG', f'You have download {num} files, want to open file folder?')
                    if ask:
                        os.startfile(path)
                        
    def gf(self):
        # Starting running asyncio get file.
        
        if self.entto.get():
            asyncio.get_event_loop().run_until_complete(self.getfile())
        else:
            messagebox.showinfo('TeleTVG', 'Please fill "To" first!', parent = self.root)        
            
    async def filcomb(self):
        # Intitiate filling contacts and languages.
        
        async with TelegramClient('ReminderTel', self.api_id, self.api_hash) as client:
            await client.connect()
            result = await client(functions.contacts.GetContactsRequest(hash=0))
            mypro = await client.get_me()
            await client.disconnect()
            if mypro.last_name:
                self.root.title(f'TeleTVG-{mypro.first_name} {mypro.last_name}')
            else:
                self.root.title(f'TeleTVG-{mypro.first_name}')
            self.users = {}
            self.langs = None
            for user in result.users:
                if user.username:
                    if user.last_name:
                        self.users[f'{user.first_name} {user.last_name}'] = f'@{user.username}'
                    else:
                        self.users[f'{user.first_name}'] = f'@{user.username}'
                else:
                    if user.last_name:
                        self.users[f'{user.first_name} {user.last_name}'] = f'+{user.phone}'
                    else:
                        self.users[f'{user.first_name}'] = f'+{user.phone}'
            self.entto.delete(0, END)
            self.entto['values'] = sorted(list(self.users))
            
    async def acc(self):
        # Checking account's folder.
        
        async with TelegramClient('ReminderTel', self.api_id, self.api_hash) as client:
            await client.connect()
            mypro = await client.get_me()
            await client.disconnect()
            ori = os.path.join(os.getcwd(), 'Telacc')
            self.chacc = f'{mypro.id}'
            if f'{mypro.id}' not in os.listdir(ori):
                os.mkdir(os.path.join(ori, f'{mypro.id}'))
                    
    def multiselect(self, event = None):
        # Select multiple recepients and save them under a group.
        
        if self.lock is False:
            self.lock = True
            users = sorted(list(self.users))
            def sure(event):
                try:
                    if event.char in string.ascii_letters:
                        if event.widget.get():
                            idx = event.widget.index(INSERT)
                            gt = event.widget.get()
                            event.widget.delete(0, END)
                            event.widget.insert(0, gt[:idx])
                            if event.widget.get():
                                for name in self.users:
                                    if event.widget.get().title() in name.title() and name.title().startswith(event.widget.get().title()[0]):
                                        event.widget.delete(0, END)
                                        event.widget.insert(END, name)
                                        MyDialog.am.see(sorted(list(self.users)).index(name))
                            event.widget.icursor(index = idx)
                except Exception as e:
                    messagebox.showwarning('TeleTVG', f'{e}', parent = self.root)
            
            class MyDialog(simpledialog.Dialog):
                am = None
                def body(self, master):
                    
                    self.title('Select users')
                    fr1 = ttk.Frame(master)
                    fr1.pack()
                    Label(fr1, text="Users: ").pack(side = LEFT)
                    self.e1 = Listbox(fr1, selectmode = MULTIPLE)
                    for i in users:
                        self.e1.insert(END, i)
                    self.e1.pack(side = LEFT)
                    MyDialog.am = self.e1
                    self.sce1 = ttk.Scrollbar(fr1, orient = 'vertical')
                    self.sce1.pack(side = RIGHT, fill = 'y')
                    self.sce1.config(command = self.e1.yview)
                    self.e1.config(yscrollcommand = self.sce1.set)
                    fr2 = ttk.Frame(master)
                    fr2.pack(anchor = W)
                    Label(fr2, text = 'Search:').grid(row = 0, column = 0, sticky = W)
                    self.e3 = Entry(fr2)
                    self.e3.grid(row = 0, column = 1)
                    self.e3.bind('<KeyRelease>', sure)
                    Label(fr2, text = 'Folder:').grid(row = 1, column = 0, sticky = W)
                    self.e2 = Entry(fr2)
                    self.e2.grid(row = 1, column = 1)
            
                def apply(self):
                    self.result = [users[int(i)] for i in self.e1.curselection()]
                    self.folder = self.e2.get()
                                
            d = MyDialog(self.root)
            self.lock = False
            if d.result is not None:
                dest = os.path.join('Telacc', self.chacc)
                mfold = os.path.join(dest, f'{d.folder}_group')            
                if d.result and d.folder:
                    if f'{d.folder}_group' not in os.listdir(dest):
                        os.mkdir(mfold)
                        with open(os.path.join(mfold,f'{d.folder}.json'), 'w') as fs:
                            mkc = {d.folder: d.result}
                            json.dump(mkc, fs)
                    else:
                        with open(os.path.join(mfold,f'{d.folder}.json')) as fs:
                            rd = dict(json.load(fs))
                            ou = rd[d.folder]
                            for u in d.result:
                                if u not in ou:
                                    ou.append(u)
                            rd[d.folder] = ou
                        with open(os.path.join(mfold,f'{d.folder}.json'), 'w') as wj:
                            json.dump(rd, wj)   
                elif d.folder:
                    if f'{d.folder}_group' in os.listdir(dest):
                        ask = messagebox.askyesno('TeleTVG', 'Do you want to delete this group?', parent = self.root)
                        if ask:
                            shutil.rmtree(mfold)
                        else:
                            messagebox.showinfo('TeleTVG', 'Deletion aborted!', parent = self.root)
                    else:
                        messagebox.showinfo('TeleTVG', 'Not created yet!', parent = self.root)
                else:
                    messagebox.showinfo('TeleTVG', 'Please create folder first!', parent = self.root)
                    
    def editmu(self):
        # To get Users in group for edit. [deleting users in group]
        
        if self.lock is False:        
            groups = [ i  for i in os.listdir(os.path.join('Telacc', self.chacc)) if '_group' in i ]
            if groups:
                self.lock = True
                class MyDialog(simpledialog.Dialog):
                
                    def body(self, master):
                        self.title('Choose Group')
                        Label(master, text="Group: ").grid(row=0, column = 0, sticky = E)
                        self.e1 = ttk.Combobox(master, state = 'readonly')
                        self.e1['values'] = groups
                        self.e1.current(0)
                        self.e1.grid(row=0, column=1)
                        return self.e1
                
                    def apply(self):
                        self.result = self.e1.get()
                                    
                d = MyDialog(self.root)
                if d.result:
                    path = os.path.join('Telacc', self.chacc, d.result,
                                        f'{d.result.partition("_")[0]}.json')
                    with open(path) as rd:
                        edt = dict(json.load(rd))
                        users = sorted(edt[d.result.partition("_")[0]])
                    class UserDialog(simpledialog.Dialog):
                        
                        def body(self, master):
                            self.title('Delete users')
                            fr1 = ttk.Frame(master)
                            fr1.pack()
                            Label(fr1, text="Users: ").pack(side = LEFT)
                            self.e1 = Listbox(fr1, selectmode = MULTIPLE)
                            for i in users:
                                self.e1.insert(END, i)
                            self.e1.pack(side = LEFT)
                            self.sce1 = ttk.Scrollbar(fr1, orient = 'vertical')
                            self.sce1.pack(side = RIGHT, fill = 'y')
                            self.sce1.config(command = self.e1.yview)
                            self.e1.config(yscrollcommand = self.sce1.set)
                    
                        def apply(self):
                            self.result = [users[int(i)] for i in self.e1.curselection()]
                                        
                    u = UserDialog(self.root)
                    self.lock = False
                    if u.result:
                        dus = [i for i in users if i not in u.result]
                        if dus:
                            edt[d.result.partition("_")[0]] = dus
                            with open(path, 'w') as wu:
                                json.dump(edt, wu)
                        else:
                            shutil.rmtree(os.path.join('Telacc', self.chacc, d.result))
                else:
                    self.lock = False
                    
    async def mulsend(self, sen, file = None):
        # Asyncio module of sending multiple.
        
        try:
            if file:
                async with TelegramClient('ReminderTel', self.api_id, self.api_hash) as client:
                    await client.connect()
                    await asyncio.gather(*[client.send_file(self.users[user], file, caption = 'TreeViewGui') for user in sen])
                    await client.disconnect()
            else:
                gms = int(len(self.text.get('1.0', END)[:-1])/4090)
                async with TelegramClient('ReminderTel', self.api_id, self.api_hash) as client:
                    await client.connect()
                    if gms == 0:
                        await asyncio.gather(*[client.send_message(self.users[user], self.text.get('1.0', END)[:-1]) for user in sen])
                    else:
                        orm = self.text.get('1.0', END)[:-1].split('\n')
                        while orm:
                            getm = ''
                            num = 0
                            for i in range(len(orm)):
                                if len(getm) + (len(orm[i])+1) < 4090:
                                    getm += ''.join(orm[i]+'\n')
                                else:
                                    num = i
                                    break
                            await asyncio.gather(*[client.send_message(self.users[user], getm) for user in sen])
                            if num:
                                orm = orm[i:]
                                continue
                            else:
                                break
                    await client.disconnect()
            tms = f'Message finished sent at {dt.isoformat(dt.now().replace(microsecond = 0)).replace("T", " ")}'
            messagebox.showinfo('TeleTVG', tms, parent = self.root)
        except:
            messagebox.showinfo('TeleTVG', f'\n{sys.exc_info()}', parent = self.root)
            await client.disconnect()        
        
    
    def multisend(self, event = None):
        # Multiple send message to group, like broadcast.
        
        if self.lock is False:        
            groups = [ i  for i in os.listdir(os.path.join('Telacc', self.chacc)) if '_group' in i ]
            if groups:
                if self.text.get('1.0', END)[:-1]:
                    sel = list(self.users)
                    self.lock = True
                    class MyDialog(simpledialog.Dialog):
                    
                        def body(self, master):
                            self.title('Choose Group')
                            Label(master, text="Group: ").grid(row=0, column = 0, sticky = E)
                            self.e1 = ttk.Combobox(master, state = 'readonly')
                            self.e1['values'] = groups
                            self.e1.current(0)
                            self.e1.grid(row=0, column=1)
                            return self.e1
                    
                        def apply(self):
                            self.result = self.e1.get()
                                        
                    d = MyDialog(self.root)
                    self.lock = False
                    if d.result:
                        tkd = os.path.join('Telacc', self.chacc, d.result, f'{d.result.rpartition("_")[0]}.json')
                        with open(tkd, 'r') as us:
                            rd = dict(json.load(us))
                        sen = [i for i in rd[d.result.rpartition("_")[0]] if i in sel]
                        if sen:
                            gf = messagebox.askyesno('TeleTVG', '"Yes" send message or "No" send file!')
                            if gf:
                                asyncio.get_event_loop().run_until_complete(self.mulsend(sen))
                            else:
                                askfile = filedialog.askopenfilename(initialdir = os.path.join(os.getcwd().rpartition('\\')[0], 'TVGPro'), filetypes = [("Encryption file","*_protected.txt")], parent = self.root)
                                if askfile:
                                    asyncio.get_event_loop().run_until_complete(self.mulsend(sen, askfile))
                                else:
                                    messagebox.showinfo('TeleTVG', 'Send files aborted!', parent = self.root)
                        else:
                            messagebox.showinfo('TeleTVG', 'This group is no longer exist, please delete it!', parent = self.root)
                else:
                    messagebox.showinfo('TeleTVG', 'No message to send?', parent = self.root)
                    
def main(stat, path, geo, message = None):
    # Start app.
    # Please create encryption for app_id and app_hash for security.
    
    api = filen("api_id_cpd.json").rpartition('_')[0]
    hash_ = filen("api_hash_cpd.json").rpartition('_')[0]    
    emj = filen("emoj.txt")
    ope = os.path.join(os.getcwd(), 's_error.tvg')
    if 'Tele_TVG' in os.listdir():
        os.chdir('Tele_TVG')
    else:
        os.mkdir('Tele_TVG')
        os.chdir('Tele_TVG')
    if api and hash_:      
        if 'Telacc' not in os.listdir():
            os.mkdir('Telacc')
        if Reminder.STATUS is False:              
            root = Tk()
            Reminder.STATUS = True
            Reminder.EMOP = emj
            Reminder.MAINST = stat
            Reminder.MAINST.root.withdraw()
            Reminder.DEST = path
            Reminder.GEO = geo
            Reminder.API = api
            Reminder.HASH_ = hash_
            begin = Reminder(root)
            if 'ReminderTel.session' not in os.listdir():
                api_id = cp.readcpd(api)
                api_hash = cp.readcpd(hash_)                
                ask = simpledialog.askstring('TeleTVG', 'Phone number:', show = '●', parent = begin.root)
                psd = simpledialog.askstring('TeleTVG', 'Password:', show = '●', parent = begin.root)
                if ask:
                    try:
                        if psd:
                            client = TelegramClient('ReminderTel', api_id, api_hash).start(ask, psd, code_callback = lambda: simpledialog.askstring('TeleTVG', 'code:', show = '⋆', parent = begin.root))
                        else:
                            client = TelegramClient('ReminderTel', api_id, api_hash).start(ask, code_callback = lambda: simpledialog.askstring('TeleTVG', 'code:', show = '⋆', parent = begin.root))
                        client.disconnect()
                        messagebox.showinfo('TeleTVG', 'Please Restart the app!')
                        begin.winexit()
                    except:
                        with open(ope, 'w') as ers:
                            ers.write(str(sys.exc_info()))
                        messagebox.showinfo('TeleTVG', sys.exc_info())
                        begin.winexit()
                else:
                    messagebox.showinfo('TeleTVG', 'Please log in first!')
                    begin.winexit()
            else:
                try:
                    asyncio.get_event_loop().run_until_complete(begin.acc())
                    asyncio.get_event_loop().run_until_complete(begin.filcomb())
                    begin.entto.focus_force()
                    if message:
                        begin.text.insert(END, message)
                    begin.root.mainloop()
                except:
                    with open(ope, 'w') as ers:
                        ers.write(str(sys.exc_info()))                    
                    messagebox.showerror('TreeViewGui', f'{sys.exc_info()}')
                    begin.winexit()
    else:
        # Please create api in telegram!
        
        root = Tk()
        root.withdraw()
        api = simpledialog.askstring('Key in api_id', 'api_id:', show = '*')
        if api:
            cp.createcpd(api, 'api_id', cp.createtoken(37,1))
            api = simpledialog.askstring('Key in api_hash', 'api_hash:', show = '*')
            if api:
                cp.createcpd(api, 'api_hash', cp.createtoken(37,1))
                messagebox.showinfo('TeleTVG', 'Please Restart Send Note!')
                root.destroy()
            else:
                messagebox.showinfo('TeleTVG', 'You need to start over again later!')
                root.destroy()
        else:
            root.destroy()  