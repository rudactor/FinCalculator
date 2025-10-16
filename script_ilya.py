# Словарь "малых чисел" — перевод слов на цифры
dict_of_numbers = {
    "один": "1",
    "одна": "1",            # (женский род для дробей: "одна восьмая")
    "два": "2",
    "две": "2",             # (женский род для дробей: "две третьих")
    "три": "3",
    "четыре": "4",
    "пять": "5",
    "шесть": "6",
    "семь": "7",
    "восемь": "8",
    "девять": "9",
    "ноль": "0",
    "десять": "10",
    "одиннадцать": "11",
    "двенадцать": "12",
    "тринадцать": "13",
    "четырнадцать": "14",
    "пятнадцать": "15",
    "шестнадцать": "16",
    "семнадцать": "17",
    "восемнадцать": "18",
    "девятнацать": "19",
    "девятнадцать": "19",
}

# Словарь "десятков" — числа 20,30,40...90
dict_of_big_numbers = {
    "двацать": "20",         # сохранён как вариант
    "двадцать": "20",
    "тридцать": "30",
    "сорок": "40",
    "пятьдесят": "50",
    "шестьдесят": "60",
    "семьдесять": "70",
    "семьдесят": "70",
    "восемьдесять": "80",
    "восемьдесят": "80",
    "девяносто": "90",
}

# Стандартизированные десятки для красивого вывода ординалов (дробных знаменателей)
standard_tens_words = {      # обратная мапа "число десятка" -> каноничное слово
    20: "двадцать",
    30: "тридцать",
    40: "сорок",
    50: "пятьдесят",
    60: "шестьдесят",
    70: "семьдесят",
    80: "восемьдесят",
    90: "девяносто",
}

# Словарь операций
dict_of_operations = {
    "плюс": "+",
    "минус": "-",
    "умножить": "*",
}

SERVICE_WORDS = {"на"}  # Внутритекстовые служебные слова

# служебное слово для смешанных дробей
MIXED_FRACTION_SEPARATOR = "и"

OPEN_PAREN_PHRASE = ("скобка", "открывается")
CLOSE_PAREN_PHRASE = ("скобка", "закрывается")

# поддержка слов-ординалов для знаменателей
ordinal_sing_f = {
    2: "вторая", 3: "третья", 4: "четвёртая", 5: "пятая", 6: "шестая",
    7: "седьмая", 8: "восьмая", 9: "девятая", 10: "десятая",
    11: "одиннадцатая", 12: "двенадцатая", 13: "тринадцатая", 14: "четырнадцатая",
    15: "пятнадцатая", 16: "шестнадцатая", 17: "семнадцатая", 18: "восемнадцатая", 19: "девятнадцатая",
    20: "двадцатая", 30: "тридцатая", 40: "сороковая", 50: "пятидесятая",
    60: "шестидесятая", 70: "семидесятая", 80: "восьмидесятая", 90: "девяностая",
}
ordinal_pl_gen = {  # 2..19 (и десятки) — мн. род. ("две пятых", "тридцатых")
    2: "вторых", 3: "третьих", 4: "четвёртых", 5: "пятых", 6: "десятых".replace("деся", "шест"),  # "шестых"
}


ordinal_pl_gen = {
    2: "вторых", 3: "третьих", 4: "четвёртых", 5: "пятых", 6: "шестых",
    7: "седьмых", 8: "восьмых", 9: "девятых", 10: "десятых",
    11: "одиннадцатых", 12: "двенадцатых", 13: "тринадцатых", 14: "четырнадцатых",
    15: "пятнадцатых", 16: "шестнадцатых", 17: "семнадцатых", 18: "восемнадцатых", 19: "девятнадцатых",
    20: "двадцатых", 30: "тридцатых", 40: "сороковых", 50: "пятидесятых",
    60: "шестидесятых", 70: "семидесятых", 80: "восьмидесятых", 90: "девяностых",
}


# Включаем как формы singular_f, так и plural_gen
denominator_word_to_int = {}
for n, w in ordinal_sing_f.items():
    denominator_word_to_int[w] = n
for n, w in ordinal_pl_gen.items():
    denominator_word_to_int[w] = n

