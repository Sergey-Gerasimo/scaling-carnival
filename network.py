from dataclasses import dataclass, field
from typing import Any

@dataclass
class Network: 
    id: int = field(compare=False)                                             # id сети 
    architecture:str = field(compare=False)                                    # архитектура сети
    sensitivity: dict = field(default_factory=dict, compare=False, repr=False)                      # кортеж чувтвительности параметров сети 

    training_performance: float = field(init=False, compare=False, repr=False) # корреляция на обучающей выборке
    validate_performance: float = field(init=False, compare=False, repr=False) # корреляция на тестовой выборке 
    test_performance: float = field(init=False, compare=False, repr=False)     # корреляция на контрольной выборке

    training_error: float = field(init=False, compare=False, repr=False)       # ошибка на обучающей выборке 
    validate_error: float = field(init=False, compare=False, repr=False)       # ошибка на тестовой выборке
    test_error: float = field(init=False, compare=False, repr=False)           # ошибка на контрольной выборке

    learning_alghoritm:str = field(init=False)                                 # алгоритм обучения 
    error_function: str = field(init=False)                                    # функция ошибки 

    activate1:str = field(init=False)                                          # функция активации на 1 слое сети 
    activate2:str = field(init=False)                                          # функция активации на 2 слое сети

 