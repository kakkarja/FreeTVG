#Copyright (c) 2020, KarjaKAK
#All rights reserved.

from tkinter import *
from tkinter import messagebox, simpledialog, ttk
import os
from FileFind import filen
from DataB import Datab as db

class Emo:
    status = True
    mainon = None
    paste = None
    pathn = None
    def __init__(self, root):
        """
        Creating Emoji for ReminderTel.
        """
        self.root = root
        self.root.title('Emojies')
        self.root.protocol('WM_DELETE_WINDOW', self.delwin)
        self.root.attributes('-toolwindow', 1)
        self.root.attributes('-topmost', 1)
        self.root.resizable(False, False)
        self.root.bind('<Up>', self.scrud)
        self.root.bind('<Down>', self.scrud)
        self.root.bind('<Control-Up>', self.jumpsc)
        self.root.bind('<Control-Down>', self.jumpsc)
        self.root.bind('<Control-s>', self.slec)
        self.root.bind('<Control-c>', self.slec)
        self.root.bind('<Control-m>', self.slec)
        self.root.bind('<Control-l>', self.slec)
        self.sel = []
        self.upt = tuple()
        self.lock = False
        self.lib = None
        self.fr = ttk.Frame(self.root)
        self.fr.pack(fill = 'both')
        self.lbe = Listbox(self.fr, font = '-*-Segoe-UI-Emoji-*--*-300-*', 
                           width = 5, height = 10 , 
                           justify ='center', bg = 'khaki', 
                           selectbackground = 'teal', selectforeground = 'gold',
                           exportselection = False, selectmode = 'multiple')
        self.lbe.pack(fill = 'x', expand = 1, padx = 3, pady = (2, 0))
        try:
            with open(filen('emoj.txt')) as emr:
                a = emr.read()
                if '{' == a[0] and a[-1] == '}':
                    self.lib = {e: chr(j) for e, j in eval(a).items()}
                else:
                    raise Exception('File corrupted!!!')
        except Exception as e:
            messagebox.showerror('Emo', f'{e}')
            self.root.destroy()
        else:
            for i in list(self.lib.values()):
                self.lbe.insert(END,i)
            self.lbe.bind('<ButtonRelease>', self.updatesel)
            self.combo = ttk.Combobox(self.root)
            self.combo.pack(pady = 2, padx = 2, fill = 'both', expand = 1)
            self.combo['values'] = sorted(list(self.lib.keys()))
            self.combo.bind('<<ComboboxSelected>>',self.selectcom)
            self.combo.bind('<KeyRelease>',self.tynam)
            self.sp =  IntVar(self.root)
            self.scl = ttk.Scale(self.fr, from_ = 0, to = len(list(self.lib.values()))-1, variable = self.sp, command = self.sclupt)
            self.scl.pack(fill = 'x', expand = 1)
            self.setscl = (0, len(a)-1)
            self.btc = Button(self.root, text = 'C O P Y', font = 'consolas 10 bold', relief = GROOVE, command = self.copem)
            self.btc.pack(fill = 'x', expand = 1)
            self.btm = Button(self.root, text = 'M A R K', font = 'consolas 10 bold', relief = GROOVE, command = self.mark)
            self.btm.pack(fill = 'x', expand = 1)        
            self.btm = Button(self.root, text = 'L O A D', font = 'consolas 10 bold', relief = GROOVE, command = self.choind)
            self.btm.pack(fill = 'x', expand = 1)
        
    def tynam(self, event = None):
        # To predict the key-in typing in combobox.
        
        import string
        
        try:
            if event.char.upper() in string.ascii_uppercase:
                #if self.combo.get():
                    idx = self.combo.index(INSERT)
                    gt = self.combo.get()
                    self.combo.delete(0, END)
                    self.combo.insert(0, gt[:idx])
                    if self.combo.get():
                        for em in self.lib:
                            if self.combo.get().upper() in em and self.combo.get().upper() == em[:len(self.combo.get())]:
                                self.combo.current(sorted(list(self.lib)).index(em))
                                idm = list(self.lib.values()).index(self.lib[em])
                                self.sp.set(idm)
                                self.lbe.see(idm)
                    self.combo.icursor(index = idx)
        except Exception as e:
            messagebox.showwarning('TeleTVG', f'{e}', parent = self.root)
    
    def selectcom(self, event):
        # Combobox selection will result emoji ready to be selected.
        
        self.lbe.focus()
        idx = list(self.lib.values()).index(self.lib[self.combo.get()])
        self.sp.set(idx)
        self.lbe.activate(idx)
        self.lbe.see(idx)
        
    def slec(self, event = None):
        # Short-cut to keyboard.
        
        if event.keysym == 's':
            self.lbe.selection_set(ACTIVE)
            self.updatesel()
        elif event.keysym == 'c':
            self.copem()
        elif event.keysym == 'm':
            self.mark()
        elif event.keysym == 'l':
            self.choind()
    
    def jumpsc(self, event = None):
        # Scroll up and down jump by 10.
        
        if event.keysym == 'Up':
            if self.sp.get() > self.setscl[0]:
                self.sp.set(self.sp.get()-10)
                self.sclupt()
            else:
                self.sp.set(self.setscl[0])
                self.sclupt()
        elif event.keysym == 'Down':
            if self.sp.get() < self.setscl[1]:
                self.sp.set(self.sp.get()+10)        
                self.sclupt()
            else:
                self.sp.set(self.setscl[1])
                self.sclupt()            
    
    def sclupt(self, event = None):
        # Using scale to scroll the listbox of emojies.
        
        self.combo.current(self.sp.get())
        fc = str(self.root.focus_get())
        if 'listbox' not in fc:
            self.lbe.focus()
        self.lbe.activate(self.sp.get())
        self.lbe.see(self.sp.get())
            
    def scrud(self, event = None):
        # Using Up and Down button to scroll emojies.
        
        if event.keysym == 'Up':
            if self.sp.get() > self.setscl[0]:
                self.sp.set(self.sp.get()-1)
                self.sclupt()
        elif event.keysym == 'Down':
            if self.sp.get() < self.setscl[1]:
                self.sp.set(self.sp.get()+1)        
                self.sclupt()
            
    def updatesel(self, event = None):
        # Precedent selection.
        
        if self.upt:
            if set(self.lbe.curselection()) - set(self.upt):
                x = list(set(self.lbe.curselection()) - set(self.upt)).pop()
                self.sel.append(x)
                self.upt = self.lbe.curselection()
            elif set(self.upt) - set(self.lbe.curselection()):
                x = list(set(self.upt)-set(self.lbe.curselection())).pop()
                del self.sel[self.sel.index(x)]
                self.upt = self.lbe.curselection()
        else:
            self.upt = self.lbe.curselection()
            self.sel.append(self.upt[0])        
        
        
    def copem(self):
        # Copy all selected emojies.

        lj = ''
        if self.sel:
            gc = self.sel
            for i in gc:
                lj += ''.join(self.lbe.get(i))
            if Emo.paste:
                Emo.paste.text.insert(INSERT, lj)
                Emo.paste.text.see(INSERT)
                Emo.paste.text.focus()
            else:
                self.root.clipboard_clear()
                self.root.clipboard_append(lj)
            self.lbe.selection_clear(0, END)
            self.sel = []
            self.upt = tuple()
            del lj
            del gc
        else:
            messagebox.showinfo('Emo', 'Nothing selected yet!', parent = self.root)
    
    def mark(self):
        # Saving emoji indexes using json database.
        
        if self.sel:
            nm = simpledialog.askstring('Emo', 'Name your marking: [if name is exist, will overwrite!]', parent = self.root)
            if nm:            
                if 'marking.json' in os.listdir(Emo.pathn):
                    mrk = db(os.path.join(Emo.pathn,'marking'))
                    m = {f'{nm}': self.sel}
                    mrk.indata(m)
                    self.lbe.selection_clear(0, END)
                    self.sel = []
                    self.upt = tuple()
                else:
                    mrk = db(os.path.join(Emo.pathn,'marking'))
                    m = {f'{nm}': self.sel}
                    mrk.createdb(m)
                    self.lbe.selection_clear(0, END)
                    self.sel = []
                    self.upt = tuple()
            else:
                messagebox.showinfo('Emo', 'Saving Mark aborted!', parent = self.root)
        else:
            messagebox.showinfo('Emo', 'Nothing selected yet!', parent = self.root)
                
    def choind(self):
        # Choose saved marking and directly copied.
        
        if self.lock is False:
            if 'marking.json' in os.listdir(Emo.pathn):
                mrk = db(os.path.join(Emo.pathn,'marking'))
                if mrk.totalrecs():
                    self.lock = True
                    class MyDialog(simpledialog.Dialog):
                    
                        def body(self, master):
                            self.title('Choose Mark')
                            Label(master, text="Marking: ").pack(side = LEFT)
                            self.e1 = ttk.Combobox(master, state = 'readonly')
                            self.e1.pack(side = LEFT)
                            self.e1['values'] = list(mrk.loadkeys())
                            self.e1.current(0)
                            return self.e1
                    
                        def apply(self):
                            self.result = mrk.takedat(self.e1.get())
                    
                    d = MyDialog(self.root)
                    self.lock = False
                    if d.result:
                        cope = ''
                        for i in d.result:
                            cope += ''.join(self.lbe.get(i))
                        if Emo.paste:
                            Emo.paste.text.insert(INSERT, cope)
                            Emo.paste.text.see(INSERT)
                            Emo.paste.text.focus()
                        else:
                            self.root.clipboard_clear()
                            self.root.clipboard_append(cope)
                            messagebox.showinfo('Emo', 'Copied!', parent = self.root)
                        del cope
                        del d.result
                    else:
                        ask = messagebox.askyesno('Emo', 'Do you want delete Mark?', parent = self.root)
                        if ask:
                            if self.lock is False:
                                if 'marking.json' in os.listdir(Emo.pathn):
                                    mrk = db(os.path.join(Emo.pathn,'marking'))
                                    self.lock = True
                                    class MyMarks(simpledialog.Dialog):
                                    
                                        def body(self, master):
                                            self.title('Choose Mark')
                                            Label(master, text="Marking: ").pack(side = LEFT)
                                            self.e1 = ttk.Combobox(master, state = 'readonly')
                                            self.e1.pack(side = LEFT)
                                            self.e1['values'] = list(mrk.loadkeys())
                                            self.e1.current(0)
                                            return self.e1
                                    
                                        def apply(self):
                                            self.result = self.e1.get()
                                    
                                    d = MyMarks(self.root)
                                    self.lock = False
                                    if d.result:
                                        mrk.deldata(d.result)
                                else:
                                    messagebox.showinfo('Emo', 'No database, please save some first!', parent = self.root)
                else:
                    messagebox.showinfo('Emo', 'Database is empty, please save some first!', parent = self.root)
            else:
                messagebox.showinfo('Emo', 'No database, please save some first!', parent = self.root)
                
    def delwin(self, event = None):
        # Exit emoji window.

        Emo.status = True
        Emo.mainon = None
        Emo.paste = None
        self.root.destroy()
           
def main(paste = None):
    # Create Emoji window for one time until it close.

    path = os.getcwd().rpartition('\\')[0]
    if 'emodb' not in os.listdir(path):
        os.mkdir(os.path.join(path, 'emodb'))
    if Emo.status:
        Emo.pathn = os.path.join(path, 'emodb')
        Emo.status = False
        if paste:
            Emo.paste = paste
        root = Tk()
        try:
            Emo(root)
            Emo.mainon = root
            Emo.mainon.focus_force()
            Emo.mainon.mainloop()
        except:
            root = Tk()
            root.withdraw()
            messagebox.showerror('Emo', 'Emoji data has been corrupted!')
            root.destroy()

if __name__ == '__main__':
    main()