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
* **[Algorithm Explanation](#-algorithm-explanation-)**
* **[Technical issues](#technical-issues-on-shortcut-buttons)**
* **[Configuration](#configuration)**
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
      * **Use "Shift" button to select massively, and ~~"Option"~~ "Control" button to select differently or unselect**
    * **Unfold**
      * **To unhide all**
  * **TAKE NOTICE:**
    * **Fold selection will retain when changing file, but not for fold all childs**
    * **~~Once Unfold, the retain selection will be erased~~**
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
* **Tk fontchooser**
  * **When dialog in focus too long**
    * **When application is quit and restarted again, it will persistently reappear at start**
    * **Resolution walk-around:**
      * **Will check the dialog visibility at beginning of starting application, and if is true, will hide it at once**

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

    * **For add-on TVG has another format please click -> [NEW](#new)**  
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
* **Fold selected enhancement**
  * **Will reload previous selections**
  * **Can click / "ctrl + s" Insight for identifying what to select**
  * **Use Shift-key for massive selection and Ctrl-key for select or unselect individually**
* **Fold enhancement**
  * **Unfolding no longer delete retain selected childs**
    * **If you press "Fold Childs" the retain ones will be folded again**
  * **Fold selected will delete the retain selected if selections is none**
  * **Fold Childs will fold all childs, if there is no retain selected**
* **[New unresolve issues](#unresolve-issues)**
  * **Refactoring, and bugs fixed or resolved**
* **EXPLANATION:**
  * **If user want to keep the selected fold and using hidden mode**
    * **Just unfold and use hidden mode**
    * **While in hidden mode, user could not use the fold function**
    * **If hidden mode is cleared, just press fold childs again and the retain ones will folded back again**
  * **For CPP function \[very powerful function for manipulating text content\]**
    * **In Hidden mode, you can select CPP to copied the text content and copied to new file or existing file**
* **In CPP function**
  * **CPP selection has been hacked for it's selection mode**
    * **By default is extended mode selection that works like charm, same as selection mode for Fold selected**
    * **However, if you find it confusing when you wanted choose the cells for manipulation, you can hacked the configuration to multiple mode**
      * **Multiple mode will choose the cells one by one selectively**

        ```Terminal
        # Will change to multiple selection for CPP function
        > tvg multiple
        
        # Combination for theme mode and selection mode
        >tvg dark multiple
        
        # or
        >tvg multiple light
        ```

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

---

* ## **Technical issues on shortcut buttons**
  
  * **Due to some similarity of shortcut buttons in TVG with the global one in a OS, therefore the functions may result weirdly**
  * **Found issues:**
    * **TVG**
      * **<ins>Ctrl+n</ins> for <ins>CPP function</ins> in <ins>MacOS X</ins>**
      * **resulting selections being canceled and only one selected below selections**
      * **For reference research [Shortcuts in MacOS X](https://support.apple.com/en-us/HT201236)**
    * **Resolution**
      * **Now change to <ins>Cmd+n</ins> for <ins>CPP function</ins> in <ins>MacOS X</ins>**

[⬆️](#freetvg-tree-view-gui)

---

* **Selection preference**
  * **Configuring selection to "multiple" will also applied to Fold selected function**
  * **Only for Hidden mode will not change, as it is "multiple" by default**
    * **No point to change to other selection mode, because the function's selection only choosing parents**
* **Insight function**
  * **Now functioning in Hidden mode, and CPP as well**
* **In Hidden Mode**
  * **No longer 2 options**
  * **The hidden mode is using reverse option only**
    * **That mean the selection parents are not hid, and the rest will be hidden.**
  * **TAKE NOTICE:**
    * **If this changes bother any user, please stay with the current installed one**
    * **However any future update changes will no more 2 options as well for Hidden Mode**
    * **This decision deliberately done because of new functions Fold**
      * **In fold hiding selections are making more sense**
* **On 2nd thought**
  * **Is not easy to just hid 1 parent, so there is the configuration for it**
  * **When starting the app in cmd prompt / terminal type**

    ```Terminal
    # Config for Hidden mode
    >TVG unreverse
    ```

  * **Will change the reverse option in Hidden mode**
    * **The selections will be hidden instead**

[⬆️](#freetvg-tree-view-gui)

* ### **Configuration**

  * **Now when user change the configuration of elements in TVG, it will be saved**
    * **User do not need to reconfigure again when starting the app**
  * **If want to set back to default setting:**
    * **While app still running Press Win [Ctrl + F5] || Mac [fn + F5]**
    * **Exit the app and run again, everyrhing back to default!**
  * **Dependency added tomlkit [@sdispater](https://pypi.org/project/tomlkit/)**
  * **Add Configuration for wrapping**
    * **By default words in TVG is unwrapped**

      ```Terminal
      # Config wrapping
      > TVG word
      ```

  * **Add configuration for cheked-box**
    * **Cheked function by default will add "✔️" or ">>[DONE]<<" depend on the OS default system encoding**
    * **Now can be configured to add "[x]"**

      ```Terminal
      # Config Checked-Box
      > TVG on
      ```

  * **Configuration values**
    * **Can be mixed as long as values are identified by TVG**

      ```Terminal
      # Config values mixed
      > TVG on light unreverse word multiple
      ```

* **Combobox algorithm enhance for selecting file or creating new file**
  * **For CPP, Change File, Template and create new file from first starting TVG**
* **Bugs fixed for checking files**
  * **To avoid processing errors**
* **In Printing**
  * **When print button clicked**
    * **The background color will turned white and the foreground color will be black**
    * **Need to click-checked for printing background, so that the marking highlight will be visible**

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
