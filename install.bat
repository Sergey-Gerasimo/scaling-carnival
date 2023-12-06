echo off 
:: Оцистка директории 
echo "cleaning"
if exist main.spec (
    rd main.spec 
)
if exist bin (
    rd /s/q bin
)

if exist dist(
    rd /s/q bin
)

if exist build (
    rd /s/q build 
)


if not exist python (
    mkdir python 
)
:: Установка Python если не установлен 
if not exist %LocalAppData%\Programs\Python\Python312 (
    if not exist python\python-3.12.0.exe (
        echo "Download Python3.12"
        curl https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe --output python\python-3.12.0.exe
    )
    echo "Install Python3.12"
    python\python-3.12.0.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
)
:: Создание venv 
if exist venv (
    echo "remove venv"
    rd /s/q venv
)

echo "install venv"
%LocalAppData%\Programs\Python\Python312\python -m venv venv
echo "install requirements"
venv\Scripts\pip install -r requirements.txt
:: компиляция 
echo "compile"
venv\Scripts\pyinstaller --onefile --noconsole --icon=logo_en.ico main.py

echo "cleaning"
mkdir bin
copy dist\main.exe bin\scaling-carnaval.exe
rd /s /q dist
rd /s /q build

