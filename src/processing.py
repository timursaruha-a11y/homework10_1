import re
from collections import Counter
from typing import Any, Dict, List


def filter_by_state(
    data: List[Dict[str, Any]], state: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """Фильтрует список словарей по значению ключа 'state'."""
    filtered_data = [item for item in data if item.get("state") == state]
    return filtered_data


def sort_by_date(
    data: List[Dict[str, Any]], reverse: bool = True
) -> List[Dict[str, Any]]:
    """Сортирует список словарей по ключу 'date'.

    По умолчанию сортировка идет от самых свежих к самым старым (по убыванию).
    """
    sorted_data = sorted(data, key=lambda item: item.get("date", ""), reverse=reverse)
    return sorted_data


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """Фильтрует список банковских операций по наличию строки поиска в описании."""
    if not search:
        return data

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [
        item
        for item in data
        if item.get("description") and pattern.search(str(item["description"]))
    ]


def process_bank_operations(
    data: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    """Подсчитывает количество операций по заданным категориям в поле 'description'."""
    category_counts: Counter[str] = Counter()
    patterns = {cat: re.compile(re.escape(cat), re.IGNORECASE) for cat in categories}

    for item in data:
        description = str(item.get("description", ""))
        for cat, pattern in patterns.items():
            if pattern.search(description):
                category_counts[cat] += 1

    return {cat: category_counts[cat] for cat in categories}
