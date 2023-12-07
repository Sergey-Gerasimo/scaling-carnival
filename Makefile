all: install compile clean 

compile: install 
	echo PWD="'${PWD}'" > req.py
	venv/bin/pyinstaller --onefile --noconsole  --hidden-import tkinter --icon=logo_en.ico main.py

install: 
	python3.12 -m venv venv 
	venv/bin/pip3 install -r requirements.txt


clean:  compile 
	if [ -d "${PWD}/bin" ]; then \
        rm -r ${PWD}/bin; \
    fi
	mkdir ${PWD}/bin;

	cp dist/main bin/scaling-carnival;
	cp -r dist/main.app bin/scaling-carnival.app;
	rm -r ${PWD}/dist 
	rm -r ${PWD}/build



