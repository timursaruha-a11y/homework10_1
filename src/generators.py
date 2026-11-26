from typing import Any, Dict, Iterator, List


def filter_by_currency(
    transactions: List[Dict[str, Any]], currency: str
) -> Iterator[Dict[str, Any]]:
    """Фильтрует транзакции по заданной валюте (поддерживает JSON, CSV и XLSX)."""
    for transaction in transactions:
        # Вариант 1: структура из JSON
        if "operationAmount" in transaction and isinstance(
            transaction["operationAmount"], dict
        ):
            code = transaction["operationAmount"].get("currency", {}).get("code")
        # Вариант 2: структура из CSV / XLSX
        else:
            code = transaction.get("currency_code")

        if code == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """Возвращает описание каждой операции по очереди."""
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """Генерирует номера карт в формате XXXX XXXX XXXX XXXX в заданном диапазоне."""
    for number in range(start, end + 1):
        # Превращаем число в строку длиной 16 символов, заполняя нулями слева
        num_str = f"{number:016d}"
        # Разрезаем на 4 блока по 4 цифры и соединяем пробелами
        yield f"{num_str[:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:]}"
