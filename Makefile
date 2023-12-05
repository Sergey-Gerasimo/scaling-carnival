all: install compile clean link

compile: install 
	pyinstaller --onefile --noconsole --icon=logo_en.ico main.py

install: 
	python3 -m venv venv 
	venv/bin/pip3 install -r requirements.txt

clean:  compile 
	rm -r build
	mkdir bin
	cp dist/main bin/scaling-carnival
	cp -r dist/main.app bin/scaling-carnival.app
	rm -r dist

link: compile
	echo "export PATH=${PWD}/bin/:$PATH" > ~/.zshrc 
	echo "export PATH=${PWD}/bin/:$PATH" > ~/.bashrc 

