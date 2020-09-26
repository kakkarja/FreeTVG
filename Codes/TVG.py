# Copyright © kakkarja (K A K)

from tkinter import *
from tkinter import ttk
from tkinter import simpledialog, messagebox, filedialog
from TreeView import TreeView as tv
import types
import os
import locale

class TreeViewGui:
    """
    This is the Gui for TreeView engine. This gui is to make the Writing and editing is viewable.
    """
    DB = None
    FREEZE = False
    def __init__(self, root, filename):
        super().__init__()
        self.filename = filename
        self.root = root
        self.root.title(f'{os.getcwd()}\\{self.filename}.txt')
        self.wwidth = self.root.winfo_reqwidth()
        self.wheight = self.root.winfo_reqheight()
        self.pwidth = int(self.root.winfo_screenwidth()/10 - self.wwidth/10)
        self.pheight = int(self.root.winfo_screenheight()/10 - self.wheight/10)
        self.root.geometry(f"+{self.pwidth}+{self.pheight}")        
        self.root.resizable(False, False)
        self.root.bind_all('<Control-f>', self.fcsent)
        self.root.bind_all('<Control-r>', self.fcsent)
        self.root.bind_all('<Control-t>', self.fcsent)
        self.root.bind_all('<Control-i>', self.fcsent)
        self.root.bind_all('<Control-w>', self.fcsent)
        self.root.bind_all('<Control-b>', self.fcsent)
        self.root.bind_all('<Control-l>', self.fcsent)
        self.root.bind_all('<Control-d>', self.fcsent)
        self.root.bind_all('<Control-m>', self.fcsent)
        self.root.bind_all('<Control-s>', self.fcsent)
        self.root.bind_all('<Control-u>', self.fcsent)
        self.root.bind_all('<Control-o>', self.fcsent)
        self.root.bind_all('<Control-p>', self.fcsent)
        self.root.bind_all('<Control-h>', self.fcsent)
        self.root.bind_all('<Control-a>', self.fcsent)
        self.root.bind_all('<Control-e>', self.fcsent)
        self.root.bind_all('<Shift-Up>', self.scru)
        self.root.bind_all('<Shift-Down>', self.scrd)
        self.root.bind('<Control-Up>', self.fcsent)
        self.root.bind('<Control-Down>', self.fcsent)
        self.root.bind('<Control-Left>', self.fcsent)
        self.root.bind('<Control-Right>', self.fcsent)
        self.root.bind('<Control-n>', self.fcsent)
        llc = ['cp65001', 'UTF-8']
        if locale.getpreferredencoding() in llc:
            self.root.bind_all('<Control-y>', self.fcsent)
        self.root.bind_all('<Control-0>', self.fcsent)
        self.root.bind_all('<Control-minus>', self.fcsent)
        
        self.bt = {}
        self.rb = StringVar()
        self.fframe = Frame(root)
        self.fframe.pack(side = TOP, fill = 'x')
        self.label = ttk.Label(self.fframe, text = 'Words')
        self.label.pack(side = LEFT, pady = 3, fill = 'x')
        self.bt['label'] = self.label
        self.entry = ttk.Entry(self.fframe, width = 56, validate = 'focusin', validatecommand = self.focus, font = 'verdana 10')
        self.entry.pack(side = LEFT, ipady = 7, pady = 3, padx = 1, fill = 'x')
        self.entry.config(state = 'disable')
        self.bt['entry'] = self.entry
        self.radio1 = ttk.Radiobutton(self.fframe, text = 'parent', value = 'parent', var = self.rb, command = self.radiobut)
        self.radio1.pack(anchor = 'w', side = LEFT, padx = 1, fill = 'x')
        self.bt['radio1'] = self.radio1
        self.radio2 = ttk.Radiobutton(self.fframe, text = 'child', value = 'child', var = self.rb, command = self.radiobut)
        self.radio2.pack(anchor = 'w', side = LEFT, padx = 1, fill ='x')
        self.bt['radio2'] = self.radio2
        self.button = ttk.Button(self.fframe, text = 'Up', command = self.moveup)
        self.button.pack(side = LEFT, pady = 3, padx = 1, fill = 'x')
        self.bt['button'] = self.button
        self.button2 = ttk.Button(self.fframe, text = 'Down', command = self.movedown)
        self.button2.pack(side = LEFT, pady = 3, padx = 1, fill = 'x')
        self.bt['button2'] = self.button2
        self.button11 = ttk.Button(self.fframe, text = 'Paste', command = self.copas)
        self.button11.pack(side = LEFT, pady = 3, padx = 1, fill = 'x')
        self.bt['button11'] = self.button11
        self.button12 = ttk.Button(self.fframe, text = 'Save as PDF', command = self.saveaspdf)
        self.button12.pack(side = LEFT, pady = 3, padx = 1, fill = 'x')
        self.bt['button12'] = self.button12
        self.button14 = ttk.Button(self.fframe, text = 'Hide Parent', command = self.hiddenchl)
        self.button14.pack(side = LEFT, pady = 3, padx = 1, fill = 'x')
        self.bt['button14'] = self.button14
        self.bframe = Frame(root)
        self.bframe.pack(side = TOP, fill = 'x')
        self.button5 = ttk.Button(self.bframe, text = 'Insert', command = self.insertwords)
        self.button5.pack(side = LEFT, pady = 3, padx = 1, fill = 'x')
        self.bt['button5'] = self.button5
        self.button6 = ttk.Button(self.bframe, text = 'Write', command =  self.writefile)
        self.button6.pack(side = LEFT, pady = 3, padx = 1, fill = 'x')
        self.bt['button6'] = self.button6
        self.button7 = ttk.Button(self.bframe, text = 'BackUp', command = self.backup)
        self.button7.pack(side = LEFT, pady = 3, padx = 1, fill = 'x')
        self.bt['button7'] = self.button7
        self.button8 = ttk.Button(self.bframe, text = 'Load', command = self.loadbkp)
        self.button8.pack(side = LEFT, pady = 3, padx = 1, fill = 'x')
        self.bt['button8'] = self.button8
        self.button9 = ttk.Button(self.bframe, text = 'Delete', command = self.deleterow)
        self.button9.pack(side = LEFT, pady = 3, padx = 1, fill = 'x')
        self.bt['button9'] = self.button9
        self.button3 = ttk.Button(self.bframe, text = 'Move Child', command = self.move_lr)
        self.button3.pack(side = LEFT, pady = 3, padx = 1, fill = 'x')
        self.bt['button3'] = self.button3
        self.label3 = ttk.Label(self.bframe, text = 'Child')
        self.label3.pack(side = LEFT, padx = 1, pady = 8, fill = 'x')
        self.bt['label3'] = self.label3
        self.entry3 = ttk.Combobox(self.bframe, width = 7, state = 'readonly')
        self.entry3.pack(side = LEFT, padx = 1, pady = 8, fill = 'x')
        self.bt['entry3'] = self.entry3
        self.button4 = ttk.Button(self.bframe, text = 'Checked', command = self.checked)
        self.button4.pack(side = LEFT, pady = 3, padx = 1, fill = 'x')
        self.bt['button4'] = self.button4
        if locale.getpreferredencoding() not in llc:
            self.button4.config(state = 'disable')
        self.button10 = ttk.Button(self.bframe, text = 'Insight', command = self.insight)
        self.button10.pack(side = LEFT, pady = 3, padx = 1, fill = 'x')            
        self.bt['button10'] = self.button10
        self.button13 = ttk.Button(self.bframe, text = 'Space', command = self.spaces)
        self.button13.pack(side = LEFT, pady = 3, padx = 1, fill = 'x')
        self.bt['button13'] = self.button13
        self.button15 = ttk.Button(self.bframe, text = 'Clear hide', command = self.delhid)
        self.button15.pack(side = LEFT, pady = 3, padx = 1, fill = 'x')
        self.bt['button15'] = self.button15
        self.button16 = ttk.Button(self.bframe, text = 'Change File', command = self.chgfile)
        self.button16.pack(side = LEFT, pady = 3, padx = 1, fill = 'x')      
        self.bt['button16'] = self.button16
        self.button17 = ttk.Button(self.bframe, text = 'CPP', width = 4, command = self.coppar)
        self.button17.pack(side = LEFT, pady = 3, padx = 1, fill = 'x')
        self.bt['button17'] = self.button17
        self.tframe = Frame(root)
        self.tframe.pack(anchor = 'w', side = TOP) 
        self.text = Text(self.tframe, width = 105, height = 33, font = ('verdana','10'), padx = 5, pady = 5)
        self.text.config(state = 'disable')
        self.text.pack(side = LEFT, pady = 3, padx = 2, fill = 'both')
        self.bt['text'] = self.text
        self.scrollbar1 = ttk.Scrollbar(self.tframe, orient="vertical") 
        self.scrollbar1.config(command = self.text.yview) 
        self.scrollbar1.pack(side="left", fill="y") 
        self.text.config(yscrollcommand = self.scrollbar1.set)
        self.bt['scrollbar1'] = self.scrollbar1
        self.listb = Listbox(self.tframe, width = 12, exportselection = False, font = 'verdana 10')
        self.listb.pack(side = LEFT, padx = 2, pady = 3, fill = 'both')
        self.bt['listb'] = self.listb
        self.scrollbar2 = ttk.Scrollbar(self.tframe, orient="vertical") 
        self.scrollbar2.config(command = self.listb.yview) 
        self.scrollbar2.pack(side="right", fill="y") 
        self.listb.config(yscrollcommand = self.scrollbar2.set)
        self.bt['scrollbar2'] = self.scrollbar2
        self.unlock = True
        
    def fcsent(self, event = None):
        # Key Bindings to keyboards.
        
        if TreeViewGui.FREEZE is False:
            if event.keysym == 'f':
                self.entry.focus()
            elif event.keysym == 'r':
                self.entry3.focus()
            elif event.keysym == 't':
                st = self.listb.curselection()
                if st:
                    self.listb.focus()
                    self.listb.select_set(int(st[0]))
                else:
                    self.listb.focus()
            elif event.keysym == 'i':
                self.insertwords()
            elif event.keysym == 'w':
                self.writefile()
            elif event.keysym == 'b':
                self.backup()
            elif event.keysym == 'l':
                self.loadbkp()
            elif event.keysym == 'd':
                self.deleterow()
            elif event.keysym == 'm':
                self.move_lr()
            elif event.keysym == 's':
                self.insight()
            elif event.keysym == 'u':
                self.moveup()
            elif event.keysym == 'o':
                self.movedown()
            elif event.keysym == 'p':
                self.saveaspdf()
            elif event.keysym == 'h':
                self.hiddenchl()
            elif event.keysym == 'a':
                if self.rb.get() == 'parent':
                    self.rb.set('child')
                    self.radiobut()
                else:
                    self.rb.set('parent')
                    self.radiobut()
            elif event.keysym == 'e':
                self.copas()
            elif event.keysym == 'y':
                self.checked()
            elif event.keysym == '0':
                self.spaces()
            elif event.keysym == 'minus':
                self.delhid()
            elif event.keysym == 'Left':
                self.pwidth = self.pwidth - 10
                self.root.geometry(f"+{self.pwidth}+{self.pheight}")
            elif event.keysym == 'Right':
                self.pwidth = self.pwidth + 10
                self.root.geometry(f"+{self.pwidth}+{self.pheight}")
            elif event.keysym == 'Down':
                self.pheight = self.pheight + 10
                self.root.geometry(f"+{self.pwidth}+{self.pheight}")
            elif event.keysym == 'Up':
                self.pheight = self.pheight - 10
                self.root.geometry(f"+{self.pwidth}+{self.pheight}")
            elif event.keysym == 'n':
                self.coppar()
                
    def radiobut(self, event = None):
        # These are the switches on radio buttons, to apply certain rule on child.
        
        case = {'': self.rb.get(),
                'child': 'child',
                'parent': 'parent'}
        self.entry.config(state = 'normal') 
        if self.entry.get() in case:
            if case[self.rb.get()] == 'child':
                self.entry3.config(values = tuple([f'child{c}' for c in range(1, 51)]))
                self.entry3.current(0)
            elif case[self.rb.get()] != 'child':
                self.entry3.config(values = '')
                self.entry3.config(state = 'normal')
                self.entry3.delete(0,END)
                self.entry3.config(state = 'readonly')
            self.entry.delete(0,END)
            self.entry.insert(0, case[''])
        else:
            if case[self.rb.get()] == 'child':
                self.entry3.config(values = tuple([f'child{c}' for c in range(1, 51)]))
                self.entry3.current(0)
            elif case[self.rb.get()] != 'child':
                self.entry3.config(values = '')
                self.entry3.config(state = 'normal')
                self.entry3.delete(0,END)
                self.entry3.config(state = 'readonly')

    def focus(self, event = None):
        # Validation for Entry
        
        if self.entry.validate:
            case = ['child', 'parent']
            if self.entry.get() in case:
                self.entry.delete(0,END)
                return True
            else:
                return False
            
    def scrd(self, event = None):
        #Scroll to the bottom on keyboard, down arrow button.
        
        a = self.text.yview()[0]
        a = eval(f'{a}')+0.01
        self.text.yview_moveto(str(a))
        self.listb.yview_moveto(str(a+0.01))
        
    def scru(self, event = None):
        #Scroll to the first position on keyboard, up arrow button.
        
        a = self.text.yview()[0]
        a = eval(f'{a}')-0.01
        self.text.yview_moveto(str(a))
        self.listb.yview_moveto(str(a))
        
    def view(self, event = None):
        # Viewing engine for most module fuction.
        
        tvg = tv(self.filename)
        self.text.config(state = 'normal')
        try:    
            with open(f'{self.filename}.txt') as file:
                rd = file.readlines()
                self.text.delete('1.0', END)
                for r in rd:
                    self.text.insert(END, r)
            self.text.config(state = 'disable')
            vals = [f' {k}: {c[0]}' for k, c  in list(tvg.insighttree().items())]
            self.listb.delete(0,END)
            for val in vals:
                self.listb.insert(END, val)
            self.entry3.delete(0, END)
            self.text.yview_moveto(1.0)
            self.listb.yview_moveto(1.0)
        except:
            self.text.insert(END, sys.exc_info()[1])
            self.text.config(state = 'disable')
    
    def chgfile(self):
        # Changing file on active app environment.
        
        if TreeViewGui.DB is None:
            def chosen(event = None):
                for i in self.bt:
                    if 'label' not in i and 'scrollbar' not in i:
                        if i == 'entry3':
                            self.bt[i].config(state='readonly')
                        else:
                            self.bt[i].config(state='normal')
                fi = spb.get()
                TreeViewGui.DB = None
                TreeViewGui.FREEZE = False
                tl.unbind_all('<Control-g>')
                tl.destroy()
                ask = messagebox.askyesno('TreeViewGui', '"Yes" to change file, "No" to delete directory')
                if ask:
                    os.chdir(os.getcwd()[:os.getcwd().rfind('\\')])
                    os.chdir(fi)
                    self.filename = fi[:fi.rfind('_')]
                    self.root.title(f'{os.getcwd()}\\{self.filename}.txt')
                    if f'{self.filename}.txt' in os.listdir():
                        if f'{self.filename}.json' not in os.listdir():
                            self.writefile()
                        else:
                            self.hidform()
                    else:
                        self.text.config(state = 'normal')
                        self.text.delete('1.0', END)
                        self.text.config(state = 'disable')
                        self.listb.delete(0,END)
                else:
                    import shutil
                    ori = os.getcwd()
                    os.chdir(os.getcwd()[:os.getcwd().rfind('\\')])
                    if ori[ori.rfind("\\")+1:] != fi:
                        lf = os.listdir(fi)
                        lsc = messagebox.askyesno('TreeViewGui', f'Do you really want to delete {fi} directory with all\n{lf}\nfiles?')
                        if lsc:
                            shutil.rmtree(fi)
                        else:
                            messagebox.showinfo('TreeViewGui', 'Deleting directory is aborted!')
                    else:
                        messagebox.showerror('TreeViewGui', 'You are unable to delete present directory!!!')
                    os.chdir(ori)
            
            for i in self.bt:
                if 'label' not in i and 'scrollbar' not in i:
                    self.bt[i].config(state='disable')
            TreeViewGui.FREEZE = True
            tl = Toplevel()
            tl.resizable(False, False)
            tl.overrideredirect(True)
            tl.wm_attributes("-topmost", 1)
            tl.bind_all('<Control-g>', chosen)
            files = [file for file in os.listdir(os.getcwd()[:os.getcwd().rfind('\\')]) if '.' not in file]
            spb = Spinbox(tl, values = files, font= 'Helvetica 20 bold')
            spb.pack(side = LEFT, padx = 5, pady = 5)
            bt = Button(tl, text = 'Choose', command = chosen)
            bt.pack(pady = 5, padx = 2)
            spb.focus()
            TreeViewGui.DB = tl
            
    def writefile(self, event = None):
        # Write first entry and on next updated line.
        # Write also on chosen row for update.
        
        self.hidcheck()
        if self.unlock:
            tvg = tv(self.filename)
            if not tvg.insighttree():
                if self.entry.get():
                    tvg.writetree(self.entry.get())
                    self.entry.delete(0,END)
            else:
                cek = ['child', 'parent']
                if self.entry3.get():
                    if self.entry.get() and self.entry.get() not in cek:
                        if self.listb.curselection():
                            rw = self.listb.curselection()
                            if tvg.insighttree()[int(rw[0])][0] != 'space':                        
                                rw = self.listb.curselection()
                                tvg.edittree(self.entry.get(),int(rw[0]),self.entry3.get())
                                self.entry.delete(0,END)
                        else:
                            tvg.quickchild(self.entry.get(), self.entry3.get())
                            self.entry.delete(0,END)
                else:
                    if self.entry.get() and self.entry.get() not in cek:
                        if self.listb.curselection():
                            rw = self.listb.curselection()
                            if tvg.insighttree()[int(rw[0])][0] != 'space':
                                tvg.edittree(self.entry.get(),int(rw[0]))
                                self.entry.delete(0,END)
                        else:
                            tvg.addparent(self.entry.get())
                            self.entry.delete(0,END)
            self.spaces()

    def deleterow(self):
        # Deletion on recorded row and updated.
        
        self.hidcheck()
        if self.unlock:
            tvg = tv(self.filename)
            ck = tvg.insighttree()
            try:
                if ck:     
                    if self.listb.curselection():
                        rw = self.listb.curselection()
                        cp = ck[int(rw[0])][0]
                        tvg.delrow(int(rw[0]))
                        self.spaces()
                        ck = tvg.insighttree()
                        if int(rw[0]) < len(ck):
                            if cp == 'parent' and int(rw[0]) != 0:
                                self.listb.select_set(int(rw[0])-1)
                            else:
                                if cp == 'space':
                                    self.listb.select_set(int(rw[0])+1)
                                else:
                                    self.listb.select_set(int(rw[0]))
                        else:
                            if len(ck) == 1:
                                self.listb.select_set(0)
                            else:
                                if cp == 'parent':
                                    self.listb.select_set(int(rw[0])-2)
                                else:
                                    self.listb.select_set(int(rw[0])-1)
            except:
                self.text.config(state = 'normal')
                self.text.delete('1.0', END)
                self.text.insert(END, sys.exc_info())
                self.text.config(state = 'disable')
    
    def move_lr(self, event = None):
        # Moving a child row to left or right, as to define spaces needed.
        
        self.hidcheck()
        if self.unlock:
            if self.listb.curselection():
                if self.entry3.get():
                    rw = self.listb.curselection()
                    tvg = tv(self.filename)
                    try:
                        self.text.config(state = 'normal')
                        tvg.movechild(int(rw[0]), self.entry3.get())
                        self.view()
                        self.listb.select_set(int(rw[0]))
                    except:
                        import sys
                        self.text.insert(END, 'Parent row is unable to be move to a child')
                        self.text.config(state = 'disable')

    def insight(self, event = None):
        # To view the whole rows, each individually with the correspondent recorded values.
        
        tvg = tv(self.filename)
        if tvg.insighttree():
            ins = tvg.insighttree()
            ins = [f'row {k}: {v[0]}, {v[1]}' for k, v in ins.items()]
            self.text.config(state = 'normal')
            self.text.delete('1.0', END)
            for d in ins:
                self.text.insert(END, f'{d}')                                            
            self.text.config(state = 'disable')

    def moveup(self, event = None):
        # Step up a row to upper row.
        
        self.hidcheck()
        if self.unlock:
            tvg = tv(self.filename)
            ck = tvg.insighttree()
            if ck:
                if self.listb.curselection():
                    rw = self.listb.curselection()
                    if ck[int(rw[0])][0] != 'space' and 'child' in ck[int(rw[0])][0]:
                        if int(rw[0]) != 0:
                            tvg.movetree(int(rw[0]), int(rw[0])-1)
                            self.spaces()
                            ck = tvg.insighttree()
                            if  ck[int(rw[0])-1][0] != 'space':
                                self.listb.select_set(int(rw[0])-1)
                            else:
                                self.listb.select_set(int(rw[0])-2)

    def movedown(self, event = None):
        # Step down a row to below row.
        
        self.hidcheck()
        if self.unlock:
            tvg = tv(self.filename)
            ck = tvg.insighttree()
            if ck:
                if self.listb.curselection():
                    rw = self.listb.curselection()
                    if ck[int(rw[0])][0] != 'space' and 'child' in ck[int(rw[0])][0]:
                        if int(rw[0]) < len(ck)-1:
                            if ck[int(rw[0])+1][0] == 'space':
                                tvg.movetree(int(rw[0]), int(rw[0])+2)
                            else:
                                tvg.movetree(int(rw[0]), int(rw[0])+1)
                            self.spaces()
                            ck = tvg.insighttree()
                            if ck[int(rw[0])+1][0] != 'parent':
                                self.listb.select_set(int(rw[0])+1)
                            else:
                                self.listb.select_set(int(rw[0])+2)
                
    def insertwords(self, event = None):
        # Insert a record to any row appear above the assign row.
        
        self.hidcheck()
        if self.unlock:
            tvg = tv(self.filename)
            if tvg.insighttree():
                cek = ['parent', 'child']
                cks = tvg.insighttree()
                if self.entry.get() and self.entry.get() not in cek :            
                    if self.listb.curselection():
                        rw = self.listb.curselection()
                        if self.entry3.get():
                            tvg.insertrow(self.entry.get(), int(rw[0]), self.entry3.get())
                            self.entry.delete(0, END)
                        else:
                            tvg.insertrow(self.entry.get(), int(rw[0]))
                            self.entry.delete(0, END)  
                        self.spaces()
                
    def checked(self, event = None):
        # To add strikethrough unicode for finished task.
        # WARNING: is active according to your computer encoding system. (Active on encoding: "utf-8")
        
        self.hidcheck()
        if self.unlock:
            tvg = tv(self.filename)
            if self.listb.curselection():
                rw = self.listb.curselection()
                tvg.checked(int(rw[0]))
                self.view()
                self.listb.select_set(int(rw[0]))
            
    def backup(self, event = None):
        # Backup to max of 10 datas on csv file.
        # And any new one above will remove the oldest one.
        
        self.hidcheck()
        if self.unlock:
            tvg = tv(self.filename)
            if tvg.insighttree():
                tvg.backuptv()
                messagebox.showinfo('Backup', 'Backup done!')
            
    def loadbkp(self, event = None):
        # Load any backup data.
        
        import csv
        self.hidcheck()
        if self.unlock:
            tvg = tv(self.filename)
            if f'{self.filename}.csv' in os.listdir():
                try:
                    with open(f'{self.filename}.csv') as csvfile:
                        reads = list(csv.reader(csvfile))
                        row  = simpledialog.askinteger('Load Backup',
                        f'There are {len(reads)-1} rows, please choose a row:')
                        if row:
                            data = eval(reads[row][1])
                            tvg.fileread(data)
                            messagebox.showinfo('Load Backup',
                            'Load backup is done, chek again!') 
                except:
                    import sys
                    self.text.config(state = 'normal')
                    self.text.delete('1.0', END)
                    self.text.insert(END, sys.exc_info())
                    self.text.config(state = 'disable')
                
    def copas(self, event = None):
        # Paste a row value to Entry for fixing value.
        
        import re
        self.hidcheck()
        if self.unlock:
            if self.listb.curselection():
                rw = self.listb.curselection()
                with open(f'{self.filename}.txt') as file:
                    rd = file.readlines()
                    self.entry.delete(0, END)                
                    if rd[int(rw[0])][0] == ' ':
                        paste = rd[int(rw[0])][re.match(r'\s+', rd[int(rw[0])]).span()[1]:-1]
                        self.entry.insert(END, paste[1:])
                    else:
                        if rd[int(rw[0])] != '\n':
                            self.entry.insert(END, rd[int(rw[0])][:-2])
                    
    def coppar(self):
        # To move parent and its childs to new rows within the records.
        
        tvg = tv(self.filename)
        ins = tvg.insighttree()
        if ins:
            getr = self.listb.curselection()
            if getr:
                if ins[int(getr[0])][0] == 'parent':
                    ask = simpledialog.askinteger('TreeViewGui', 
                                                  f'Move to which row? must less then {len(ins)} rows')
                    if ask is not None and ask < len(ins):
                        gr = int(getr[0])+1
                        while gr < len(ins):
                            if ins[gr][0] == 'parent':
                                break
                            gr += 1                            
                        with open(f'{self.filename}.txt') as file:
                            rd = file.readlines()
                            cop = [i for i in rd[int(getr[0]):gr]]
                            for i in range(int(getr[0]), gr):
                                rd[i] = '\n' 
                            if ask < len(ins)-1:
                                for i in cop[::-1]:
                                    rd.insert(ask, i)
                            else:
                                for i in cop:
                                    rd.append(i)
                        with open(f'{self.filename}.txt', 'w') as file:
                            file.writelines(rd)
                        self.spaces()
                        
    def saveaspdf(self):
        # Saving records to a pdf.
        
        from CreatePDF import Pydf
        
        if TreeViewGui.DB is None:
            gch = ''
            def chosen(event = None):
                global gch
                fildir = filedialog.askdirectory()
                for i in self.bt:
                    if 'label' not in i and 'scrollbar' not in i:
                        if i == 'entry3':
                            self.bt[i].config(state='readonly')
                        else:
                            self.bt[i].config(state='normal')
                gch = spb.get()
                TreeViewGui.DB = None
                TreeViewGui.FREEZE = False
                tl.unbind_all('<Control-g>')
                tl.destroy()                
                try:
                    if fildir:
                        ori = os.getcwd()
                        if f'{self.filename}.json' in os.listdir():
                            ans = messagebox.askyesno('TreeViewGui', 'Do you want print the hidden parents?')
                            if ans:
                                self.hidform()
                                os.chdir(fildir)
                                showt = self.text.get('1.0', END)[:-2]
                                self.root.clipboard_append(showt)
                                pdf = Pydf(f'{self.filename}')
                                ppath = f"c:\\WINDOWS\\Fonts\\{gch}.ttf"
                                pdf.add_font(f'{gch}', '', ppath, uni=True)
                                pdf.alias_nb_pages()
                                pdf.add_page() 
                                pdf.set_font(f'{gch}', '', 12) 
                                pdf.multi_cell(0, 5, showt) 
                                pdf.output(pdf.filename, 'F')
                                messagebox.showinfo('Save as PDF', f'{self.filename}.pdf is created!')
                            else:
                                with open(f'{self.filename}.txt') as file:
                                    frd = file.read()
                                    self.root.clipboard_append(frd)
                                    os.chdir(fildir)
                                    pdf = Pydf(f'{self.filename}')
                                    ppath = f"c:\\WINDOWS\\Fonts\\{gch}.ttf"
                                    pdf.add_font(f'{gch}', '', ppath, uni=True)
                                    pdf.alias_nb_pages()
                                    pdf.add_page() 
                                    pdf.set_font(f'{gch}', '', 12) 
                                    pdf.multi_cell(0, 5, frd) 
                                    pdf.output(pdf.filename, 'F')
                                messagebox.showinfo('Save as PDF', f'{self.filename}.pdf is created!')
                        else:
                            with open(f'{self.filename}.txt') as file:
                                frd = file.read()
                                self.root.clipboard_append(frd)
                                os.chdir(fildir)
                                pdf = Pydf(f'{self.filename}')
                                ppath = f"c:\\WINDOWS\\Fonts\\{gch}.ttf"
                                pdf.add_font(f'{gch}', '', ppath, uni=True)
                                pdf.alias_nb_pages()
                                pdf.add_page() 
                                pdf.set_font(f'{gch}', '', 12)
                                pdf.multi_cell(0, 5, frd) 
                                pdf.output(pdf.filename, 'F')
                            messagebox.showinfo('Save as PDF', f'{self.filename}.pdf is created!')
                        os.chdir(ori)
                    else:
                        messagebox.showinfo('Save as PDF', 'Please choose a directory first!')
                except:
                    messagebox.showinfo('Save as PDF', f'{sys.exc_info()}')
                        
            for i in self.bt:
                if 'label' not in i and 'scrollbar' not in i:
                    self.bt[i].config(state='disable')
            TreeViewGui.FREEZE = True
            tl = Toplevel()
            tl.resizable(False, False)
            tl.overrideredirect(True)
            tl.wm_attributes("-topmost", 1)
            tl.bind_all('<Control-g>', chosen)
            a = [i[:i.rfind('.')] for i in os.listdir(r'c:\WINDOWS\Fonts') if '.ttf' in i]
            spb = Spinbox(tl, values = a, font= 'Helvetica 20 bold')
            spb.pack(side = LEFT, padx = 5, pady = 5)
            bt = Button(tl, text = 'Choose', command = chosen)
            bt.pack(pady = 5, padx = 2)
            spb.focus()
            TreeViewGui.DB = tl
            
    def spaces(self):
        # Mostly used by other functions to clear an obselete spaces.
        # To appropriate the display better.
        
        self.hidcheck()
        if self.unlock:
            tvg = tv(self.filename)
            cks =  tvg.insighttree()  
            num2 = 1
            if cks:
                while num2 !=  len(cks):
                    try:
                        if cks[num2][0] == 'parent':
                            if cks[num2 - 1][0] != 'space':
                                tvg.insertspace(num2)
                                cks =  tvg.insighttree()
                            else:
                                num2 += 1
                        elif cks[num2][0] == 'space':
                            if cks[num2 - 1][0] == 'space':
                                tvg.delrow(num2)
                                cks =  tvg.insighttree()
                            else:
                                num2 += 1
                        elif 'child' in cks[num2][0]:
                            if cks[num2 - 1][0] == 'space':
                                tvg.delrow(num2-1)
                                num2 -= 1
                                cks =  tvg.insighttree()
                            else:
                                num2 += 1
                        else:
                            num2 += 1
                    except:
                        print(sys.exc_info())
                        break
                if cks[0][0] == 'space':
                    tvg.delrow(0)
                    cks =  tvg.insighttree()
                if cks[len(cks)-1][0] == 'space':
                    tvg.delrow(len(cks)-1)             
                self.view()
            else:
                self.view()
    
    def hidcheck(self):
        # Core checking for hidden parent on display, base on existing json file.
        
        if f'{self.filename}.json' in os.listdir():
            ans = messagebox.askyesno('TreeViewGui', f'Delete {self.filename}.json?')
            if ans:
                os.remove(f'{self.filename}.json')
                self.view()
                self.unlock = True
                messagebox.showinfo('TreeViewGui', f'{self.filename}.json has been deleted!')
            else:
                self.unlock = False
                messagebox.showinfo('TreeViewGui', 'This function has been terminated!!!')
        else:
            if self.unlock == False:
                self.unlock = True

    def hidform(self):
        # To display records and not hidden one from collection position in json file.
        
        import json
        tvg = tv(self.filename)
        if f'{self.filename}.json' in os.listdir():
            self.view()
            with open(f'{self.filename}.json') as jfile:
                rd = dict(json.load(jfile))
                rolrd = list(rd.values())  
            for wow, wrow in rolrd:
                showt = self.text.get('1.0', END).split('\n')[:-2]
                firstpart = showt[:wow]
                if wrow < len(showt):
                    scdpart = showt[wrow:]
                    allpart = firstpart + scdpart
                else:
                    allpart = firstpart
                self.text.config(state = 'normal')
                self.text.delete('1.0', END)
                ih =[]
                for put in allpart:
                    self.text.insert(END, f'{put}\n')
                    ih.append(f'{put}\n')
                self.text.config(state = 'disable')
                vals = [f' {k}: {c[0]}' for k, 
                c  in list(tvg.insighthidden(ih).items())]
                self.listb.delete(0,END)
                for val in vals:
                    self.listb.insert(END, val)
            return rd            
        
    def hiddenchl(self, event = None):
        # Create Hidden position of parent and its childs in json file. 
        
        import json
        tvg = tv(self.filename)
        if tvg.insighttree():
            if self.listb.curselection():
                row = int(self.listb.curselection()[0])
                if self.text.get('1.0', END):
                    if f'{self.filename}.json' not in os.listdir():
                        rows = tvg.insighthidden(self.text.get('1.0', END).split('\n')[:-2])
                        if row in rows:
                            if rows[row][0] == 'parent' and 'child' in rows[row+1][0]:
                                showt = self.text.get('1.0', END).split('\n')[:-2]
                                srow = row+1
                                while True:
                                    if srow < len(showt):
                                        if rows[srow][0] == 'parent':
                                            srow += 1
                                            break
                                        srow +=1
                                    else:
                                        break
                                with open(f'{self.filename}.json', 'w') as jfile:
                                    hd = {0:(row, srow)}
                                    json.dump(hd, jfile, indent = 4)
                                firstpart = showt[:row]
                                if srow < len(showt):
                                    scdpart = showt[srow:]
                                    allpart = firstpart + scdpart
                                else:
                                    allpart = firstpart
                                self.text.config(state = 'normal')
                                self.text.delete('1.0', END)
                                ih =[]
                                for put in allpart:
                                    self.text.insert(END, f'{put}\n')
                                    ih.append(f'{put}\n')
                                self.text.config(state = 'disable')
                                vals = [f' {k}: {c[0]}' for k, 
                                c  in list(tvg.insighthidden(ih).items())]
                                self.listb.delete(0,END)
                                for val in vals:
                                    self.listb.insert(END, val)
                    else:
                        rd = self.hidform()
                        rows = tvg.insighthidden(self.text.get('1.0', END).split('\n')[:-2])
                        if row in rows:
                            if rows[row][0] == 'parent' and 'child' in rows[row+1][0]:
                                showt = self.text.get('1.0', END).split('\n')[:-2]
                                srow = row+1
                                while True:
                                    if srow < len(showt):
                                        if rows[srow][0] == 'parent':
                                            srow += 1
                                            break
                                        srow +=1
                                    else:
                                        break
                                with open(f'{self.filename}.json', 'w') as jfile:
                                    rd[len(rd)+1] = (row, srow)
                                    json.dump(rd, jfile, indent = 4)
                                firstpart = showt[:row]
                                if srow < len(showt):
                                    scdpart = showt[srow:]
                                    allpart = firstpart + scdpart
                                else:
                                    allpart = firstpart
                                self.text.config(state = 'normal')
                                self.text.delete('1.0', END)
                                ih =[]
                                for put in allpart:
                                    self.text.insert(END, f'{put}\n')
                                    ih.append(f'{put}\n')
                                self.text.config(state = 'disable')
                                vals = [f' {k}: {c[0]}' for k, 
                                c  in list(tvg.insighthidden(ih).items())]
                                self.listb.delete(0,END)
                                for val in vals:
                                    self.listb.insert(END, val) 
            else:
                self.hidform()

    def delhid(self, event = None):
        # Deleting accordingly each position in json file, or can delete the file. 
        
        import json
        if f'{self.filename}.json' in os.listdir():
            with open(f'{self.filename}.json') as jfile:
                rd = list(dict(json.load(jfile)).values())
            ans = messagebox.askyesno('TreeViewGui', 
            'Please choose "Yes" to delete ascending order, or "No" to delete all?')
            if ans:
                if rd:
                    rd.pop()
                    rd = {k:v for k, v in list(enumerate(rd))}
                    with open(f'{self.filename}.json', 'w') as jfile:
                        json.dump(rd, jfile, indent = 4)
                    self.hidform()
                else:
                    os.remove(f'{self.filename}.json')
                    self.view()
                    messagebox.showinfo('TreeViewGui', f'{self.filename}.json has been deleted!')
            else:
                os.remove(f'{self.filename}.json')
                self.view()         
                messagebox.showinfo('TreeViewGui', f'{self.filename}.json has been deleted!')                

def main(filename = None):
    # Starting point of running TVG and making directory for non-existing file.
    
    root = Tk()
    root.wm_iconbitmap(default='tvg.ico')
    root.withdraw()
    if not filename:
        filename = simpledialog.askstring('Filename','Please create file: ')
    if filename:
        filename = filename.capitalize()
        root.deiconify()
        if f'{filename}_tvg' not in os.listdir():
            try:
                os.mkdir(f'{filename}_tvg')
                os.chdir(f'{filename}_tvg')
            except:
                os.chdir(f'{filename}_tvg')
        else:
            os.chdir(f'{filename}_tvg')        
        begin = TreeViewGui(root, filename)
        root.mainloop()
    else:
        messagebox.showwarning('File', 'No File Name!')    
    

if __name__ == '__main__':
    main()    
    
