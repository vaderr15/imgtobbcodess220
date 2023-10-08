@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

rem Запрос названия изображения
set /p image_name=Введите название изображения: 

rem Установка значения по умолчанию для --diff
set "diff=49"

rem Запрос степени шакальности --diff
set /p diff_value=Введите степень шакальности --diff (по умолчанию 49): 
if not "%diff_value%"=="" (
    set "diff=%diff_value%"
)

rem Запуск PowerShell для выполнения скрипта ss14img.py
powershell.exe -ExecutionPolicy Bypass -Command "python ss14img.py !image_name! --diff !diff!"
pause

endlocal
