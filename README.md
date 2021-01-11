# TVG
>## TreeViewGui
* **TVG is an outline note for viewing in tree structure.**
* **Please give feedback if there is known error by creating issues.**

**Note: Block using '#' in the code on icon, because not provided in the repository**

### **New addition function :joy:**
* **Add send note with Telethon [Telegram api wrapper].**
    * **Please install first Telethon https://github.com/LonamiWebs/Telethon**
>**Please get ProtectData for Lock File function https://github.com/kakkarja/PTD**  
>  
>**Please get CreatePassword for encrypting telegram apis https://github.com/kakkarja/CP**
### Changes:
* **TVG has evolved to more than just taking simple outline note.**
    * **Now can convert a simple note to outline note.**
        * **FORMAT:**  
          >Sample  =>  "parent" [first-line]  
          >This is the format of child. Will be split to two.  =>  "child1" [split by "."/"?"/"!"]
        * **RESULT:**
          ```TEXT
          Sample:
            -This is the format of child.
            -Will be split to two.
          ```
    * **You can use CPP function to move or even clone rows to other row within existing rows.**
    * **No folding child like other outline, but..**
        * **Can hide parents and its childs.**
            * **This function better than folding, when the outline in hide mode, you can save as pdf or even send note for the visible one.**
    * **Now combine with Telethon wrapper for Telegram.** 
        * **Send note:**
            * **With emojies.**
            * **Scheduler**
            * **Send file [only the TVG outline note]**
            * **Get files ~~[except pictures and stickers]~~**
            * **Multi accounts**
            * **Send multiple chat in group**
        * **You have to create Telegram api "https://core.telegram.org/api" to use this incredible function.**
    * **Can choose color for setting the text and listbox background color. [No button, only event binding. Control+.]**
    * **Can change font setting for text and listbox. [No button, only event binding. Control+,]**
        * **The size is ~~locked~~ on size 10 to 12, to preserve viewing.**
        * **TAKE NOTICE:**
            * **Not all fonts will appear nicely if change the size.**
    * **Can delete setting back to original. [No button, only event binding. Control+/]**
    * **~~File Lock~~ has been replace with Editor.** 
        * **FORMAT:**
          >**s: => 'space'**  
          >**p:Format => 'parent'**  
          >**c1:Editor that write directly. => 'child1' ['c1' to 'c50' represent 'child1' to 'child50']**
        * **RESULT:**
          ```TEXT
          \n
          Format:
             Editor that write directly.
          ```
    * **~~Convert~~ has been deleted and replace with <u>TeleCalc</u>.**
        * **Convert now become part of Editor.~~[2 functions in one]~~**
    * **Can do calculation and get latest exchange rate.**
        * **Built with https://fixer.io api.**
        * **Fixer wrapper for python is used in this project.**
        * **Get free api in https://fixer.io**
        * **Exchange Rate from a currency to all currency in library [157 currencies].**
        * **For free api only can convert the base currency ["EUR"].**
        * **Convert amount of currency to another currency.**
            * **Only available for paid api.**
    * **Can transfer calculation or rates/convert, back to TVG for outline note record.**
        * **This convinient for Send Note.**
    * **Wrap mode:**
        * **Make long sentences appear nice in childs.**
    * **Can copy calculation or exchange rate to TVG Editor.**
        * **For calculation have 2 choices.**
            * **As TVG note format** 
            * **TeleCalc format [for re-editing].**
    * **Can edit calculation in TVG and translated to TeleCalc.**
        * **FORMAT:**
          >**cal: 2500500/7 => "Calculation"**  
          >**ans: => "Answer" [just empty or not empty in re-editing]**  
          >**note: Awesome => "Note" [optional]**
        * **TAKE NOTICE:**
            * **"ans:" is ignored, because it will be recalculate by the changes in "cal:".**
        * **RESULT: [in TeleCalc]**
          ```TEXT
          CAL: 2,500,500/7
          ANS: 357,214.28571428574
          Note: Awesome
          ```
    * **Add few functions for complementing the Editor:**
        * **Ex [Edit existing] for editing existing file in Editor instead using the entry box.**
            * **Very useful for editing long records of outline document.**
            * **Very quick aditting as well with Editor's format.**
            * **TAKE NOTICE:**
                * **Is advisable to backup file before edit with Ex function.**
                * **In case you want to revert back, you can load back anytime with your backup file.**
        * **Template for saving frequently used format of outlines.**
            * **You can load them for applying the template on the editor mode.**
            * **Template can help you to forget about retyping same format again-and-again.**
    * **~~Save as pdf~~ is replace with <u>Printing</u>.**
        * **Convert TVG file to HTML and open in browser.**
          >**Please get markdown first for Printing to work https://github.com/Python-Markdown/markdown.**
        * **Just click the print button and save to pdf or print direct to a printer.**
    * **Emoji now can paste direct to TeleTVG screen.**
        * **Now can delete Mark that no longer use.**
    * **Can write markdown style.**
        * **TAKE NOTE:**
            * **This is not markdown editor, so not all markdown style will give desired result.**
            * **Simple markdowns style will applied [eg. _emphasize_].**
    * **Can print with checkboxes.**
    * **Now can paste emoji to editor.**
        * **~~No~~ Button for emoji, ~~only~~ key binding [Control+';']**
    * **Can view created html from Printing, with HTML View.**
