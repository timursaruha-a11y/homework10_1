from src.masks import get_mask_account as account
from src.masks import get_mask_card_number as card


def mask_account_card(data_of_card: str) -> str:
    """Принимает номер карты или номер счета и возвращает его под маской."""
    parts = data_of_card.split()
    number = parts[-1]
    name = " ".join(parts[:-1])

    if name.lower() == "счет":
        return f"{name} {account(number)}"
    else:
        return f"{name} {card(number)}"


def get_date(string_whith_data: str) -> str:
    """Изменяет формат даты."""
    return ".".join(string_whith_data.split("T")[0].split("-")[::-1])
