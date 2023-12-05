# scaling-carnival
Install 
Linux & MacOs
```bash
git clone https://github.com/Sergey-Gerasimo/scaling-carnival.git
cd scaling-carnival
python3 -m venv venv 
source venv/bin/activate 
pip3 install openpyxl 
sudo echo "alias scaling-carnival="${PWD}/venv/bin/python3 main.py"" >> ./bashrc && source ./bashrc 
```

Useage 
```bash 
scaling-carnival -f somefile.xlsx
```
or 

```bash
scaling-carnival
```
