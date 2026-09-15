from enum import StrEnum


class Visibility(StrEnum):
    SHARED = "shared"
    PRIVATE = "private"


class TransactionType(StrEnum):
    ADD = "add"
    DEDUCT = "deduct"
    WASTE = "waste"
    ADJUST = "adjust"


class Unit(StrEnum):
    GRAM = "g"
    KILOGRAM = "kg"
    MILLILITER = "ml"
    LITER = "l"
    PIECE = "piece"
    PACK = "pack"
