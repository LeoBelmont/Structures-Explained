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
\rhead{\includegraphics[width=0.05\textwidth]{figs/logo.png}}
\lhead{Structures Explained}
\cfoot{\thepage}
\renewcommand{\footrulewidth}{0.4pt}
\usepackage[scaled=1]{helvet}
\renewcommand{\familydefault}{\sfdefault}
"""


def makeCover(title, language):
    cover = r"""
            \begin{titlepage}
            
            \newcommand{\HRule}{\rule{\linewidth}{0.5mm}}
            
            \center
            
            \includegraphics[width=0.75\textwidth]{figs/logo.png}\\[1cm]
            \vspace{\fill}
            {\LARGE Structures Explained\\ """ + title + r"""}\\[1.5cm]
            
            \HRule \\[0.6cm]
            """
    if language == "PT":
        cover += r"""
                 \large\textbf{Laboratório AeroTech}\\[0.5cm]
                 \large\textbf{Departamento de Engenharia Aeronáutica}\\[0.5cm]
                 \textsc{\Large Universidade de São Paulo}\\[0.5cm]
                 """
    elif language == "EN":
        cover += r"""
                 \large\textbf{AeroTech Laboratory}\\[0.5cm]
                 \large\textbf{Departament of Aeronautic Engineering}\\[0.5cm]
                 \textsc{\Large University of São Paulo}\\[0.5cm]
                 """

    cover += r"""
             \HRule \\[1.5cm]            
            
             \vfill
        
             \end{titlepage}
        
             \newpage
             """

    return cover
