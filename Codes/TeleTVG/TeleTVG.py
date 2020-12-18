# -*- coding: utf-8 -*-
#Copyright (c) 2020, KarjaKAK
#All rights reserved.

from CreatePassword import CreatePassword as cp
from telethon import TelegramClient
from telethon import functions
from telethon.tl import types
from tkinter import *
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime as dt
from Scheduler import Settimer as stm
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
    def __init__(self, root):
        self.root = root
        self.root.resizable(False, False)
        self.root.title('TeleTVG')
        self.wid = int(self.root.winfo_screenwidth()/2)
        self.hei = int(self.root.winfo_screenheight()/1.207)
        self.pwidth = int(self.root.winfo_screenwidth()/2 - self.wid/2)
        self.pheight = int(self.root.winfo_screenheight()/3 - self.hei/3)
        self.root.geometry(f'{self.wid}x{self.hei}+{self.pwidth}+{self.pheight}')
        self.root.protocol('WM_DELETE_WINDOW', self.winexit)
        self.root.bind_all('<Control-s>', self.chacct)
        self.root.bind_all('<Control-p>', self.paste)
        self.root.bind_all('<Control-c>', self.copc)
        self.root.bind_all('<Control-x>', self.clear)
        self.seconds = None
        self.langs = None
        self.chacc = None
        self.lock = False
        self.api_id = cp.readcpd("api_id")
        self.api_hash = cp.readcpd("api_hash")
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
        self.bem = Button(self.frm2, text = 'E M O J I', font = 'consolas 10 bold', 
                          relief = GROOVE, command = self.emj)
        self.bem.pack(side = LEFT, padx = 2, pady = (0, 5), fill = 'x', expand = 1)        
        self.bup = Button(self.frm2, text = 'P A S T E', font = 'consolas 10 bold', 
                          relief = GROOVE, command = self.paste)
        self.bup.pack(side = LEFT, padx = 2, pady = (0, 5), fill = 'x', expand = 1)
        self.buo = Button(self.frm2, text = 'C O P I E D', font = 'consolas 10 bold', 
                          relief = GROOVE, command = self.copc)
        self.buo.pack(side = LEFT, padx = 2, pady = (0, 5), fill = 'x', expand = 1)        
        self.buc = Button(self.frm2, text = 'C L E A R', font = 'consolas 10 bold', 
                          relief = GROOVE, command = self.clear)
        self.buc.pack(side = LEFT, padx = 2, pady = (0, 5), fill = 'x', expand = 1)      
        self.bsel = Button(self.frm2, text = 'M U L T I', font = 'consolas 10 bold', 
                          relief = GROOVE, command = self.multiselect)
        self.bsel.pack(side = LEFT, padx = 2, pady = (0, 5), fill = 'x', expand = 1)        
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
        self.schb = Button(self.frms, text = 'S C H E D U L E R  S E N D  T E L E G R A M', 
                           command = self.scheduler, font = 'consolas 12 bold', relief = GROOVE)
        self.schb.pack(padx = 2, pady = (0, 5), fill = 'x', expand = 1)
        self.frm3 = Frame(self.root)
        self.frm3.pack(fill = 'x')
        self.text = Text(self.frm3, font = '-*-Segoe-UI-Emoji-*--*-153-*', pady = 3, padx = 5, 
                         relief = FLAT, wrap = 'word', height = 12)
        self.text.pack(side = LEFT, padx = (5,0), pady = (0, 5), fill = 'both', expand = 1)
        self.scroll = Scrollbar(self.frm3)
        self.scroll.pack(side = RIGHT, fill = 'y', padx = (0,5), pady = (0, 5))
        self.scroll.config(command = self.text.yview)
        self.text.config(yscrollcommand = self.scroll.set)
        self.frbs = Frame(self.root)
        self.frbs.pack(fill = 'x')
        self.sbut = Button(self.frbs, text = 'S E N D  N O W', command = self.sentem, 
                           font = 'consolas 12 bold', relief = GROOVE)
        self.sbut.pack(side =  LEFT, padx = 2, pady = (0, 5), fill = 'x', expand = 1)
        self.busf = Button(self.frbs, text = 'S E N D  F I L E', command = self.sf, 
                           font = 'consolas 12 bold', relief = GROOVE)
        self.busf.pack(side =  RIGHT, padx = (0, 2), pady = (0, 5), fill = 'x', expand = 1)
        self.busf = Button(self.frbs, text = 'S E N D  M U L T I', command = self.multisend, 
                           font = 'consolas 12 bold', relief = GROOVE)
        self.busf.pack(side =  RIGHT, padx = (0, 2), pady = (0, 5), fill = 'x', expand = 1)        
        self.frm4 = Frame(self.root)
        self.frm4.pack(fill = 'x')
        self.text2 = Text(self.frm4, font = '-*-Segoe-UI-Emoji-*--*-153-*', pady = 3, padx = 5, 
                         relief = FLAT, wrap = 'word', height = 12)
        self.text2.pack(side = LEFT, padx = (5,0), pady = (0, 5), fill = 'both', expand = 1)
        self.scroll2 = Scrollbar(self.frm4)
        self.scroll2.pack(side = RIGHT, fill = 'y', padx = (0,5), pady = (0, 5))
        self.scroll2.config(command = self.text2.yview)
        self.text2.config(yscrollcommand = self.scroll2.set)
        self.text2.config(state = 'disable')
        self.frgr = Frame(self.root)
        self.frgr.pack(fill = 'x')
        self.bugr = Button(self.frgr, text = 'G E T  R E P L Y', command = self.getrep, 
                           font = 'consolas 12 bold', relief = GROOVE)
        self.bugr.pack(side = LEFT, padx = 2, pady = (0, 5), fill = 'x', expand = 1)
        self.bugf = Button(self.frgr, text = 'G E T  F I L E', command = self.gf, 
                           font = 'consolas 12 bold', relief = GROOVE)
        self.bugf.pack(side = RIGHT, padx = (0, 2), pady = (0, 5), fill = 'x', expand = 1)        
        self.entto.focus()
    
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
            messagebox.showwarning('ReminderTel', f'{e}', parent = self.root)
        
    def emj(self):
        # Emoji window.
        
        emo.main()
        
    def winexit(self):
        # Will close ReminderTel and Emoji window as well.
        
        if emo.Emo.status is False:
            emo.Emo.status = True
            emo.Emo.mainon.destroy()
        os.chdir(Reminder.DEST)
        Reminder.STATUS = False
        Reminder.DEST = None
        Reminder.MAINST.deiconify()
        Reminder.MAINST = None
        self.root.destroy()
        
    def paste(self, event = None):
        # Paste any copied text.

        try:
            p = self.root.clipboard_get()
            if p:
                ask = messagebox.askyesno('ReminderTel', 'Do you want to paste text?', parent = self.root)
                if ask:
                    self.text.delete('1.0', END)
                    self.text.insert(END, p)
                    self.root.clipboard_clear()
        except:
            pass
    
    def copc(self, event = None):
        # Copied text and delete them on screen.

        if self.text.get('1.0', END)[:-1]:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.text.get('1.0', END)[:-1])
            self.text.delete('1.0', END)
            messagebox.showinfo('ReminderTel', 'The text has been copied!', parent = self.root)
    
    def clear(self, event = None):
        # Clear screen.
        
        if self.text.get('1.0', END)[:-1]:
            ask = messagebox.askyesno('ReminderTel', 'Do you want to clear the text?', parent = self.root)
            if ask:
                self.text.delete('1.0', END)
        
    def scheduler(self, event = None):
        # Scheduling Telegram to be sent, using seconds.
        # - 60 = 1 minute
        # - 3600 = 1 hour
        # - 86400 = 1 day
        
        if self.entto.get():
            if self.text.get('1.0', END)[:-1]:
                try:
                    schd = {}
                    ask = stm(days = eval(self.sp1.get()), 
                              hours = eval(self.sp2.get()), 
                              minutes = eval(self.sp3.get()), 
                              seconds = eval(self.sp4.get()),
                              )
                    if ask:
                        tm = int(dt.timestamp(dt.today().replace(microsecond = 0)))
                        schd['schedule'] = tm + ask.settimer()
                        schd['to'] = self.entto.get()
                        schd['text'] = self.text.get('1.0', END)
                        with open(f'schedule_{tm}', 'wb') as scf:
                            scf.write(f'{schd}'.encode())
                        self.seconds = ask.scheduletk()
                        self.runsend(f'schedule_{tm}')
                    else:
                        messagebox.showinfo('ReminderTel', 'Schedule send message aborted!', parent = self.root)
                except:
                    messagebox.showinfo('ReminderTel', 'Please give number only!', parent = self.root)
            else:
                messagebox.showinfo('ReminderTel', 'Please write message!', parent = self.root)
        else:
            messagebox.showinfo('ReminderTel', 'Please fill "To"!', parent = self.root)
                    
    def schedulerun(self):
        # Rerun scheduler on the opening app.
        
        schedules = [i for i in os.listdir() if 'schedule_' in  i]
        if schedules:
            for i in schedules:
                with open(i, 'rb') as scr:
                    gtm = eval(scr.read().decode('utf-8'))
                    gtm = gtm['schedule']
                    nt = int(dt.timestamp(dt.today().replace(microsecond = 0)))
                if gtm <= nt:
                    self.runsend(i)
                else:
                    self.seconds = (gtm - nt) * 1000
                    self.runsend(i)
            messagebox.showinfo('ReminderTel', 'Schedule has been set previously, now running!', parent = self.root)
    
    async def runs(self, filename):
        # Run Scheduler to send Telegram
        
        with open(filename, 'rb') as rsc:
            sem = eval(rsc.read().decode('utf-8'))
        if dt.isoformat(dt.fromtimestamp(sem['schedule'])) <= dt.isoformat(dt.today().replace(microsecond=0)):
            gms = int(len(sem['text'])/4096)
            async with TelegramClient('ReminderTel', self.api_id, self.api_hash) as client:
                try:
                    await client.connect()
                    if gms == 0:
                        await client.send_message(self.users[sem['to']], sem['text'])
                    else:
                        orm = sem['text']
                        while orm:
                            if len(orm) > 4090:
                                await client.send_message(self.users[sem['to']], orm[:4091])
                                orm = orm[4091:]
                            else:
                                await client.send_message(self.users[sem['to']], orm)
                                orm = None
                    await client.disconnect()
                    os.remove(filename)
                    self.seconds = None
                    tms = f'Message finished sent at {dt.isoformat(dt.now().replace(microsecond = 0)).replace("T", " ")}'
                    messagebox.showinfo('ReminderTel', tms, parent = self.root)
                except:
                    await client.disconnect()
                    os.remove(filename)
                    self.seconds = None
                    msg = f'This file {filename} is deleted as well!'
                    messagebox.showinfo('ReminderTel', f'\n{sys.exc_info()}\n\n{msg}', parent = self.root)
        else:
            self.root.after(self.seconds, self.runsend, filename)        
            
    def runsend(self, filename):
        # Asyncio method of calling for running schedulers.
        
        asyncio.get_event_loop().run_until_complete(self.runs(filename))
                
    async def sent(self, event =  None):
        # Sending Telegram as Reminder to anyone.
        
        try:
            gms = int(len(self.text.get('1.0', END)[:-1])/4096)
            async with TelegramClient('ReminderTel', self.api_id, self.api_hash) as client:
                await client.connect()
                if gms == 0:
                    await client.send_message(self.users[self.entto.get()], self.text.get('1.0', END)[:-1])
                else:
                    orm = self.text.get('1.0', END)[:-1]
                    while orm:
                        if len(orm) > 4090:
                            await client.send_message(self.users[self.entto.get()], orm[:4091])
                            orm = orm[4091:]
                        else:
                            await client.send_message(self.users[self.entto.get()], orm)
                            orm = None
                await client.disconnect()
            tms = f'Message finished sent at {dt.isoformat(dt.now().replace(microsecond = 0)).replace("T", " ")}'
            messagebox.showinfo('ReminderTel', tms, parent = self.root)
        except:
            messagebox.showinfo('ReminderTel', f'\n{sys.exc_info()}', parent = self.root)
            await client.disconnect()
            
    def sentem(self):
        # Asyncio method of calling for sending message at once.
        
        if self.entto.get():
            if self.text.get('1.0', END)[:-1]:
                asyncio.get_event_loop().run_until_complete(self.sent())
            else:
                messagebox.showinfo('ReminderTel', 'Please write message!', parent = self.root)
        else:
            messagebox.showinfo('ReminderTel', 'Please fill "To" first!', parent = self.root)            
            
    async def sentfile(self):
        # Sending file to user.
        
        try:
            ask = filedialog.askopenfilename(filetypes = [("Encryption file","*_protected.txt")], parent = self.root)
            if ask:
                async with TelegramClient('ReminderTel', self.api_id, self.api_hash) as client:
                    await client.connect()
                    await client.send_file(self.users[self.entto.get()], ask, caption = 'TreeViewGui')
                    await client.disconnect()
                tms = f'Message finished sent at {dt.isoformat(dt.now().replace(microsecond = 0)).replace("T", " ")}'
                messagebox.showinfo('ReminderTel', tms, parent = self.root)
            else:
                messagebox.showinfo('ReminderTel', 'Send file is aborted!', parent = self.root)
        except:
            messagebox.showinfo('ReminderTel', f'\n{sys.exc_info()}', parent = self.root)
            await client.disconnect()
    
    def sf(self):
        # Sending file using asyncio call
        
        if self.entto.get():
            asyncio.get_event_loop().run_until_complete(self.sentfile())
        else:
            messagebox.showinfo('ReminderTel', 'Please fill "To" first!', parent = self.root)        
    
    async def rep(self):
        # Getting reply from a user [get the last 5 messages]
        
        async with TelegramClient('ReminderTel', self.api_id, self.api_hash) as client:
            await client.connect()
            self.text2.config(state = 'normal')
            self.text2.delete('1.0', END)
            async for message in client.iter_messages(self.users[self.entto.get()], 5):
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
                
    def getrep(self):
        # Asyncio method of calling for getting reply.
        
        if self.entto.get():
            asyncio.get_event_loop().run_until_complete(self.rep())
        else:
            messagebox.showinfo('ReminderTel', 'Please fill "To" first!', parent = self.root)
            
    async def getfile(self):
        # Getting file from a user [get the last 5 messages]
        
        ori = os.getcwd()
        mmd = []
        try:
            async with TelegramClient('ReminderTel', self.api_id, self.api_hash) as client:
                await client.connect()
                async for message in client.iter_messages(self.users[self.entto.get()], 5):
                    if message.media:
                        if isinstance(message.media.document.attributes[0], types.DocumentAttributeFilename):
                            takm = message.media.document.attributes[0].file_name
                            await client.download_media(message, takm)
                            mmd.append(takm)
                await client.disconnect()
        except:
            await client.disconnect()
            messagebox.showerror('TeleTVG', f'{sys.exc_info()}')
        finally:
            if mmd:
                os.chdir(ori[:ori.rfind('\\')])
                if not 'TeleFile' in os.listdir():
                    os.mkdir('TeleFile')
                    os.chdir('TeleFile')
                else:
                    os.chdir('TeleFile')                
                for med in mmd:
                    fname = os.path.join(ori, med)
                    if med not in os.listdir():
                        shutil.move(fname, os.getcwd())
                os.startfile(os.getcwd())
            
            os.chdir(ori)
            if mmd in os.listdir():
                os.remove(mmd)
                    
    def gf(self):
        # Starting running asyncio get file.
        
        if self.entto.get():
            asyncio.get_event_loop().run_until_complete(self.getfile())
        else:
            messagebox.showinfo('ReminderTel', 'Please fill "To" first!', parent = self.root)        
            
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
            ori = os.getcwd()
            os.chdir('Telacc')
            self.chacc = f'{mypro.id}'
            if f'{mypro.id}' not in os.listdir():
                os.mkdir(f'{mypro.id}')
            os.chdir(ori)
            
    
    async def accs(self):
        # Switching existing accounts.
        
        async with TelegramClient('ReminderTel', self.api_id, self.api_hash) as client:
            await client.connect()
            mypro = await client.get_me()
            await client.disconnect()
            ori = os.getcwd()
            if f'{mypro.id}' != self.chacc:
                shutil.move('ReminderTel.session', os.path.join(ori, 'Telacc', f'{mypro.id}'))
                shutil.move(os.path.join(ori, 'Telacc', self.chacc, 'ReminderTel.session'), ori)
    
    def newacc(self):
        # To get existing client stored.
        
        ori = os.getcwd()
        shutil.move('ReminderTel.session', os.path.join(ori, 'Telacc', self.chacc))
        self.winexit()
                    
    def chacct(self, event = None):
        # Choosing an account in existing accounts.
        
        if self.lock is False:
            self.lock = True
            accounts = os.listdir('Telacc')
            gid = accounts.index(self.chacc)
            accounts.append('New')
            class MyDialog(simpledialog.Dialog):
            
                def body(self, master):
                    self.title('Choose Account')
                    Label(master, text="Acc: ").grid(row=0, column = 0, sticky = E)
                    self.e1 = ttk.Combobox(master, state = 'readonly')
                    self.e1['values'] = accounts
                    self.e1.current(gid)
                    self.e1.grid(row=0, column=1)
                    return self.e1
            
                def apply(self):
                    self.result = self.e1.get()
                                
            d = MyDialog(self.root)
            self.lock = False
            if d.result:
                if d.result == 'New':
                    self.newacc()
                else:
                    self.chacc = d.result
                    asyncio.get_event_loop().run_until_complete(self.accs())
                    asyncio.get_event_loop().run_until_complete(self.filcomb())
    
    def multiselect(self, event = None):
        # Select multiple recepients and save them under a group.
        
        if self.lock is False:
            self.lock = True
            users = sorted(list(self.users))
            class MyDialog(simpledialog.Dialog):
                
                def body(self, master):
                    self.title('Select users')
                    Label(master, text="Users: ").grid(row = 0, column = 0, sticky = E)
                    self.e1 = Listbox(master, selectmode = MULTIPLE)
                    for i in users:
                        self.e1.insert(END, i)
                    self.e1.grid(row=0, column=1)
                    Label(master, text = 'Folder name:').grid(row = 1, column = 0, sticky = E)
                    self.e2 = Entry(master)
                    self.e2.grid(row = 1, column = 1)
            
                def apply(self):
                    self.result = self.e1.curselection()
                    self.folder = self.e2.get()
                                
            d = MyDialog(self.root)
            self.lock = False
            if d.result is not None:
                dest = os.path.join('Telacc', self.chacc)
                mfold = os.path.join(dest, f'{d.folder}_group')            
                if d.result and d.folder:
                    with open(f'{d.folder}.json', 'w') as fs:
                        mkc = {d.folder: d.result}
                        json.dump(mkc, fs)                
                    if f'{d.folder}_group' not in os.listdir(dest):
                        os.mkdir(mfold)
                    else:
                        os.remove(os.path.join(mfold, f'{d.folder}.json'))
                    shutil.move(f'{d.folder}.json', mfold)
                elif d.folder:
                    if f'{d.folder}_group' in os.listdir(dest):
                        ask = messagebox.askyesno('TeleTVG', 'Do you want to delete this group?')
                        if ask:
                            shutil.rmtree(mfold)
                        else:
                            messagebox.showinfo('TeleTVG', 'Deletion aborted!')
                    else:
                        messagebox.showinfo('TeleTVG', 'Not created yet!')
                else:
                    messagebox.showinfo('TeleTVG', 'Please create folder first!')
                    
    async def mulsend(self, sen):
        # Asyncio module of sending multiple.
        
        try:
            gms = int(len(self.text.get('1.0', END)[:-1])/4096)
            async with TelegramClient('ReminderTel', self.api_id, self.api_hash) as client:
                await client.connect()
                for user in sen:
                    if gms == 0:
                        await client.send_message(self.users[user], self.text.get('1.0', END)[:-1])
                    else:
                        orm = self.text.get('1.0', END)[:-1]
                        while orm:
                            if len(orm) > 4090:
                                await client.send_message(self.users[user], orm[:4091])
                                orm = orm[4091:]
                            else:
                                await client.send_message(self.users[user], orm)
                                orm = None
                await client.disconnect()
            tms = f'Message finished sent at {dt.isoformat(dt.now().replace(microsecond = 0)).replace("T", " ")}'
            messagebox.showinfo('ReminderTel', tms, parent = self.root)
        except:
            messagebox.showinfo('ReminderTel', f'\n{sys.exc_info()}', parent = self.root)
            await client.disconnect()        
        
    
    def multisend(self, event = None):
        # Multiple send message to group, like broadcast.
        
        groups = [ i  for i in os.listdir(os.path.join('Telacc', self.chacc)) if '_group' in i ]
        if groups:
            if self.text.get('1.0', END)[:-1]:
                sel = sorted(list(self.users))
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
                    sen = [sel[int(i)] for i in rd[d.result.rpartition("_")[0]]]
                    asyncio.get_event_loop().run_until_complete(self.mulsend(sen))
            else:
                messagebox.showinfo('TeleTVG', 'No message to send?')
                
