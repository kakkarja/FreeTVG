#Copyright (c) 2020, KarjaKAK
#All rights reserved.

from tkinter import *
from tkinter import messagebox
import os

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
        self.lbe = Listbox(self.root, font = '-*-Segoe-UI-Emoji-*--*-300-*', 
                           width = 5, height = 10 , 
                           justify ='center', bg = 'light gray', 
                           exportselection = False, selectmode = 'multiple')
        self.lbe.pack()
        with open('emoj.txt') as emr:
            a  = [chr(i) for i in eval(emr.read())]
        for i in a:
            self.lbe.insert(END,i)
        self.btc = Button(self.root, text = 'C O P Y', font = 'consolas 10 bold', relief = GROOVE, command = self.copem)
        self.btc.pack(fill = 'x', expand = 1)
        self.btm = Button(self.root, text = 'M A R K', font = 'consolas 10 bold', relief = GROOVE, command = self.mark)
        self.btm.pack(fill = 'x', expand = 1)        
    
    def copem(self):
        # Copy all selected emojis.
        
        lj = ''
        if self.lbe.curselection():
            gc = self.lbe.curselection()
            for i in gc:
                lj += ''.join(self.lbe.get(i))
            self.root.clipboard_clear()
            self.root.clipboard_append(lj)
            self.lbe.selection_clear(0, END)
    
    def mark(self):
        if self.lbe.curselection():
            if 'marking' in os.listdir() and os.path.isfile('marking'):
                ask = messagebox.askyesno('Emojies', 'Do you want to change marking?')
                if ask:
                    m = {'Index': self.lbe.curselection()}
                    with open('marking', 'wb') as mw:
                        mw.write(str(m).encode())
                else:
                    with open('marking', 'rb') as rm:
                        m = eval(rm.read().decode('utf-8'))
                    self.lbe.selection_clear(0, END)
                    for i in m['Index']:
                        self.lbe.selection_set(i)
                    self.lbe.see(m['Index'][-1])
            else:
                m = {'Index': self.lbe.curselection()}
                with open('marking', 'wb') as mw:
                    mw.write(str(m).encode())
        else:
            if 'marking' in os.listdir() and os.path.isfile('marking'):
                with open('marking', 'rb') as rm:
                    m = eval(rm.read().decode('utf-8'))            
                for i in m['Index']:
                    self.lbe.selection_set(i)
                self.lbe.see(m['Index'][-1])
    
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