from setuptools import setup

setup(
    name='StructuresExplained',
    version='1.0',
    packages=['StructuresExplained',
              'StructuresExplained.pdfconfig',
              'StructuresExplained.pdfconfig.translations',
              'StructuresExplained.solutions',
              'StructuresExplained.UI'
              ],
    download_url='https://github.com/LeoBelmont/Structures-Explained',
    license='GPL-3.0',
    author='Leonardo Bornia',
    author_email='lbornia6@gmail.com',
    description='Didactic software for 2D structures analysis',
    install_requires=["matplotlib>=3.0", "numpy>=1.15.4", "pyqt5", "anastruct", "qdarkstyle", "pylatex", "sympy"],
    depencency_links=["https://github.com/LeoBelmont/anaStruct-1.2.0"]
)
