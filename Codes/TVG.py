# -*- coding: utf-8 -*-
# Copyright © kakkarja (K A K)

from tkinter import *
from tkinter import ttk
from tkinter import simpledialog, messagebox, filedialog
from TreeView import TreeView as tv
import sys
import os
import TeleTVG
from datetime import datetime as dt

class TreeViewGui:
    """
    This is the Gui for TreeView engine. This gui is to make the Writing and editing is viewable.
    """
    DB = None
    FREEZE = False
    MARK = False
    def __init__(self, root, filename):
        super().__init__()
        self.filename = filename
        self.root = root
        self.root.title(f'{os.getcwd()}\\{self.filename}.txt')
        self.wwidth = int(self.root.winfo_screenwidth()/1.4)
        self.wheight = int(self.root.winfo_screenheight()/2)
        self.pwidth = int(self.root.winfo_screenwidth()/2 - self.wwidth/2)
        self.pheight = int(self.root.winfo_screenheight()/12 - self.wheight/12)
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
        self.root.bind_all('<Control-n>', self.fcsent)
        self.root.bind_all('<Control-y>', self.fcsent)
        self.root.bind_all('<Control-0>', self.fcsent)
        self.root.bind_all('<Control-minus>', self.fcsent)
        self.root.bind_all('<Control-Key-1>', self.fcsent)
        self.root.bind_all('<Control-Key-2>', self.fcsent)
        self.root.bind_all('<Control-Key-3>', self.fcsent)
        self.root.bind_all('<Control-Key-4>', self.fcsent)
        self.root.bind_all('<Control-Key-5>', self.fcsent)
        self.root.bind_all('<Control-Key-6>', self.fcsent)
        self.root.bind_all('<Control-Key-7>', self.fcsent)
        self.root.bind_all('<Control-Key-8>', self.fcsent)
        self.root.bind_all('<Control-Key-9>', self.fcsent)
        self.bt = {}
        self.rb = StringVar()
        
        # 1st frame. 
        # Frame for label and Entry.
        self.fframe = Frame(root)
        self.fframe.pack(side = TOP, fill = 'x')
        self.label = ttk.Label(self.fframe, text = 'Words')
        self.label.pack(side = LEFT, pady = 3, fill = 'x')
        self.bt['label'] = self.label
        self.entry = ttk.Entry(self.fframe, validate = 'focusin', validatecommand = self.focus, font = 'consolas 12')
        self.entry.pack(side = LEFT, ipady = 5, pady = (3, 0), padx = 1, fill = 'x', expand = 1)
        self.entry.config(state = 'disable')
        self.bt['entry'] = self.entry
       
        # 2nd frame in first frame.
        # Frame for radios button.
        self.frbt = ttk.Frame(self.fframe)
        self.frbt.pack()
        self.frrb = ttk.Frame(self.frbt)
        self.frrb.pack(side = BOTTOM)
        self.radio1 = ttk.Radiobutton(self.frbt, text = 'parent', value = 'parent', var = self.rb, command = self.radiobut)
        self.radio1.pack(side = LEFT,anchor = 'w', padx = 1)
        self.bt['radio1'] = self.radio1
        self.radio2 = ttk.Radiobutton(self.frbt, text = 'child', value = 'child', var = self.rb, command = self.radiobut)
        self.radio2.pack(side = RIGHT, anchor = 'w', padx = 1)
        self.bt['radio2'] = self.radio2
        
        # 3rd frame in 2nd frame.
        # Frame for Child ComboBox
        self.frcc = ttk.Frame(self.frrb)
        self.frcc.pack(side = TOP)
        self.label3 = ttk.Label(self.frcc, text = 'Child')
        self.label3.pack(side = LEFT, padx = 1, pady = (0, 2), fill = 'x')
        self.bt['label3'] = self.label3
        self.entry3 = ttk.Combobox(self.frcc, width = 8, state = 'readonly', justify = 'center')
        self.entry3.pack(side = LEFT, padx = 1, pady = (0, 2), fill = 'x')
        self.bt['entry3'] = self.entry3        
        
        # 3rd frame for top buttons.
        # Frame for first row Buttons.
        self.bframe = Frame(root)
        self.bframe.pack(side = TOP, fill = 'x')
        self.button5 = ttk.Button(self.bframe, text = 'Insert', command = self.insertwords)
        self.button5.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button5'] = self.button5
        self.button6 = ttk.Button(self.bframe, text = 'Write', command =  self.writefile)
        self.button6.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button6'] = self.button6
        self.button9 = ttk.Button(self.bframe, text = 'Delete', command = self.deleterow)
        self.button9.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button9'] = self.button9        
        self.button7 = ttk.Button(self.bframe, text = 'BackUp', command = self.backup)
        self.button7.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button7'] = self.button7
        self.button8 = ttk.Button(self.bframe, text = 'Load', command = self.loadbkp)
        self.button8.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button8'] = self.button8
        self.button3 = ttk.Button(self.bframe, text = 'Move Child', command = self.move_lr)
        self.button3.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button3'] = self.button3        
        self.button16 = ttk.Button(self.bframe, text = 'Change File', command = self.chgfile)
        self.button16.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button16'] = self.button16
        self.button17 = ttk.Button(self.bframe, text = 'CPP', command = self.cmrows)
        self.button17.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button17'] = self.button17
        self.button18 = ttk.Button(self.bframe, text = 'Send Note', command = self.sendtel)
        self.button18.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button18'] = self.button18
        self.button19 = ttk.Button(self.bframe, text = 'Look Up', command = self.lookup)
        self.button19.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button19'] = self.button19        
        self.button21 = ttk.Button(self.bframe, text = 'Save', command = self.endec)
        self.button21.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button21'] = self.button21        
        self.button23 = ttk.Button(self.bframe, text = 'Create file', command = self.createf)
        self.button23.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button23'] = self.button23
        self.button26 = ttk.Button(self.bframe, text = 'Convert', command = self.converting)
        self.button26.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button26'] = self.button26        
        
        # 4th frame for below buttons.
        # Frame for second row buttons.
        self.frb1 = ttk.Frame(self.root)
        self.frb1.pack(fill = X)
        self.button10 = ttk.Button(self.frb1, text = 'Insight', command = self.insight)
        self.button10.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button10'] = self.button10
        self.button13 = ttk.Button(self.frb1, text = 'Arrange', command = self.spaces)
        self.button13.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button13'] = self.button13
        self.button11 = ttk.Button(self.frb1, text = 'Paste', command = self.copas)
        self.button11.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button11'] = self.button11
        self.button4 = ttk.Button(self.frb1, text = 'Checked', command = self.checked)
        self.button4.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button4'] = self.button4        
        self.button = ttk.Button(self.frb1, text = 'Up', command = self.moveup)
        self.button.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button'] = self.button
        self.button2 = ttk.Button(self.frb1, text = 'Down', command = self.movedown)
        self.button2.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button2'] = self.button2
        self.button12 = ttk.Button(self.frb1, text = 'Save as PDF', command = self.saveaspdf)
        self.button12.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button12'] = self.button12
        self.button14 = ttk.Button(self.frb1, text = 'Hide Parent', command = self.hiddenchl)
        self.button14.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button14'] = self.button14
        self.button15 = ttk.Button(self.frb1, text = 'Clear hide', command = self.delhid)
        self.button15.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button15'] = self.button15
        self.button20 = ttk.Button(self.frb1, text = 'Date-Time', command = self.dattim)
        self.button20.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button20'] = self.button20        
        self.button22 = ttk.Button(self.frb1, text = 'Open', command = self.openf)
        self.button22.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button22'] = self.button22        
        self.button24 = ttk.Button(self.frb1, text = 'Lock File', command = self.lockf)
        self.button24.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button24'] = self.button24        
        self.button25 = ttk.Button(self.frb1, text = 'Un/Wrap', command = self.wrapped)
        self.button25.pack(side = LEFT, pady = (0, 3), padx = 1, fill = 'x', expand = 1)
        self.bt['button25'] = self.button25        
        
        # 5th frame.
        # Frame for text, listbox and scrollbars.
        self.tframe = Frame(root)
        self.tframe.pack(anchor = 'w', side = TOP, fill = 'x')
        self.text = Text(self.tframe, width = 105, height = 33, 
                         font = ('verdana','10'), padx = 5, pady = 5, wrap = NONE)
        self.text.config(state = 'disable')
        self.text.pack(side = LEFT, padx = 2, fill = 'both', expand = 1)
        self.text.bind('<MouseWheel>', self.mscrt)
        self.bt['text'] = self.text
        self.scrollbar1 = ttk.Scrollbar(self.tframe, orient="vertical")
        self.scrollbar1.config(command = self.text.yview) 
        self.scrollbar1.pack(side="left", fill="y") 
        self.scrollbar1.bind('<ButtonRelease>', self.mscrt)
        self.text.config(yscrollcommand = self.scrollbar1.set)
        self.bt['scrollbar1'] = self.scrollbar1
        self.listb = Listbox(self.tframe, width = 12, exportselection = False, font = 'verdana 10')
        self.listb.pack(side = LEFT, fill = 'both')
        self.bt['listb'] = self.listb
        self.scrollbar2 = ttk.Scrollbar(self.tframe, orient = "vertical")
        self.scrollbar2.config(command = self.listb.yview) 
        self.scrollbar2.pack(side = "right", fill = "y")
        self.scrollbar2.bind('<ButtonRelease>', self.mscrl)
        self.listb.config(yscrollcommand = self.scrollbar2.set)
        self.listb.bind('<<ListboxSelect>>', self.infobar)
        self.listb.bind('<MouseWheel>', self.mscrl)
        self.listb.bind('<Up>', self.mscrl)
        self.listb.bind('<Down>', self.mscrl)
        self.listb.bind('<FocusIn>', self.flb)
        self.bt['scrollbar2'] = self.scrollbar2
        
        # 6th frame.
        # Frame for horizontal scrollbar and info label.
        self.fscr = Frame(root)
        self.fscr.pack(fill = 'x')
        self.scrolh = ttk.Scrollbar(self.fscr, orient = "horizontal")
        self.scrolh.pack(side = LEFT, fill = 'x', expand = 1)
        self.scrolh.config(command = self.text.xview)
        self.text.config(xscrollcommand = self.scrolh.set)
        self.info = StringVar()
        self.info.set(f'{dt.strftime(dt.today(),"%a %d %b %Y")}')
        self.labcor = Label(self.fscr, textvariable = self.info, width = 18, justify = CENTER)
        self.labcor.pack(side = RIGHT, fill = 'x')
        self.unlock = True
        
    def wrapped(self, event = None):
        # Wrap the records so that it is filling the windows.
        # The scrolling horizontal become inactive.
        
        if str(self.text.cget('wrap')) == 'none':
            self.text.config(wrap = WORD)
        else:
            self.text.config(wrap = NONE)
    
    def converting(self, event =  None):
        # Convert any text that is paste or written in text window.
        # Example format:
        #      """
        #      Testing => to parent
        #      This is the format that will be converted appropriately. With
        #      no spaces after '\n'. And the period is needed for child. => to child1 [2 child]
        #      """
        
        import string
        
        if str(self.text.cget('state')) == 'disabled':
            self.text.config(state = 'normal')
            self.text.delete('1.0', END)
            for i in self.bt:
                if 'label' not in i and 'scrollbar' not in i:
                    if i != 'button26' and i != 'text':
                        self.bt[i].config(state='disable')
            TreeViewGui.FREEZE = True
        else:
            if self.text.get('1.0', END)[:-1]:
                fn = str(self.root.title())
                fn = fn[fn.rfind('\\')+1:]
                ask = messagebox.askyesno('TreeViewGui', 
                                          f'Do yout want to convert to this file {fn}?')
                if ask:
                    gt = self.text.get('1.0', END)[:-1]
                    keys = [k for k in gt.split('\n') if k and '.' not in k]
                    values = [v.split('. ') for v in gt.split('\n') if '. ' in v]
                    conv = dict(zip(keys, values))
                    tvg = tv(self.filename)
                    ck = string.ascii_letters
                    if conv:
                        for i in conv:
                            if self.checkfile():
                                tvg.addparent(i)
                            else:
                                tvg.writetree(i)
                            
                            for j in conv[i]:
                                if j:
                                    if j[-1] in ck:
                                        tvg.quickchild(f'{j}.', 'child1')
                                    else:
                                        tvg.quickchild(j, 'child1')
                else:
                    messagebox.showinfo('TreeViewGui', 'Converting is aborted!')
            self.text.config(state = DISABLED)
            for i in self.bt:
                if 'label' not in i and 'scrollbar' not in i:
                    if i == 'entry3':
                        self.bt[i].config(state='readonly')
                    elif i == 'entry':
                        if not self.rb.get():
                            self.bt[i].config(state='disable')
                        else:
                            self.bt[i].config(state='normal')
                    else:
                        if i != 'text':
                            self.bt[i].config(state='normal')
            TreeViewGui.FREEZE = False
            self.spaces()
            
    def infobar(self, event = None):
        # Info Bar telling the selected rows in listbox.
        # If nothing, it will display today's date.
        
        if f'{self.filename}_hid.json' in os.listdir():
            self.info.set('Hidden Mode')
        elif str(self.listb.cget('selectmode')) == EXTENDED:
            self.info.set('CPP Mode')
        elif self.listb.curselection():
            tvg = tv(f'{self.filename}')
            ck = tvg.insighttree()[int(self.listb.curselection()[0])][1][:10]
            self.info.set(f'{self.listb.curselection()[0]}: {ck[:-1]}...')
            del ck
        elif ':' in self.info.get() or 'Mode' in self.info.get():
            self.info.set(f'{dt.strftime(dt.today(),"%a %d %b %Y")}')
                    
    def checkfile(self):
        # Checking file if it is exist
        
        if f'{self.filename}.txt' in os.listdir():
            return True
        else:
            return False
        
    def mscrt(self, event = None):
        # Mouse scroll on text window, will sync with list box on the right.
        
        if self.text.yview()[1] < 1.0:
            self.listb.yview_moveto(self.text.yview()[0])
        else:
            self.listb.yview_moveto(self.text.yview()[1])
            
    def mscrl(self, event = None):
        # Mouse scroll on list box window, will sync with text window on the right.
    
        if self.listb.yview()[1] < 1.0:
            self.text.yview_moveto(self.listb.yview()[0])
        else:
            self.text.yview_moveto(self.listb.yview()[1])
            
    def fcsent(self, event = None):
        # Key Bindings to keyboards.

        fcom = str(self.root.focus_get())
        if TreeViewGui.FREEZE is False:
            if event.keysym == 'f':
                self.entry.focus()
            elif event.keysym == 'r':
                self.entry3.focus()
            elif event.keysym == 't':
                st = self.listb.curselection()
                if st:
                    self.listb.focus()
                    self.listb.activate(int(st[0]))
                    self.listb.see(int(st[0]))
                    self.text.yview_moveto(self.listb.yview()[0])
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
            elif event.keysym == 'Left' and 'entry' not in fcom:
                self.pwidth = self.pwidth - 10
                self.root.geometry(f"+{self.pwidth}+{self.pheight}")
            elif event.keysym == 'Right' and 'entry' not in fcom:
                self.pwidth = self.pwidth + 10
                self.root.geometry(f"+{self.pwidth}+{self.pheight}")
            elif event.keysym == 'Down' and 'entry' not in fcom:
                self.pheight = self.pheight + 10
                self.root.geometry(f"+{self.pwidth}+{self.pheight}")
            elif event.keysym == 'Up' and 'entry' not in fcom:
                self.pheight = self.pheight - 10
                self.root.geometry(f"+{self.pwidth}+{self.pheight}")
            elif event.keysym == 'n':
                self.cmrows()
            elif event.keysym == '1':
                self.sendtel()
            elif event.keysym == '2':
                self.lookup()
            elif event.keysym == '3':
                self.dattim()
            elif event.keysym == '4':
                self.endec()
            elif event.keysym == '5':
                self.openf()
            elif event.keysym == '6':
                self.createf()
            elif event.keysym == '7':
                self.lockf()
            elif event.keysym == '8':
                self.converting()
            elif event.keysym == '9':
                self.wrapped()
                
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
            if len(str(self.entry.focus_get()))> 5:
                if str(self.entry.focus_get())[-5:] != 'entry':
                    self.entry.insert(0, case[''])
            else:
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
            self.entry.selection_clear()

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
        
        try:
            if self.checkfile():
                tvg = tv(self.filename)
                self.text.config(state = 'normal')                
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
        
        if TreeViewGui.DB is None and self.checkfile():
            def chosen(event = None):
                for i in self.bt:
                    if 'label' not in i and 'scrollbar' not in i:
                        if i == 'entry3':
                            self.bt[i].config(state='readonly')
                        elif i == 'entry':
                            if not self.rb.get():
                                self.bt[i].config(state='disable')
                            else:
                                self.bt[i].config(state='normal')
                        else:
                            if i != 'text':
                                self.bt[i].config(state='normal')
                fi = spb.get()
                TreeViewGui.DB = None
                TreeViewGui.FREEZE = False
                tl.unbind_all('<Control-g>')
                tl.destroy()
                ask = messagebox.askyesno('TreeViewGui', '"Yes" to change file, "No" to delete directory')
                if ask:
                    os.chdir(os.path.join(os.getcwd().rpartition('\\')[0], fi))
                    self.filename = fi.rpartition('_')[0]
                    self.root.title(f'{os.getcwd()}\\{self.filename}.txt')
                    if f'{self.filename}.txt' in os.listdir():
                        if f'{self.filename}_hid.json' not in os.listdir():
                            self.spaces()
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
                    os.chdir(os.getcwd().rpartition('\\')[0])
                    if ori.rpartition('\\')[2] != fi:
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
            files = [file for file in os.listdir(os.getcwd()[:os.getcwd().rfind('\\')]) if '_tvg' in file]
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
            if not self.checkfile():
                if self.entry.get():
                    if not self.entry3.get():
                        tvg = tv(self.filename)
                        cek = ['child', 'parent']
                        if self.entry.get() not in cek:
                            tvg.writetree(self.entry.get())
                            self.entry.delete(0,END)
                            self.spaces()
                    else:
                        messagebox.showinfo('TreeViewGui', f'No {self.filename}.txt file yet created please choose parent first!')
                else:
                    messagebox.showinfo('TreeViewGui', f'No {self.filename}.txt file yet created!')                
            else:
                tvg = tv(self.filename)
                cek = ['child', 'parent']
                rw =  None
                if self.entry3.get():
                    if self.entry.get() and self.entry.get() not in cek:
                        if TreeViewGui.MARK:
                            rw = self.listb.curselection()[0]
                            appr = messagebox.askyesno('Edit', f'Edit cell {rw}?')
                            if appr:
                                if tvg.insighttree()[int(rw)][0] != 'space':
                                    tvg.edittree(self.entry.get(),int(rw),self.entry3.get())
                                    self.entry.delete(0,END)
                        else:
                            tvg.quickchild(self.entry.get(), self.entry3.get())
                            self.entry.delete(0,END)
                        self.spaces()                       
                else:
                    if self.entry.get() and self.entry.get() not in cek:
                        if TreeViewGui.MARK:
                            rw = self.listb.curselection()[0]
                            appr = messagebox.askyesno('Edit', f'Edit cell {rw}?')
                            if appr:
                                if tvg.insighttree()[int(rw)][0] != 'space':
                                    tvg.edittree(self.entry.get(),int(rw))
                                    self.entry.delete(0,END)
                        else:
                            tvg.addparent(self.entry.get())
                            self.entry.delete(0,END)
                        self.spaces()
                if rw and rw < len(tvg.insighttree())-1:
                    self.text.see(f'{int(rw)+1}.0')
                    self.listb.see(rw)
                        
    def flb(self, event = None):
        # Set Mark for cheking row for edit.
        
        TreeViewGui.MARK = True
        
    def deleterow(self):
        # Deletion on recorded row and updated.
        
        self.hidcheck()
        if self.unlock:
            try:
                if self.checkfile():
                    tvg = tv(self.filename)
                    if self.listb.curselection():
                        rw = self.listb.curselection()
                        tvg.delrow(int(rw[0]))
                        self.spaces()
                        ck = tvg.insighttree()
                        if int(rw[0]) < len(ck):
                            cp = ck[int(rw[0])][0]
                            if cp == 'parent' and int(rw[0]) != 0:
                                self.listb.select_set(int(rw[0])-2)
                                self.listb.see(int(rw[0])-2)
                                self.text.see(f'{(int(rw[0])-2)+1}.0')
                            else:
                                if cp == 'space':
                                    self.listb.select_set(int(rw[0])-1)
                                    self.listb.see(int(rw[0])-1)
                                    self.text.see(f'{(int(rw[0])-1)+1}.0')
                                else:
                                    self.listb.select_set(int(rw[0]))
                                    self.listb.see(int(rw[0]))
                                    self.text.see(f'{int(rw[0])+1}.0')
                        else:
                            if len(ck) == 1:
                                self.listb.select_set(0)
                            else:
                                self.listb.select_set(len(ck)-1)
                                self.listb.see(len(ck)-1)
                                self.text.see(f'{(len(ck)-1)+1}.0')
                        self.infobar()
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
                        self.spaces()
                        self.listb.select_set(int(rw[0]))
                        self.listb.see(int(rw[0]))
                        self.text.see(f'{int(rw[0])+1}.0')
                    except:
                        self.text.insert(END, 'Parent row is unable to be move to a child')
                        self.text.config(state = 'disable')
                    self.infobar()
                        
    def insight(self, event = None):
        # To view the whole rows, each individually with the correspondent recorded values.
        
        self.hidcheck()
        if self.unlock:
            if self.checkfile():
                tvg = tv(self.filename)
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
            if self.checkfile():
                tvg = tv(self.filename)
                ck = tvg.insighttree()                
                if self.listb.curselection():
                    rw = self.listb.curselection()
                    if ck[int(rw[0])][0] != 'space' and 'child' in ck[int(rw[0])][0]:
                        if int(rw[0]) != 0:
                            tvg.movetree(int(rw[0]), int(rw[0])-1)
                            self.spaces()
                            ck = tvg.insighttree()
                            if  ck[int(rw[0])-1][0] != 'space':
                                self.listb.select_set(int(rw[0])-1)
                                self.listb.see(int(rw[0])-1)
                                self.text.see(f'{(int(rw[0])-1)+1}.0')
                            else:
                                self.listb.select_set(int(rw[0])-2)
                                self.listb.see(int(rw[0])-2)
                                self.text.see(f'{(int(rw[0])-2)+1}.0')
                            self.infobar()
                                
    def movedown(self, event = None):
        # Step down a row to below row.
        
        self.hidcheck()
        if self.unlock:
            if self.checkfile():
                tvg = tv(self.filename)
                ck = tvg.insighttree()                
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
                                self.listb.see(int(rw[0])+1)
                                self.text.see(f'{(int(rw[0])+1)+1}.0')
                            else:
                                self.listb.select_set(int(rw[0])+2)
                                self.listb.see(int(rw[0])+2)
                                self.text.see(f'{(int(rw[0])+2)+1}.0')
                            self.infobar()
                                
    def insertwords(self, event = None):
        # Insert a record to any row appear above the assign row.
        
        self.hidcheck()
        if self.unlock:
            if self.checkfile():
                tvg = tv(self.filename)
                cek = ['parent', 'child']
                if self.entry.get() and self.entry.get() not in cek :
                    if TreeViewGui.MARK:
                        appr = messagebox.askyesno('Edit', f'Edit cell {self.listb.curselection()[0]}?')
                        if appr:                    
                            if self.listb.curselection():
                                rw = self.listb.curselection()
                                if self.entry3.get():
                                    tvg.insertrow(self.entry.get(), int(rw[0]), self.entry3.get())
                                    self.entry.delete(0, END)
                                else:
                                    tvg.insertrow(self.entry.get(), int(rw[0]))
                                    self.entry.delete(0, END)  
                                self.spaces()
                                self.listb.see(int(rw[0]))
                                self.text.see(f'{int(rw[0])+1}.0')
                                 
    def checked(self, event = None):
        # To add checked unicode for finished task.
        # WARNING: is active according to your computer encoding system. (Active on encoding: "utf-8")
        
        self.hidcheck()
        if self.unlock:
            tvg = tv(self.filename)
            if self.listb.curselection():
                rw = self.listb.curselection()
                tvg.checked(int(rw[0]))
                self.view()
                self.listb.select_set(int(rw[0]))
                self.listb.see(int(rw[0]))
                self.text.see(f'{int(rw[0])+1}.0')
                self.infobar()
            
    def backup(self, event = None):
        # Backup to max of 10 datas on csv file.
        # And any new one will remove the oldest one.
        
        self.hidcheck()
        if self.unlock:
            if self.checkfile():
                tvg = tv(self.filename)
                tvg.backuptv()
                messagebox.showinfo('Backup', 'Backup done!')
            
    def loadbkp(self, event = None):
        # Load any backup data.
        
        from DataB import Datab as db
        
        self.hidcheck()
        if self.unlock:
            tvg = tv(self.filename)
            dbs = db(self.filename)
            try:
                row  = simpledialog.askinteger('Load Backup',
                f'There are {dbs.totalrecs()} rows, please choose a row:')
                if row and row <= dbs.totalrecs():
                    tvg.loadbackup(self.filename, row = row-1, stat = True)
                    messagebox.showinfo('Load Backup',
                    'Load backup is done, chek again!')
                    self.spaces()
            except:
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
                        
    def cmrows(self):
        # Copy or move any rows to any point of a row within existing rows
        
        self.hidcheck()
        if self.unlock:
            if self.checkfile():
                if self.text.get('1.0',END)[:-1]:
                    ckc = ['listb', 'button17', 'text']
                    if self.listb.cget('selectmode') == 'browse':
                        for i in self.bt:
                            if 'label' not in i and 'scrollbar' not in i:
                                if i not in ckc:
                                    self.bt[i].config(state='disable')
                        self.listb.config(selectmode = EXTENDED)
                        TreeViewGui.FREEZE = True
                    else:
                        tvg = tv(self.filename)
                        ins = tvg.insighttree()                        
                        if self.listb.curselection():
                            gcs = [int(i) for i in self.listb.curselection()]
                            ask = simpledialog.askinteger('TreeViewGui', 
                                                          f'Move to which row? choose between 0 to {len(ins)-1} rows')
                            if ask < len(ins):
                                deci = messagebox.askyesno('TreeViewGui', '"Yes" to MOVE to, "No" to COPY to')
                                if deci:
                                    with open(f'{self.filename}.txt') as file:
                                        rd = file.readlines()
                                        cop = [i for i in rd[gcs[0]:gcs[-1]+1]]
                                        for i in range(gcs[0], gcs[-1]+1):
                                            rd[i] = '\n'
                                        if ask < len(ins)-1:
                                            if ask == 0:
                                                if ins[gcs[0]][0] == 'parent':
                                                    for i in cop[::-1]:
                                                        rd.insert(ask, i)
                                                else:
                                                    for i in cop[::-1]:
                                                        rd.insert(ask+1, i)
                                            else:
                                                for i in cop[::-1]:
                                                    rd.insert(ask, i)
                                        else:
                                            for i in cop:
                                                rd.append(i)
                                    with open(f'{self.filename}.txt', 'w') as file:
                                        file.writelines(rd)
                                    self.spaces()
                                else:
                                    with open(f'{self.filename}.txt') as file:
                                        rd = file.readlines()
                                        cop = [i for i in rd[gcs[0]:gcs[-1]+1]]
                                        if ask < len(ins)-1:
                                            if ask == 0:
                                                if ins[gcs[0]][0] == 'parent':
                                                    for i in cop[::-1]:
                                                        rd.insert(ask, i)
                                                else:
                                                    for i in cop[::-1]:
                                                        rd.insert(ask+1, i)
                                            else:
                                                for i in cop[::-1]:
                                                    rd.insert(ask, i)
                                        else:
                                            for i in cop:
                                                rd.append(i)
                                    with open(f'{self.filename}.txt', 'w') as file:
                                        file.writelines(rd)
                                    self.spaces()
                                for i in self.bt:
                                    if 'label' not in i and 'scrollbar' not in i:
                                        if i not in ckc:
                                            if i == 'entry3':
                                                self.bt[i].config(state='readonly')
                                            elif i == 'entry':
                                                if not self.rb.get():
                                                    self.bt[i].config(state='disable')
                                                else:
                                                    self.bt[i].config(state='normal')
                                            else:
                                                self.bt[i].config(state='normal')
                                self.listb.config(selectmode = BROWSE)
                                TreeViewGui.FREEZE = False
                                self.listb.see(ask)
                                self.text.yview_moveto(self.listb.yview()[0])
                            else:
                                for i in self.bt:
                                    if 'label' not in i and 'scrollbar' not in i:
                                        if i not in ckc:
                                            if i == 'entry3':
                                                self.bt[i].config(state='readonly')
                                            elif i == 'entry':
                                                if not self.rb.get():
                                                    self.bt[i].config(state='disable')
                                                else:
                                                    self.bt[i].config(state='normal')
                                            else:
                                                self.bt[i].config(state='normal')
                                self.listb.config(selectmode = BROWSE)
                                TreeViewGui.FREEZE = False
                                messagebox.showerror('TreeViewGui', f'row {ask} is exceed existing rows')
                        else:
                            ask = messagebox.askyesno('TreeViewGui', 'Cancel this operation?')
                            if ask:
                                for i in self.bt:
                                    if 'label' not in i and 'scrollbar' not in i:
                                        if i not in ckc:
                                            if i == 'entry3':
                                                self.bt[i].config(state='readonly')
                                            elif i == 'entry':
                                                if not self.rb.get():
                                                    self.bt[i].config(state='disable')
                                                else:
                                                    self.bt[i].config(state='normal')
                                            else:
                                                self.bt[i].config(state='normal')
                                self.listb.config(selectmode = BROWSE)
                                TreeViewGui.FREEZE = False
                    self.infobar()
                    
    def saveaspdf(self):
        # Saving records to a pdf.
        
        from CreatePDF import Pydf
        
        if TreeViewGui.DB is None and self.checkfile():
            gch = ''
            def chosen(event = None):
                global gch
                fildir = filedialog.askdirectory()
                for i in self.bt:
                    if 'label' not in i and 'scrollbar' not in i:
                        if i == 'entry3':
                            self.bt[i].config(state='readonly')
                        elif i == 'entry':
                            if not self.rb.get():
                                self.bt[i].config(state='disable')
                            else:
                                self.bt[i].config(state='normal')
                        else:
                            if i != 'text':
                                self.bt[i].config(state='normal')
                gch = spb.get()
                TreeViewGui.DB = None
                TreeViewGui.FREEZE = False
                tl.unbind_all('<Control-g>')
                tl.destroy()
                try:
                    if fildir:
                        ori = os.getcwd()
                        if f'{self.filename}_hid.json' in os.listdir():
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
                                pdf.set_font(f'{gch}', '', 10) 
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
                                    pdf.set_font(f'{gch}', '', 10) 
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
                                pdf.set_font(f'{gch}', '', 10)
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
            a = [i.rpartition('.')[0] for i in os.listdir(r'c:\WINDOWS\Fonts') if '.ttf' in i]
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
            if self.checkfile():
                if TreeViewGui.MARK:
                    TreeViewGui.MARK = False
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
                            messagebox.showerror('TreeViewGui', sys.exc_info())
                            break
                    if cks[0][0] == 'space':
                        tvg.delrow(0)
                        cks =  tvg.insighttree()
                    if cks[len(cks)-1][0] == 'space':
                        tvg.delrow(len(cks)-1)
                    self.view()
                else:
                    self.view()
            if str(self.root.focus_get()) != '.':
                self.root.focus()
            self.infobar()
            
    def hidcheck(self):
        # Core checking for hidden parent on display, base on existing json file.
        
        if f'{self.filename}_hid.json' in os.listdir():
            ans = messagebox.askyesno('TreeViewGui', f'Delete {self.filename}_hid.json?')
            if ans:
                os.remove(f'{self.filename}_hid.json')
                self.view()
                self.unlock = True
                messagebox.showinfo('TreeViewGui', f'{self.filename}_hid.json has been deleted!')
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
        if f'{self.filename}_hid.json' in os.listdir():
            with open(f'{self.filename}_hid.json') as jfile:
                rd = dict(json.load(jfile))
                            
            if rd['reverse'] is False:
                self.view()
                rolrd = [i for i in list(rd.values()) if isinstance(i, list)]
                showt = self.text.get('1.0', END).split('\n')[:-2]
                for wow, wrow in rolrd:
                    for i in range(wow, wrow+1):
                        showt[i] = 0
                self.text.config(state = 'normal')
                self.text.delete('1.0', END)
                showt = [f'{i}\n' for i in showt if i != 0]
                for i in showt:
                    self.text.insert(END, f'{i}')
                self.text.config(state = 'disable')
                vals = [f' {k}: {c[0]}' for k, 
                c  in list(tvg.insighthidden(showt).items())]
                self.listb.delete(0,END)
                for val in vals:
                    self.listb.insert(END, val)
            else:
                self.view()
                rolrd = [i for i in list(rd.values()) if isinstance(i, list)]
                showt = self.text.get('1.0', END).split('\n')[:-2]
                ih = []
                for wow, wrow in rolrd:
                    for i in range(wow, wrow+1):
                        ih.append(f'{showt[i]}\n')
                
                self.text.config(state = 'normal')
                self.text.delete('1.0', END)
                for i in ih:
                    self.text.insert(END, f'{i}')
                self.text.config(state = 'disable')
                vals = [f' {k}: {c[0]}' for k, 
                c  in list(tvg.insighthidden(ih).items())]
                self.listb.delete(0,END)
                for val in vals:
                    self.listb.insert(END, val)                
                    
    def hiddenchl(self, event = None):
        # Create Hidden position of parent and its childs in json file.
        
        import json
    
        if self.checkfile():
            if f'{self.filename}_hid.json' not in os.listdir():
                ckc = ['listb', 'button14', 'text']
                if self.listb.cget('selectmode') == 'browse':
                    for i in self.bt:
                        if 'label' not in i and 'scrollbar' not in i:
                            if i not in ckc:
                                self.bt[i].config(state='disable')
                    self.listb.config(selectmode = MULTIPLE)
                    TreeViewGui.FREEZE = True
                else:
                    if self.listb.curselection():
                        ask = messagebox.askyesno('TreeViewGui', '"Yes" to hide selected, "No" reverse hide instead!')
                        tvg = tv(self.filename)
                        allrows = [int(i) for i in self.listb.curselection()]
                        rows = tvg.insighttree()
                        hd = {}
                        num = 0
                        for row in allrows:
                            num += 1
                            if row in rows:
                                if row < len(rows)-1:
                                    if rows[row][0] == 'parent' and 'child' in rows[row+1][0]:
                                        srow = row+1
                                        while True:
                                            if srow < len(rows):
                                                if rows[srow][0] == 'space':
                                                    break
                                                srow +=1
                                            else:
                                                srow -=1
                                                break
                                        hd[num] = (row, srow)
                                    else:
                                        if rows[row][0] == 'parent':
                                            hd[num] = (row, row+1)                                        
                                else:
                                    if rows[row][0] == 'parent':
                                        hd[num] = (row, row)
                        if hd:
                            if ask:
                                rev = {'reverse': False}
                                with open(f'{self.filename}_hid.json', 'w') as jfile:
                                    json.dump(hd | rev, jfile)
                                self.hidform()                                
                            else:
                                rev = {'reverse': True}
                                with open(f'{self.filename}_hid.json', 'w') as jfile:
                                    json.dump(hd | rev, jfile)
                                self.hidform()
                        else:
                            self.listb.selection_clear(0, END)
                            messagebox.showinfo('TreeViewGui', 'Please choose Parent only!')
                    for i in self.bt:
                        if 'label' not in i and 'scrollbar' not in i:
                            if i not in ckc:
                                if i == 'entry3':
                                    self.bt[i].config(state='readonly')
                                elif i == 'entry':
                                    if not self.rb.get():
                                        self.bt[i].config(state='disable')
                                    else:
                                        self.bt[i].config(state='normal')
                                else:
                                    self.bt[i].config(state='normal')
                    self.listb.config(selectmode = BROWSE)
                    TreeViewGui.FREEZE = False
                    self.infobar()
            else:
                messagebox.showinfo('TreeViewGui', 'Hidden parent is recorded, please clear all first!')
            
    def delhid(self, event = None):
        # Deleting accordingly each position in json file, or can delete the file.
        
        import json
        
        if f'{self.filename}_hid.json' in os.listdir():
            with open(f'{self.filename}_hid.json') as jfile:
                rd = dict(json.load(jfile))
            if rd['reverse'] is False:
                rd = [i for i in list(rd.values()) if isinstance(i, list)]
                ans = messagebox.askyesno('TreeViewGui',
                'Please choose "Yes" to delete ascending order, or "No" to delete all?')
                if ans:
                    if rd:
                        rd.pop()
                        if rd:
                            rd = {k:v for k, v in list(enumerate(rd))}
                            rev = {'reverse': False}
                            with open(f'{self.filename}_hid.json', 'w') as jfile:
                                json.dump(rd | rev, jfile)
                            self.hidform()
                        else:
                            os.remove(f'{self.filename}_hid.json')
                            self.spaces()
                            messagebox.showinfo('TreeViewGui', f'{self.filename}_hid.json has been deleted!')
                else:
                    os.remove(f'{self.filename}_hid.json')
                    self.spaces()         
                    messagebox.showinfo('TreeViewGui', f'{self.filename}_hid.json has been deleted!')
            else:
                os.remove(f'{self.filename}_hid.json')
                self.spaces()
                messagebox.showinfo('TreeViewGui', f'{self.filename}_hid.json has been deleted!')
            
    def sendtel(self):
        # This is the sending note with Telethon [Telegram api wrapper].
        
        ori = os.getcwd()
        os.chdir(os.getcwd()[:os.getcwd().rfind('\\')])
        if self.text.get('1.0', END)[:-1]:
            TeleTVG.main(self.root, ori, self.text.get('1.0', END)[:-1])
        else:
            os.chdir(ori)
            messagebox.showinfo('TreeViewGui', 'Nothing to be sent!')
            
    def lookup(self):
        # To lookup word on row.
        
        self.hidcheck()
        if self.unlock:
            if self.checkfile():
                if self.entry.get():
                    tvg = tv(self.filename)
                    dat = tvg.insighttree()
                    num = len(dat)
                    sn = 0                    
                    sw = self.entry.get()
                    if sw.isdigit():
                        sw = int(sw)
                        if sw <= num-1:
                            self.listb.see(sw)
                            self.text.see(f'{sw+1}.0')                            
                            self.listb.focus()
                            self.listb.selection_clear(0, END)
                            self.listb.activate(sw)
                            self.listb.selection_set(sw)
                    else:
                        while sn < num:
                            if sw in dat[sn][1]:
                                self.text.see(f'{sn+1}.0')
                                self.listb.see(sn)
                                self.listb.selection_clear(0, END)
                                self.listb.selection_set(sn)
                                ask = messagebox.askyesno('TreeViewGui', 'Continue lookup?')
                                self.listb.focus()
                                self.listb.activate(sn)
                                if ask:
                                    sn += 1
                                    continue
                                else:
                                    break
                            else:
                                sn += 1
                    self.infobar()
    
    def dattim(self):
        # To insert date and time.
        
        import re
        
        if str(self.entry.cget('state')) == 'normal':
            dtt = f'[{dt.isoformat(dt.today().replace(microsecond = 0)).replace("T"," ")}]'
            ck = ['parent', 'child']
            if self.entry.get() in ck:
                self.entry.delete(0, END)
            if self.entry.get():
                hold = self.entry.get()
                gt = re.match(r'\[.*?\]', hold)
                if not gt:
                    self.entry.delete(0, END)
                    self.entry.insert(0, f'{dtt} {hold}')
                else:
                    try:
                        if isinstance(dt.fromisoformat(gt.group()[1:20]), dt):
                            self.entry.delete(0, END)
                            self.entry.insert(0, f'{dtt} {hold[22:]}')
                    except:
                        self.entry.delete(0, END)
                        self.entry.insert(0, f'{dtt} {hold}')                        
            else:
                self.entry.insert(0, f'{dtt} ')
    
    def endec(self):
        # Data encrypt and saved for sharing.
        
        from ProtectData import ProtectData as ptd
        
        self.hidcheck()
        if self.unlock:
            if self.checkfile():
                try:
                    enc = ptd.complek(self.text.get('1.0', END)[:-1], stat = False, t1 = 5, t2 = 7)
                    ins = f'{enc[0]}'
                    key = f'{[[j for j in i] for i in enc[1]]}'
                    with open(f'{self.filename}_protected.txt', 'wb') as encrypt:
                        encrypt.write(str({key:ins}).encode())
                    messagebox.showinfo('TreeViewGui', 'Encryption created!')
                except Exception as e:
                    messagebox.showerror('TreeViewGui', f'{e}')

    def openf(self):
        # Data decrypt and can be saved as _tvg file.
        
        from ProtectData import ProtectData as ptd
        
        self.hidcheck()
        if self.unlock:
            ask = filedialog.askopenfilename(filetypes = [("Encryption file","*_protected.txt")])
            if ask:
                try:
                    with open(f'{ask}', 'rb') as encrypt:
                        rd  = eval(encrypt.read().decode('utf-8'))
                    key = list(rd)[0]
                    ins = rd[key]
                    dec = ptd.complek(ins, key =((j for j in i) for i in eval(key)), 
                                      stat = False, t1 = 5, t2 = 7)
                    self.text.config(state = 'normal')
                    self.text.delete('1.0', END)
                    self.text.insert(END, dec)
                    self.text.config(state = 'disabled')
                    que = messagebox.askyesno('TreeViewGui', 'Want to save as this file?')
                    if que:
                        tvg = tv(f'{self.filename}')
                        tak = [f'{i}\n' for i in dec.split('\n') if i]
                        wtvg = tvg.insighthidden(tak)
                        tvg.fileread(wtvg)
                        self.spaces()
                    os.remove(ask)
                except Exception as e:
                    messagebox.showerror('TreeViewGui', f'{e}')
                    
    def createf(self):
        # Creating new file not able to open existing one.
        
        ask = messagebox.askyesno('TreeViewGui', 'Create new file?')
        if ask:
            fl = simpledialog.askstring('TreeViewGui', 'What is the name?')
            if fl:
                mkd = f'{fl.title()}_tvg' 
                dr = os.getcwd().rpartition('\\')[0]
                files = [file for file in os.listdir(dr) if '_tvg' in file]
                if mkd not in files:
                    os.chdir(dr)
                    os.mkdir(mkd)
                    os.chdir(mkd)
                    self.filename = fl.title()
                    self.root.title(f'{os.getcwd()}\{self.filename}.txt')
                    self.text.config(state = NORMAL)
                    self.text.delete('1.0', END)
                    self.text.config(state = DISABLED)
                    self.entry.delete(0, END)
                    self.rb.set('')
                    self.entry.config(state = DISABLED)
                else:
                    messagebox.showinfo('TreeViewGui', f'The file {mkd}/{fl.title()}.txt is already exist!')
            else:
                messagebox.showinfo('TreeViewGui', 'Nothing created yet!')
        else:
            messagebox.showinfo('TreeViewGui', 'Create new file is aborted!')
                
    def lockf(self):
        # Lock file as encrypted file.
        # Also unclock it directly when open with TVG.
        
        from ProtectData import ProtectData as ptd
        
        self.hidcheck()
        if self.unlock:
            if os.path.isfile(f'{self.filename}.txt'):
                try:
                    enc = ptd.complek(self.text.get('1.0', END)[:-1], stat = False, t1 = 5, t2 = 7)
                    ins = f'{enc[0]}'
                    key = f'{[[j for j in i] for i in enc[1]]}'
                    with open(f'{self.filename}.protected', 'wb') as encrypt:
                        encrypt.write(str({key:ins}).encode())
                    os.remove(f'{self.filename}.txt')
                    messagebox.showinfo('TreeViewGui', f'{self.filename}.txt is locked!')
                    self.root.destroy()
                except Exception as e:
                    messagebox.showerror('TreeViewGui', f'{e}')
            elif os.path.isfile(f'{self.filename}.protected'):
                try:
                    with open(f'{self.filename}.protected', 'rb') as encrypt:
                        rd  = eval(encrypt.read().decode('utf-8'))
                    key = list(rd)[0]
                    ins = rd[key]
                    dec = ptd.complek(ins, key =((j for j in i) for i in eval(key)), 
                                      stat = False, t1 = 5, t2 = 7)
                    tvg = tv(f'{self.filename}')
                    tak = [f'{i}\n' for i in dec.split('\n') if i]
                    wtvg = tvg.insighthidden(tak)
                    tvg.fileread(wtvg)
                    self.spaces()
                    os.remove(f'{self.filename}.protected')
                except Exception as e:
                    messagebox.showerror('TreeViewGui', f'{e}')
                
