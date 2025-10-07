from fractions import Fraction

# словарь от 0 до 19

dict_of_numbers = {
    "ноль": "0",
    "один": "1",
    "одна": "1",
    "два": "2",
    "две": "2",
    "три": "3",
    "четыре": "4",
    "пять": "5",
    "шесть": "6",
    "семь": "7",
    "восемь": "8",
    "девять": "9",
    "десять": "10",
    "одиннадцать": "11",
    "двенадцать": "12",
    "тринадцать": "13",
    "четырнадцать": "14",
    "пятнадцать": "15",
    "шестнадцать": "16",
    "семнадцать": "17",
    "восемнадцать": "18",
    "девятнадцать": "19"
}

# словарь десятков

dict_of_big_numbers = {
    "двадцать": "20",
    "тридцать": "30",
    "сорок": "40",
    "пятьдесят": "50",
    "шестьдесят": "60",
    "семьдесят": "70",
    "восемьдесят": "80",
    "девяносто": "90"
}

# словарь операций

dict_of_operations = {
    "плюс": "+",
    "минус": "-",
    "разделить_на": "/",
    "умножить_на": "*",
    "остаток_от_деления": "%"
}

# словарь десятичных долей

fraction_units = {
    "десятая": 1,
    "десятых": 1,
    "сотая": 2,
    "сотых": 2,
    "тысячная": 3,
    "тысячных": 3,
    "десятитысячная": 4, "десятитысячных": 4,
    "стотысячная": 5, "стотысячных": 5,
    "миллионная": 6, "миллионных": 6
}

# словарь скобок

brackets = {
    "скобкаоткрывается": "(",
    "скобказакрывается": ")"
} 

# сливаем все вместе и считаем в конце

def calc(string: str) -> int:
    string = string.replace(" на", "_на").replace("скобка ", "скобка")
    list_string_numbers = string.split()
    i = 0
    while i < len(list_string_numbers):
        token = list_string_numbers[i]
        if token in fraction_units:
            j = i
            while j > 0 and list_string_numbers[j-1] not in dict_of_operations:
                j -= 1
            frac_part = " ".join(list_string_numbers[j:i+1])
            decimal_number = words_to_decimal(frac_part)
            list_string_numbers = list_string_numbers[:j] + [str(decimal_number)] + list_string_numbers[i+1:]
            i = j
        i += 1

    string_end = ""
    for index, element in enumerate(list_string_numbers):
        if index > 0 and list_string_numbers[index - 1] == 'разделить_на' and element == 'ноль':
            return "Деление на ноль"

        if element in dict_of_numbers:
            string_end += dict_of_numbers[element]
        elif element in dict_of_operations:
            string_end += dict_of_operations[element]
        elif element in brackets:
            string_end += brackets[element]
        elif element in dict_of_big_numbers:
            if index + 1 < len(list_string_numbers) and list_string_numbers[index + 1] in dict_of_numbers:
                string_end += "(" + dict_of_big_numbers[element] + "+" + dict_of_numbers[list_string_numbers[index + 1]] + ")"
                list_string_numbers[index + 1] = ""
            else:
                string_end += dict_of_big_numbers[element]
        else:
            string_end += element

    result = eval(string_end)
    frac_result = Fraction(result).limit_denominator(10**6)
    
    if abs(result) > 100:
        return "Число больше ста"
    return fraction_to_words(frac_result)

# парсим десятичные числа

def fraction_to_words(frac: Fraction) -> str:
    integer_part = frac.numerator // frac.denominator
    remainder = frac.numerator % frac.denominator

    if remainder == 0:
        return convert_to_str(integer_part)

    decimals = []
    seen = {}
    pos = 0
    period_start = None

    while remainder and pos < 20:
        if remainder in seen:
            period_start = seen[remainder]
            break
        seen[remainder] = pos
        remainder *= 10
        decimals.append(str(remainder // frac.denominator))
        remainder %= frac.denominator
        pos += 1

    if period_start is not None:
        non_periodic = "".join(decimals[:period_start])
        periodic = "".join(decimals[period_start:period_start+4])
    else:
        non_periodic = "".join(decimals)
        periodic = ""

    res_parts = []
    res_parts.append(convert_to_str(integer_part))

    if non_periodic:
        res_parts.append("и " + convert_to_str(int(non_periodic)) + " " + unit_for_len(len(non_periodic)))
    if periodic:
        res_parts.append("и " + convert_to_str(int(periodic)) + " в периоде")

    return " ".join(res_parts)

def unit_for_len(n: int) -> str:
    if n == 1: return "десятых"
    if n == 2: return "сотых"
    if n == 3: return "тысячных"
    if n == 4: return "десятитысячных"
    if n == 5: return "стотысячных"
    if n == 6: return "миллионных"
    return "дробь"

# формируем десятичные числа

def words_to_decimal(s: str):
    s = s.lower()
    parts = s.split(" и ")
    integer_part = words_to_int(parts[0])

    if len(parts) == 1:
        return float(integer_part)

    fraction_words = parts[1].strip().split()
    number = words_to_int(" ".join(fraction_words[:-1]))
    unit = fraction_units[fraction_words[-1]]
    fraction_str = str(number).zfill(unit)
    return float(f"{integer_part}.{fraction_str}")

# формируем числа

def words_to_int(s: str) -> int:
    tokens = s.split()
    string_end = ""
    for index, element in enumerate(tokens):
        if element in dict_of_numbers:
            string_end += dict_of_numbers[element]
        elif element in dict_of_big_numbers:
            if index + 1 < len(tokens) and tokens[index + 1] in dict_of_numbers:
                string_end += "(" + dict_of_big_numbers[element] + "+" + dict_of_numbers[tokens[index + 1]] + ")"
                tokens[index + 1] = ""
            else:
                string_end += dict_of_big_numbers[element]
    return eval(string_end)

# конвертируем в строку

def convert_to_str(number): 
    number = round(number, 3)

    if abs(number - round(number)) < 1e-6:
        number = int(round(number))

    if number < 0:
        return "минус " + convert_to_str(abs(number))

    if isinstance(number, float) and number % 1 != 0:
        integer_part = int(number)
        fraction_str = str(number).split(".")[1]
        fraction_str = fraction_str.rstrip('0')
        fraction_number = int(fraction_str)

        if len(fraction_str) == 1:
            unit_word = "десятая" if fraction_number == 1 else "десятых"
        elif len(fraction_str) == 2:
            unit_word = "сотая" if fraction_number == 1 else "сотых"
        else:
            unit_word = "тысячная" if fraction_number == 1 else "тысячных"

        integer_words = "" if integer_part == 0 else convert_to_str(integer_part)
        fraction_words = convert_to_str(fraction_number)

        return f"{integer_words} и {fraction_words} {unit_word}" if integer_words else f"{fraction_words} {unit_word}"

    number = int(number)
    if number < 20:
        return [k for k,v in dict_of_numbers.items() if v == str(number)][0]
    else:
        tens, ones = divmod(number, 10)
        tens_word = next(k for k,v in dict_of_big_numbers.items() if v == str(tens*10))
        return tens_word if ones == 0 else f"{tens_word} {convert_to_str(ones)}"

print(calc(str(input())))