from readxl import read
from output import create_work_book
import argparse
import os, sys
from typing import final 

def main() -> None:
    CWD: final = os.getcwd()                            # текущая директория

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Путь до файла xlsx')
    parser.add_argument('-s', '--store', help='Включает сохранение сетей в БД', action="store_true")
    args = parser.parse_args()

    if args.file is None: 
        file = input("введите путь до файла: ")
    else: 
        file = args.file 

    file = os.path.normpath(file)

    if args.store: 
        print("Сохранение в БД еще в разработке")

    if not os.path.exists(file): 
        print(f"Файл {file} не существут или указан неверный путь", file=sys.stderr())
        exit(1)


    nets = read(file)                                     # собираем данные из файла 
    wb = create_work_book(nets)                           # формируем новый файл 
    wb.save('out.xlsx')                                   # сохраняем новый файл 
    


if __name__ == "__main__":
    main()
