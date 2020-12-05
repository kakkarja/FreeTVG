# TVG
>## TreeViewGui
* **TVG is an outline note for viewing in tree structure.**
* **Can be save as PDF to a user preferred directory.**
* **To use the PDF function user must download PyFPDF. [https://github.com/reingart/pyfpdf]**
* **Please give feedback if there is known error by creating issues.**

**Note: Block using '#' in the code on icon, because not provided in the repository**

### **New addition function :joy:**
* **Add send note with Telethon [Telegram api wrapper].**
    * **Please install first Telethon https://github.com/LonamiWebs/Telethon**

![TVG](/TVG.png)
![TeleTVG](/TeleTVG.png)
![SavedPDF](/SavedPDF.png)
---
# **TreeView**

## **TreeView is part of TVG [TreeViewGUI]**

***https://github.com/kakkarja/TVG***

>### **TreeView is an outline note that save to text file in tree structure**

:white_check_mark: **This can be use in console mode**

* **Example write a parent for first time:**
    ```python
    from TreeView import TreeView
    w = 'Amazing Grace'
    tv = TreeView('testtv')
    tv.writetree(w)
    tv.readtree()
    ```
    * **Result:**
    
        ```python
        Amazing Grace:
        ```
        
* **Example write childs:**
    ```python
    for i in range(5):
        tv.quickchild(w, child = f'child{i}')
    tv.readtree()
    ```
    * **Result:**
        ```python
        Amazing Grace:
        
            -Amazing Grace
        
                -Amazing Grace
        
                    -Amazing Grace
        
                        -Amazing Grace
        ```
* **Example edit:**
    ```python
    tv.edittree('Amazing Grace, how sweet the sound')
    tv.edittree('Mantaaaaaaap!', row = 4, child = 'child2')
    tv.readtree()
    ```
    * **Result:**
        ```python
        Amazing Grace, how sweet the sound:
        
            -Amazing Grace
        
                -Amazing Grace
        
                    -Amazing Grace
        
                -Mantaaaaaaap!
        ```
* **Example add parent childs and deleting:**
    ```python
    tv.addparent('Wow good job')
    tv.edittree('Wow good job buddy', row = 6)
    tv.quickchild('Totally awesome', child = 'child1')
    tv.quickchild('This is quick child edit', child = 'child2')
    tv.quickchild('Thank You', child = 'child1')
    tv.delrow(8)
    tv.readtree()
    ```
    * **Result:**
        ```python
        Amazing Grace, how sweet the sound:
        
            -Amazing Grace
        
                -Amazing Grace
        
                    -Amazing Grace
        
                -Mantaaaaaaap!
        
        Wow good job buddy:
        
            -Totally awesome
        
            -Thank You
        ```
* **Example insert, move tree position and move child position:**
    ```python
    tv.insertrow('God bless you', row = 8, child = 'child1' )
    tv.movetree(4, 6)
    tv.movechild(6, child = 'child1')
    tv.readtree()
    ```
    * **Result:**
        ```python
        Amazing Grace, how sweet the sound:
        
            -Amazing Grace
        
                -Amazing Grace
        
                    -Amazing Grace
        
        Wow good job buddy:
        
            -Mantaaaaaaap!
        
            -Totally awesome
        
            -God bless you
        
            -Thank You
        ```
* **Example insighttree:**
    ```python
    from pprint import pprint
    pprint(tv.insighttree())
    ```
    * **Result:**
        ```python
        {0: ('parent', 'Amazing Grace, how sweet the sound:\n'),
         1: ('child1', '-Amazing Grace\n'),
         2: ('child2', '-Amazing Grace\n'),
         3: ('child3', '-Amazing Grace\n'),
         4: ('space', '\n'),
         5: ('parent', 'Wow good job buddy:\n'),
         6: ('child1', '-Mantaaaaaaap!\n'),
         7: ('child1', '-Totally awesome\n'),
         8: ('child1', '-God bless you\n'),
         9: ('child1', '-Thank You\n')}
        ```
