import re

def normalize(number: str) -> str:
    if re.fullmatch(r"\d{1,3}(?:[.,]\d{3})+", number):
        return re.sub(r"[.,]", "", number)  # 1.000 or 1,000 -> 1000
    return number.replace(",", ".") # 3,5 -> 3.5

def numbers_in(text: str) -> set:
    return {normalize(n) for n in re.findall(r"\d+(?:[.,]\d+)*", text)}

def missing_numbers(source: str, summary: str) -> list:
    return sorted(numbers_in(summary) - numbers_in(source))