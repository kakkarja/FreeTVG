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
* **[Changes](#changes)**
* **[Unresolved Issues](#unresolve-issues)**
* **[Development Purpose](#development-purpose)**
* **[Latest Notice](#latest-notice)**
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

[⬆️](#freetvg-tree-view-gui)

* ### **Add-On for TVG**

  ```Terminal
  pip3 install -U addon-tvg-karjakak
  ```

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
      * **Use "Shift" button to select massively, and "Option" button to select differently or unselect**
    * **Unfold**
      * **To unhide all**
  * **TAKE NOTICE:**
    * **Fold selection will retain when changing file, but not for fold all childs**
    * **Once Unfold, the retain selection will be erased as well**
  * **The difference between Fold and Hidden mode**
    * **Fold only hide childs and Hidden mode, hide parents and their childs**
    * **In fold all other functions working properly and in Hidden mode, all other functions are freeze**

[⬆️](#freetvg-tree-view-gui)

## Changes

* **Tutorial TVG.pdf press: <Ctrl+F1> or <fn+F1> in MacOS**
* **Send note from default email: <Ctrl+F4> or <fn+F4> in MacOs**
  * **Can choose copy to clipboard. (set indentation shorter)**
    * **Can be use to send message in [TeleTVG](https://github.com/kakkarja/TeleTVG)**
* **Clean-up some comment line.**
* **Can run TVG directly without creating a script.**
* **6 buttons deleted [Calculator, Send Note, Save, Open, Emoji, and ViewHTML].**
  * **Free from annoying message pop-up.**
  * **View HTML deleted as well, because the purpose is not much and basically the same as printing.**
* **Bugs fixed on overflowing memory usage.**
* **Tooltip now available in MacOS X.**
* **For Add-On TVG**
  * **For function Sum-Up**
    * **Much faster calculation for thousands lines.**
    * **Just delete "TOTAL..." lines manually that need to be change, will be much faster instead.**
  * **For Expression Calculation (F5/Ctrl+F5)**
    * **Works for simple calculation.**
    * **All double operator like eg. "\*\*", disabled.**
      * **To avoid overlflow result.**
    * **Able to paste directly without clicking result first.**
    * **Will paste exactly where the position of numbers suppose to be**
* **Template has been overhauled for improvement**
  * **Can delete a saved template**
* **Look-Up now more informative (not in editor mode)**
* **Add Markdown buttons in Editor mode for convinience**

* ### [treeview](https://github.com/kakkarja/TV)

  * **Part of TVG engine has been seperated and has its own repo.**
  * **TVG has been partly overhaul for adapting the new engine.**
  * **More robust and faster.**

[⬆️](#freetvg-tree-view-gui)

## Unresolve Issues

* **For Add-On TVG**
  * **For PieChart-Graph**
    * **Some issue in matplotlib**
      * **Will raise exception after closing the graph, if configure window (within the tool bar) is already closed beforhand.**
    * **Nonetheless**
      * **Will not raise exception if configure window is not close yet.**
* **Short-Cut Issues**
  * **Virtual OS Windows in Mac**
    * **Some short-cuts works only with "Control" + "Option" or "Shift" + ...**

[⬆️](#freetvg-tree-view-gui)

## Development Purpose

* **TreeViewGui is using Excptr Module to catch any error exceptions**
  * **Plese often check the folder "FreeTVG_TRACE" in "HOME" / "USERPROFILE" path directory.**
  * **Raise issues with copy of it, thank you!**

[⬆️](#freetvg-tree-view-gui)

## Latest Notice

* **Found very little bug in Template**
  * **Has been fixed in 2.8.18**
* **When send to email**
  * **For MacOs X**
    * **Markdown escape "\\" will <ins>not</ins> be ~~deleted~~ when send with default email ([F4/Ctrl+F4] send mail function)**
  * **Email will be copied to default email app**
* **Theme set globally according to system default theme**
  * **No longer active through function button (previously F3/Ctrl+F3 button)**
* **Send to email assign to F3/Ctrl+F3 button**
* **Express Calc assign to F4/Ctrl+F4 button and no longer F5/Ctrl+F5**
* **Some bugs fixed**
  * **Editor on raise error, no longer shut the markdown buttons**
  * **After pressing markdown button, the focus back to text editor**
* **You can force dark mode in daylight global setting and vice-versa**

  ```Terminal
  # Will change the light theme to dark
  > tvg dark

  # Will change the dark theme to light
  > tvg light
  ```

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

    * **For add-on TVG has another format please click -> [NEW](https://github.com/kakkarja/FreeTVG#new)**  
* **Printing will fill the background and foreground according to the text editor background and foreground**
* **Fix little in light mode theme**
* **Enhancing Fold**
  * **Making fold running faster in huge records**
* **Fold is already release just**

  ```Terminal
  pip3 install -U FreeTVG-karjkak
  ```

* **Send email (fn+F3 / Ctrl+F3)**
  * **For MacOs X**
    * **Enhance the text by converting emojies to text description**
    * **Using dependency: demoji**
      * **[@bsolomon1124](https://pypi.org/project/demoji/)**
* **Printing**
  * **Printing have no more option for ~~check-box~~**
    * **Since markdown has involved for checked-box, ~~check-box~~ option become obsolete**
* **Markdown has short-cut**
  * **Check it out in tutorial press `Ctrl+F1 / fn+F1`**
* **Filename enhancement**
  * **Abbriviation in uppercase will be kept unchange otherwise all will be title**

[⬆️](#freetvg-tree-view-gui)

## TVG

![TVG](/Pics/TVG.png)

[⬆️](#freetvg-tree-view-gui)

## With Add-On FreeTVG

![SumAll](/Pics/sumup.png)

![PieChart](/Pics/piechart.png)

![ExpressionCalc](/Pics/expressioncalc.png)

[⬆️](#freetvg-tree-view-gui)

## Markdown

![Markdown](/Pics/markdown.png)

![Printing](/Pics/printing.png)

[⬆️](#freetvg-tree-view-gui)
