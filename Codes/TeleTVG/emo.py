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
        self.fr = ttk.Frame(self.root)
        self.fr.pack(fill = 'both')
        self.lbe = Listbox(self.fr, font = '-*-Segoe-UI-Emoji-*--*-300-*', 
                           width = 5, height = 10 , 
                           justify ='center', bg = 'khaki', 
                           selectbackground = 'teal', selectforeground = 'gold',
                           exportselection = False, selectmode = 'multiple')
        self.lbe.pack(fill = 'x', expand = 1, padx = 3, pady = (2, 0))
        with open(filen('emoj.txt')) as emr:
            a  = [chr(i) for i in eval(emr.read())]
        for i in a:
            self.lbe.insert(END,i)
        self.lbe.bind('<ButtonRelease>', self.updatesel)
        self.sp =  IntVar(self.root)
        self.scl = ttk.Scale(self.fr, from_ = 0, to = len(a)-1, variable = self.sp, command = self.sclupt)
        self.scl.pack()
        self.setscl = (0, len(a)-1)
        self.btc = Button(self.root, text = 'C O P Y', font = 'consolas 10 bold', relief = GROOVE, command = self.copem)
        self.btc.pack(fill = 'x', expand = 1)
        self.btm = Button(self.root, text = 'M A R K', font = 'consolas 10 bold', relief = GROOVE, command = self.mark)
        self.btm.pack(fill = 'x', expand = 1)        
        self.btm = Button(self.root, text = 'L O A D', font = 'consolas 10 bold', relief = GROOVE, command = self.choind)
        self.btm.pack(fill = 'x', expand = 1)
        
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
                if 'marking.json' in os.listdir():
                    mrk = db('marking')
                    m = {f'{nm}': self.sel}
                    mrk.indata(m)
                    self.lbe.selection_clear(0, END)
                    self.sel = []
                    self.upt = tuple()
                else:
                    mrk = db('marking')
                    m = {f'{nm}': self.sel}
                    mrk.createdb(m)
                    self.lbe.selection_clear(0, END)
                    self.sel = []
                    self.upt = tuple()
            else:
                messagebox.showinfo('Emo', 'Adding mark is aborted!', parent = self.root)
        else:
            messagebox.showinfo('Emo', 'Nothing selected yet!', parent = self.root)
                
    def choind(self):
        # Choose saved marking and directly copied.
        
        if 'marking.json' in os.listdir():
            mrk = db('marking')
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
            if d.result:
                cope = ''
                for i in d.result:
                    cope += ''.join(self.lbe.get(i))
                self.root.clipboard_clear()
                self.root.clipboard_append(cope)
                del cope
                del d.result
                messagebox.showinfo('Emo', 'Copied!', parent = self.root)
        else:
            messagebox.showinfo('Emo', 'No database, please save some first!', parent = self.root)
            
    def delwin(self, event = None):
        # Exit emoji window.

        Emo.status = True
        Emo.mainon = None
        self.root.destroy()
           
def main():
    # Create Emoji window for one time until it close.
    
    if Emo.status:
        root = Tk()
        Emo.status = False
        Emo(root)
        Emo.mainon = root
        Emo.mainon.mainloop()

if __name__ == '__main__':
    main()