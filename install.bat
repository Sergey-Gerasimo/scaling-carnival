python -m venv venv 
venv/Scripts/pip install -r requirements.txt
pyinstaller --onefile --noconsole --icon=logo_en.ico main.py
mkdir bin
xcopy dist/main.exe bin/scaling-carnaval.exe
rd dist
rd build
set PATH=%PATH%;%CD%\bin