# -*- coding: utf-8 -*-
# Copyright © kakkarja (K A K)

from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import simpledialog, messagebox, colorchooser
from .TreeView import TreeView as tv
import sys
import os
import re
from .mdh import convhtml
from .DataB import Datab as db
from datetime import datetime as dt

class TreeViewGui:
    """
    This is the Gui for TreeView engine. This gui is to make the Writing and editing is viewable.
    """
    DB = None
    FREEZE = False
    MARK = False
    MODE = False
    GEO = None
    def __init__(self, root, filename):
        self.filename = filename
        self.root = root
        self.root.title(f'{os.getcwd()}\\{self.filename}.txt')
        self.root.protocol('WM_DELETE_WINDOW', self.tvgexit)
        self.wwidth = 835
        self.wheight = 610
        self.pwidth = int(self.root.winfo_screenwidth()/2 - self.wwidth/2)
        self.pheight = int(self.root.winfo_screenheight()/3 - self.wheight/3)
        self.root.geometry(f"{self.wwidth}x{self.wheight}+{self.pwidth}+{self.pheight}")
        TreeViewGui.GEO = f"{self.wwidth}x{self.wheight}+{self.pwidth}+{self.pheight}"
        gpath = os.getcwd().rpartition('\\')[0]
        gem = None
        if 'geo.tvg' in os.listdir(gpath):
            with open(os.path.join(gpath, 'geo.tvg'), 'rb') as geo:
                gem = geo.read().decode('utf-8')
            if '{' == gem[0] and '}' == gem[-1]:
                gem = eval(gem)
                self.root.geometry(gem['geo'])
                TreeViewGui.GEO = gem['geo']
        del gpath
        del gem
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
        self.root.bind_all('<Control-Key-2>', self.lookup)
        self.root.bind_all('<Control-Key-3>', self.dattim)
        self.root.bind_all('<Control-Key-6>', self.fcsent)
        self.root.bind_all('<Control-Key-7>', self.fcsent)
        self.root.bind_all('<Control-Key-9>', self.fcsent)
        self.root.bind_all('<Control-Key-period>', self.fcsent)
        self.root.bind_all('<Control-Key-comma>', self.fcsent)
        self.root.bind_all('<Control-Key-slash>', self.fcsent)
        self.root.bind_all('<Control-Key-bracketleft>', self.fcsent)
        self.root.bind_all('<Control-Key-bracketright>', self.temp)
        self.root.bind_all('<Control-Key-g>', self.fcsent)
        self.root.bind_all('<Control-Key-backslash>', self.fcsent)
        self.root.bind_all('<Control-Key-question>', self.fcsent)
        self.root.bind_all('<Shift-Return>', self.inenter)
        self.root.bind_all('<Control-Key-F2>', self.fcsent)
        self.root.bind_class('TButton', '<Enter>', self.ttip)
        self.root.bind_class('TButton', '<Leave>', self.leave)
        self.root.bind_class('TRadiobutton', '<Enter>', self.ttip)
        self.root.bind_class('TRadiobutton', '<Leave>', self.leave)
        self.root.bind_all('<Control-Key-F3>', self.fcsent)
        self.bt = {}
        self.rb = StringVar()
        self.lock = False
        self.store = None
        self.editorsel = None
        self.stl = ttk.Style(self.root)
        self.stl.theme_use('clam')
        self.stl.map('Horizontal.TScrollbar', background = [('active', '#eeebe7')])
        self.stl.map('Vertical.TScrollbar', background = [('active', '#eeebe7')])
        
        # 1st frame. 
        # Frame for label and Entry.
        self.fframe = ttk.Frame(root)
        self.fframe.pack(side = TOP, fill = 'x')
        self.label = ttk.Label(self.fframe, text = 'Words')
        self.label.pack(side = LEFT, pady = 3, fill = 'x')
        self.bt['label'] = self.label
        self.entry = ttk.Entry(self.fframe, validate = 'focusin', validatecommand = self.focus, font = 'consolas 12')
        self.entry.pack(side = LEFT, ipady = 5, pady = (3, 1), fill = 'both', expand = 1)
        self.entry.config(state = 'disable')
        self.bt['entry'] = self.entry
       
        # 2nd frame in first frame.
        # Frame for radios button.
        self.frbt = ttk.Frame(self.fframe)
        self.frbt.pack()
        self.frrb = ttk.Frame(self.frbt)
        self.frrb.pack(side = BOTTOM)
        self.radio1 = ttk.Radiobutton(self.frbt, text = 'parent', value = 'parent', var = self.rb, command = self.radiobut)
        self.radio1.pack(side = LEFT,anchor = 'w')
        self.bt['radio1'] = self.radio1
        self.radio2 = ttk.Radiobutton(self.frbt, text = 'child', value = 'child', var = self.rb, command = self.radiobut)
        self.radio2.pack(side = RIGHT, anchor = 'w')
        self.bt['radio2'] = self.radio2
        
        # 3rd frame in 2nd frame.
        # Frame for Child ComboBox
        self.frcc = ttk.Frame(self.frrb)
        self.frcc.pack(side = TOP)
        self.label3 = ttk.Label(self.frcc, text = 'Child')
        self.label3.pack(side = LEFT, padx = 1, pady = (0, 1), fill = 'x')
        self.bt['label3'] = self.label3
        self.entry3 = ttk.Combobox(self.frcc, width = 8, exportselection = False, state = 'readonly', justify = 'center')
        self.entry3.pack(side = LEFT, padx = 1, pady = (0, 1), fill = 'x')
        self.bt['entry3'] = self.entry3
        
        # 3rd frame for top buttons.
        # Frame for first row Buttons.
        self.bframe = ttk.Frame(self.root)
        self.bframe.pack(side = TOP, fill = 'x')
        self.button5 = ttk.Button(self.bframe, text = 'Insert', width = 3, command = self.insertwords)
        self.button5.pack(side = LEFT, pady = (2, 3), padx = (1, 1), fill = 'x', expand = 1)
        self.button5.propagate(0)
        self.bt['button5'] = self.button5
        self.button6 = ttk.Button(self.bframe, text = 'Write', width = 3, command =  self.writefile)
        self.button6.pack(side = LEFT, pady = (2, 3), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button6'] = self.button6
        self.button9 = ttk.Button(self.bframe, text = 'Delete', width = 3, command = self.deleterow)
        self.button9.pack(side = LEFT, pady = (2, 3), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button9'] = self.button9        
        self.button7 = ttk.Button(self.bframe, text = 'BackUp', width = 3, command = self.backup)
        self.button7.pack(side = LEFT, pady = (2, 3), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button7'] = self.button7
        self.button8 = ttk.Button(self.bframe, text = 'Load', width = 3, command = self.loadbkp)
        self.button8.pack(side = LEFT, pady = (2, 3), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button8'] = self.button8
        self.button3 = ttk.Button(self.bframe, text = 'Move Child', width = 3, command = self.move_lr)
        self.button3.pack(side = LEFT, pady = (2, 3), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button3'] = self.button3        
        self.button16 = ttk.Button(self.bframe, text = 'Change File', width = 3, command = self.chgfile)
        self.button16.pack(side = LEFT, pady = (2, 3), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button16'] = self.button16
        self.button17 = ttk.Button(self.bframe, text = 'CPP', width = 3, command = self.cmrows)
        self.button17.pack(side = LEFT, pady = (2, 3), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button17'] = self.button17
        self.button18 = ttk.Button(self.bframe, text = 'Send Note', width = 3, 
                                   command = lambda: self.messages('<<TVG>>\n\nNot available\n\nin free version!', 2000))
        self.button18.pack(side = LEFT, pady = (2, 3), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button18'] = self.button18
        self.button19 = ttk.Button(self.bframe, text = 'Look Up', width = 3, command = self.lookup)
        self.button19.pack(side = LEFT, pady = (2, 3), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button19'] = self.button19
        
        # 4th frame for below buttons.
        # Frame for second row buttons.
        self.frb1 = ttk.Frame(self.root)
        self.frb1.pack(fill = X)
        self.button10 = ttk.Button(self.frb1, text = 'Insight', width = 3, command = self.insight)
        self.button10.pack(side = LEFT, pady = (0, 3), padx = (1, 1), fill = 'x', expand = 1)
        self.bt['button10'] = self.button10
        self.button13 = ttk.Button(self.frb1, text = 'Arrange', width = 3, command = self.spaces)
        self.button13.pack(side = LEFT, pady = (0, 3), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button13'] = self.button13
        self.button11 = ttk.Button(self.frb1, text = 'Paste', width = 3, command = self.copas)
        self.button11.pack(side = LEFT, pady = (0, 3), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button11'] = self.button11
        self.button4 = ttk.Button(self.frb1, text = 'Checked', width = 3, command = self.checked)
        self.button4.pack(side = LEFT, pady = (0, 3), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button4'] = self.button4
        self.button = ttk.Button(self.frb1, text = 'Up', width = 3, command = self.moveup)
        self.button.pack(side = LEFT, pady = (0, 3), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button'] = self.button
        self.button2 = ttk.Button(self.frb1, text = 'Down', width = 3, command = self.movedown)
        self.button2.pack(side = LEFT, pady = (0, 3), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button2'] = self.button2
        self.button12 = ttk.Button(self.frb1, text = 'Printing', width = 3, command = self.saveaspdf)
        self.button12.pack(side = LEFT, pady = (0, 3), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button12'] = self.button12
        self.button14 = ttk.Button(self.frb1, text = 'Hide Parent', width = 3, command = self.hiddenchl)
        self.button14.pack(side = LEFT, pady = (0, 3), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button14'] = self.button14
        self.button15 = ttk.Button(self.frb1, text = 'Clear hide', width = 3, command = self.delhid)
        self.button15.pack(side = LEFT, pady = (0, 3), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button15'] = self.button15
        self.button20 = ttk.Button(self.frb1, text = 'Date-Time', width = 3, command = self.dattim)
        self.button20.pack(side = LEFT, pady = (0, 3), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button20'] = self.button20        
        
        # 7th Frame
        # For third row  of buttons
        self.frb2 = ttk.Frame(self.root)
        self.frb2.pack(fill = X)
        self.button21 = ttk.Button(self.frb2, text = 'Save', width = 3, 
                                   command = lambda: self.messages('<<TVG>>\n\nNot available\n\nin free version!', 2000))
        self.button21.pack(side = LEFT, pady = (0, 2), padx = (1, 1), fill = 'x', expand = 1)
        self.bt['button21'] = self.button21
        self.button22 = ttk.Button(self.frb2, text = 'Open', width = 3, 
                                   command = lambda: self.messages('<<TVG>>\n\nNot available\n\nin free version!', 2000))
        self.button22.pack(side = LEFT, pady = (0, 2), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button22'] = self.button22          
        self.button23 = ttk.Button(self.frb2, text = 'Create file', width = 3, command = self.createf)
        self.button23.pack(side = LEFT, pady = (0, 2), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button23'] = self.button23
        self.button24 = ttk.Button(self.frb2, text = 'Editor', width = 3, command = self.editor)
        self.button24.pack(side = LEFT, pady = (0, 2), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button24'] = self.button24
        self.button25 = ttk.Button(self.frb2, text = 'Un/Wrap', width = 3, command = self.wrapped)
        self.button25.pack(side = LEFT, pady = (0, 2), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button25'] = self.button25        
        self.button26 = ttk.Button(self.frb2, text = 'Calculator', width = 3, 
                                   command = lambda: self.messages('<<TVG>>\n\nNot available\n\nin free version!', 2000))
        self.button26.pack(side = LEFT, pady = (0, 2), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button26'] = self.button26
        self.button27 = ttk.Button(self.frb2, text = 'Ex', width = 3, command = self.editex)
        self.button27.pack(side = LEFT, pady = (0, 2), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button27'] = self.button27
        self.button28 = ttk.Button(self.frb2, text = 'Template', width = 3, command = self.temp)
        self.button28.pack(side = LEFT, pady = (0, 2), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button28'] = self.button28
        self.button29 = ttk.Button(self.frb2, text = 'Emoji', width = 3, command = lambda: self.messages('<<TVG>>\n\nNot available\n\nin free version!', 2000))
        self.button29.pack(side = LEFT, pady = (0, 2), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button29'] = self.button29
        self.button30 = ttk.Button(self.frb2, text = 'HTML View', width = 3, command = self.htmlview)
        self.button30.pack(side = LEFT, pady = (0, 2), padx = (0, 1), fill = 'x', expand = 1)
        self.bt['button30'] = self.button30
        self.stl.configure('TButton', font = 'verdana 8 bold')
        
        # 5th frame.
        # Frame for text, listbox and scrollbars.
        frw = int(round(self.root.winfo_screenwidth() * 0.9224011713030746))
        lbw = int(round(frw * 0.09285714285714286))
        scw = int(round(frw * 0.011904761904761904))
        ftt = 'verdana 11'
        self.tframe = ttk.Frame(root)
        self.tframe.pack(anchor = 'w', side = TOP, fill = 'both', expand = 1)
        self.txframe = Frame(self.tframe)
        self.txframe.pack(anchor = 'w', side = LEFT, fill = 'both', expand = 1)
        self.txframe.pack_propagate(0)
        self.text = Text(self.txframe, font = ftt, padx = 5, pady = 3, wrap = NONE, 
                         undo = True, autoseparators = True, maxundo = -1)
        self.text.config(state = 'disable')
        self.text.pack(side = LEFT, fill = 'both', padx = (2,1), pady = (1,0), expand = 1)
        self.text.bind('<MouseWheel>', self.mscrt)
        self.text.bind('<Control-z>', self.undo)
        self.text.bind('<Control-Shift-Key-Z>', self.redo)
        self.text.pack_propagate(0)
        self.bt['text'] = self.text
        self.sc1frame = ttk.Frame(self.tframe, width = scw-1)
        self.sc1frame.pack(anchor = 'w', side = LEFT, fill = 'y', pady = 1)
        self.sc1frame.pack_propagate(0)
        self.scrollbar1 = ttk.Scrollbar(self.sc1frame, orient="vertical")
        self.scrollbar1.config(command = self.text.yview) 
        self.scrollbar1.pack(side="left", fill="y") 
        self.scrollbar1.bind('<ButtonRelease>', self.mscrt)
        self.text.config(yscrollcommand = self.scrollbar1.set)
        self.bt['scrollbar1'] = self.scrollbar1
        self.tlframe = ttk.Frame(self.tframe, width = lbw)
        self.tlframe.pack(anchor = 'w', side = LEFT, fill = 'y')
        self.tlframe.pack_propagate(0)        
        self.listb = Listbox(self.tlframe, font = ftt, exportselection = False)
        self.listb.pack(side = LEFT, fill = 'both', expand = 1)
        self.listb.pack_propagate(0)
        self.bt['listb'] = self.listb
        self.sc2frame = ttk.Frame(self.tframe, width = scw)
        self.sc2frame.pack(anchor = 'w', side = LEFT, fill = 'y', pady = 1)
        self.sc2frame.pack_propagate(0)
        self.scrollbar2 = ttk.Scrollbar(self.sc2frame, orient = "vertical")
        self.scrollbar2.config(command = self.listb.yview) 
        self.scrollbar2.pack(side = "left", fill = "y")
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
        self.fscr = ttk.Frame(self.root)
        self.fscr.pack(fill = 'x')
        self.frsc = ttk.Frame(self.fscr, height = scw+1)
        self.frsc.pack(side = LEFT, fill = 'x', padx = (2, 1), expand = 1)
        self.frsc.propagate(0)
        self.scrolh = ttk.Scrollbar(self.frsc, orient = "horizontal")
        self.scrolh.pack(side = LEFT, fill = 'x', expand = 1)
        self.scrolh.config(command = self.text.xview)
        self.scrolh.propagate(0)
        self.text.config(xscrollcommand = self.scrolh.set)
        self.info = StringVar()
        self.info.set(f'{dt.strftime(dt.today(),"%a %d %b %Y")}')        
        self.frlab = ttk.Frame(self.fscr, width = lbw + (scw*2), height = scw)
        self.frlab.pack(side = LEFT, fill = 'x')
        self.frlab.propagate(0)
        self.labcor = Label(self.frlab, textvariable = self.info,
                            font = 'consolas 10 bold', justify = CENTER)
        self.labcor.pack(side = LEFT, fill = 'x', expand = 1)
        self.labcor.propagate(0)
        self.unlock = True
        if 'ft.tvg' in os.listdir(os.getcwd().rpartition('\\')[0]):
            self.ft(path = os.path.join(os.getcwd().rpartition('\\')[0], 'ft.tvg'))        
        if 'theme.tvg' in os.listdir(os.getcwd().rpartition('\\')[0]):
            self.txtcol(path = os.path.join(os.getcwd().rpartition('\\')[0],'theme.tvg'), wr = False)
        if os.path.isfile(os.path.join(os.getcwd().rpartition('\\')[0], 'hbts.tvg')):
            frm = [self.bframe, self.frb1, self.frb2]
            for fr in frm:
                fr.pack_forget()
            del frm
        if os.path.isfile(os.path.join(os.getcwd().rpartition('\\')[0], 'sty.tvg')):
            with open(os.path.join(os.getcwd().rpartition('\\')[0], 'sty.tvg')) as ty:
                rd = ty.read()
                if rd == 'ease': self.ldmode()
            del rd
        self.tpl = None
        self.ai = None
        self.scribe = {
                       'Insert': 'Insert word in outline on selected row', 
                       'Write': 'Write word to outline base on chosen as parent or child', 
                       'Delete': 'Delete an outline row', 
                       'BackUp': 'Backup outline note [max 10 and recycle]', 
                       'Load': 'Load a backuped note', 
                       'Move Child': 'Move a child base note to left or right', 
                       'Change File': 'Change to another existing file', 
                       'CPP': 'Copy or move selected outline rows', 
                       'Send Note': 'Switch to TeleTVG for sending note or chat', 
                       'Look Up': 'Look up word in outline list and in Editor mode', 
                       'Insight': 'Details about outline position rows', 
                       'Arrange': 'Clear selected row and arrange outline internally', 
                       'Paste': 'Paste selected row to word for editing', 
                       'Checked': 'Insert "Check mark" or "Done" in selected row ', 
                       'Up': 'Move selected row up', 
                       'Down': 'Move selected row down', 
                       'Printing': 'Create html page for printing', 
                       'Hide Parent': 'Hiding parent and its childs or reverse', 
                       'Clear hide': 'Clearing hidden back to appearing again', 
                       'Date-Time': 'Insert time-stamp in Word and Editor mode', 
                       'Save': 'Save note as encrypted text and can be send', 
                       'Open': 'Open the encrypted TVG text file and can be saved', 
                       'Create file': 'Create new empty note', 
                       'Editor': 'To create outline note without restriction with proper format', 
                       'Un/Wrap': 'Wrap or unwrap outline note', 
                       'Calculator': 'Switch to calculator', 
                       'Ex': 'Edit whole notes or selected parent in Editor mode', 
                       'Template': 'Create template for use frequently in Editor mode', 
                       'Emoji': 'Insert emoji to note', 
                       'HTML View': 'Viewing html page that has been created before',
                       'parent': 'Create parent',
                       'child': 'Create child ["Child" for positioning]'
                       }
            
    def ldmode(self, event = None):
        # Dark mode for easing the eye.
        
        oribg = '#dcdad5'
        chbg = 'grey30'
        orifg = 'black'
        chfg = 'white'
        if self.stl.lookup('.', 'background') != chbg:
            self.stl.configure('.', background = chbg,
                               foreground = chfg,
                               fieldbackground = chbg,
                               insertcolor = chfg,
                               troughcolor = chbg,
                               arrowcolor = chfg,
                               bordercolor = chbg
                              )
            self.stl.map('.', background = [('background', chbg)],
                        )
            self.stl.map('TCombobox', fieldbackground = [('readonly', chbg)],
                         background = [('active', 'gold')],
                         arrowcolor = [('active', 'black')]
                        )
            self.stl.map('Horizontal.TScrollbar', background = [('active', 'gold')],
                         arrowcolor = [('active', 'black')],
                        )
            self.stl.map('Vertical.TScrollbar', background = [('active', 'gold')],
                        arrowcolor = [('active', 'black')], 
                        )            
            self.stl.configure('TEntry', fieldbackground = chbg)
            self.labcor.config(bg = chbg, fg = chfg)
            if str(self.text.cget('background')) == 'SystemWindow':
                with open(os.path.join(os.getcwd().rpartition('\\')[0], 'theme.tvg'), 'w') as thm:
                    thm.write('#4d4d4d')
                self.txtcol(path = os.path.join(os.getcwd().rpartition('\\')[0], 'theme.tvg'), wr = False)
            with open(os.path.join(os.getcwd().rpartition('\\')[0], 'sty.tvg'), 'w') as ty:
                ty.write('ease')
        else:
            self.stl.configure('.', background = oribg,
                               foreground = orifg,
                               fieldbackground = oribg,
                               insertcolor = orifg,
                               troughcolor = '#bab5ab',
                               arrowcolor = orifg,
                               bordercolor = '#9e9a91',
                              )
            self.stl.map('.', background=[('background', oribg)])
            self.stl.configure('TEntry', fieldbackground = 'white')
            self.stl.map('TCombobox', foreground = [('focus', 'white')],
                         fieldbackground = [('focus', 'dark blue'),
                                            ('readonly', oribg),
                                           ],
                         background = [('active', '#eeebe7')],
                        )
            self.stl.map('Horizontal.TScrollbar', background = [('active', '#eeebe7')])
            self.stl.map('Vertical.TScrollbar', background = [('active', '#eeebe7')])
            self.labcor.config(bg = 'White', fg = orifg)
            os.remove(os.path.join(os.getcwd().rpartition('\\')[0], 'sty.tvg'))
    
    def ttip(self, event =  None):
        # Tooltip for TVG buttons.
        
        def exit():
            self.root.update()
            self.ai = None
            self.tpl = None
            master.destroy()
        master = Toplevel(self.root)
        master.overrideredirect(1)
        tx = self.scribe[event.widget['text']]
        ft = font.Font(master, font='verdana')
        if event.widget['text'] in ['Save', 'Insight', 'Insert']:
            master.geometry(f'{int(ft.measure(tx)/1.6)}x{15}+{event.widget.winfo_pointerx()}+{event.widget.winfo_pointery()+30}')
        elif event.widget['text'] in ['Look Up', 'Date-Time', 'HTML View', 'child']:
            master.geometry(f'{int(ft.measure(tx)/1.6)}x{15}+{event.widget.winfo_pointerx()-220}+{event.widget.winfo_pointery()+30}')
        else:
            master.geometry(f'{int(ft.measure(tx)/1.6)}x{15}+{event.widget.winfo_pointerx()-80}+{event.widget.winfo_pointery()+30}')
        a = Message(master= master, text = tx, justify = 'center', aspect = int(ft.measure(tx)*50), bg = 'white', font = 'verdana 7')
        a.pack(fill = 'both', expand = 1)
        self.ai = self.root.after(3000, exit)
        self.tpl = master
        
    def leave(self, event = None):
        # On hovering and leaving a button the tooltip will be destroyed.
        
        if self.ai and self.tpl:
            self.root.after_cancel(self.ai)
            self.tpl.destroy()
            
    def hidbs(self, event =  None):
        # Hide Buttons.
        
        frm = [self.bframe, self.frb1, self.frb2]
        pth = os.path.join(os.getcwd().rpartition('\\')[0], 'hbts.tvg')        
        self.tframe.pack_forget()
        self.fscr.pack_forget()
        if bool(frm[0].winfo_ismapped()):
            for fr in frm:
                fr.pack_forget()
            with open(pth, 'w') as bh:
                bh.write('buttons hide')
        else:
            for fr in frm:
                fr.pack(side = TOP, fill = 'x')
            self.stl.configure('TButton', font = 'verdana 8 bold')
            os.remove(pth)
        self.tframe.pack(anchor = 'w', side = TOP, fill = 'both', expand = 1)
        self.fscr.pack(fill ='x')
        del frm
        
    def inenter(self, event):
        # For invoking any focus button or radiobutton
        
        ck = ['button', 'radio']
        fcs = str(event.widget).rpartition('!')[2]
        if ck[0] in fcs or ck[1] in fcs:
            event.widget.invoke()
            
    def undo(self, event = None):
        # Undo only in Editor.
        
        if str(self.text['state']) == 'normal':
            try:
                self.text.edit_undo()
            except:
                messagebox.showerror('TreeViewGui', 'Nothing to undo!')
                
    def redo(self, event =None):
        # Redo only in Editor.
        
        if str(self.text['state']) == 'normal':
            try:
                self.text.edit_redo()
            except:
                messagebox.showerror('TreeViewGui', 'Nothing to redo!')
                
    def wrapped(self, event = None):
        # Wrap the records so that all filled the text window.
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
        
        if self.text.get('1.0', END)[:-1]:
            gt = self.text.get('1.0', END)[:-1]
            keys = [k for k in gt.split('\n') if k and '.' not in k]
            x = re.compile(r'.*?[\.|\!|\?]')
            values = [[w.removeprefix(' ') for w in x.findall(v)] for v in gt.split('\n') if '.' in v]
            conv = dict(zip(keys, values))
            tvg = tv(self.filename)
            if conv and len(keys) == len (values):
                for i in conv:
                    if self.checkfile():
                        tvg.addparent(i)
                    else:
                        tvg.writetree(i)
                    for j in conv[i]:
                        if j:
                            tvg.quickchild(j, 'child1')
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
            else:
                messagebox.showinfo('TreeViewGui', 'Unable to convert!')
            
    def infobar(self, event = None):
        # Info Bar telling the selected rows in listbox.
        # If nothing, it will display today's date.

        if f'{self.filename}_hid.json' in os.listdir():
            self.info.set('Hidden Mode')
        elif TreeViewGui.FREEZE and str(self.bt['button17']['state']) == 'normal':
            self.info.set('CPP Mode')
        elif TreeViewGui.FREEZE and str(self.bt['button24']['state']) == 'normal':
            self.info.set('Editor Mode')
        elif self.listb.curselection():
            tvg = tv(f'{self.filename}')
            ck = tvg.insighttree()[int(self.listb.curselection()[0])][1][:12]
            self.info.set(f'{self.listb.curselection()[0]}: {ck[:-1]}...')
            self.text.see(f'{self.listb.curselection()[0]}.0')
            del ck
        else:
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
                self.pwidth = self.root.winfo_x() - 1
                self.root.geometry(f"+{self.pwidth}+{self.pheight}")
            elif event.keysym == 'Right' and 'entry' not in fcom:
                self.pwidth = self.root.winfo_x() + 1
                self.root.geometry(f"+{self.pwidth}+{self.pheight}")
            elif event.keysym == 'Down' and 'entry' not in fcom:
                self.pheight = self.root.winfo_y() + 1
                self.root.geometry(f"+{self.pwidth}+{self.pheight}")
            elif event.keysym == 'Up' and 'entry' not in fcom:
                self.pheight = self.root.winfo_y() - 1
                self.root.geometry(f"+{self.pwidth}+{self.pheight}")
            elif event.keysym == 'n':
                self.cmrows()
            elif event.keysym == 'g':
                self.chgfile()
            elif event.keysym == '6':
                self.createf()
            elif event.keysym == '7':
                self.editor()
            elif event.keysym == '9':
                self.wrapped()
            elif event.keysym == 'bracketleft':
                self.editex()
            elif event.keysym == 'period':
                self.txtcol()
            elif event.keysym == 'comma':
                self.ft()
            elif event.keysym == 'slash':
                self.oriset()
            elif event.keysym == 'backslash':
                self.htmlview()
            elif event.keysym == 'F2':
                self.hidbs()
            elif event.keysym == 'F3':
                self.ldmode()            
        else:
            if str(self.bt['button17'].cget('state')) == 'normal' and event.keysym  == 'n':
                self.cmrows()
            elif str(self.bt['button14'].cget('state')) == 'normal' and event.keysym  == 'h':
                self.hiddenchl()
            elif str(self.bt['button24'].cget('state')) == 'normal' and event.keysym  == '7':
                self.editor()
                
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
                    nf = str(self.text.cget('font'))
                    try:
                        text_font = font.Font(self.root, font = nf, name = nf, exists=True)
                    except:
                        text_font = font.Font(self.root, font = nf, name = nf, exists=False)
                    g = re.compile(r'\s+')
                    em = text_font.measure(" ")
                    for r in rd:
                        gr = g.match(r)
                        if gr and gr.span()[1] > 1:
                            if str(gr.span()[1]) not in self.text.tag_names():
                                bullet_width = text_font.measure(f'{gr.span()[1]*" "}-')
                                self.text.tag_configure(f"{gr.span()[1]}", lmargin1=em, lmargin2=em+bullet_width)
                            self.text.insert(END, r, f'{gr.span()[1]}')
                        else:
                            self.text.insert(END, r)
                self.text.config(state = 'disable')
                vals = [f' {k}: {c[0]}' for k, c  in list(tvg.insighttree().items())]
                self.listb.delete(0,END)
                for val in vals:
                    self.listb.insert(END, val)
                self.text.yview_moveto(1.0)
                self.listb.yview_moveto(1.0)
        except:
            self.text.insert(END, sys.exc_info()[1])
            self.text.config(state = 'disable')
            
    def chgfile(self):
        # Changing file on active app environment.
        
        def chosen(file):
            fi = file
            TreeViewGui.FREEZE = False
            ask = messagebox.askyesno('TreeViewGui', '"Yes" to change file, "No" to delete directory')
            if ask:
                os.chdir(os.path.join(os.getcwd().rpartition('\\')[0], fi))
                self.filename = fi.rpartition('_')[0]
                self.root.title(f'{os.getcwd()}\\{self.filename}.txt')
                if f'{self.filename}.txt' in os.listdir():
                    if f'{self.filename}_hid.json' not in os.listdir():
                        self.spaces()
                        self.infobar()
                    else:
                        self.hidform()
                        self.infobar()
                else:
                    self.text.config(state = 'normal')
                    self.text.delete('1.0', END)
                    self.text.config(state = 'disable')
                    self.listb.delete(0,END)
            else:
                import shutil
                ori = os.getcwd()
                if ori.rpartition('\\')[2] != fi:
                    lf = os.listdir(os.path.join(os.getcwd().rpartition('\\')[0], fi))
                    lsc = messagebox.askyesno('TreeViewGui', f'Do you really want to delete {fi} directory with all\n{lf}\nfiles?')
                    if lsc:
                        shutil.rmtree(os.path.join(os.getcwd().rpartition('\\')[0], fi))
                    else:
                        messagebox.showinfo('TreeViewGui', 'Deleting directory is aborted!')
                else:
                    messagebox.showerror('TreeViewGui', 'You are unable to delete present directory!!!')
                    
        if self.lock is False:
            TreeViewGui.FREEZE = True        
            self.lock = True
            files = [file for file in os.listdir(os.getcwd()[:os.getcwd().rfind('\\')]) if '_tvg' in file]
            class MyDialog(simpledialog.Dialog):
            
                def body(self, master):
                    self.title('Choose File')
                    Label(master, text="File: ").grid(row=0, column = 0, sticky = E)
                    self.e1 = ttk.Combobox(master, state = 'readonly')
                    self.e1['values'] = files
                    self.e1.current(0)
                    self.e1.grid(row=0, column=1)
                    return self.e1
            
                def apply(self):
                    self.result = self.e1.get()
                                
            d = MyDialog(self.root)
            self.lock = False
            if d.result:
                chosen(d.result)
            else:
                TreeViewGui.FREEZE = False
                
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
                try:
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
                        self.text.see(f'{int(rw)}.0')
                        self.listb.see(rw)
                except Exception as e:
                    messagebox.showerror('TreeViewGui', f'{e}')
                    
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
                        TreeViewGui.MODE = True
                        rw = self.listb.curselection()
                        if int(rw[0]) != 0: tvg.delrow(int(rw[0]))
                        self.spaces()
                        ck = tvg.insighttree()
                        if int(rw[0]) < len(ck):
                            cp = ck[int(rw[0])][0]
                            if cp == 'parent' and int(rw[0]) != 0:
                                self.listb.select_set(int(rw[0])-2)
                                self.listb.see(int(rw[0])-2)
                                self.text.see(f'{(int(rw[0])-2)}.0')
                            else:
                                if cp == 'space':
                                    self.listb.select_set(int(rw[0])-1)
                                    self.listb.see(int(rw[0])-1)
                                    self.text.see(f'{(int(rw[0])-1)}.0')
                                else:
                                    self.listb.select_set(int(rw[0]))
                                    self.listb.see(int(rw[0]))
                                    self.text.see(f'{int(rw[0])}.0')
                        else:
                            if len(ck) == 1:
                                self.listb.select_set(0)
                            else:
                                self.listb.select_set(len(ck)-1)
                                self.listb.see(len(ck)-1)
                                self.text.see(f'{(len(ck)-1)}.0')
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
                    TreeViewGui.MODE = True
                    rw = self.listb.curselection()
                    tvg = tv(self.filename)
                    try:
                        self.text.config(state = 'normal')
                        tvg.movechild(int(rw[0]), self.entry3.get())
                        self.spaces()
                        self.listb.select_set(int(rw[0]))
                        self.listb.see(int(rw[0]))
                        self.text.see(f'{int(rw[0])}.0')
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
                        if int(rw[0]) != 0 and int(rw[0])-1 != 0:
                            TreeViewGui.MODE = True
                            tvg.movetree(int(rw[0]), int(rw[0])-1)
                            self.spaces()
                            ck = tvg.insighttree()
                            if  ck[int(rw[0])-1][0] != 'space':
                                self.listb.select_set(int(rw[0])-1)
                                self.listb.see(int(rw[0])-1)
                                self.text.see(f'{(int(rw[0])-1)}.0')
                            else:
                                self.listb.select_set(int(rw[0])-2)
                                self.listb.see(int(rw[0])-2)
                                self.text.see(f'{(int(rw[0])-2)}.0')
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
                            TreeViewGui.MODE = True
                            if ck[int(rw[0])+1][0] == 'space':
                                tvg.movetree(int(rw[0]), int(rw[0])+2)
                            else:
                                tvg.movetree(int(rw[0]), int(rw[0])+1)
                            self.spaces()
                            ck = tvg.insighttree()
                            if ck[int(rw[0])+1][0] != 'parent':
                                self.listb.select_set(int(rw[0])+1)
                                self.listb.see(int(rw[0])+1)
                                self.text.see(f'{(int(rw[0])+1)}.0')
                            else:
                                self.listb.select_set(int(rw[0])+2)
                                self.listb.see(int(rw[0])+2)
                                self.text.see(f'{(int(rw[0])+2)}.0')
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
                                self.text.see(f'{int(rw[0])}.0')
                                 
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
                self.listb.activate(int(rw[0]))
                self.listb.see(int(rw[0]))
                self.text.see(f'{int(rw[0])}.0')
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
        # Copy or move any rows to any point of a row within existing rows.
        # And copy parents and childs in hidden modes to another existing file or new file.
        
        askmove = messagebox.askyesno('TreeViewGui', 'Want to move to other file?') if self.info.get() == 'Hidden Mode' else None
        if askmove:
            def chosen(flname):
                TreeViewGui.FREEZE = False
                if flname == 'New':
                    askname = simpledialog.askstring('TreeViewGui', 'New file name:')
                    if askname:
                        if not os.path.isdir(os.path.join(os.getcwd().rpartition('\\')[0], f'{askname.title()}_tvg')):
                            tak = [f'{i}\n' for i in self.text.get('1.0', END)[:-1].split('\n') if i]
                            self.createf(askname)
                            tvg = tv(f'{self.filename}')
                            wtvg = tvg.insighthidden(tak)
                            tvg.fileread(wtvg)
                            self.spaces()
                            self.infobar()
                        else:
                            messagebox.showinfo('TreeViewGui', 'Cannot create new file because is already exist!!!')
                    else:
                        messagebox.showinfo('TreeViewGui', 'Copying is aborted!')
                else:
                    if f'{flname.rpartition("_")[0]}.txt' in os.listdir(os.path.join(os.getcwd().rpartition('\\')[0], flname)):
                        if f'{flname.rpartition("_")[0]}_hid.json' not in os.listdir(os.path.join(os.getcwd().rpartition('\\')[0], flname)):
                            self.filename = flname.rpartition("_")[0]
                            os.chdir(os.path.join(os.getcwd().rpartition('\\')[0], flname))
                            self.root.title(f'{os.getcwd()}\\{self.filename}.txt')
                            with open(f'{self.filename}.txt', 'a') as cp:
                                cp.write(self.text.get('1.0', END)[:-1])
                            self.spaces()
                            self.infobar()
                        else:
                            messagebox.showinfo('TreeViewGui', 'You cannot copied to hidden mode file!')
                    else:
                        self.filename = flname.rpartition("_")[0]
                        os.chdir(os.path.join(os.getcwd().rpartition('\\')[0], flname))
                        self.root.title(f'{os.getcwd()}\\{self.filename}.txt')                        
                        tak = [f'{i}\n' for i in self.text.get('1.0', END)[:-1].split('\n') if i]
                        tvg = tv(f'{self.filename}')
                        wtvg = tvg.insighthidden(tak)
                        tvg.fileread(wtvg)
                        self.spaces()
                        self.infobar()                        
                        
            TreeViewGui.FREEZE = True        
            self.lock = True
            files = [file for file in os.listdir(os.getcwd()[:os.getcwd().rfind('\\')]) if '_tvg' in file]
            files.insert(0, 'New')
            class MyDialog(simpledialog.Dialog):
            
                def body(self, master):
                    self.title('Choose File')
                    Label(master, text="File: ").grid(row=0, column = 0, sticky = E)
                    self.e1 = ttk.Combobox(master, state = 'readonly')
                    self.e1['values'] = files
                    self.e1.current(0)
                    self.e1.grid(row=0, column=1)
                    return self.e1
            
                def apply(self):
                    self.result = self.e1.get()
                                
            d = MyDialog(self.root)
            self.lock = False
            if d.result:
                chosen(d.result)
            else:
                TreeViewGui.FREEZE = False            
        else:
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
                                if ask is not None and ask < len(ins):
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
                                    self.text.see(f'{ask}.0')
                                    self.listb.see(ask)
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
                                    if ask:
                                        messagebox.showerror('TreeViewGui', f'row {ask} is exceed existing rows')
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
                        self.infobar()
                    
    def saveaspdf(self):
        # Show to browser and directly print as pdf or direct printing.
        
        try:
            if self.checkfile():
                if (a := self.text['font'].find('}')) != -1:
                    px = int(re.search(r'\d+', self.text['font'][a:]).group()) * 1.3333333
                else:
                    px = int(re.search(r'\d+', self.text['font']).group()) * 1.3333333
                ck = ['bold', 'italic']
                sty = ''
                for i in ck:
                    if i in self.text['font']:
                        sty += ''.join(f'{i} ')
                if sty:
                    add = f' {sty}{px:.3f}px '
                else:
                    add = f' {px:.3f}px '
                if '}' in self.text['font']:
                    fon = self.text['font'].partition('}')[0].replace('{','')
                    fon  = f'{add}{fon}'
                else:
                    fon = self.text['font'].partition(' ')[0]
                    fon  = f'{add}{fon}'                    
                ask = messagebox.askyesno('TreeViewGui', 'Add checkboxes?')
                if f'{self.filename}_hid.json' in os.listdir():
                    if ask:
                        convhtml(self.text.get('1.0', END)[:-1], f'{self.filename}', fon, ckb = True)
                    else:
                        convhtml(self.text.get('1.0', END)[:-1], f'{self.filename}', fon)
                else:
                    if ask:
                        convhtml(f'{self.filename}.txt', f'{self.filename}', fon, ckb = True)
                    else:
                        convhtml(f'{self.filename}.txt', f'{self.filename}', fon)
        except Exception as e:
            messagebox.showerror('TreeViewGui', f'{e}')
    
    def htmlview(self):
        # Can view html file that created from Printing from every TVG folders.
        
        self.hidcheck()
        if self.unlock:
            if self.checkfile():
                if self.lock is False:
                    path = os.getcwd().rpartition('\\')[0]
                    ltvg = [i for i in os.listdir(path) if '_tvg' in i]
                    ghtm = {}
                    for i in ltvg:
                        if f'{i.rpartition("_")[0]}.html' in os.listdir(os.path.join(path,i)):
                            ghtm[i] = f'{i.rpartition("_")[0]}.html'
                        
                    if ghtm:
                        self.lock = True
                        class MyDialog(simpledialog.Dialog):
                        
                            def body(self, master):
                                self.title('Choose HTML File')
                                Label(master, text="File: ").grid(row=0, column = 0, columnspan = 3, sticky = E)
                                self.e1 = ttk.Combobox(master, state = 'readonly')
                                self.e1['values'] = [f'{j}: {k}' for j, k in ghtm.items()]
                                self.e1.current(0)
                                self.e1.grid(row=0, column=1)
                                return self.e1
                        
                            def apply(self):
                                self.result = self.e1.get()
                                            
                        d = MyDialog(self.root)
                        self.lock = False
                        if d.result:
                            os.startfile(os.path.join(path, d.result.partition(':')[0], d.result.partition(':')[2][1:]))
                    else:
                        messagebox.showinfo('TreeViewGui', 'Nothing yet!')
                
    def spaces(self):
        # Mostly used by other functions to clear an obselete spaces.
        # To appropriate the display better.
        
        self.hidcheck()
        if self.unlock:
            if self.checkfile():
                if TreeViewGui.MARK and TreeViewGui.MODE is False:
                    TreeViewGui.MARK = False
                else:
                    TreeViewGui.MODE = False
                tvg = tv(self.filename)
                cks = tvg.insighttree()
                num2 = 1
                if cks:
                    while num2 !=  len(cks):
                        try:
                            if cks[num2][0] == 'parent' and num2 != 0:
                                if cks[num2 - 1][0] != 'space':
                                    tvg.insertspace(num2)
                                    cks = tvg.insighttree()
                                else:
                                    num2 += 1
                            elif cks[num2][0] == 'space':
                                if cks[num2 - 1][0] == 'space':
                                    tvg.delrow(num2)
                                    cks = tvg.insighttree()
                                else:
                                    num2 += 1
                            elif 'child' in cks[num2][0]:
                                if num2 == 0:
                                    tvg.insertrow('[Auto generate a parent]')
                                    cks = tvg.insighttree()
                                elif cks[num2 - 1][0] == 'space':
                                    tvg.delrow(num2-1)
                                    num2 -= 1
                                    cks = tvg.insighttree()
                                else:
                                    num2 += 1
                            else:
                                num2 += 1
                        except Exception as e:
                            messagebox.showerror('TreeViewGui', f'{e}')
                            break
                    if cks[0][0] == 'space':
                        tvg.delrow(0)
                        cks = tvg.insighttree()
                    if cks[len(cks)-1][0] == 'space':
                        tvg.delrow(len(cks)-1)
                    self.view()
                else:
                    self.view()
            else:
                if self.listb.get(0, END):
                    self.listb.delete(0, END)            
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
            g = re.compile(r'\s+')
            nf = str(self.text.cget('font'))
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
                try:
                    text_font = font.Font(self.root, font = nf, name = nf, exists=True)
                except:
                    text_font = font.Font(self.root, font = nf, name = nf, exists=False)
                em = text_font.measure(" ")
                for i in showt:
                    gr = g.match(i)
                    if gr and gr.span()[1] > 1:
                        if str(gr.span()[1]) not in self.text.tag_names():
                            bullet_width = text_font.measure(f'{gr.span()[1]*" "}-')
                            self.text.tag_configure(f"{gr.span()[1]}", lmargin1=em, lmargin2=em+bullet_width)
                        self.text.insert(END, i, f'{gr.span()[1]}')
                    else:
                        self.text.insert(END, i)
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
                try:
                    text_font = font.Font(self.root, font = nf, name = nf, exists=True)
                except:
                    text_font = font.Font(self.root, font = nf, name = nf, exists=False)
                em = text_font.measure(" ")
                for i in ih:
                    gr = g.match(i)
                    if gr and gr.span()[1] > 1:
                        if str(gr.span()[1]) not in self.text.tag_names():
                            bullet_width = text_font.measure(f'{gr.span()[1]*" "}-')
                            self.text.tag_configure(f"{gr.span()[1]}", lmargin1=em, lmargin2=em+bullet_width)
                        self.text.insert(END, i, f'{gr.span()[1]}')
                    else:
                        self.text.insert(END, i)
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
                
    def lookup(self, event = None):
        # To lookup word on row and also on editor mode.
        
        self.hidcheck()
        if self.unlock:
            if str(self.text.cget('state')) == 'normal' and str(self.bt['button24'].cget('state')) == 'normal':
                if self.text.get('1.0', END)[:-1]:
                    
                    def searchw(words: str):
                        self.text.tag_config('hw', underline = 1)
                        idx = self.text.search(words, '1.0', END, nocase=1)
                        ghw = None
                        while idx:
                            idx2 = f'{idx}+{len(words)}c'
                            ghw = self.text.get(idx, idx2)
                            self.text.delete(idx, idx2)
                            self.text.insert(idx, ghw, 'hw')
                            self.text.see(idx2)                            
                            c = messagebox.askyesno('TreeViewGui', 'Continue search?')
                            if c:
                                self.text.delete(idx, idx2)
                                self.text.insert(idx, ghw)
                                idx = self.text.search(words, idx2, END, nocase = 1)
                                self.text.mark_set('insert', idx2)
                                self.text.focus()                                
                                continue
                            else:
                                r = messagebox.askyesno('TreeViewGui', 'Replace word?')
                                if r:
                                    rpl = simpledialog.askstring('Replace', 'Type word:')
                                    if rpl:
                                        self.text.delete(idx, idx2)
                                        self.text.insert(idx, rpl)
                                        self.text.mark_set('insert', f"{idx}+{len(rpl)}c")
                                        self.text.focus()
                                    else:
                                        self.text.delete(idx, idx2)
                                        self.text.insert(idx, ghw)
                                        self.text.mark_set('insert', idx2)
                                        self.text.focus()
                                else:
                                    self.text.delete(idx, idx2)
                                    self.text.insert(idx, ghw)
                                    self.text.mark_set('insert', idx2)
                                    self.text.focus()
                                break
                        self.text.tag_delete(*['hw'])
                        del ghw
                        
                    if self.lock is False:
                        self.lock = True
                        self.root.update()
                        class MyDialog(simpledialog.Dialog):
                            
                            def body(self, master):
                                self.title('Search Words')
                                Label(master, text="Words: ").grid(row=0, column = 0, sticky = E)
                                self.e1 = ttk.Entry(master)
                                self.e1.grid(row=0, column=1)
                                return self.e1
                            
                            def apply(self):
                                self.result = self.e1.get()
                            
                        d = MyDialog(self.root)
                        self.lock = False
                        if d.result:
                            searchw(d.result)
            else:
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
                                self.text.see(f'{sw}.0')                            
                                self.listb.focus()
                                self.listb.selection_clear(0, END)
                                self.listb.activate(sw)
                                self.listb.selection_set(sw)
                        else:
                            while sn < num:
                                if sw in dat[sn][1]:
                                    self.text.see(f'{sn}.0')
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
    
    def dattim(self, event = None):
        # To insert date and time.
        
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
        elif str(self.text.cget('state')) == 'normal' and str(self.bt['button20'].cget('state')) == 'normal':
            dtt = f'[{dt.isoformat(dt.today().replace(microsecond = 0)).replace("T"," ")}]'
            self.text.insert(INSERT, f'{dtt} ')
            self.text.focus()
            
    def createf(self, name: str = None):
        # Creating new file not able to open existing one.
        
        if name:
            ask = name
        else:
            ask = messagebox.askyesno('TreeViewGui', 'Create new file?')
        if ask:
            if ask == name:
                fl = name
                del ask
            else:
                fl = simpledialog.askstring('TreeViewGui', 'What is the name?')
            if fl:
                mkd = f'{fl.title()}_tvg' 
                dr = os.getcwd().rpartition('\\')[0]
                files = [file for file in os.listdir(dr) if '_tvg' in file]
                if mkd not in files:
                    os.mkdir(os.path.join(dr, mkd))
                    os.chdir(os.path.join(dr, mkd))
                    self.filename = fl.title()
                    self.root.title(f'{os.getcwd()}\{self.filename}.txt')
                    self.text.config(state = NORMAL)
                    self.text.delete('1.0', END)
                    self.text.config(state = DISABLED)
                    self.entry.delete(0, END)
                    self.rb.set('')
                    self.entry.config(state = DISABLED)
                    self.listb.delete(0, END)
                else:
                    messagebox.showinfo('TreeViewGui', f'The file {mkd}/{fl.title()}.txt is already exist!')
            else:
                messagebox.showinfo('TreeViewGui', 'Nothing created yet!')
        else:
            messagebox.showinfo('TreeViewGui', 'Create new file is aborted!')
            
    def editex(self, event = None):
        # Edit existing file in the editor mode which can be very convinient and powerful.
        # However, before edit in editor mode, it is advice to make backup first!
        # Just in case you want to get back to previous file. 
        
        self.hidcheck()
        if self.unlock:
            if self.checkfile:
                ask = messagebox.askyesno('TreeViewGui', '"Yes" Edit whole file, or "No" Edit selected parent only?')
                if ask:
                    tvg = tv(self.filename)
                    edit = list(tvg.insighttree().values())
                    c = {f'child{i}': f'c{i}'  for i in range(1, 51)}
                    self.editor()
                    for ed in edit:
                        if ed[0] == 'parent':
                            self.text.insert(END, f'p:{ed[1][:-2]}\n')
                        elif ed[0] == 'space':
                            self.text.insert(END, f's:\n')
                        else:
                            self.text.insert(END, f'{c[ed[0]]}:{ed[1][1:]}')
                    self.text.see(self.text.index(INSERT))
                    os.remove(f'{self.filename}.txt')
                else:
                    if self.listb.curselection(): 
                        stor = int(self.listb.curselection()[0])
                        tvg = tv(self.filename)
                        ckp = tvg.insighttree()
                        if ckp[stor][0] == 'parent':
                            self.editor()
                            self.text.insert(END, f'p:{ckp[stor][1][:-2]}\n')
                            num = stor + 1
                            while num < len(ckp):
                                if 'child' in ckp[num][0]:
                                    chn = ckp[num][0].partition('d')[0][0] + ckp[num][0].partition('d')[2]
                                    self.text.insert(END, f'{chn}:{ckp[num][1][1:]}')
                                    num += 1
                                else:
                                    break
                            self.editorsel = (stor, num)
                    else:
                        messagebox.showinfo('TreeViewGui', 'Please select a parent row first!')
        self.text.focus()
    
    def temp(self, event = None):
        # This is to compliment the editor mode.
        # If you have to type several outline that has same format,
        # You can save them as template and re-use again in the editor mode.
        
        if str(self.text.cget('state')) == 'normal' and str(self.bt['button24'].cget('state')) == 'normal': 
            ori = os.getcwd()
            if 'Templates' not in os.listdir(ori.rpartition('\\')[0]):
                os.mkdir(os.path.join(ori.rpartition('\\')[0], 'Templates'))
            ask = messagebox.askyesno('TreeViewGui', 'Want to save template? ["No" to load template]')
            if ask:            
                if self.text.get('1.0', END)[:-1]:
                    fname = simpledialog.askstring('TreeViewGui', 'Name?')
                    if fname:
                        dest = os.path.join(ori.rpartition('\\')[0], 'Templates', f'{fname}.tvg')
                        with open(dest, 'w') as wt:
                            wt.write(str([i for i in self.text.get('1.0', END)[:-1].split('\n') if i]))
                        messagebox.showinfo('TreeViewGui', f'Template {fname}.tvg saved!')
                    else:
                        messagebox.showinfo('TreeViewGui', 'Save template is aborted!')
                else:
                    messagebox.showinfo('TreeViewGui', 'Nothing to be save!')
            else:
                if self.lock is False:        
                    self.lock = True
                    files = [i for i in os.listdir(os.path.join(ori.rpartition('\\')[0], 'Templates'))]
                    if files:
                        def tynam(event):
                            try:
                                if event.widget.get():
                                    idx = event.widget.index(INSERT)
                                    gt = event.widget.get()
                                    event.widget.delete(0, END)
                                    event.widget.insert(0, gt[:idx])
                                    if event.widget.get():
                                        r = 2
                                        while r:                                        
                                            for em in files:
                                                if event.widget.get().lower() in em.lower() and event.widget.get().lower() == em.lower()[:len(event.widget.get().lower())]:
                                                    event.widget.current(files.index(em))
                                            r -= 1
                                    event.widget.icursor(index = idx)
                            except Exception as e:
                                messagebox.showwarning('TeleTVG', f'{e}')
                                    
                        class MyDialog(simpledialog.Dialog):
                        
                            def body(self, master):
                                self.title('Choose Template')
                                Label(master, text="File: ").grid(row=0, column = 0, sticky = E)
                                self.e1 = ttk.Combobox(master)
                                self.e1['values'] = files
                                self.e1.bind('<KeyRelease>', tynam)
                                self.e1.grid(row=0, column=1)
                                return self.e1
                        
                            def apply(self):
                                self.result = self.e1.get()
                                            
                        d = MyDialog(self.root)
                        self.lock = False
                        if d.result:
                            path = os.path.join(ori.rpartition('\\')[0], 'Templates', d.result)
                            with open(path) as rdf:
                                gf = rdf.read()
                            if gf[0] == '[' and gf[-1] == ']':
                                gf = eval(gf)
                                if len(gf) == 1:
                                    self.text.insert(INSERT, gf[0])
                                else:
                                    tot = 0
                                    for pr in gf:
                                        if not tot:
                                            gw = self.text.get(INSERT, f'{INSERT} lineend')
                                        if gw == '':
                                            if int(self.text.index(INSERT).rpartition('.')[2]):
                                                self.text.insert(INSERT, f'\n{pr}')
                                            else:
                                                self.text.insert(INSERT, f'{pr}\n')
                                            tot += 1
                                        else:
                                            ind = float(self.text.index(INSERT))+float(tot)
                                            self.text.insert(f'{ind} lineend ', f'\n{pr}')
                                            tot += 1
                                del gf
                            else:
                                messagebox.showerror('TreeViewGui', 'Template has been corrupted!')
                        else:
                            messagebox.showinfo('TreeViewGui', 'Loading template aborted!')
                    else:
                        self.lock = False
                        messagebox.showinfo('TreeViewGui', 'No templates yet!')
        self.text.focus()
                        
    def editor(self):
        # This is direct editor on text window.
        # FORMAT:
        # "s:" for 'space'
        # "p:" for 'parent'
        # "c1:" - "c50:" for 'child1' to 'child50'
        
        self.hidcheck()
        if self.unlock:
            if str(self.text.cget('state')) == 'disabled':
                self.text.config(state = 'normal')
                self.text.delete('1.0', END)
                ckb = ['button24', 'button28', 'button20', 'button29', 'button19', 'text']
                for i in self.bt:
                    if 'label' not in i and 'scrollbar' not in i and i not in ckb:
                        self.bt[i].config(state='disable')
                TreeViewGui.FREEZE = True
                if self.store:
                    self.text.insert(END, self.store)
                    self.store = None
                self.text.edit_reset()
                self.text.focus()
            else:
                try:
                    if self.text.get('1.0', END)[:-1]:
                        ask = messagebox.askyesno('TreeViewGui', 'Do you want to convert[y] or Edit[n]?')
                        if ask:
                            self.converting()
                        else:                        
                            if self.checkfile():
                                if self.editorsel:
                                    stor = self.editorsel
                                    tvg = tv(self.filename)
                                    p1 = {j: k for j, k in tvg.insighttree().items() if j < stor[0]}
                                    ed = [i for i in self.text.get('1.0', END)[:-1].split('\n') if i]
                                    ckc = {f'c{i}': f'child{i}' for i in range(1, 51)}
                                    et = len(p1)-1
                                    p2 = {}
                                    for i in ed:
                                        et += 1
                                        if 's:' == i.lower()[:2]:
                                            p2[et] = ('space', '\n')
                                        elif 'p:' == i.lower()[:2]:
                                            if i.partition(':')[2].isspace() or not bool(i.partition(':')[2]):
                                                raise Exception('Parent cannot be empty!')
                                            else:
                                                p2[et] = ('parent', i[2:].removeprefix(' '))
                                        elif i.lower().partition(':')[0] in list(ckc):
                                            if i.partition(':')[2].isspace():
                                                p2[et] = (ckc[i.partition(':')[0]], i.partition(':')[2])
                                            elif bool(i.partition(':')[2]):
                                                p2[et] = (ckc[i.partition(':')[0]], i.partition(':')[2].removeprefix(' '))
                                    if len(ed) != len(p2):
                                        raise Exception('Not Editable!')
                                    combi = p1 | p2
                                    p3 = [k for j, k in tvg.insighttree().items() if j > stor[1]]
                                    if p3:
                                        p3 = {(len(combi)) + i: p3[i] for i in range(len(p3))}
                                        tvg.fileread(combi | p3)
                                    else:
                                        tvg.fileread(combi)
                                else:
                                    tvg = tv(self.filename)
                                    p1 = tvg.insighttree()
                                    et = len(p1)-1
                                    ed = [i for i in self.text.get('1.0', END)[:-1].split('\n') if i]
                                    ckc = {f'c{i}': f'child{i}' for i in range(1, 51)}
                                    p2 = {}
                                    for i in ed:
                                        et += 1
                                        if 's:' == i.lower()[:2]:
                                            p2[et] = ('space', '\n')
                                        elif 'p:' == i.lower()[:2]:
                                            if i.partition(':')[2].isspace() or not bool(i.partition(':')[2]):
                                                raise Exception('Parent cannot be empty!')
                                            else:
                                                p2[et] = ('parent', i[2:].removeprefix(' '))
                                        elif i.lower().partition(':')[0] in list(ckc):
                                            if i.partition(':')[2].isspace():
                                                p2[et] = (ckc[i.partition(':')[0]], i.partition(':')[2])
                                            elif bool(i.partition(':')[2]):
                                                p2[et] = (ckc[i.partition(':')[0]], i.partition(':')[2].removeprefix(' '))
                                    if len(ed) != len(p2):
                                        raise Exception('Not Editable!')
                                    tvg.fileread(p1 | p2)
                            else:
                                tvg = tv(self.filename)
                                ed = [i for i in self.text.get('1.0', END)[:-1].split('\n') if i]
                                et = -1
                                ckc = {f'c{i}': f'child{i}' for i in range(1, 51)}
                                p2 = {}
                                for i in ed:
                                    et += 1
                                    if 's:' == i.lower()[:2]:
                                        p2[et] = ('space', '\n')
                                    elif 'p:' == i.lower()[:2]:
                                        if i.partition(':')[2].isspace() or not bool(i.partition(':')[2]):
                                            raise Exception('Parent cannot be empty!')
                                        else:
                                            p2[et] = ('parent', i[2:].removeprefix(' '))
                                    elif i.lower().partition(':')[0] in list(ckc):
                                        if i.partition(':')[2].isspace():
                                            p2[et] = (ckc[i.partition(':')[0]], i.partition(':')[2])
                                        elif bool(i.partition(':')[2]):
                                            p2[et] = (ckc[i.partition(':')[0]], i.partition(':')[2].removeprefix(' '))
                                if len(ed) != len(p2):
                                    raise Exception('Not Editable!')
                                tvg.fileread(p2)
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
                            if self.editorsel:
                                self.text.see(f'{self.editorsel[0]}.0')
                                self.editorsel = None
                    else:
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
                        if self.editorsel:
                            self.editorsel = None
                except Exception as a:
                    messagebox.showerror('TreeViewGui', f'{a}')
            self.text.edit_reset()
            self.infobar()
                    
    def tvgexit(self, event = None):
        # Exit mode for TVG and setting everything back to default.
        
        if TreeViewGui.FREEZE is False:
            ori = os.getcwd().rpartition('\\')[0]
            if self.checkfile():
                with open(os.path.join(ori, 'lastopen.tvg'), 'wb') as lop:
                    lop.write(str({'lop': self.filename}).encode())
                if str(self.root.winfo_geometry()) == TreeViewGui.GEO:
                    with open(os.path.join(ori, 'geo.tvg'), 'wb') as geo:
                        geo.write(str({'geo': TreeViewGui.GEO}).encode())
                else:
                    ask = messagebox.askyesno('TreeViewGui', "Do you want to set your new window's position?")
                    if ask:
                        with open(os.path.join(ori, 'geo.tvg'), 'wb') as geo:
                            geo.write(str({'geo': str(self.root.winfo_geometry())}).encode())
                    else:
                        with open(os.path.join(ori, 'geo.tvg'), 'wb') as geo:
                            geo.write(str({'geo': TreeViewGui.GEO}).encode())
            self.root.destroy()
        else:
            messagebox.showerror('TreeViewGui', 'Do not exit before a function end!!!')
    
    def txtcol(self, event = None, path = None, wr = True):
        # Setting colors for text and listbox.
        
        color = None
        if path:
            with open(path) as rd:
                color = rd.read()
        else:
            color = colorchooser.askcolor()[1]
        if color:
            rgb = [int(f'{i}{j}', 16)/255 for i, j in list(zip(color[1:][0::2], color[1:][1::2]))]
            rgb = True if round(((1/2) * (max(rgb) + min(rgb))) * 100) < 47 else False
            if  rgb:
                self.text.config(foreground = 'white')
                self.text.config(insertbackground = 'white')
                self.listb.config(foreground = 'white')
            else:
                self.text.config(foreground = 'black')
                self.text.config(insertbackground = 'black')
                self.listb.config(foreground = 'black')
            self.text.config(bg = color)
            self.listb.config(bg = color)
            del rgb
            if wr:
                with open(os.path.join(os.getcwd().rpartition('\\')[0], 'theme.tvg'), 'w') as thm:
                    thm.write(color)
                    
    def clb(self, event, wr = True):
        # Setting font for text and listbox.
        
        ckf = [str(i) for i in range(41) if i >= 10]
        if '}' in event:
            n = len(event[:event.find('}')])
            f = re.search(r'\d+', event[event.find('}'):])
            fl = event[:(n + f.span()[0])] + '11' + event[(n+f.span()[1]):]
            if f.group() in ckf:
                f = event
            else:
                if int(f.group()) < 10:
                    f = event[:(n + f.span()[0])] + '10' + event[(n + f.span()[1]):]
                else:
                    f = event[:(n + f.span()[0])] + '40' + event[(n + f.span()[1]):]
        else:
            f = re.search(r'\d+', event)
            fl = event[:f.span()[0]] + '11' + event[f.span()[1]:]
            if f.group() in ckf:
                f = event
            else:
                if int(f.group()) < 10:
                    f = event[:(f.span()[0])] + '10' + event[(f.span()[1]):]
                else:
                    f = event[:(f.span()[0])] + '40' + event[(f.span()[1]):]
                    
        for i in self.text.tag_names():
            self.text.tag_remove(i, '1.0', END)
        self.text.tag_delete(*self.text.tag_names())
        self.text['font'] = f
        if wr:
            if fl != self.listb['font']:
                self.reblist(fl)
            with open(os.path.join(os.getcwd().rpartition('\\')[0], 'ft.tvg'), 'w') as ftvg:
                ftvg.write(event)
        else:
            self.listb['font'] = fl
        if f'{self.filename}_hid.json' not in os.listdir():
            self.spaces()
        else:
            self.hidform()
                
    def reblist(self, fon: str):
        # Destroy Listbox and rebuild it again,
        # for font in listbox to be appear correctly.
        
        self.listb.destroy()
        self.listb = Listbox(self.tlframe, background = self.text['background'],
                             foreground = self.text['foreground'], font = fon)
        self.listb.pack(side = LEFT, fill = 'both', expand = 1)
        self.listb.pack_propagate(0)
        self.bt['listb'] = self.listb
        self.listb.config(yscrollcommand = self.scrollbar2.set)
        self.scrollbar2.config(command = self.listb.yview)
        self.listb.bind('<<ListboxSelect>>', self.infobar)
        self.listb.bind('<MouseWheel>', self.mscrl)
        self.listb.bind('<Up>', self.mscrl)
        self.listb.bind('<Down>', self.mscrl)
        self.listb.bind('<FocusIn>', self.flb)
        
        
    def ft(self, event = None, path = None):
        # Initial starting fonts chooser.
        
        if path:
            with open(path) as rd:
                self.clb(rd.read(), wr = False)
        else:
            self.root.tk.call('tk', 'fontchooser', 'configure', 
                              '-font', self.text['font'], '-command', 
                              self.root.register(self.clb))
            self.root.tk.call('tk', 'fontchooser', 'show')
            
    def oriset(self, event = None):
        # Set back to original setting of theme and font.
        
        pth = os.getcwd().rpartition('\\')[0]
        lf = [i for i in os.listdir(pth) if i == 'ft.tvg' or i == 'theme.tvg']
        if lf:
            ask = messagebox.askyesno('TreeViewGui', 'Set back to original?')
            if ask:
                for i in lf:
                    os.remove(os.path.join(pth, i))
                messagebox.showinfo('TreeViewGui', 'All set back to original setting!')
            else:
                messagebox.showinfo('TreeViewGui', 'None change yet!')
            
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
        frm = Frame(a, borderwidth = 7, bg = 'grey30', width = 250, height = 250)
        frm.pack(fill = 'both', expand = 1)
        tx = m
        lab = Label(frm, text = tx, justify = 'center', anchor = 'center', font = 'verdana 15 bold', width = 250, height = 250, bg = 'gray30', fg = 'grey97')
        lab.pack(fill = 'both', expand = 1)    
        
def askfile(root):
    # Asking file for creating or opening initial app start.
    
    files = [file.rpartition('_')[0] for file in os.listdir(os.getcwd()) if '_tvg' in file]
    class MyDialog(simpledialog.Dialog):
        
        def body(self, master):
            self.title("Choose File")
            self.geometry('230x70')
            Label(master, text="File: ").grid(row=0, column = 0, sticky = E)
            self.e1 = ttk.Combobox(master)
            self.e1['values'] = files
            self.e1.grid(row=0, column=1)
            return self.e1
    
        def apply(self):
            self.result = self.e1.get()
                        
    d = MyDialog(root)
    if d.result:
        return d.result
    else:
        return None
        
def main():
    # Starting point of running TVG and making directory for non-existing file.
    
    #if os.path.isdir('TVGPro') is False:
        #os.mkdir('TVGPro')
    root = Tk()
    root.withdraw()
    if 'lastopen.tvg' in os.listdir():
        root.update()
        ask = messagebox.askyesno('TreeViewGui', 'Want to open previous file?')
        if ask:
            with open('lastopen.tvg', 'rb') as lop:
                rd = eval(lop.read().decode('utf-8'))
            filename = rd['lop']
        else:
            os.remove('lastopen.tvg')
            filename = askfile(root)
    else:
        filename = askfile(root)    
    if filename:
        filename = filename.title()
        if f'{filename}_tvg' not in os.listdir():
            try:
                os.mkdir(f'{filename}_tvg')
                os.chdir(f'{filename}_tvg')
            except:
                os.chdir(f'{filename}_tvg')
        else:
            os.chdir(f'{filename}_tvg')
        begin = TreeViewGui(root = root, filename = filename)
        begin.root.deiconify()
        if f'{filename}_hid.json' in os.listdir():
            begin.hidform()
            begin.infobar()
        else:
            begin.view()
        begin.text.edit_reset()            
        begin.root.mainloop()
    else:
        messagebox.showwarning('File', 'No File Name!')
        root.destroy()