# Вспомогательные функции для работы с текстом чисел
def to_int_word(n: int) -> str:
    """Текст для целого (1..99) — используем исходные словари как «обратные»."""
    if 0 <= n <= 9:
        return next(k for k, v in dict_of_numbers.items() if v == str(n))
    if 10 <= n <= 19:
        return next(k for k, v in dict_of_numbers.items() if v == str(n))
    if 20 <= n <= 99:
        tens = (n // 10) * 10
        ones = n % 10
        tens_word = standard_tens_words.get(tens) or next(k for k, v in dict_of_big_numbers.items() if v == str(tens))
        if ones == 0:
            return tens_word
        ones_word = next(k for k, v in dict_of_numbers.items() if v == str(ones))
        return f"{tens_word} {ones_word}"
    if n == 100:
        return "сто"
    return str(n)

# NEW: ординал для знаменателя — жен. ед. (для числителя = 1)
def denom_ordinal_sing_f(n: int) -> str:
    if n in ordinal_sing_f:
        return ordinal_sing_f[n]
    # Составные: 21, 31, ... -> "двадцать первая", "тридцать первая"
    if 20 < n < 100 and n % 10 != 0:
        tens = (n // 10) * 10
        ones = n % 10
        tens_word = standard_tens_words[tens]
        return f"{tens_word} {ordinal_sing_f[ones]}"
    # Иначе — десятки типа 20,30,... уже покрыты словарём
    return str(n)

# мн. род. (для числителя >= 2)
def denom_ordinal_pl_gen(n: int) -> str:
    if n in ordinal_pl_gen:
        return ordinal_pl_gen[n]
    if 20 < n < 100 and n % 10 != 0:
        tens = (n // 10) * 10
        ones = n % 10
        tens_word = standard_tens_words[tens]
        return f"{tens_word} {ordinal_pl_gen[ones]}"
    return str(n)

# корректные формы "1" и "2" в числителе с учётом женского рода
def cardinal_for_numerator(n: int) -> str:
    if n == 1:
        return "одна"
    if n == 2:
        return "две"
    return to_int_word(n)

# Перевод слов в токены (числа, операции, скобки, дроби)
from fractions import Fraction

def words_to_tokens(s: str):
    words = s.lower().split()
    i = 0
    tokens = []

    def push_number(n):
        # Изменено: все числа приводим к Fraction для единого вычислителя
        tokens.append(Fraction(int(n), 1))

    # попытка распознать дробь (простую или смешанную) с позиции i
    # Примеры: "две третьих", "одна шестая", "один и четыре пятых"
    def try_parse_fraction(start_idx):
        j = start_idx
        # читаем целую часть (возможна в смешанной дроби)
        whole = None
        if j < len(words) and (words[j] in dict_of_numbers or words[j] in dict_of_big_numbers):
            # возможная целая часть
            # получаем целое значение
            if words[j] in dict_of_numbers:
                whole_val = int(dict_of_numbers[words[j]])
                j1 = j + 1
            else:
                tens = int(dict_of_big_numbers[words[j]])
                j1 = j + 1
                if j1 < len(words) and words[j1] in dict_of_numbers:
                    ones = int(dict_of_numbers[words[j1]])
                    whole_val = tens + ones
                    j1 += 1
                else:
                    whole_val = tens
            # если далее идёт "и", то это кандидат на смешанную дробь
            if j1 < len(words) and words[j1] == MIXED_FRACTION_SEPARATOR:
                whole = whole_val
                j = j1 + 1  # после "и"
            else:
                # это может быть не смешанная дробь — вернёмся, пусть основной парсер обработает как обычное число
                whole = None

        # читаем числитель
        if j < len(words) and (words[j] in dict_of_numbers or words[j] in dict_of_big_numbers):
            # получаем числитель как целое
            if words[j] in dict_of_numbers:
                num = int(dict_of_numbers[words[j]])
                j += 1
            else:
                tens = int(dict_of_big_numbers[words[j]])
                j += 1
                if j < len(words) and words[j] in dict_of_numbers:
                    ones = int(dict_of_numbers[words[j]])
                    num = tens + ones
                    j += 1
                else:
                    num = tens
        else:
            return None  # не дробь

        # читаем знаменатель-слово (ординал)
        if j < len(words):
            # допускаем 1 или 2 слова в знаменателе: "тридцать пятых"
            # пробуем 2-словный вариант
            if j + 1 < len(words):
                two = f"{words[j]} {words[j+1]}"
                if two in denominator_word_to_int:
                    den = denominator_word_to_int[two]
                    j += 2
                else:
                    # или по отдельности
                    if words[j] in denominator_word_to_int:
                        den = denominator_word_to_int[words[j]]
                        j += 1
                    else:
                        return None
            else:
                if words[j] in denominator_word_to_int:
                    den = denominator_word_to_int[words[j]]
                    j += 1
                else:
                    return None
        else:
            return None

        if den == 0:
            return None

        frac = Fraction(num, den)
        if whole is not None:
            value = Fraction(whole, 1) + frac
        else:
            value = frac
        return value, j  # вернём значение дроби и новую позицию

    while i < len(words):
        w = words[i]

        # проверка на "(скобка открывается)"
        if i + 1 < len(words) and (w, words[i + 1]) == OPEN_PAREN_PHRASE:
            tokens.append("(")
            i += 2
            continue

        # проверка на "(скобка закрывается)"
        if i + 1 < len(words) and (w, words[i + 1]) == CLOSE_PAREN_PHRASE:
            tokens.append(")")
            i += 2
            continue

        # операции
        if w in dict_of_operations:
            tokens.append(dict_of_operations[w])
            i += 1
            continue

        # служебное "на" — пропускаем
        if w in SERVICE_WORDS:
            i += 1
            continue

        # пробуем распарсить дробь/смешанную дробь отсюда
        try_frac = try_parse_fraction(i)
        if try_frac is not None:
            value, new_i = try_frac
            tokens.append(value)
            i = new_i
            continue

        # числа 0..19
        if w in dict_of_numbers:
            push_number(dict_of_numbers[w])
            i += 1
            continue

        # десятки и их сочетания
        if w in dict_of_big_numbers:
            tens = int(dict_of_big_numbers[w])
            i += 1
            if i < len(words) and words[i] in dict_of_numbers:
                ones = int(dict_of_numbers[words[i]])
                tokens.append(Fraction(tens + ones, 1))
                i += 1
            else:
                tokens.append(Fraction(tens, 1))
            continue

        # отдельная проверка "минуса" (унарный на этапе ОПЗ)
        if w == "минус":
            tokens.append("-")
            i += 1
            continue

        i += 1
    return tokens

# функция, которая преобразует выражение в обратную польскую запись
def shunting_yard(tokens):
    out = []
    stack = []

    # приоритеты операций
    def precedence(op):
        if op == "u-":   # унарный минус
            return 3
        if op == "*":
            return 2
        if op in {"+", "-"}:
            return 1
        return 0

    # проверка: является ли оператором
    def is_operator(x):
        return x in {"+", "-", "*", "u-"}

    prev = None

    for t in tokens:
        # Изменено: числа теперь могут быть Fraction
        if isinstance(t, (int, Fraction)):  # поддержим старый int на всякий случай
            out.append(Fraction(t, 1) if isinstance(t, int) else t)  # нормализуем
            prev = "num"
            continue
        if t == "(":
            stack.append(t)
            prev = "("
            continue
        if t == ")":
            while stack and stack[-1] != "(":
                out.append(stack.pop())
            if stack and stack[-1] == "(":
                stack.pop()
            prev = ")"
            continue
        if t in {"+", "-", "*"}:
            # проверка унарного минуса (например "-3" или "- одна вторая")
            if t == "-" and (prev is None or prev in {"op", "("}):
                op = "u-"
            else:
                op = t
            while stack and is_operator(stack[-1]) and (
                (precedence(stack[-1]) > precedence(op)) or
                (precedence(stack[-1]) == precedence(op) and op != "u-")
            ):
                out.append(stack.pop())
            stack.append(op)
            prev = "op"
            continue
    while stack:
        out.append(stack.pop())
    return out

# Вычисление выражения в обратной польской записи
def eval_rpn(rpn):
    st = []
    for t in rpn:
        if isinstance(t, (int, Fraction)):
            st.append(Fraction(t, 1) if isinstance(t, int) else t)
            continue
        if t == "u-":   # унарный минус
            a = st.pop()
            st.append(-a)
            continue
        b = st.pop()
        a = st.pop()
        if t == "+":
            st.append(a + b)
        elif t == "-":
            st.append(a - b)
        elif t == "*":
            st.append(a * b)
    return st[-1] if st else Fraction(0, 1)

# ====== Перевод результата обратно в слова (целые и дроби) ======
def convert_to_str_number(number: int) -> str:
    """Старый формат для целых чисел (≤100 по модулю)."""
    if number < 0:
        return "минус " + convert_to_str_number(-number)
    if number == 0:
        return "ноль"
    if number == 100:
        return "сто"
    if 1 <= number <= 99:
        return to_int_word(number)
    return str(number)

# перевод Fraction в корректную запись (смешанная/правильная дробь)
def convert_fraction_to_str(fr: Fraction) -> str:
    if fr == 0:
        return "ноль"
    neg = fr < 0
    fr = abs(fr)
    whole = fr.numerator // fr.denominator
    rem = fr.numerator % fr.denominator
    den = fr.denominator

    parts = []
    if neg:
        parts.append("минус")

    if rem == 0:
        # чистое целое
        parts.append(convert_to_str_number(whole))
        return " ".join(parts)

    # правильная дробь или смешанная
    if whole > 0:
        parts.append(convert_to_str_number(whole))
        parts.append("и")

    # числитель
    num_word = cardinal_for_numerator(rem)
    # знаменатель
    if rem == 1:
        den_word = denom_ordinal_sing_f(den)
    else:
        den_word = denom_ordinal_pl_gen(den)

    parts.append(f"{num_word} {den_word}")
    return " ".join(parts)

def convert_to_str(number_or_fraction):
    if isinstance(number_or_fraction, Fraction):
        if abs(number_or_fraction.numerator) > 100 * number_or_fraction.denominator:
            return "Число больше ста"
        return convert_fraction_to_str(number_or_fraction) 
    return convert_to_str_number(int(number_or_fraction))

# Общая функция калькулятора
def calc(string: str) -> str:
    tokens = words_to_tokens(string)   # переводим слова в токены (включая дроби Fraction)
    rpn = shunting_yard(tokens)        # делаем ОПЗ
    result = eval_rpn(rpn)             # вычисляем (Fraction)
    return convert_to_str(result)      # переводим в слова (целое/правильная/смешанная дробь)

if __name__ == "__main__":
    print(calc(input()))
