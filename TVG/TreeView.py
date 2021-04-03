# -*- coding: utf-8 -*-
# Copyright © kakkarja (K A K)

import re
import datetime
import os
from .DataB import Datab as db

class TreeView:
    """
    This is a class of writing in txt file in treeview/outline mode.
    The beginning of creating TreeView text file, you need to start with-
    TreeView.writetree() to create parent at the beginning.
    The rest you must use other functions, to edit, add child and parent.
    WARNING: Do not use anymore writetree function, after the initial start-
    of making TreeView text file. Because it will erase everything in the text file.
    """
    def __init__(self, filename):
        """
        The child position can be adjusted.
        The default is 4 spaces
        The number of childs also can be adjusted.
        The default is 50 childs
        """
        self.filename = filename
        self.parent = {'parent':0}
        self.childs = {f'child{c//4}': c for c in range(201) if c % 4 == 0 and c != 0}
        
    def writetree(self, words):
        """
        This is initial start for creating Treeview with a parent.
        WARNING: After the initial, do not use this function anymore,
        otherwise, it can override the whole txt file like it is new. 
        """
        with open(f'{self.filename}.txt', 'w') as file:
            if isinstance(words, str):
                file.write(f'{words}:\n')
            else:
                print('Need to be string!!!')
                
    def insighttree(self):
        """
        This is very useful for looking at your TreeView data,
        with understanding your structure. Looking at rows, child and written words. 
        """
        try:
            childs = {b:a for a, b in list(self.childs.items())}
            with open(f'{self.filename}.txt') as file:
                reads = (file.readlines())
            di = {}
            for d in range(len(reads)):
                if reads[d] == '\n':
                    di[d] = ('space', reads[d])
                elif re.match(r'\s+', reads[d]) == None:
                    di[d] = (list(self.parent.items())[0][0], reads[d])
                else:
                    di[d] = (childs[re.match(r'\s+', reads[d]).span()[1]], 
                             reads[d][re.match(r'\s+', reads[d]).span()[1]:])
            return di
        except Exception as e:
            raise e
            
    def insighthidden(self, data):
        """
        This is very useful for looking at your TreeView data,
        with understanding your structure. Looking at rows, child and written words. 
        """
        try:
            childs = {b:a for a, b in list(self.childs.items())}
            if isinstance(data, list):
                di = {}
                for d in range(len(data)):
                    if data[d] == '\n':
                        di[d] = ('space', data[d])
                    elif re.match(r'\s+', data[d]) == None:
                        di[d] = (list(self.parent.items())[0][0], data[d])
                    else:
                        di[d] = (childs[re.match(r'\s+', data[d]).span()[1]], 
                                 data[d][re.match(r'\s+', data[d]).span()[1]:])
                return di
        except Exception as e:
            raise e
            
    def quickchild(self, words, child ):
        """
        You must define the variable child e.g: 'child1'. 
        """
        if child in self.childs:
            if isinstance(words, str):
                with open(f'{self.filename}.txt', 'a') as file:
                    file.write(f'{" " * self.childs[child]}-{words}\n')  
            else:
                print('Need to be string!!!')
                
    def edittree(self, words, row = 0, child = None):
        """
        You can edit the structure of your tree from row and child.
        Using the insighttree() will help you identifies which row and child to change. 
        """
        try:
            if isinstance(words, str):
                d = self.insighttree()
                if child:
                    if child in self.childs:
                        if isinstance(row, int) and len(d)-1 >= row > 0 :
                            d[row] = (child, f'-{words}\n')
                            with open(f'{self.filename}.txt', 'r') as file:
                                read = file.readlines()
                            read[row] = f'{" " * self.childs[d[row][0]]}{d[row][1]}'
                            with open(f'{self.filename}.txt', 'w') as file:
                                file.writelines(read)
                        else:
                            print(f'"row" must be int number and less or equal to {len(d)-1}!')
                    else:
                        print('Please identify child accordingly, e.g. "child1"')
                else:
                    if isinstance(row, int) and len(d)-1 >= row:
                        d[row] = (list(self.parent.items())[0][0], f'{words}:\n')
                        with open(f'{self.filename}.txt', 'r') as file:
                            read = file.readlines()
                        read[row] = f'{" " * self.parent[d[row][0]]}{d[row][1]}'
                        with open(f'{self.filename}.txt', 'w') as file:
                            file.writelines(read)
                    else:
                        print(f'"row" must be int number and less or equal to {len(d)-1}!')                    
            else:
                print('Need to be string!!!')                                
        except Exception as e:
            raise e
            
    def addparent(self, words):
        """
        Use this if you want to add new parent. Do not use the writetree() anymore.
        """
        if isinstance(words, str):
            with open(f'{self.filename}.txt', 'r') as file:
                read = file.readlines()
            read.append('\n')    
            read.append(f'{words}:\n')
            with open(f'{self.filename}.txt', 'w') as file:
                file.writelines(read)
        else:
            print('Need to be string!!!')
            
    def delrow(self, row):
        """
        This function is to delete a row in a TreeView text file.
        """
        if isinstance(row, int):
            with open(f'{self.filename}.txt') as file:
                read = file.readlines()
            if row <= len(read)-1:
                del read[row]
                with open(f'{self.filename}.txt', 'w') as file:
                    file.writelines(read)
            else:
                print('The row is not exist!')
        else:
            print('Need to be integer!')
            
    def insertrow(self, words, row = 0, child = None):
        """
        This function is to insert words into a decided row within the TreeView structure. 
        """
        if isinstance(words,str):
            if child:
                words = f'{" " * self.childs[child]}-{words}\n'
            else:
                words = f'{words}:\n'
            with open(f'{self.filename}.txt') as file:
                read = file.readlines()
            if row <= len(read)-1:
                read.insert(row, words)
                with open(f'{self.filename}.txt', 'w') as file:
                    file.writelines(read)
            else:
                print('"row" need to be less or equal to {len(read)-1}')
        else:
            print('Need to be string!!!')
            
    def movetree(self, row, to):
        """
        Moving one row to another. From row to another row. Suggested to use insighttree(),
        for knowing where to move.
        """
        if isinstance(row, int) and isinstance(to, int):
            moving = []
            with open(f'{self.filename}.txt') as file:
                read = file.readlines()
                if read[row] != '\n':
                    moving.append(read[row])
                    del read[row]
                    if to >= len(read):
                        read.append(moving[0])
                    else:
                        read.insert(to, moving[0])
            with open(f'{self.filename}.txt', 'w') as file:
                file.writelines(read)
    
    def movechild(self, row, child):
        """
        Moving row to left or right side using child. Suggested to use insighttree(),
        for knowing where to move.
        """
        if row and child:
            if child in self.childs:
                with open(f'{self.filename}.txt') as file:
                    read = file.readlines()
                if read[row] != '\n' and row <= len(read)-1:
                    bond = read[row][re.match(r"\s+", read[row]).span()[1]:]
                    read[row] = f'{" " * self.childs[child]}{bond}' 
                    with open(f'{self.filename}.txt', 'w') as file:
                        file.writelines(read)
                            
    def readtree(self):
        """
        Print out your TreeView in console.
        """
        if self.filename:
            with open(f'{self.filename}.txt') as file:
                read = file.readlines()
                for r in read:
                    print(r)
                    
    def fileread(self, file):
        """
        File need to be a dict or list. The pattern need to be:
            - Dict:
                {0:('parent', 'This is the beginning of TreeView structure'),
                 1:('child1', 'This is the child structure'),
                }
                Note: However, the dict will converted to list as well.
                      This dict pattern is the same as the insighttree() function.
            - List:
                [('parent', 'This is the beginning of TreeView structure'),
                 ('child1', 'This is the child structure'),
                ]
        This file will be written to a filename.txt.
        
        WARNING: Make sure you create blank filename.txt.
        If you use existing TreeView structure, all that has been written will be lost.
        The new file will overwrite the existing one.
        """
        if file:
            try:
                if isinstance(file, dict):
                    file = list(file.values())

                if isinstance(file, list):
                    with open(f'{self.filename}.txt', 'w') as wfile:
                        for f in file:
                            span, word = f
                            if span == 'parent':
                                if word[-2:] == ':\n' :
                                    wfile.write(f'{word}')
                                else:
                                    wfile.write(f'{word}:\n')
                            elif span in self.childs:
                                if  word[0] == '-' and word[-1] == '\n':
                                    wfile.write(f'{" " * self.childs[span]}{word}')
                                else:
                                    wfile.write(f'{" " * self.childs[span]}-{word}\n')
                            elif span == 'space':
                                wfile.write('\n')
                else:
                    print('Unidentified file!!!')
            except Exception as e:
                raise e
                
    def backuptv(self):
        """
        Backup TreeView structure in json database file. The backup max is 10 records only.
        The max can be change in line with '< 11'
        """
        try:
            log = int(datetime.datetime.timestamp(datetime.datetime.now()))
            data = list(self.insighttree().values())
            do = {log: data}
            dbs = db(self.filename)
            if str(dbs) not in os.listdir():
                dbs.createdb(do)
            else:
                if dbs.totalrecs() < 10:
                    dbs.indata(do)
                else:
                    dbs.indata(do)
                    key = sorted(list(dbs.loadkeys()))[0]
                    dbs.deldata(key)
        except Exception as e:
            raise e
            
    def loadbackup(self, filename, row = 0, stat = False):
        """
        This function can call back your previous data saved by backuptv() and 
        overwrite your existing one.
        """
        dbs = db(filename)
        if str(dbs) in os.listdir():
            if stat:
                if row <= dbs.totalrecs()-1:
                    key = sorted(list(dbs.loadkeys()))[row]
                    self.fileread(dbs.takedat(key))
            else:
                if row <= dbs.totalrecs()-1:
                    key = sorted(list(dbs.loadkeys()))[row]
                    return {n: tuple(w)  for n,w in enumerate(dbs.takedat(key))}
                
    def checked(self, row):
        """ 
        Appearing nice only in 'utf-8' encoding.
        WARNING: Depend on computer encoding system for appropriate display.
        """
        import locale
        if self.filename:
            if isinstance(row, int):
                try:
                    callrows = self.insighttree()
                    if not callrows is None and row in callrows:
                        if all(callrows[row][0] != a for a in['parent', 'space']):
                            gety = ''
                            if locale.getdefaultlocale()[1] == 'cp65001':                                
                                stc = chr(10004)
                            else:
                                stc = '«[DONE]»'
                            if stc not in callrows[row][1]:
                                gety = f'{callrows[row][1][:-1]}{stc}\n'
                                convert = list(callrows[row])
                                convert[1] = gety                         
                                callrows[row] = tuple(convert)
                                self.fileread(callrows)
                            else:
                                gety = callrows[row][1].replace(stc,'')
                                convert = list(callrows[row])
                                convert[1] = gety                         
                                callrows[row] = tuple(convert)
                                self.fileread(callrows)
                except Exception as e:
                    raise e
                    
    def insertspace(self, row):
        """
        Insert spaces before creating parent
        """
        if self.insighttree():
            d = self.insighttree()
            if row <= len(d) and d[row][0] == 'parent':
                with open(f'{self.filename}.txt') as file:
                    read = file.readlines()
                    read.insert(row, '\n')
                with open(f'{self.filename}.txt', 'w') as file:
                    file.writelines(read)
                    
