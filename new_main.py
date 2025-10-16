from fractions import Fraction
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

def calc(string: str) -> str:
    string = string.replace(" на", "_на").replace("скобка ", "скобка_").replace("в степени", "в_степени")\
                   .replace("синус от", "синус_от").replace("косинус от", "косинус_от")\
                   .replace("тангенс от", "тангенс_от")
    
    tokens = string.split()
    print(tokens)
    validate_number_words(tokens)
    string_end = ""
    print(tokens)
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
            token not in ['размещенийиз', 'сочетанийиз', 'перестановокиз'] and token != 'по':
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


def safe_eval(expr):
    """Выполнение выражения с защитой от деления на ноль"""
    try:
        result = eval(expr)
        return result
    except ZeroDivisionError:
        raise ZeroDivisionError("Деление на ноль")



print(calc(str(input())))