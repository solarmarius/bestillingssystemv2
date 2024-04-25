from enum import Enum

BILER = (771, 772, 780, 781, 790, 791, 792)


class Mode(Enum):
    DEFAULT = 0
    DISPLAY_FPAKK = 1


class Operation(Enum):
    BESTILLING = 1
    OVERFORING = 2
    PERSONAL = 3
    VRAKORDRE = 4
    VARETELLING = 5


"""
TODO:
Lage seperat innlogg for ulike depoter, og hver sin depot har hver sine biler
"""


class Depot(Enum):
    TROMSO = (790, 791, 792)
    HARSTAD = (771, 772)
    BODO = (780, 781)
