::@echo off 
:: Оцистка директории 
if not exist  requ.py echo PWD="%CD:\=\\%" > requ.py
echo "cleaning"
if exist %CD%\main.spec rd %CD%\main.spec 

if exist %CD%\bin rd /s/q %CD%\bin

if exist %CD%\dist rd /s/q %CD%\dist

if exist %CD%\build rd /s/q %CD%\build

if not exist %CD%\python  mkdir %CD%\python

:: Установка Python если не установлен 
if not exist %LocalAppData%\Programs\Python\Python312 (
    if not exist %CD%\python\python-3.12.0.exe (
        echo "Download Python3.12"
        curl https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe --output python\python-3.12.0.exe
    )
    echo "Install Python3.12"
    python\python-3.12.0.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
)
:: Создание venv 
if exist %CD%\venv (
    echo "remove venv"
    rd /s/q %CD%\venv
)

echo "install venv"
%LocalAppData%\Programs\Python\Python312\python -m venv venv
echo "install requirements"
venv\Scripts\pip install -r requirements.txt
:: компиляция 
echo "compile"
venv\Scripts\pyinstaller --onefile --noconsole --icon=logo_en.ico main.py

echo "cleaning"
mkdir %CD%\bin
copy %CD%\dist\main.exe %CD%\bin\scaling-carnaval.exe
rd /s /q %CD%\dist
rd /s /q %CD%\build

