import logging
import os
from typing import Union

# Получаем путь к корню проекта и создаем папку logs
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# Создаем логер для модуля masks
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

# Защита от дублирования обработчиков при повторном импорте
if not logger.handlers:
    log_file = os.path.join(LOGS_DIR, "masks.log")
    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


def get_mask_card_number(number_card: Union[int, str]) -> str:
    """Функция получает на входе номер карты,
    возвращает строковое значение где цифры разбиты в группы по 4 и все
    кроме первых 6-ти и последних 4-х цифрах карты заменены на *"""
    logger.info(f"Начало маскирования номера карты: {number_card}")
    number_str = str(number_card).replace(" ", "")

    if len(number_str) != 16 or not number_str.isdigit():
        logger.error(f"Некорректный номер карты: {number_card}")
        return ""

    mask_card = []
    number_card_asterix = ""
    for number in number_str:
        if (
            len(number_card_asterix) < 6
            or len(number_card_asterix) > len(number_str) - 5
        ):
            number_card_asterix += number
        else:
            number_card_asterix += "*"

    start_index_of_interval = 0
    for index in range(4, len(number_card_asterix) + 1, 4):
        mask_card.append(number_card_asterix[start_index_of_interval:index])
        start_index_of_interval = index

    result = " ".join(mask_card)
    logger.info(f"Номер карты успешно замаскирован: {result}")
    return result


def get_mask_account(accaut_number: Union[int, str]) -> str:
    """Функция получает на входе номер счета и
    возвращает ** и последние 4 цифры счета"""
    logger.info(f"Начало маскирования номера счета: {accaut_number}")
    acc_str = str(accaut_number).replace(" ", "")

    if len(acc_str) < 4 or not acc_str.isdigit():
        logger.error(f"Некорректный номер счета: {accaut_number}")
        return ""

    result = "**" + acc_str[-4:]
    logger.info(f"Номер счета успешно замаскирован: {result}")
    return result