if __name__ == '__main__':
    """
    For preview purpose to see result of using TreeView
    """
    import os
    from pprint import pprint 
    
    w = 'Amazing Grace'
    tv = TreeView('testtv')
    tv.writetree(w)
    for i in range(5):
        tv.quickchild(w, child = f'child{i}')
    tv.edittree('Amazing Grace, how sweet the sound')
    tv.edittree('Mantaaaaaaap!', row = 4, child = 'child2')
    tv.addparent('Wow good job')
    tv.edittree('Wow good job buddy', row = 6)
    tv.quickchild('Totally awesome', child = 'child1')
    tv.quickchild('This is quick child edit', child = 'child2')
    tv.quickchild('Thank You', child = 'child1')
    tv.delrow(8)
    tv.insertrow('God bless you', row = 8, child = 'child1' )
    tv.movetree(4, 6)
    tv.movechild(6, child = 'child1')
    tv.readtree()
    pprint(tv.insighttree())
    print()
    tv.readtree()
    tv.backuptv()
    nf = TreeView('testftv')
    file = {0:('parent', 'This is the beginning of TreeView structure'),
            1:('child1', '-This is the child structure\n'),
           }
    nf.fileread(file)
    nf.checked(1)
    pprint(nf.insighttree())
    print()
    nf.checked(1)
    pprint(nf.insighttree())
    print()
    nf.readtree()
    ans = input('Overwrite Data? ')
    if isinstance(ans, str):
        if ans.lower() == 'y':
            nf.loadbackup('testtv', stat = True)
            pprint(nf.insighttree())
            print()
            nf.readtree()
        else:
            pprint(nf.loadbackup('testtv'))
    
    if 'testtv.txt' in os.listdir():
        os.remove('testtv.txt')
        print('Done')
    else:
        print('Nothing')
    if 'testftv.txt' in os.listdir():
        os.remove('testftv.txt')
        print('Done')
    else:
        print('Nothing')
    if 'testtv.json' in os.listdir():
        os.remove('testtv.json')
        print('Done')
    else:
        print('Nothing')    