* **And many more.. :joy:**
                
![TVG](/TVG.png)
![TVG2](/TVG3.png)
![TVG2](/TVG4.png)
![TVG2](/TVG2.png)
![TVG1](/TVG1.png)
![TeleTVG](/TeleTVG.png)
![TeleCalc](/TeleCalc.png)
![ColorTVG](/ColorTVG.png)
![FontTVG](/FontTVG.png)

---
# **TreeView**

## **TreeView is part of TVG [TreeViewGUI]**

***https://github.com/kakkarja/TVG***

>### **TreeView is an outline note that save to text file in tree structure**

:white_check_mark: **This can be use in console mode**

* **Example write a parent for first time:**
    ```PYTHON
    from TreeView import TreeView
    w = 'Amazing Grace'
    tv = TreeView('testtv')
    tv.writetree(w)
    tv.readtree()
    ```
    * **Result:**
    
        ```TEXT
        Amazing Grace:
        ```
        
* **Example write childs:**
    ```PYTHON
    for i in range(5):
        tv.quickchild(w, child = f'child{i}')
    tv.readtree()
    ```
    * **Result:**
        ```TEXT
        Amazing Grace:
        
            -Amazing Grace
        
                -Amazing Grace
        
                    -Amazing Grace
        
                        -Amazing Grace
        ```
* **Example edit:**
    ```PYTHON
    tv.edittree('Amazing Grace, how sweet the sound')
    tv.edittree('Mantaaaaaaap!', row = 4, child = 'child2')
    tv.readtree()
    ```
    * **Result:**
        ```TEXT
        Amazing Grace, how sweet the sound:
        
            -Amazing Grace
        
                -Amazing Grace
        
                    -Amazing Grace
        
                -Mantaaaaaaap!
        ```
* **Example add parent childs and deleting:**
    ```PYTHON
    tv.addparent('Wow good job')
    tv.edittree('Wow good job buddy', row = 6)
    tv.quickchild('Totally awesome', child = 'child1')
    tv.quickchild('This is quick child edit', child = 'child2')
    tv.quickchild('Thank You', child = 'child1')
    tv.delrow(8)
    tv.readtree()
    ```
    * **Result:**
        ```TEXT
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
    ```PYTHON
    tv.insertrow('God bless you', row = 8, child = 'child1' )
    tv.movetree(4, 6)
    tv.movechild(6, child = 'child1')
    tv.readtree()
    ```
    * **Result:**
        ```TEXT
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
    ```PYTHON
    from pprint import pprint
    pprint(tv.insighttree())
    ```
    * **Result:**
        ```TEXT
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
