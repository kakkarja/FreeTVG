# FreeTVG [Tree View Gui]

## **Tree View Gui is an outline note for viewing in tree structure**

### **Visit [TVG](https://treeviewgui.work) for tutorials and support**

---

<details>
  <summary>
    <font size=3>
      <strong>Jump-Start to:</strong>
    </font>
  </summary>
(click to see contents)

* **[Install](#installation)**
* **[Usage](#usage)**
* **[NEW](#new)**
  * **[Add-On for TVG](#add-on-for-tvg)**
  * **[Markdown](#markdown)**
  * **[Folding](#folding)**
  * **[Dynamic Theme Changes](#dynamic-theme-changes)**
  * **[Direct Print PDF](#direct-print-pdf)**
* **[Development Purpose](#development-purpose)**
* **[Latest Notice](#latest-notice)**
* **[Algorithm Explanation](#-algorithm-explanation-)**
* **[Configuration](#configuration)**
* **[Editor Enhancement](#editor-new-enhancement)**
* **[Ex Func Changes](#ex-function-changes)**
* **[Dynamic Theme](#dynamic-theme)**
* **[Text Viewer Enhencement](#text-view)**
  * **[Known Limitation](#known-limitation)**
* **[New Backup](#new-backup)**
* **[New Function Bible Reader](#bible-reader-and-journal)**
* **[Versions Highlights](#versions-highlights)**
* **[Picture TVG](#tvg)**
* **[Picture with Add-On TVG](#with-add-on-freetvg)**
* **[Picture Markdown](#markdown-1)**

</details>

---

## Installation

```pip3 install -U FreeTVG-karjakak```

[⬆️](#freetvg-tree-view-gui)

## Usage

**With script:**

```Python
from TVG import main

# Start TVG outline note
main()
```

**Without script:**

* **Press keyboard buttons at the same time => [(Windows Logo) + "r"].**
  * **Open "Run" window.**
  * **In "open" field key in "TVG".**
  * **Press "ok" button.**
* **Create TVG folder by default in "\user\Documents" or "\user".**
  * **Every TVG text note that created will be saved in TVG folder.**  

**Without script for MacOS X user:**  

```Terminal
# In Terminal
% TVG
```

[⬆️](#freetvg-tree-view-gui)

## NEW

* ### **Add-On for TVG**
  
  * **Become required dependency in FreeTVG**
  * **Add extra 3 Functions:**
    * **Sum-Up**
      * **format editor:**

        ```Python
        p:+Parent
        c1:child1 1,000.00
        c1:child1 1,000.00
        ```

      * **Result 1st click:**

        ```Python
        +Parent:
            -child1 1,000.00
            -child1 1,000.00
            -TOTAL 2,000.00
        ```

      * **Result 2nd click (good for \[printing] in browser):**

        ```Python
        # gather all sums and turn to hidden mode
        +Parent:
            -child1 1,000.00
            -child1 1,000.00
            -TOTAL 2,000.00

        TOTAL SUMS = 2,000.00
        ```

    * **Pie Chart**
      * **Create Pie-Chart for all sums**
      * **Using \<matplotlib> and \<tkinter>**
    * **Del Total**
      * **Delete all Totals**
    * **Expression Calculation**
      * **Calculator for Editor Mode**
      * **"F5" for MacOS X and "Ctrl+F5" for Windows**
      * **Works only in editor mode**
      * **Will formatting numbers when paste in editor mode**

        ```Python
        # format with 2 float numbers
        1,234,567.89
        ```

[⬆️](#freetvg-tree-view-gui)

* ### **Markdown**

  * **Usage how to use markdown in pdf [fn+f1 or ctrl+f1]**
    * **Nicely presented in HTML and printed in pdf [Printing function]**
  * **Special thanks to:**
    * **[@Python-Markdown](https://github.com/Python-Markdown/markdown)**
    * **[@facelessuser](https://github.com/facelessuser/pymdown-extensions)**

[⬆️](#freetvg-tree-view-gui)

* ### **Folding**

  * **Now user can hide childs with folding functions**
    * **Cand hide all childs or selected childs**
    * **Even when childs are hidden, the other functions still working, unlike in "Hidden mode"**
  * **3 buttons added to TVG**
    * **Fold Childs**
      * **Will fold all childs**
    * **Fold selected**
      * **Will fold selected childs**
      * **Use "Shift" button to select massively, and "Control" button to select differently or unselect**
    * **Unfold**
      * **To unhide all**
  * **TAKE NOTICE:**
    * **Fold selection will retain when changing file, but not for fold all childs**
    * **~~Once Unfold, the retain selection will be erased~~**
  * **The difference between Fold and Hidden mode**
    * **Fold only hide childs and Hidden mode, hide parents and their childs**
    * **In fold almost all other functions working properly and in Hidden mode, all other functions are freeze**

[⬆️](#freetvg-tree-view-gui)

* ### **Dynamic Theme Changes**

  * **Theme will change dynamically when user chage the os system's theme \[**Dark / Light**\]**
    * **Using dependency of <em><u>Dark-Detect</u></em>**
      * **[@albertosottile](https://github.com/albertosottile/darkdetect)**

* ### **Direct Print PDF**

  * **For MacOS X and Windows**
    * **Dependency using <em><u>PdfKit</u></em>**
      * **[JazzCore](https://github.com/JazzCore/python-pdfkit)**
    * **IMPORTANT!**
      * **Need to install wkhtmltopdf using homebrew for MacOS Users**

        ```Terminal
        brew install homebrew/cask/wkhtmltopdf
        ```

      * **For Windows users**
        * **Need to download the installer on [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html)**
        * **When installing, choose default path:**

        ```Terminal
        # Program Files folder in Windows
        C:\Program Files\wkhtmltopdf
        ```

      * **If wkhtmltopdf not installed, Printing will directed to browser instead**

![DirectPrintInMac](Pics/printedPDF.png)

[⬆️](#freetvg-tree-view-gui)

* ### [treeview](https://github.com/kakkarja/TV)

  * **Part of TVG engine has been seperated and has its own repo.**
  * **TVG has been partly overhaul for adapting the new engine.**
  * **More robust and faster.**

[⬆️](#freetvg-tree-view-gui)

## Development Purpose

* **TreeViewGui is using Excptr Module to catch any error exceptions**
  * **Plese often check the folder "FreeTVG_TRACE" in "HOME" / "USERPROFILE" path directory.**
  * **Raise issues with copy of it, thank you!**

[⬆️](#freetvg-tree-view-gui)

## Latest Notice

* **Express Calc assign to F4/Ctrl+F4 button and no longer F5/Ctrl+F5**
* **In Markdown**
  * **When dragging curssor with mouse/trackpad on text**
    * **Markdown will wrapped the text when insert**
    * **Only for B, I, U, S, L, SP, and SB (Bold, Italic, Underline, Strikethrough, Link hypertext website, Superscript, and Subscript)**
      * **Add two more buttons M and SA (Marking highlight and Special Attribute)**
  * **Inserting markdown will wrapping selection text**

* **In Editor**
  * **Function for convert has been deleted**
    * **There only one editor mode, which using the specific format**

      ```Text
      # Editing in Editor mode wih specific format
      # "p" for parent, "c<number>" for child, and "s" for space

      p:Parent input
      c1:Child input and <number> can up to 50
      s:

      # Result:

      Parent input:
          -Child input and <number> can up to 50

      ```

    * **For add-on TVG has another format please click -> [NEW](#new)**  
* **Send email (fn+F3 / Ctrl+F3)**
  * **For MacOs X**
    * **Enhance the text by converting emojies to text description**
    * **Using dependency: demoji**
      * **[@bsolomon1124](https://pypi.org/project/demoji/)**
* **Markdown has short-cut**
  * **Check it out in tutorial press `Ctrl+F1 / fn+F1`**
* **Filename enhancement**
  * **Abbriviation in uppercase will be kept unchange otherwise all will be title**
* **Fold selected enhancement**
  * **Will reload previous selections**
  * **Can click / "ctrl + s" Insight for identifying what to select**
  * **Use Shift-key for massive selection and Ctrl-key for select or unselect individually**
* **Fold enhancement**
  * **Unfolding no longer delete retain selected childs**
    * **If you press "Fold Childs" the retain ones will be folded again**
  * **Fold selected have a choice to delete or not when none selected**
  * **Fold Childs will fold all childs, if there is no retain selected**

* **EXPLANATION:**
  * **If user want to keep the selected fold and using hidden mode**
    * **Just unfold and use hidden mode**
    * **While in hidden mode, user could not use the fold function**
    * **If hidden mode is cleared, just press fold childs again and the retain ones will folded back again**
  * **For CPP function \[very powerful function for manipulating text content\]**
    * **In Hidden mode, you can select CPP to copied the text content and copied to new file or existing file**
* **The algorithm of CPP has been improved**
  * **Now selections that is not in order can be copied and moved to chosen selected line number**

    >---
    >
    > ### **🤔 ALGORITHM EXPLANATION 💡**
    >
    >---
    > **\# in moving mode (also works for copying)**
    >
    > **<ins>used to be in order only</ins>**
    >
    > **selections in order -> [1,2,3,4] (ascending only)**
    >
    > **chosen line 8**
    >
    > **Result:**
    >
    > * **0,5,6,7,1,2,3,4,8,.. (records stay the same)**
    >
    >---
    > **\# in copying mode (also works for moving)**
    >
    > **<ins>Now also can be unordered</ins>**
    >
    > **selections unordered -> [1,3,5,7] (ascending only)**
    >
    > **chosen line 8**
    >
    > **Result:**
    >
    > * **0,1,2,3,4,5,6,7,1,3,5,7,8,.. (records are expanding)**
    >
    >---

[⬆️](#freetvg-tree-view-gui)

* ### **Configuration**

  * **Press Win [Ctrl + F5] || Mac [fn + F5]**
    * **Can modified Configuration directly; please refer to Tutorial by pressing MacOs X [fn + F1] and Windows [Ctrl + F1]**

* ### **Dynamic Theme**
  
  * **Title-Bar in windows can be change to dark or light**
    * **Not for dialogs and messages yet!**

* **Mail \[fn+F3 / ctrl+F3\]**
  * **For macos bug fixed**

* ### **Editor new enhancement**
  
  * **Editor can write to any row in working document**
    * **Click any row in the list-box before goto Editor mode**

* ### **Control Fold-Selected flow**

  * **Fold-selected will be viewed folded even after (intact)**
    * **Editing or writing in Editor**
    * **After deletion a row in Delete**
    * **After inserting a row in Insert**
    * **After editing a parent and its child in Ex**
    * **Sum-Up addon for TVG**
    * **Del Total addon for TVG**
    * **When COPY function copying data to other row (not for MOVE)**
    * **When moving a child Up or Down**
    * **When changing child's state to left or right**

* ### **Ex Function changes**

  * **Edit only for a Parent and its childs**
  * **Option for Edit whole document has been no more!**

* ### **Text View**
  
  * **Text View convert Markdown attribute**
    * **To bold, italic, underline, strikethrough, highlight, superscript, and subscript**
  
  ![Text View](Pics/text_view.png)

  * ### **Known Limitation**

    * **Markdown language and how Text View works**
      * **Text View cannot interprate eg. "\*\*\*Testing this \^\^text\^\^\*\*\*"**
      * **The position of text that marked inside another marked will cause entirely bolded and italic also underline**
      * **To avoid such cases, it should be "\*\*\*Testing This\*\*\* \*\*\*\^\^text\^\^\*\*\*"**
      * **In some rare case like eg. "\^\^\*\*\*Good 20M\*\*\*\^\^\^\*\*\*2\*\*\*\^ area"**
      * **Will work perfectly fine in text view**
      * **However in Markdown language will interprate them bewilderedly**

* ### **NEW Backup**

  * **Backup was using json, now change to SQLite database**
  * **Database dependency using SQLModel**
    * **[@tiangolo](https://sqlmodel.tiangolo.com/)**
  * **Now Backup function also backup fold selection data, if any!**

* ### **Bible Reader and Journal**

  * **New function for Reading Bible and take journal**
    * **Short-Cut [fn/control + F7]**
  * **Bible provided KJV**
  * **Can have more bibles**
    * **Download bibles in [BIBLE4U](https://www.google.com/search?q=bible4u)**
    * **Download XML zipfile**
    * **Unarchive it to:**

    ```Terminal
    /user_name/Documents/TVG/Bibles

    #if no documents folder than

    /user_name/TVG/Bibles
    ```

    * **In TVG open configuration by pressing [fn/control + F5]**
    * **Select the Bible you have downloaded**
    ![Configure](Pics/Config.png)
    * **WARNING!**
      * **Not all bibles will result properly**
        * **Try choosing right fonts before opening a bible so that it will work well**
        * **For windows 10 and 11 users, you can set the global setting of unicode to [utf-8 (edited3)](https://superuser.com/questions/1715715/can-i-enable-unicode-utf-8-worldwide-support-in-windows-11-but-set-another-enco)**
        * **Change the font styles of TVG (refer to help > fn/control + F1)**
      * **In case of error, please raise an issue 🙏**
        * **Will alert what kind of error**
        * **Can check at folder "FreeTVG_TRACE" for error log ([for development purpose](#development-purpose))**

  ![Bible Reader](Pics/Bible_Reader.png)

  * **When press journal, the displayed verses copied to Editor for journal purpose 🙏**

>---
>
> # Revelation
>
> ### I testify to everyone who hears the prophetic words of this book: If anyone adds to them, God will add to him the plagues described in this book. And if anyone subtracts from the prophetic words of this book, God will remove his portion from the Tree of Life and in the holy city, which are described in this book
>
>---

* ### **Versions Highlights**

  * **Version 3.3.12**
    * **Layout change**
      * **The entry for writing and inserting are now at the bottom, for easy viewing when writing and editting**
  * **Version 3.3.14**
    * **Add functionality to Text Viewer**
      * **Text View, which convert markdown attributes to look like rich text ([for common attributes only](#text-view))**
  * **Version 3.3.17**
    * **Bugs fixed**
      * **Printing work accordingly in hidden mode**
      * **Checked work nice with Text View functionality**
      * **Hidden mode also work with Text View**
  * **Version 3.4.0**
    * **Backup now using SQLite with dependency package SQLModel**
    * **Bugs fixed**
      * **On copying data from hidden mode to a new or existing file (part of CPP function)**
        * **Works well with text view functionality**
      * **Infobar display text of selected row from text view (used to be from original text)**
  * **Version 3.4.1**
    * **Bug fixed in database**
  * **Version 3.5.0**
    * **Add new fuction**
      * **Bible Reading [⇪](#bible-reader-and-journal)**
  * **Version 3.5.1**
    * **Bible Reading**
      * **When open again will open to last open book 🙏**
  * **Version 3.5.2**
    * **Catch error in Bible Reading for issuing purpose**
      * **TVG will work fine now**
  * **Version 3.5.3**
    * **Now every bible has it's own last open saved file**
      * **No conflict of opening a bible that have different language transaltion**
  * **Version 3.5.4**
    * **Little bugs fixed in Editor**
    * **The layout for writing entry appearance has been fixed for Windows and MacOS as well**
  * **Version 3.5.5**
    * **Direct PDF creation for Windows**
      * **[Direct Print PDF](#direct-print-pdf)**
  * **Version 3.5.6**
    * **Markdown marking highlight stay yellow and font color turn to black**
    * **Infor-Bar font smaller in Windows**
  * **Version 3.5.8**
    * **Fix bugs for previous version**
    * **Some tweak on appearance in Windows**
      * **Font look smaller on Buttons**
      * **Font look smaller on Bible**
      * **Font look smaller on info-bar**
      * **others..**
  * **Version 3.5.9**
    * **Bug fix - Font look smaller on Buttons**
  * **Version 3.5.10**
    * **Bug fix for CPP function that copying to last row**
    * **Sending TVG note with default mail is in development (for Windows only!)**
      * **Edge browser no longer able to send email with mailto, due to max capacity set in url**
  * **Version 3.5.11**
    * **Nothing change on compose mail in Windows**
      * **User need to manually change the App Default for Mail**
        * **Choose => MAILTO open on Mail (instead of browser)**
    * **Reference: [CHANGING DEFAULT EMAIL APP](https://helpdesk.telebroad.com/support/solutions/articles/4000185298-changing-the-default-email-app-windows-macos-chrome-firefox)**
  * **Version 3.5.12**
    * **Some bugs fixed on Hidden function**
      * **Both hidden mode unreverse and reverse**
        * **When try to hide a parent that the child is on last row, was not included -> FIXED**
        * **When hide a parent, where the last child not the last row, the "space" was included -> FIXED**
  * **Version 3.5.13**
    * **Some Bugs fixed on Editor and Write functions**
      * **With the short-cut button changing between listbox widget to entry widget create editing to "None" row -> FIXED**
      * **Editor could not begin if the file is not exist yet -> FIXED**
  * **Version 3.5.14**
    * **Fixed some bug in Folding Selection function**
      * **When edit in Ex function, some folded child is not folded -> FIXED**
        * **However if changes on both between a folded one, the folded will set to unfolded**

[⬆️](#freetvg-tree-view-gui)

## TVG

![TVG](Pics/TVG.png)

![TVG](Pics/TVG2.png)

[⬆️](#freetvg-tree-view-gui)

## With Add-On FreeTVG

![SumAll](Pics/sumup.png)

![PieChart](Pics/piechart.png)

![ExpressionCalc](Pics/expressioncalc.png)

[⬆️](#freetvg-tree-view-gui)

## Markdown

![Markdown](Pics/markdown.png)

![Printing](Pics/printing.png)

[⬆️](#freetvg-tree-view-gui)
