# TVG
>## TreeViewGui
* **TVG is an outline note for viewing in tree structure.**

**Note: Block using '#' in the code on icon, because not provided in the repository**

### **New addition function**
* **Add send note with Telethon [Telegram api wrapper].**
    * **https://github.com/LonamiWebs/Telethon**

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
     * **Send note:**
        * **With emojies.**
        * **Scheduler**
        * **Send and Get file [only the TVG outline note]**
        * **Send multiple chat in group**
    * **Can choose color for setting the text and listbox background color. [No button, only event binding. Control+.]**
    * **Can change font setting for text and listbox. [No button, only event binding. Control+,]**
        * **The size is ~~locked~~ on size 10 to 40.**
        * **TAKE NOTICE:**
            * **Not all fonts are available in html view.**
                * **If not available the browser will use default font styles.** 
    * **Can delete setting back to original. [No button, only event binding. Control+/]**
    * **~~File Lock~~ has been replace with *<ins>Editor</ins>*.** 
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
    * **~~Convert~~ has been deleted and replace with *<ins>TeleCalc</ins>*.**
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
            * **WARNING:**
                * **If you edit using Ex choosing whole document, actually the existing file is deleted.**
                * **If you do backup, you can revert back to previous file.**
        * **Template for saving frequently used format of outlines.**
            * **You can load them for applying the template on the editor mode.**
            * **Template can help you to forget about retyping same format again-and-again.**
    * **~~Save as pdf~~ is replace with *<ins>Printing</ins>*.**
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
    * **Can edit just a parent with its childs in Ex.**
        * **TAKE NOTE:**
            * **In case want to cancel editing, just click editor back.**
            * **Or delete everyrhing in editor without leaving an extra blank line.**
                * **If you wanted to delete them instead, then just leave an extra blank line.**
    * **Can scalling pixel in different resolution.**
        * **TAKE NOTE:**
            * **When scalling, TVG may appear too small and other app function may appear overly sized.**
            * **Best resolution is 1366 x 768 [base on dev res] :pray:**
            * **Better handling in resolution now.**
                * **Almost all resolution can adapt [some still need scaling].**
    * **Can Undo or Redo.**
        * **[Control+z] for undo and [Control+Shift+z] to redo.**
    * **Special Function for TeleCalc [no button, only shortcut Control+k].**
        * **Recalculate changes of a calculation formula in a row.**
            * **Can recalculate other rows that link from result.**
                * **Select the "From" and "To" [range that link from result].**
                * **Avoid recalculate one-by-one [unless not linked]**
    * **Can write Telethon [Telegram wrapper] markdown style.**
        * **Difference with markdown only on the italic.**
            * **Markdown using `*italic*` :arrow_right: *italic*, in Telegram double underscore.**
            * **Link webpage, just directly the url.**
    * **Can LookUp in editor mode.**
        * **Look for words and replace it with new words.**
    * **TVG now resizeable :joy:**
    * **Can search emoji by its name in the combobox.**
    * **Can search saved template in the combobox.**
    * **Can search a contact in <ins>TeleTVG - Multi</ins>.**
    * **Can set TVG new geometry position as default [will remember the last position and resize that user has set].**
    * **Can hide buttons for almost full screen text editor**
        * **Short-Cut keyboards is active**
    * **TeleCalc and TeleTVG now resizeable :joy:**
        * **There are minsize for them, depend on resolution, both may still appear too large.**
    * **Can save to mark, emojies that selected in text [only emoji that exist in TVG library].**
    * **Can call Emoji in TVG without in Editor mode.**
        * **Can paste on entry box.**
    * **Can send file to a group.**
    * **Can schedule send message to a group.**
    * **TVG has darker mode for easing eyes :joy:**
    * **TeleTVG has autotext/textpander function.**
        * **Save often used words or even emojies to an abbreviation.**
        * **FORMAT:**
            * **\<abbreviation\>::<often used words/emojies>**
            * **EXAMPLE:**
                * **Tq::Thank You**
                * **Typed "Tq" :arrow_right: "Thank you".**
        * **Can save multiple lines of autotext format.**
    * **Encryption to saved text for sharing to other tvg user, is much better encrypted.**
        * **TAKE NOTE:**
            * **However the speed is much slower than previous one for larger file.**
    * **Add tooltip for TVG buttons.**
    * **CPP now can copy parents and its childs in hidden mode..**
        * **to existing file or new file. :joy:** 
            
#### **Source codes for TeleTVG and TeleCalc, are no longer available. If anyone wanted to built along with these apps, please do not hesitate to contact the dev.**
    

![TVG](/TVG.png)
![TVG3](/TVG3.png)
![TVG6](/TVG6.png)
![TVG4](/TVG4.png)
![TVG5](/TVG5.png)
![TeleTVG](/TeleTVG.png)
![TeleCalc](/TeleCalc.png)
