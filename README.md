# FreeTVG [Tree View Gui]
## **Tree View Gui is an outline note for viewing in tree structure**
### **Visit [TVG](https://treeviewgui.work) for tutorials and support**
## Installation
```pip install FreeTVG-karjakak```   
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
## Changes:
* **Tutorial TVG.pdf press: <Ctrl+F4>**
* **Tutorial TVG.pdf is updated.**
* **Clean-up some comment line.**
* **Can run TVG directly without creating a script.**
* **6 buttons deleted [Calculator, Send Note, Save, Open, Emoji, and ViewHTML].**
    * **Free from annoying message pop-up.**
    * **View HTML deleted as well, because the purpose is not much and basically the same as printing.**
* **Bugs fixed on overflowing memory usage.**
* ### [treeview](https://github.com/kakkarja/TV)
    * **Part of TVG engine has been seperated and has its own repo.**
		* **For TVG Windows user only.**
    * **TVG has been partly overhaul for adapting the new engine.**
    * **More robust and faster.**