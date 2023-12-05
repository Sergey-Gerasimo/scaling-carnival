import tkinter as tk 
from tkinter import filedialog, messagebox
from pathlib import Path
from exceptions import IncorrectFileName, IncorrectFile, EmptyPath
from readxl import read
from output import create_work_book
import io

class Main(tk.Tk): 

    def __init__(self, *args, **kwargs) -> None: 
        super().__init__(*args, **kwargs)
        self.title("scaling-carnival")
        self.__logo = tk.PhotoImage(file='logo_en.png')
        tk.Label(image=self.__logo).pack()
        self.iconphoto(False, tk.PhotoImage(file='logo_en.png'))
        self.path_to_file = Path('')
        self.path_to_save = Path("output.xlsx")

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

            if (self.path_to_file.as_posix() == '.') or (not self.path_to_save.as_posix() == '.'): 
                raise  EmptyPath
            
            nets = read(self.path_to_file.as_posix())
            wb = create_work_book(nets)
            wb.save(self.path_to_save.as_posix())

        except IncorrectFile: 
            messagebox.showerror("Неверный файл", "Файл должен иметь расширение xlsx")

        except IncorrectFileName: 
            messagebox.showerror("Неверный файл", "Файл должен иметь расширение xlsx")

        except EmptyPath:
            messagebox.showerror("Не все поля заполнены", "Введите все недостающие данные")

            

    def __set_row2(self) -> None: 
        self.row2 = tk.Frame(self)
        self.row2.pack(fill=tk.X)

        tk.Label(self.row2, text="Путь до сохраняемого файла: ").pack(side=tk.LEFT)
        self.path_to_save_label = tk.Label(self.row2, text=self.path_to_save)
        self.path_to_save_label.pack(side=tk.LEFT)
        self.path_to_save_label['fg'] = "green"
        tk.Button(self.row2, text='Выбрать файл', command=self.__get_path_to_save).pack(side=tk.RIGHT)

    def __get_path_to_save(self) -> None: 
        path:io.TextIOWrapper | str = tk.filedialog.asksaveasfilename(filetypes=[("Excel", '*.xlsx')])

        if not path: 
            raise EmptyPath
        
        self.path_to_save = Path(path)
        self.path_to_save_label['text'] = self.path_to_save.name

        try:
            self.__validate_file(self.path_to_save, self.path_to_save_label)

        except IncorrectFileName: 
            messagebox.showerror("Неверный файл", "Файл должен иметь расширение xlsx")
        

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
            messagebox.showerror("Неверный файл", "Файл должен иметь расширение xlsx")
        

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