def main(stat, path, message):
    # Start app.
    # Please create encryption for app_id and app_hash for security.
    
    ori = os.getcwd()
    files = [i for i in os.listdir() if '_cpd' in i]
    if "emoj.txt" in os.listdir():
        files.extend(["emoj.txt"])
    if 'Schedule' in os.listdir():
        os.chdir('Schedule')
    else:
        os.mkdir('Schedule')
        os.chdir('Schedule')
    if files:
        for file in files:
            shutil.move(os.path.join(ori, file), os.getcwd())
    files = [i for i in os.listdir() if '_cpd' in i]
    if len(files) == 2:
        if 'Telacc' not in os.listdir():
            os.mkdir('Telacc')
        if Reminder.STATUS is False:
            root = Tk()
            Reminder.STATUS = True
            Reminder.MAINST = stat
            Reminder.DEST = path
            begin = Reminder(root)
            begin.MAINST.withdraw()
            api_id = cp.readcpd("api_id")
            api_hash = cp.readcpd("api_hash")            
            if 'ReminderTel.session' not in os.listdir():
                ask = simpledialog.askstring('ReminderTel', 'Phone number:', show = '●', parent = begin.root)
                psd = simpledialog.askstring('ReminderTel', 'Password:', show = '●', parent = begin.root)
                if ask:
                    try:
                        if psd:
                            client = TelegramClient('ReminderTel', api_id, api_hash).start(ask, psd, code_callback = lambda: simpledialog.askstring('ReminderTel', 'code:', show = '⋆', parent = begin.root))
                        else:
                            client = TelegramClient('ReminderTel', api_id, api_hash).start(ask, code_callback = lambda: simpledialog.askstring('ReminderTel', 'code:', show = '⋆', parent = begin.root))
                        client.disconnect()
                        messagebox.showinfo('ReminderTel', 'Please Restart the app!')
                        begin.winexit()
                    except:
                        messagebox.showinfo('ReminderTel', sys.exc_info())
                        begin.winexit()
                else:
                    messagebox.showinfo('ReminderTel', 'Please log in first!')
                    begin.winexit()
            else:
                try:
                    asyncio.get_event_loop().run_until_complete(begin.acc())
                    asyncio.get_event_loop().run_until_complete(begin.filcomb())
                    begin.schedulerun()
                    begin.entto.focus_force()
                    begin.text.insert(END, message)
                    begin.root.mainloop()
                except:
                    messagebox.showerror('TreeViewGui', f'{sys.exc_info()}')
                    begin.winexit()