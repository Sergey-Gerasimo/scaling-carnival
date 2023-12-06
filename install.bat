mkdir python
curl https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe --output python\python-3.12.0.exe
python\python-3.12.0.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0

%LocalAppData%\Programs\Python\Python312\python -m venv venv
venv\Scripts\pip install -r requirements.txt
venv\Scripts\pyinstaller --onefile --noconsole --icon=logo_en.ico main.py
mkdir bin
copy dist\main.exe bin\scaling-carnaval.exe
rd /s /q dist
rd /s /q build
rd /s /q %LocalAppData%\Programs\Python\Python312