def main():
    # Starting point of running TVG and making directory for non-existing file.
    
    root = Tk()
    root.wm_iconbitmap(default = 'TVG.ico')
    root.withdraw()
    if 'lastopen.tvg' in os.listdir():
        ask = messagebox.askyesno('TreeViewGui', 'Want to open previous file?')
        if ask:
            with open('lastopen.tvg', 'rb') as lop:
                rd = eval(lop.read().decode('utf-8'))
            filename = rd['lop']
        else:
            os.remove('lastopen.tvg')
            filename = simpledialog.askstring('Filename', 'Create filename:')
    else:
        filename = simpledialog.askstring('Filename', 'Create filename:')    
    if filename:
        filename = filename.title()
        if f'{filename}_tvg' not in os.listdir():
            try:
                os.mkdir(f'{filename}_tvg')
                os.chdir(f'{filename}_tvg')
            except:
                os.chdir(f'{filename}_tvg')
        else:
            with open('lastopen.tvg', 'wb') as lop:
                lop.write(str({'lop': filename}).encode())
            os.chdir(f'{filename}_tvg')
        begin = TreeViewGui(root = root, filename = filename)
        begin.root.deiconify()
        if f'{filename}.protected' in os.listdir():
            begin.lockf()
        else:
            if f'{filename}_hid.json' in os.listdir():
                begin.hidform()
                begin.infobar()
            else:
                begin.view()
        begin.root.mainloop()
    else:
        messagebox.showwarning('File', 'No File Name!')
        root.destroy()
        
if __name__ == '__main__':
    main()