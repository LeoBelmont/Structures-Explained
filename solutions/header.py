from PyQt5.QtGui import QPixmap
from UI import resources

PDFsettingss = r"""
\usepackage[left=1.5cm,right=1.5cm,top=2cm,bottom=2cm]{geometry}
\usepackage{setspace}
\onehalfspacing
\usepackage[portuguese]{babel}
\usepackage{indentfirst}
\usepackage{graphicx}
\usepackage{caption}
\usepackage{amsmath}
\usepackage{multicol}
\usepackage[colorlinks=true,linkcolor=black,anchorcolor=black,citecolor=black,filecolor=black,menucolor=black,runcolor=black,urlcolor=black]{hyperref}
\usepackage{cals, ragged2e, lmodern}
\usepackage{pdflscape}
\usepackage{float}
\usepackage{breqn}
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}
"""

PDFsettings = r"""
\usepackage[left=1.5cm,right=1.5cm,top=2cm,bottom=2cm]{geometry}
\usepackage{setspace}
\onehalfspacing
\usepackage[portuguese]{babel}
\usepackage{caption}
\usepackage{amsmath}
\usepackage{cals, ragged2e}
\usepackage{breqn}
\usepackage{pdflscape}
\usepackage{multicol}
\usepackage[colorlinks=true,linkcolor=black,anchorcolor=black,citecolor=black,filecolor=black,menucolor=black,runcolor=black,urlcolor=black]{hyperref}
\usepackage{float}
\usepackage{gensymb}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\rhead{oi}
\lhead{Laboratório AeroTech}
\cfoot{\thepage}
\usepackage[scaled=1]{helvet}
\renewcommand{\familydefault}{\sfdefault}
"""


def makeCover(title):
    cover = r"""
            \begin{titlepage}
            
            \newcommand{\HRule}{\rule{\linewidth}{0.5mm}}
            
            \center
            
            \vspace{\fill}
            {\LARGE Structures Explained\\ """ + title + r"""}\\[1.5cm]
            
            \HRule \\[0.6cm]
            \large\textbf{Laboratório AeroTech}\\[0.5cm]
            \large\textbf{Departamento de Engenharia Aeronáutica}\\[0.5cm]
            \textsc{\Large Universidade de São Paulo}\\[0.5cm]
            \HRule \\[1.5cm]
            
            \vfill
            
            \end{titlepage}
            
            \newpage
            """

    return cover

# \includegraphics[width=0.75\textwidth]{:/Figures/cross_section.png}\\[1cm]
