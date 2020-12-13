#Copyright (c) 2020, KarjaKAK
#All rights reserved.

from tkinter import *
from tkinter import messagebox, simpledialog, ttk
import os
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
        self.sel = []
        self.upt = tuple()
        self.lbe = Listbox(self.root, font = '-*-Segoe-UI-Emoji-*--*-300-*', 
                           width = 5, height = 10 , 
                           justify ='center', bg = 'light gray', 
                           exportselection = False, selectmode = 'multiple')
        self.lbe.pack()
        with open('emoj.txt') as emr:
            a  = [chr(i) for i in eval(emr.read())]
        for i in a:
            self.lbe.insert(END,i)
        self.lbe.bind('<ButtonRelease>', self.updatesel)
        self.btc = Button(self.root, text = 'C O P Y', font = 'consolas 10 bold', relief = GROOVE, command = self.copem)
        self.btc.pack(fill = 'x', expand = 1)
        self.btm = Button(self.root, text = 'M A R K', font = 'consolas 10 bold', relief = GROOVE, command = self.mark)
        self.btm.pack(fill = 'x', expand = 1)        
        self.btm = Button(self.root, text = 'L O A D', font = 'consolas 10 bold', relief = GROOVE, command = self.choind)
        self.btm.pack(fill = 'x', expand = 1)        
        
    def updatesel(self, event = None):
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
            messagebox.showinfo('Emo', 'Nothing selected yet!')
    
    def mark(self):
        # Saving emoji indexes using json database.
        
        if self.sel:
            nm = simpledialog.askstring('Emo', 'Name your marking: [if name is exist, will overwrite!]')
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
                messagebox.showinfo('Emo', 'Adding mark is aborted!')
        else:
            messagebox.showinfo('Emo', 'Nothing selected yet!')
                
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
                messagebox.showinfo('Emo', 'Copied!')
        else:
            messagebox.showinfo('Emo', 'No database, please save some first!')
            
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