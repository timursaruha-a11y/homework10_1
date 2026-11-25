import os
from typing import Any, Dict, List

from src.processing import filter_by_state, process_bank_search, sort_by_date
from src.utils import (
    read_transactions_csv,
    read_transactions_excel,
    zip_transactions_from_json,
)
from src.widget import get_date, mask_account_card


def get_currency_code(transaction: Dict[str, Any]) -> str:
    """Извлекает код валюты с учетом разной структуры JSON и CSV/XLSX."""
    if "operationAmount" in transaction and isinstance(transaction["operationAmount"], dict):
        return str(transaction["operationAmount"].get("currency", {}).get("code", ""))
    return str(transaction.get("currency_code", ""))


def get_amount_str(transaction: Dict[str, Any]) -> str:
    """Формирует строку с суммой и валютой (для RUB выводит 'руб.')."""
    if "operationAmount" in transaction and isinstance(transaction["operationAmount"], dict):
        amount = transaction["operationAmount"].get("amount", "")
        currency = transaction["operationAmount"].get("currency", {}).get("code", "")
    else:
        amount = transaction.get("amount", "")
        currency = transaction.get("currency_code", "")

    try:
        num_amount = float(amount)
        if num_amount.is_integer():
            amount = int(num_amount)
    except (ValueError, TypeError):
        pass

    currency_label = "руб." if currency == "RUB" else currency
    return f"Сумма: {amount} {currency_label}"


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует одну транзакцию для вывода в консоль."""
    raw_date = str(transaction.get("date", "")).strip()
    formatted_date = get_date(raw_date) if raw_date else ""
    description = str(transaction.get("description", "")).strip()

    from_raw = str(transaction.get("from", "")).strip()
    to_raw = str(transaction.get("to", "")).strip()

    from_str = mask_account_card(from_raw) if from_raw else ""
    to_str = mask_account_card(to_raw) if to_raw else ""

    if from_str and to_str:
        transfer_line = f"{from_str} -> {to_str}"
    else:
        transfer_line = to_str or from_str

    amount_line = get_amount_str(transaction)

    return f"{formatted_date} {description}\n{transfer_line}\n{amount_line}"


def main() -> None:
    """Основная функция запуска и взаимодействия с пользователем."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    data: List[Dict[str, Any]] = []
    while True:
        choice = input().strip()
        if choice == "1":
            print("Для обработки выбран JSON-файла.")
            data = zip_transactions_from_json(os.path.join("data", "operations.json"))
            break
        elif choice == "2":
            print("Для обработки выбран CSV-файла.")
            data = read_transactions_csv(os.path.join("data", "transactions.csv"))
            break
        elif choice == "3":
            print("Для обработки выбран XLSX-файла.")
            data = read_transactions_excel(os.path.join("data", "transactions_excel.xlsx"))
            break
        else:
            print("Некорректный выбор. Пожалуйста, введите 1, 2 или 3.")

    # Фильтрация по статусу
    valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}
    while True:
        print(
            "Введите статус, по которому необходимо выполнить фильтрацию. "
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
        )
        status_input = input().strip()
        if status_input.upper() in valid_statuses:
            status = status_input.upper()
            print(f'Операции отфильтрованы по статусу "{status}"')
            data = filter_by_state(data, status)
            break
        else:
            print(f'Статус операции "{status_input}" недоступен.')

    # Сортировка по дате
    print("Отсортировать операции по дате? Да/Нет")
    if input().strip().lower() == "да":
        print("Отсортировать по возрастанию или по убыванию?")
        order = input().strip().lower()
        is_descending = order == "по убыванию"
        data = sort_by_date(data, reverse=is_descending)

    # Фильтрация по рублевым транзакциям
    print("Выводить только рублевые транзакции? Да/Нет")
    if input().strip().lower() == "да":
        data = [tx for tx in data if get_currency_code(tx) == "RUB"]

    # Поиск по слову в описании
    print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    if input().strip().lower() == "да":
        print("Введите слово для поиска:")
        search_word = input().strip()
        data = process_bank_search(data, search_word)

    # Вывод результата
    print("Распечатываю итоговый список транзакций...")
    if not data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(data)}\n")
        for transaction in data:
            print(format_transaction(transaction))
            print()


if __name__ == "__main__":
    main()
