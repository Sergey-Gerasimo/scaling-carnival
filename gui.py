import tkinter as tk 
from tkinter import filedialog, messagebox
from pathlib import Path
from exceptions import IncorrectFileName, IncorrectFile, EmptyPath
from readxl import read
from output import create_work_book
import io
import os 
from typing import final, Sequence
from network import Network
from warnings_ import * 

def resource_path(filename):
    exe_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(exe_dir, filename)
    return image_path

def get_norm_path(path:str) -> str: 
    path =  path.replace('/', '\\')

    if os.name != 'nt':
        path = path.replace('\\', '/')
    
    return path 

IMAGE_PATH: final = os.path.normpath(get_norm_path(f'images\\logo_en.png'))

def clean(nets:Sequence[Network, ]) -> Sequence[Network, ]: 
    out = [] 
    for net in nets: 
        for param, sensitivity in net.sensitivity: 
            if sensitivity is None: 
                break
        else: 
            out += [net]
    return out 

class Main(tk.Tk): 
    def __init__(self, *args, **kwargs) -> None: 
        super().__init__(*args, **kwargs)
        self.title("scaling-carnival")
        self.__logo = tk.PhotoImage(file=IMAGE_PATH)
        tk.Label(image=self.__logo).pack()
        self.iconphoto(False, tk.PhotoImage(file=IMAGE_PATH))
        self.path_to_file = Path('')
        self.path_to_save = Path(os.path.normpath(get_norm_path(f"output.xlsx")))

        self.__set_up()
        self.resizable(width=False, height=False)
        
    def __set_up(self) -> None: 
        self.__set_row1()
        self.__set_row2()  
        self.__set_row3()

    def __set_row3(self) -> None: 
        calcbnt = tk.Button(self, text="Начать исследование", command=self.__getxl)
        calcbnt.pack(fill=tk.X)

    def __getxl(self) -> None: 
        try:
            print(self.path_to_file.as_posix())
            print(self.path_to_save.as_posix())

            if (self.path_to_file.as_posix() == '.') or (self.path_to_save.as_posix() == '.'): 
                print(self.path_to_file.as_posix())
                print(self.path_to_save.as_posix())
                raise  EmptyPath
            
            nets = read(self.path_to_file.as_posix())
            nets = clean(nets)

            wb = create_work_book(nets)
            wb.save(self.path_to_save.as_posix())

        except IncorrectFile as err: 
            messagebox.showerror("Неверный файл", err)

        except IncorrectFileName: 
            messagebox.showerror("Неверный файл", err)

        except EmptyPath:
            messagebox.showerror("Не все поля заполнены", err)
        
        except KeyError: 
            messagebox.showwarning("Не все поля заполнены" "Не все сети присутвуюит в обоих файлах")

        else: 
            if ConfigNotAllData is not None: 
                messagebox.showwarning(ConfigNotAllData)

            if NotAllData is not None: 
                messagebox.showwarning(NotAllData)

            messagebox.showinfo("Все успешно", "Файл был успешно обработан")

            

    def __set_row2(self) -> None: 
        self.row2 = tk.Frame(self)
        self.row2.pack(fill=tk.X)

        tk.Label(self.row2, text="Путь до сохраняемого файла: ").pack(side=tk.LEFT)
        self.path_to_save_label = tk.Label(self.row2, text=self.path_to_save.name)
        self.path_to_save_label.pack(side=tk.LEFT)
        self.path_to_save_label['fg'] = "green"
        tk.Button(self.row2, text='Выбрать файл', command=self.__get_path_to_save).pack(side=tk.RIGHT)

    def __get_path_to_save(self) -> None: 
        path:io.TextIOWrapper | str = tk.filedialog.asksaveasfilename(filetypes=[("Excel", '*.xlsx')])

        if not path: 
            raise EmptyPath
        
        self.path_to_save = Path(path)
        print(path)
        self.path_to_save_label['text'] = self.path_to_save.name

        try:
            self.__validate_file(self.path_to_save, self.path_to_save_label)

        except IncorrectFileName: 
            messagebox.showerror("Неверный файл", f"Файл {self.path_to_save.name} должен иметь расширение xlsx")
        

    def __set_row1(self) -> None: 
        """Функция найтройки первой строки приложения"""
        self.row1 = tk.Frame(self)
        self.row1.pack(fill=tk.X)

        tk.Label(self.row1, text="Файл с данными: ").pack(side=tk.LEFT)
        self.path_info = tk.Label(self.row1, text=self.path_to_file.name)
        self.path_info.pack(side=tk.LEFT)
        tk.Button(self.row1, text='Выбрать файл', command=self.__get_path_to_file).pack(side=tk.RIGHT)

    def __get_path_to_file(self) -> None: 
        """Функция запроса у пользователя пути до необходимого файла"""
        path:io.TextIOWrapper | str = tk.filedialog.askopenfile(filetypes=[("Excel", '*.xlsx')])
        if not path: 
            raise EmptyPath
        else: 
            path: str = path.name
            print(path)
        
        self.path_to_file = Path(path)
        self.path_info['text'] = self.path_to_file.name

        try:
            self.__validate_file(self.path_to_file, self.path_info)

        except IncorrectFileName: 
            messagebox.showerror("Неверный файл", f"Файл {self.path_to_file.name} должен иметь расширение xlsx")
        

    def __validate_file(self, path:Path, label:tk.Label) -> None: 
        """Провека имени файла на соответвие необходимому расширению"""
        if path.suffix == '.xlsx': 
            label['fg'] = "green"
        else: 
            label['fg'] = "red"
            raise IncorrectFileName
        
def main() -> None:
    win = Main()
    win.mainloop()