# Copyright © kakkarja (K A K)

import re
import sys

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
        self.filename = filename
        self.parent = dict()
        self.childs = dict()
    
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
        self.parent = {'parent':0}
        self.childs = {f'child{c//4}': c for c in range(201) if c % 4 == 0 and c != 0}
        
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
        except:
            import sys
            print(sys.exc_info()[0])
    
    def insighthidden(self, data):
        """
        This is very useful for looking at your TreeView data,
        with understanding your structure. Looking at rows, child and written words. 
        """
        self.parent = {'parent':0}
        self.childs = {f'child{c//4}': c for c in range(201) if c % 4 == 0 and c != 0}
        
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
        except:
            import sys
            print(sys.exc_info()[0])
                            
    def quickchild(self, words, child ):
        """
        Adding child to a parent. You can create as much as 100 childs.
        You must define the variable child e.g: 'child1'. 
        """
        self.childs = {f'child{c//4}': c for c in range(201) if c % 4 == 0 and c != 0}
        
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
        self.parent = {'parent':0}
        self.childs = {f'child{c//4}': c for c in range(201) if c % 4 == 0 and c != 0}
        try:
            if isinstance(words, str):
                d = self.insighttree()
                if child:
                    if child in self.childs:
                        if isinstance(row, int) and row > 0:
                            for r in range(len(d)):
                                if row == r :
                                    d[row] = (child, f'-{words}\n')
                            with open(f'{self.filename}.txt', 'r') as file:
                                read = file.readlines()
                            read[row] = f'{" " * self.childs[d[row][0]]}{d[row][1]}'
                            with open(f'{self.filename}.txt', 'w') as file:
                                file.writelines(read)
                else:
                    d[row] = (list(self.parent.items())[0][0], f'{words}:\n')
                    read = []
                    with open(f'{self.filename}.txt', 'r') as file:
                        read = file.readlines()
                    read[row] = f'{" " * self.parent[d[row][0]]}{d[row][1]}'
                    with open(f'{self.filename}.txt', 'w') as file:
                        file.writelines(read)
            else:
                print('Need to be string!!!')                                
        except:
            import sys
            print(sys.exc_info())
            
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
    
        with open(f'{self.filename}.txt') as file:
            read = file.readlines()
            del read[row]
        with open(f'{self.filename}.txt', 'w') as file:
            file.writelines(read)
    
    def insertrow(self, words, row = 0, child = None):
        """
        This function is to insert words into a decided row within the TreeView structure. 
        """
        self.childs = {f'child{c//4}': c for c in range(201) if c % 4 == 0 and c != 0}
        if isinstance(words,str):
            if child:
                words = f'{" " * self.childs[child]}-{words}\n'
            else:
                words = f'{words}:\n'
            with open(f'{self.filename}.txt') as file:
                read = file.readlines()
                read.insert(row, words)
            with open(f'{self.filename}.txt', 'w') as file:
                file.writelines(read)
        else:
            print('Need to be string!!!')
            
    def movetree(self, row, to):
        """
        Moving one row to another. From row to another row. Suggested to use insighttree(),
        for knowing where to move.
        """
        if row and to:
            if isinstance(row, int) and isinstance(to, int):
                moving = []
                with open(f'{self.filename}.txt') as file:
                    read = file.readlines()
                    if read[row] != '\n':
                        moving.append(read[row])
                        del read[row]                  
                        if to > len(read):
                            for move in moving:
                                read.append(move)
                        else:
                            for move in moving:
                                read.insert(to, move)
                with open(f'{self.filename}.txt', 'w') as file:
                    file.writelines(read)
    
    def movechild(self, row, child):
        """
        Moving row to left or right side using child. Suggested to use insighttree(),
        for knowing where to move.
        """
        self.childs = {f'child{c//4}': c for c in range(201) if c % 4 == 0 and c != 0}
        if row and child:
            if child in self.childs:
                with open(f'{self.filename}.txt') as file:
                    read = file.readlines()
                    if read[row] != '\n':
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
        self.childs = {f'child{c//4}': c for c in range(201) if c % 4 == 0 and c != 0}
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
                                    wfile.write(f'{word[:-2]}:\n')
                                else:
                                    wfile.write(f'{word}:\n')
                            elif span in self.childs:
                                if  word[0] == '-' and word[-1] == '\n':
                                    wfile.write(f'{" " * self.childs[span]}-{word[1:-1]}\n')
                                else:
                                    wfile.write(f'{" " * self.childs[span]}-{word}\n')
                            elif span == 'space':
                                wfile.write('\n')
                else:
                    print('Unidentified file!!!')
            except:
                import traceback
                traceback.print_exc()
                #import sys
                #print(sys.exc_info()[0])
                
    def backuptv(self):
        """
        Backup TreeView structure in csv file. The backup max is 10 records only.
        """
        import datetime
        import csv
        import os
        try:
            log = str(datetime.datetime.now())[:-7]
            data = list(self.insighttree().values())
            if data:
                do = {'log': log, 'data': data}
                if not f'{self.filename}.csv' in os.listdir():
                    with open(f'{self.filename}.csv', 'w', newline='') as file:
                        fieldnames = ['log', 'data']
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerow(do)
                else:
                    with open(f'{self.filename}.csv') as file:
                        rd = list(csv.reader(file))
                        if len(rd) >= 11:
                            dat = rd[-9:]
                            dat.insert(0,rd[0])
                            with open(f'{self.filename}.csv', 'w') as wfile:
                                fill = csv.writer(wfile, delimiter = ',')
                                for d in dat:
                                    fill.writerow(d)      
                    
                    with open(f'{self.filename}.csv', 'a', newline='') as file:
                        fieldnames = ['log', 'data']
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writerow(do)
            else:
                print('No data to be backup!!!')
        except:
            import sys
            print(sys.exc_info()[0])
            
    def loadbackup(self, filename, row = 0, stat = False):
        """
        This function can call back your previous data saved by backuptv() and 
        overwrite your existing one.
        """
        import csv
        import os
        try:
            if filename:
                if f'{filename}.csv' in os.listdir():
                    with open(f'{filename}.csv') as csvfile:
                        reads = list(csv.reader(csvfile))
                        if stat:
                            if row:
                                if len(reads)-1 >= row:
                                    data = eval(reads[row][1])
                                    self.fileread(data)
                                else:
                                    print('No data is loaded!')
                            else:
                                data = eval(reads[1][1])
                                self.fileread(data)
                        else:
                            data = list(eval(reads[1][1]))
                            data  = {n:w  for n,w in enumerate(data)}
                            return data         
                else:
                    print('No such file!')
        except:
            import sys
            print(sys.exc_info()[0])

    def checked(self, row):
        """ 
        Using 'u0336' unicode for strikethrough.
        Apearing nice only in 'utf-8' encoding.
        WARNING: Depend on computer encoding system for appropriate display.
        """
        if self.filename:
            if isinstance(row, int):
                callrows = self.insighttree()
                if not callrows is None and row in callrows:
                    if all(callrows[row][0] != a for a in['parent', 'space']):
                        gety = ''
                        stc = str(u"\u0336")
                        if callrows[row][1][2] != stc:
                            for callrow in callrows[row][1][1:-1]:
                                gety += f'{stc}'.join(callrow) + f'{stc}'
                            convert = list(callrows[row])
                            convert[1] = gety                         
                            callrows[row] = tuple(convert)
                            self.fileread(callrows)
                        else:
                            cutt = callrows[row][1][1:-1]
                            for cut in range(len(cutt)):
                                if cut % 2 == 0:
                                    gety += ''.join(cutt[cut])
                            convert = list(callrows[row])
                            convert[1] = gety                         
                            callrows[row] = tuple(convert)
                            self.fileread(callrows) 
    
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
    os.chdir(os.getcwd()[:34])
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
    if 'testtv.csv' in os.listdir():
        os.remove('testtv.csv')
        print('Done')
    else:
        print('Nothing')    
    
    w = 'Amazing Grace'
    tv = TreeView('testtv')
    tv.writetree(w)
    for i in range(5):
        tv.quickchild(w, child = f'child{i+1}')
    tv.edittree('Amazing Grace, how sweet the sound')
    tv.edittree('Masih bisa dan keren', row = 4, child = 'child2')
    tv.edittree('Mantaaapppp', row = 5, child = 'child3')    
    tv.addparent('Wow good job')
    tv.edittree('Wow good job buddy', row = 6)
    tv.quickchild('Totally awesome', child = 'child1')
    tv.quickchild('This is quick child edit', child = 'child2')
    tv.quickchild('Thank You', child = 'child1')
    tv.delrow(8)
    tv.insertrow('God bless you', row = 8, child = 'child1' )
    tv.movetree(4, 6)
    tv.movetree(4, 6)
    tv.movechild(5, child = 'child1')
    tv.movechild(6, child = 'child2')
    pprint(tv.insighttree())
    print()
    tv.readtree()
    tv.backuptv()
    nf = TreeView('testftv')
    file = {0:('parent', 'This is the beginning of TreeView structure'),
            1:('child1', 'This is the child structure'),
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