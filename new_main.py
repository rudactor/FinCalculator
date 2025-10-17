from fractions import Fraction
import re
from math import pi, sin, cos, tan, factorial

# словарь от 0 до 19

dict_of_numbers = {
    "ноль": "0",
    "один": "1", "одна": "1", "одно": "1", "одним": "1", "одной": "1", "одного": "1", "одному": "1", "одним": "1", "одном": "1", "одной": "1",
    "два": "2", "две": "2", "двумя": "2", "двух": "2",
    "три": "3", "трем": "3", "тремя": "3", "трёх": "3", "трех": "3",
    "четыре": "4", "четырем": "4", "четырьмя": "4", "четырёх": "4",
    "пять": "5", "пяти": "5", "пятью": "5",
    "шесть": "6", "шести": "6", "шестью": "6",
    "семь": "7", "семи": "7", "семью": "7",
    "восемь": "8", "восьми": "8", "восьмью": "8",
    "девять": "9", "девяти": "9", "девятью": "9",
    "десять": "10", "десяти": "10", "десятью": "10",
    "одиннадцать": "11", "двенадцать": "12", "тринадцать": "13", "четырнадцать": "14",
    "пятнадцать": "15", "шестнадцать": "16", "семнадцать": "17", "восемнадцать": "18",
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

hundreds_map = {
    "сто": 100, "двести": 200, "триста": 300, "четыреста": 400,
    "пятьсот": 500, "шестьсот": 600, "семьсот": 700,
    "восемьсот": 800, "девятьсот": 900
}


# словарь операций

dict_of_operations = {
    "плюс": "+",
    "минус": "-",
    "разделить_на": "/",
    "умножить_на": "*",
    "остаток_от_деления": "%",
    "в_степени": "**",
    "синус_от": "sin",
    "косинус_от": "cos",
    "тангенс_от": "tan"
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

trigometric = {
    "пи": "pi"
}

word_map = {
        "вторых": 2, "третьих": 3, "четвёртых": 4, "четвертых": 4,
        "пятых": 5, "шестых": 6, "седьмых": 7, "восьмых": 8,
        "девятых": 9, "десятых": 10, "одиннадцатых": 11, "двенадцатых": 12,
        "тринадцатых": 13, "четырнадцатых": 14, "пятнадцатых": 15,
        "шестнадцатых": 16, "семнадцатых": 17, "восемнадцатых": 18, "девятнадцатых": 19,
        "двадцатых": 20, "тридцатых": 30, "сороковых": 40
    }

words_to_denominators = {
    "вторая": 2,
    "третья": 3, "третьи": 3, "треть": 3, "третьих": 3,
    "четвертая": 4, "четвертые": 4, "четверть": 4,
    "пятая": 5, "пятые": 5, "пятых": 5,
    "шестая": 6, "шестые": 6, "шестых": 6,
    "седьмая": 7, "седьмые": 7, "седьмых": 7,
    "восьмая": 8, "восьмые": 8,
    "девятая": 9, "девятые": 9,
    "десятая": 10, "десятые": 10
}

numbers_to_words = {v: k for k, v in dict_of_numbers.items()}
denominators_to_words = {v: k for k, v in words_to_denominators.items()}

def parse_fraction_words(s: str) -> Fraction:
    s = s.lower().strip()
    
    # Цифровая дробь: "9/5"
    if re.match(r'^\d+/\d+$', s):
        numerator, denominator = map(int, s.split("/"))
        return Fraction(numerator, denominator)
    
    # Целое число цифрой
    if s.isdigit():
        return Fraction(int(s), 1)
    
    tokens = s.split()
    
    # Дробь с целой частью: "один и четыре пятых"
    if "и" in tokens:
        idx = tokens.index("и")
        whole_words = tokens[:idx]
        frac_words = tokens[idx+1:]
        
        # Целая часть
        whole = sum(int(dict_of_numbers.get(w, 0)) for w in whole_words)
        
        # Дробная часть
        if len(frac_words) != 2:
            raise ValueError(f"Неверный формат дробной части: {' '.join(frac_words)}")
        numerator_word, denominator_word = frac_words
        numerator = int(dict_of_numbers.get(numerator_word, 0))
        denominator = words_to_denominators.get(denominator_word)
        if denominator is None:
            raise ValueError(f"Неизвестный знаменатель: {denominator_word}")
        return Fraction(whole * denominator + numerator, denominator)
    
    # Простая дробь без целой части: "шесть седьмых"
    if len(tokens) == 2:
        numerator = int(dict_of_numbers.get(tokens[0], 0))
        denominator = words_to_denominators.get(tokens[1])
        if denominator is None:
            raise ValueError(f"Неизвестный знаменатель: {tokens[1]}")
        return Fraction(numerator, denominator)
    
    # Целое число словами: "три"
    if len(tokens) == 1 and tokens[0] in dict_of_numbers:
        return Fraction(int(dict_of_numbers[tokens[0]]), 1)
    
    raise ValueError(f"Не удалось распознать дробь: {s}")

trig_functions = {
    "синус_от": sin,
    "косинус_от": cos,
    "тангенс_от": tan
}

trig_constants = {
    "пи": "pi"
}

# словарь скобок

brackets = {
    "скобка_открывается": "(",
    "скобка_закрывается": ")"
} 

def fraction_to_words_drobs(frac: Fraction) -> str:
    frac = frac.limit_denominator()
    whole = frac.numerator // frac.denominator
    numerator = frac.numerator % frac.denominator
    denominator = frac.denominator

    parts = []

    # --- целая часть ---
    if whole > 0:
        parts.append(convert_to_str(whole))

    # --- дробная часть ---
    if numerator > 0:
        # числитель
        if numerator == 1:
            numerator_word = "одна"
        elif numerator == 2:
            numerator_word = "две"
        else:
            numerator_word = convert_to_str(numerator)

        # знаменатель
        denom_word = convert_to_str(denominator)
        # корректная морфология
        if numerator == 1:
            if denom_word.endswith("ь"):
                denom_word = denom_word[:-1] + "ая"
            elif denom_word.endswith("и"):
                denom_word = denom_word[:-1] + "ая"
            elif denom_word.endswith("е"):
                denom_word = denom_word[:-1] + "ая"
            else:
                denom_word += "я"
        else:
            if denom_word.endswith("я"):
                denom_word = denom_word[:-1] + "их"
            elif denom_word.endswith("е"):
                denom_word = denom_word[:-1] + "ых"
            elif denom_word.endswith("а"):
                denom_word = denom_word[:-1] + "ых"
            else:
                denom_word += "ых"

        frac_part = f"{numerator_word} {denom_word}"
        if whole > 0:
            parts.append("и " + frac_part)
        else:
            parts.append(frac_part)

    if not parts:
        return "ноль"

    return " ".join(parts)


def operate_fractions(frac1_words: str, operator: str, frac2_words: str) -> str:
    f1 = parse_fraction_words(frac1_words)
    f2 = parse_fraction_words(frac2_words)
    
    if operator == "плюс":
        result = f1 + f2
    elif operator == "минус":
        result = f1 - f2
    elif operator == "умножить_на":
        result = f1 * f2
    elif operator == "разделить_на":
        if f2 == 0:
            raise ZeroDivisionError("Деление на ноль")
        result = f1 / f2
    else:
        raise ValueError(f"Неподдерживаемая операция: {operator}")
    
    return fraction_to_words_drobs(result)

# сливаем все вместе и считаем в конце

def combinatorial_calc(tokens):
    # Размещения: A(n, k) = n! / (n-k)!
    if "размещений" in tokens:
        i = tokens.index("из")
        n = words_to_int(tokens[i+1])
        k = words_to_int(tokens[i+3])
        if k > n:
            return 0
        return factorial(n) // factorial(n - k)
    # Сочетания: C(n, k) = n! / (k! * (n-k)!)
    elif "сочетаний" in tokens:
        i = tokens.index("из")
        n = words_to_int(tokens[i+1])
        k = words_to_int(tokens[i+3])
        if k > n:
            return 0
        return factorial(n) // (factorial(k) * factorial(n - k))
    # Перестановки: P(n) = n!
    elif "перестановок" in tokens:
        i = tokens.index("из")
        n = words_to_int(tokens[i+1])
        return factorial(n)
    return None

def is_plain_fraction(s: str) -> bool:
    tokens_s = s.lower().split()
    if not tokens_s:
        return False
    if len(tokens_s) == 1:
        return tokens_s[0] in dict_of_numbers
    if "и" in tokens_s:
        idx = tokens_s.index("и")
        frac_words = tokens_s[idx+1:]
        return len(frac_words) == 2 and frac_words[0] in dict_of_numbers and frac_words[1] in words_to_denominators
    if len(tokens_s) == 2:
        return tokens_s[0] in dict_of_numbers and tokens_s[1] in words_to_denominators
    return False

def calc(string: str) -> str:
    string = string.replace(" на", "_на").replace("скобка ", "скобка_").replace("в степени", "в_степени")\
                   .replace("синус от", "синус_от").replace("косинус от", "косинус_от")\
                   .replace("тангенс от", "тангенс_от")
    
    tokens = string.lower().split()
    
    for i, token in enumerate(tokens):
        if token in ["плюс", "минус", "умножить_на", "разделить_на"]:
            frac1_words = " ".join(tokens[:i])
            operator = token
            frac2_words = " ".join(tokens[i+1:])
            
            if is_plain_fraction(frac1_words) and is_plain_fraction(frac2_words):
                validate_fraction_words(frac1_words)
                validate_fraction_words(frac2_words)
                return operate_fractions(frac1_words, operator, frac2_words)
            else:
                continue
    
    tokens = string.split()
    
    validate_number_words(tokens)
    string_end = ""
    i = 0
    
    comb_result = combinatorial_calc(tokens)
    if comb_result is not None:
        return convert_to_str(comb_result)
    
    while i < len(tokens):
        token = tokens[i]

        if token in brackets:
            string_end += brackets[token]

        elif token in trig_functions:
            func = trig_functions[token] 
            arg_tokens = []
            i += 1
            while i < len(tokens):
                t = tokens[i]
                if t in dict_of_numbers:
                    arg_tokens.append(dict_of_numbers[t])
                elif t in dict_of_big_numbers:
                    arg_tokens.append(dict_of_big_numbers[t])
                elif t in dict_of_operations:
                    arg_tokens.append(dict_of_operations[t])
                elif t in trig_constants:
                    arg_tokens.append(str(trig_constants[t]))
                else:
                    arg_tokens.append(str(pi))
                i += 1
            # Вычисляем аргумент и функцию
            arg_value = safe_eval("".join(arg_tokens))
            value = func(arg_value)
            value = round(value, 3)
            frac_value = Fraction(value).limit_denominator(10**6)
            return fraction_to_words(frac_value)

        elif token in dict_of_numbers or token in dict_of_big_numbers:
            num_words = [token]
            j = i + 1
            while j < len(tokens) and tokens[j] not in dict_of_operations and tokens[j] not in brackets:
                num_words.append(tokens[j])
                j += 1
            string_end += str(words_to_decimal(" ".join(num_words)))
            i = j - 1
        # --- операции ---
        elif token in dict_of_operations:
            string_end += dict_of_operations[token]

        elif token in dict_of_numbers:
            string_end += dict_of_numbers[token]
        elif token in dict_of_big_numbers:
            if i + 1 < len(tokens) and tokens[i+1] in dict_of_numbers:
                string_end += f"({dict_of_big_numbers[token]}+{dict_of_numbers[tokens[i+1]]})"
                tokens[i+1] = ""
            else:
                string_end += dict_of_big_numbers[token]
        else:
            string_end += token

        i += 1

    # --- Вычисление обычного выражения ---
    print(string_end)
    validate_expression_sequence(string_end)
    result = safe_eval(string_end)
    frac_result = Fraction(result).limit_denominator(10**6)
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
        non_periodic_int = int(non_periodic) if non_periodic else 0
        res_parts.append(
            "и " + convert_to_str(non_periodic_int) + " " + unit_for_len(len(non_periodic))
        )
    if periodic:
        # каждая цифра в словах
        periodic_words = [convert_to_str(int(d)) for d in periodic]
        periodic_str = " ".join(periodic_words)
        res_parts.append(f"и {periodic_str} в периоде")

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
    total = 0
    temp = 0
    for token in tokens:
        if token in dict_of_numbers:
            temp += int(dict_of_numbers[token])
        elif token in dict_of_big_numbers:
            temp += int(dict_of_big_numbers[token])
    total += temp
    return total

# конвертируем в строку

def convert_to_str(number): 
    number = round(number, 3)

    if abs(number - round(number)) < 1e-6:
        number = int(round(number))

    if number < 0:
        return "минус " + convert_to_str(abs(number))

    # Дробные числа
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

    # Числа < 20
    if number < 20:
        return [k for k,v in dict_of_numbers.items() if v == str(number)][0]

    # Числа < 100
    elif number < 100:
        tens, ones = divmod(number, 10)
        tens_word = next((k for k,v in dict_of_big_numbers.items() if int(v) == tens*10), "")
        return tens_word if ones == 0 else f"{tens_word} {convert_to_str(ones)}"

    # Числа >= 100 и < 1000
    elif number < 1000:
        hundreds, remainder = divmod(number, 100)
        hundreds_word = {1:"сто", 2:"двести",3:"триста",4:"четыреста",5:"пятьсот",
                         6:"шестьсот",7:"семьсот",8:"восемьсот",9:"девятьсот"}[hundreds]
        if remainder == 0:
            return hundreds_word
        else:
            return f"{hundreds_word} {convert_to_str(remainder)}"

    # Числа >= 1000 оставляем как цифры (можно расширить на тысячи)
    else:
        return str(number)

# валидация

def validate_number_words(tokens):
    tokens = list(" ".join(tokens).replace("размещений из", "размещенийиз").replace("сочетанийиз", "сочетаний из").replace("перестановок из", "перестановокиз").split())
    for token in tokens:
        if token not in dict_of_numbers and token not in dict_of_big_numbers and \
            token not in hundreds_map and token not in dict_of_operations and \
            token not in fraction_units and token not in trigometric and \
            token not in word_map and token not in trig_functions and \
            token not in trig_constants and token != 'и' and token not in brackets and\
            token not in ['размещенийиз', 'сочетанийиз', 'перестановокиз'] and token != 'по' and\
            token not in words_to_denominators:
                raise ValueError(f"Неправильная запись числа: {token}")
        

def validate_expression_sequence(expr: str):
    prev_type = None  # "number", "operator", "open_bracket", "close_bracket"
    stack = []
    tokens = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c.isdigit() or c == '.':
            num = c
            i += 1
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                num += expr[i]
                i += 1
            tokens.append(num)
            prev_type = "number"
            continue
        elif c in "+-":
            # разрешаем двойные знаки ++, --, +-,-+
            op = c
            if i + 1 < len(expr) and expr[i+1] in "+-":
                op += expr[i+1]
                i += 1
            if prev_type not in ("number", "close_bracket", None):
                raise ValueError(f"Неправильная последовательность операторов: '{op}'")
            tokens.append(op)
            prev_type = "operator"
        elif c in "*/%":
            if prev_type not in ("number", "close_bracket"):
                raise ValueError(f"Оператор '{c}' должен идти после числа или закрывающей скобки")
            if c == "*" and i + 1 < len(expr) and expr[i+1] == "*":
                tokens.append("**")
                i += 1
            else:
                tokens.append(c)
            prev_type = "operator"
        elif c == "(":
            if prev_type in ("number", "close_bracket"):
                raise ValueError("Открывающая скобка не может идти после числа или закрывающей скобки")
            tokens.append(c)
            stack.append(c)
            prev_type = "open_bracket"
        elif c == ")":
            if prev_type in ("operator", None):
                raise ValueError("Закрывающая скобка не может идти после оператора или в начале")
            if not stack:
                raise ValueError("Лишняя закрывающая скобка")
            tokens.append(c)
            stack.pop()
            prev_type = "close_bracket"
        i += 1
    if stack:
        raise ValueError("Лишняя открывающая скобка")

def validate_fraction_words(s: str):
    """Проверяет, что дробь корректна и может быть распознана."""
    s = s.lower().strip()
    tokens = s.split()

    if not tokens:
        raise ValueError("Пустая дробь недопустима")

    # Цифровая дробь: "9/5"
    if re.match(r'^\d+/\d+$', s):
        numerator, denominator = map(int, s.split("/"))
        if denominator == 0:
            raise ValueError("Знаменатель не может быть равен нулю")
        return

    # Целое число
    if len(tokens) == 1:
        if tokens[0] not in dict_of_numbers:
            raise ValueError(f"Неизвестное число: {tokens[0]}")
        return

    # Смешанное число: "один и четыре пятых"
    if "и" in tokens:
        idx = tokens.index("и")
        whole_words = tokens[:idx]
        frac_words = tokens[idx+1:]

        if len(frac_words) != 2:
            raise ValueError(f"Неверный формат дробной части: {' '.join(frac_words)}")

        numerator_word, denominator_word = frac_words

        if numerator_word not in dict_of_numbers:
            raise ValueError(f"Неизвестный числитель дроби: {numerator_word}")
        if denominator_word not in words_to_denominators:
            raise ValueError(f"Неизвестный знаменатель дроби: {denominator_word}")

        # Проверяем знаменатель != 0
        if words_to_denominators[denominator_word] == 0:
            raise ValueError("Знаменатель не может быть равен нулю")
        return

    # Простая дробь без целой части: "шесть седьмых"
    if len(tokens) == 2:
        numerator_word, denominator_word = tokens
        if numerator_word not in dict_of_numbers:
            raise ValueError(f"Неизвестный числитель дроби: {numerator_word}")
        if denominator_word not in words_to_denominators:
            raise ValueError(f"Неизвестный знаменатель дроби: {denominator_word}")
        if words_to_denominators[denominator_word] == 0:
            raise ValueError("Знаменатель не может быть равен нулю")
        return

    raise ValueError(f"Невозможно распознать дробь: {s}")

def safe_eval(expr):
    """Выполнение выражения с защитой от деления на ноль"""
    try:
        result = eval(expr)
        return result
    except ZeroDivisionError:
        raise ZeroDivisionError("Деление на ноль")


print("Ваш ответ ", calc(str(input("Введите арифметическое выражение: "))))