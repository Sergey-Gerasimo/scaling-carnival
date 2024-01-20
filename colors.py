from typing import TypeAlias
from enum import Enum, auto
from copy import deepcopy
from typing import Generator

Red: TypeAlias = int 
Green: TypeAlias = int 
Blue: TypeAlias = int 


class ChenalType(Enum):
    RED = 'R'
    BLUE = 'G'
    GREEN = 'B'


class Chenal:
    def __init__(self, chanalType: ChenalType):
        self.type = chanalType

    def _validate(self, value):
        if value < 0 or value > 255:
            raise TypeError(f'{value} not between 0 and 255')
        
        if not isinstance(value, int):
            raise TypeError(f'{self.type} chanal must be integer')

    def __set__(self, instance, value: int):
        self._validate(value)

        match self.type:
            case ChenalType.RED:
                instance._color = value, instance._color[1], instance._color[2]
            
            case ChenalType.GREEN:
                instance._color = instance._color[0], value, instance._color[2]

            case ChenalType.BLUE:
                instance._color = instance._color[0], instance._color[1], value

            case _:
                raise TypeError('Unavalibal type chanal {self.type}')
            
    def __get__(self, instance, owner):
        match self.type:
            case ChenalType.RED:
                return instance._color[0]
            
            case ChenalType.GREEN:
                return instance._color[1]

            case ChenalType.BLUE:
                return instance._color[2]

            case _:
                raise TypeError('Unavalibal type chanal {self.type}')


class Color: 
    R = Chenal(ChenalType.RED)
    G = Chenal(ChenalType.GREEN)
    B = Chenal(ChenalType.BLUE)

    def __init__(self, _color: tuple[Red, Green, Blue] = (0, 0, 0)): 
        self._color = _color

    @staticmethod
    def fromHex(color: str):
        if not isinstance(color, str): 
            raise TypeError(f'{type(color)} != str')
        
        r = int(color[:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:], 16)
        return Color((r, g, b))
    
    def __repr__(self):
        return f'R: {self.R}, G: {self.G}, B: {self.B}'

    @staticmethod
    def fromTuple(color: tuple[Red, Green, Blue]):
        if not isinstance(color, tuple):
            raise TypeError(f'{type(color)} != tuple')
        
        return Color(color)
    
    @staticmethod
    def _getnorm(value: str):
        return '0'*(2-len(value)) + value

    @property
    def Hex(self):
        return f'{self._getnorm(hex((self.R))[2:])}{self._getnorm(hex(self.G)[2:])}{self._getnorm(hex(self.B)[2:])}'

def Gradient2(color1: str | Color = "FF0000", color2: str | Color = "0000FF", count: int = 100) -> Generator[Color, None, None]:
    if not isinstance(color1, Color):
        color1 = Color.fromHex(color1)

    if not isinstance(color2, Color):
        color2 = Color.fromHex(color2)  

    color3 = Color.fromHex('000000')

    for i in range(count):
        color3.R = int(color1.R * (i/count) + color2.R * (1 - i/count))
        color3.G = int(color1.G * (i/count) + color2.G * (1 - i/count))
        color3.B = int(color1.B * (i/count) + color2.B * (1 - i/count))

        yield deepcopy(color3)

def Gradient(*args: str | Color, count: int = 100) -> Generator[Color, None, None]:
    if all(map(lambda item: isinstance(item, str), args)):
        args = [Color.fromHex(item) for item in args]

    for color_id in range(len(args)-1):
        for color in Gradient2(args[color_id], args[color_id+1], count=count):
            yield color 

