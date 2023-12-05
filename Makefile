all: install compile clean 

compile: 
	pyinstaller --onefile --noconsole --icon=logo_en.ico main.py

install: 
	python3 -m venv venv 
	venv/bin/pip3 install -r requirements.txt

clean:  
	rm -r build
	mkdir bin
	cp dist/main bin/scaling-carnaval
	cp -r dist/main.app bin/scaling-carnaval.app
	rm -r dist

