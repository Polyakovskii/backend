import enum


class TransactionTypeEnum(enum.IntEnum):
    purchase = 1
    sale = 2

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)


class OrderTypeEnum(enum.IntEnum):
    market = 1
    limit = 2
    stop_loss = 3

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)
