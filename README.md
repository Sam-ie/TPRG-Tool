# TPRG-Tool
A tool for TPRG log processing.



pyinstaller --name="文本处理工具" ^
            --icon=images/favicon.ico ^
            --add-data "images;images" ^
            --add-data "dictionary;dictionary" ^
            --add-data "languages;languages" ^
            --add-data "controller;controller" ^
            --add-data "model;model" ^
            --add-data "view;view" ^
            --add-data "utils;utils" ^
            --windowed ^
            --noconfirm ^
            main.py
