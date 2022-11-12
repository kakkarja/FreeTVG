# FreeTVG [Tree View Gui]

## **Tree View Gui is an outline note for viewing in tree structure**

### **Visit [TVG](https://treeviewgui.work) for tutorials and support**

## Installation

```pip3 install -U FreeTVG-karjakak```

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

## NEW

* ### **Add-On for TVG**

    ```Python
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

* ### [treeview](https://github.com/kakkarja/TV)

  * **Part of TVG engine has been seperated and has its own repo.**
  * **TVG has been partly overhaul for adapting the new engine.**
  * **More robust and faster.**

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

## Development Purpose

* **TreeViewGui is using Excptr Module to catch any error exceptions**
  * **Plese often check the folder "FreeTVG_TRACE" in "HOME" / "USERPROFILE" path directory.**
  * **Raise issues with copy of it, thank you!**

## Notice and Apologize

* **Found very little bug in Template**
  * **Has been fixed in 2.8.18**
  * **Sorry for the inconvenience 🙏**

![TVG](/Pics/TVG.png)

## With Add-On FreeTVG

![SumAll](/Pics/sumup.png)

![PieChart](/Pics/piechart.png)

![ExpressionCalc](/Pics/expressioncalc.png)
