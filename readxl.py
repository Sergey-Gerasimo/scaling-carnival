from openpyxl import load_workbook, Workbook, worksheet
from dataclasses import dataclass, field
from typing import Sequence, TypeAlias, Mapping
from network import Network
from exceptions import IncorrectFile

id: TypeAlias = int 


def read(filename:str) ->  Sequence[Network, ]:  
    """Функция четения данных их файла Excel"""
    workbook = load_workbook(filename)
    networks = dict()   
    if len(workbook.sheetnames) < 2: 
        raise IncorrectFile

    networks = get_networks_sesensitivity(workbook[workbook.sheetnames[0]], networks)
    get_networks_config(workbook[workbook.sheetnames[1]], networks)

    return list(networks.values())
    

def get_networks_config(ws: worksheet, networks: Mapping[id, Network]) -> Mapping[id, Network]:
    """Функция сбора информации о сетях из файла xlsx"""
    rows = tuple(ws.values)[1:]
    for row in map(tuple, rows):
        id, arhitecture, training_performance, validate_performance,  test_performance, training_erro, validate_error, \
             test_error, learning_alghoritm, error_function, activate1, activate2 = row
        
        network = networks[id]
        network.architecture = arhitecture
        network.training_performance = training_performance
        network.validate_performance = validate_performance
        network.test_performance = test_performance
        network.training_error = training_erro
        network.validate_error = validate_error
        network.test_error = test_error
        network.learning_alghoritm = learning_alghoritm
        network.error_function = error_function
        network.activate1 = activate1
        network.activate2 = activate2

    return networks


def get_networks_sesensitivity(ws: worksheet, networks) -> Mapping[id, Network]: 
    """Функция для чтения анализа чувствительности из файла xlsx"""
    parameters: tuple[str, ] | None = None
    for row in list(map(list, ws.values)): 
        if parameters is None: 
            parameters = row[1:]
            print(*parameters, file=open("out.txt", 'w'), sep='\n')
            print(len(parameters))
            continue

        if len(row[0].split('.')) == 2: 
            id, architecture, _ = *row[0].split('.'), ()
            sensitivity = tuple(zip(parameters, row[1:]))
            networks[int(id)] = Network(id, architecture, sensitivity)
            
    
    return networks 


if __name__ == "__main__": 
    networks = read('outt.xlsx')
    print(len(networks))