# Structures Explained
![Logo_SX_Structures_Explained](https://user-images.githubusercontent.com/58717653/117903033-2b419b80-b2a5-11eb-8891-985ef0d5ce18.png)
Structures Explained is a didactic 2D structural analysis software. It includes 2D structures,
 cross section and Mohr's Circle calculations and step by step solution in a PDF file. Also has a user friendly UI (English and Portuguese languages), with manual and examples.

2D Structure:
![struct](https://user-images.githubusercontent.com/58717653/110705615-6d7f2b80-81d5-11eb-97da-9a9029219c9c.gif)

Cross Section:
![crossSec](https://user-images.githubusercontent.com/58717653/110705128-b2ef2900-81d4-11eb-934d-485389ae5f9f.gif)

Mohr's Circle:
![mohr](https://user-images.githubusercontent.com/58717653/110705023-8b985c00-81d4-11eb-80ba-0b388a1e2ec3.gif)

How to Install:

For now Structures Explained and it's dependencies must be installed manually.

To do so clone the repository and install the following:

matplotlib>=3.0, numpy>=1.15.4, pyqt5, qdarkstyle, pylatex, sympy


You will also need my anaStruct fork, the current master utilizes the legacy branch, found at:

https://github.com/LeoBelmont/anaStruct/tree/sx-legacy


to install use:

pip install git+git://github.com/LeoBelmont/anaStruct@sx-legacy
