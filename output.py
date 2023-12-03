from network import Network
from typing import Sequence, TypeAlias, Mapping, NamedTuple, Final
from readxl import read 
from openpyxl import Workbook, worksheet
import openpyxl
from dataclasses import dataclass, field


parameter: TypeAlias = str 
sensitivity: TypeAlias = float
id: TypeAlias = int 
NetworkSequence = Sequence[Network, ]

LANG: Final = sorted('QWERTYUIOPASDFGHJKLMNBVCXZ')
NORMAL_COLOR: Final = '000000'
SELECTED_COLOR: Final = 'FFAA00'


class Cell(NamedTuple): 
    data: str | int | float 
    font: openpyxl.styles.Font = openpyxl.styles.Font(color=NORMAL_COLOR, 
                                                      bold=False, 
                                                      italic=False, 
                                                      size=12)

@dataclass
class Row: 
    parameter: str=''
    sensitivity: list[Cell, ] = field(init=False, repr=False, default_factory=list)
    count: int = 0


def __get_the_worst_param(net:Network, count:int=6) -> Mapping[parameter, sensitivity]: 
    """Фунция, возрващающая count намиенее значимых параметров в конкретной нейронной сети"""
    parameters = tuple(net.sensitivity.items())
    parameters = sorted(parameters, key=lambda x: x[1])
    return dict(parameters[:count])

def get_dict_the_worst_param(networks: NetworkSequence) -> dict[id, tuple[str,]]: 
    """Функция, возвращающая список нименее чувствительных параметров для каждый сети в списке"""
    network_dict = dict() 
    for net in networks: 
        the_worst = __get_the_worst_param(net)                                      # на выход получаем список из картежей (параметр, чувствительность)
        network_dict[net.id] = the_worst.keys()                                     # переводим в формат славаря 

    return network_dict
    
def get_sheet(networks: NetworkSequence) -> Sequence[Sequence[Cell,], ]: 
    sheet:list[Row, ] = []                                                          # иницилианизируем таблицу 
    parameters = list(networks[1].sensitivity.keys())                               # получаем список параметров 
    worst = get_dict_the_worst_param(networks)                                      # находим худшие параметры для каждой сети

    ids = sorted(map(lambda x: x.id, networks), key=int)                            # сортируем id 
    networks = sorted(networks, key=lambda x: int(x.id))                            # сортируем сети по id 
    

    header = list(map(Cell, ["Параметр", 
                             *tuple(map(lambda x: "Сеть " + str(x), ids)), 
                             "Количесво вхождений в худшие параметры"]))
    
    for param in parameters:                                                        # проходимся по параметрам 
        sheet += [__get_row(networks, param, worst)] 

    return [header] + sorted(sheet, key=lambda x: x[-1].data, reverse=True)         

def __get_row(networks:NetworkSequence, param:str, worst:dict[id, tuple[str, ...]]) -> Row: 
    """Функция, возвращающая строку таблицы"""
    row = Row(parameter=param)
    for net in networks:                                                            # проходим по всем сетям и смотрим в каких сетях этот параметр в списке худших
        if param in worst[net.id]:                                                  # Если в списке, то помечаем ячейку
            row.count += 1 
            row.sensitivity += [Cell(net.sensitivity[param], 
                                     openpyxl.styles.Font(color=SELECTED_COLOR, 
                                                          bold=False, 
                                                          italic=False, 
                                                          size=12))]
        else: 
            row.sensitivity += [Cell(net.sensitivity[param])]                       # Иначе оставляем стандартное форматирование 
                                 
    return [Cell(data=row.parameter), *row.sensitivity, Cell(data=row.count)]

def get_norm_pos(a:int) -> str: 
    """Функция перевода числа в вид столбца Excel"""
    out = ''
    while a: 
        out += LANG[((a-1)%len(LANG))]
        a = (a-1)//len(LANG)
    return out[::-1]

def write_sheet(ws: worksheet, sheet: Sequence[Sequence[Cell, ], ]) -> None: 
    column_index = 1
    row_index = 1
    for row in sheet: 
        for cell in row: 
            column = get_norm_pos(column_index)
            ws[column+str(row_index)].font = cell.font
            ws[column+str(row_index)] = cell.data
            column_index += 1 
        else:
            column_index = 1
            row_index += 1 

def create_work_book(networks: NetworkSequence, name:str='Анализ') -> Workbook: 
    wb = Workbook()
    ws = wb.active
    ws.title = name
    sheet = get_sheet(networks)
    write_sheet(ws, sheet)
    return wb 

if __name__ == "__main__": 
    nets = read('outt.xlsx')
    wb = create_work_book(nets)
    wb.save("out.xlsx")