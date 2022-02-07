# sklad
**Študentský projekt TIS 2021**

Projekt obsahuje 2 spôsoby spustenia programu.

1. spôsob (rýchlejší)

    Pre prácu stačí stiahnuť priečinok “exe_file”, nastavenie súboru “data/config.txt” a monitorov. 

   priečinok “exe_file”:
     - obsahuje spustiteľný “WarehouseVis.exe” program 
       - po nastavení configu stačí spustiť tento súbor
     - obsahuje priečinok “data”, ktorého súbory treba upraviť nasledovne:
       - súbor “config.txt” treba nastaviť podľa návodu:
          https://github.com/TIS2021-FMFI/sklad/blob/a8259b42c1d4bf1521383a05d125550dc0a68385/Documentation/Konfiguracia_exportu_zo_SAP.docx
       - súbor “warehouse_config.json” netreba meniť (je nastavený k aktuálnemu skladu (15.1.2022))
         - pre akúkoľvek zmenu sa treba riadiť návodom:
         https://github.com/TIS2021-FMFI/sklad/blob/a8259b42c1d4bf1521383a05d125550dc0a68385/Documentation/WarehouseVis_manual.docx
     
    
2. spôsob (pomalší)

    Nainštalovanie pythonu, knižníc, nastavenie configu “data/config.txt” a nastavenie monitorov:

   - inštalácia PYTHON: na stránke www.python.org/downloads/
   - inštalácia PYTHON modulov:
     - Vyžaduje mať nainštalovaný nástroj na sťahovanie python balíčkov PIP
     https://pypi.org/project/pip/#files
     - Treba mať nainštalované pythonovské knižnice cez prikaz: 
     *pip install “nazov_kniznice”*
       - openpyxl
       - PIL
       - tkinter
       - pyglet
   - súbor “config.txt” treba nastaviť podľa návodu: https://github.com/TIS2021-FMFI/sklad/blob/a8259b42c1d4bf1521383a05d125550dc0a68385/Documentation/Konfiguracia_exportu_zo_SAP.docx
   - spustiť súbor ”WarehouseController.py”



**Monitory:**
- pre prácu s 2+ monitormi sa treba riadiť návodom: https://github.com/TIS2021-FMFI/sklad/blob/245a38c256e60834270da1afbd5752fde66bba03/Documentation/Navod_na_nastavenie_monitorov.pptx



**Generovanie exe súboru zo skriptov:**

 - Spustením skriptu installer.py sa vygenerujú priečinky build a dist. 
 - V priečinku dist sa nachádza exe súbor WarehouseController.exe. 
 - Súbor možno premenovať a presunúť podľa potreby. 
 - Exe súbor vyžaduje aby v koreňovom priečinku bol priečinok data, ktorý obsahuje súbory: 
   - config.txt
   - warehouse_config.json
   - legend_sk.png 

   tieto súbory sa dajú stiahnuť z github-u. 
 - Priečinok dist a build možno vymazať.





