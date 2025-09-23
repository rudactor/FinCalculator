from word2number import w2n

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

dict_of_operations = {
    "плюс": "+",
    "минус": "-",
    "разделить_на": "/",
    "умножить_на": "*",
    "остаток_от_деления": "%"
}

fraction_units = {
    "десятая": 1,
    "десятых": 1,
    "сотая": 2,
    "сотых": 2,
    "тысячная": 3,
    "тысячных": 3
}

def calc(string: str) -> int:
    string = string.replace(" на", "_на")
    list_string_numbers = string.split()
    while any(key in list_string_numbers for key in fraction_units):
        for key in fraction_units:
            if key in list_string_numbers:
                idx = list_string_numbers.index(key)
                frac_part = " ".join(list_string_numbers[:idx + 1])
                decimal_number = words_to_decimal(frac_part)
                list_string_numbers = [decimal_number] + list_string_numbers[idx + 1:]
                break
    string_end = ""
    for index, element in enumerate(list_string_numbers):
        if list_string_numbers[index - 1] == 'разделить_на' and element == 'ноль':
            return "Деление на ноль"
        if element in dict_of_numbers:
            string_end += dict_of_numbers[element]
        elif element in dict_of_operations:
            string_end += dict_of_operations[element]
        elif element in dict_of_big_numbers:
            if index + 1 < len(list_string_numbers) and list_string_numbers[index + 1] in dict_of_numbers:
                string_end += "(" + dict_of_big_numbers[element] + "+" + dict_of_numbers[list_string_numbers[index + 1]] + ")"
                list_string_numbers[index + 1] = ""
            else:
                string_end += dict_of_big_numbers[element]
        else:
            string_end += element
    result = eval(string_end)
    if abs(result) > 100:
        return "Число больше ста"
    return convert_to_str(result)

def words_to_decimal(s: str):
    s = s.lower()
    parts = s.split(" и ")
    list_string_numbers = parts[0].strip().split()
    string_end = ''
    for index, element in enumerate(list_string_numbers):
        if element in dict_of_numbers:
            string_end += dict_of_numbers[element]
        elif element in dict_of_big_numbers:
            if index + 1 < len(list_string_numbers) and list_string_numbers[index + 1] in dict_of_numbers:
                string_end += "(" + dict_of_big_numbers[element] + "+" + dict_of_numbers[list_string_numbers[index + 1]] + ")"
                list_string_numbers[index + 1] = ""
            else:
                string_end += dict_of_big_numbers[element]
    integer_part = eval(string_end)
    if len(parts) > 1:
        fraction_words = parts[1].strip().split()[:-1]
        string_end = ''
        for index, element in enumerate(fraction_words):
            if element in dict_of_numbers:
                string_end += dict_of_numbers[element]
            elif element in dict_of_big_numbers:
                if index + 1 < len(fraction_words) and fraction_words[index + 1] in dict_of_numbers:
                    string_end += "(" + dict_of_big_numbers[element] + "+" + dict_of_numbers[fraction_words[index + 1]] + ")"
                    fraction_words[index + 1] = ""
                else:
                    string_end += dict_of_big_numbers[element]
        fraction_number = eval(string_end)
        return str(integer_part) + '.' + str(fraction_number)

def convert_to_str(number): 
    if number < 0: 
        return "минус " + convert_to_str(abs(number)) 
    if number % 1 != 0:
        integer_part = int(number)
        fraction_str = str(number).split(".")[1] 
        fraction_number = int(fraction_str)
        if len(fraction_str) == 1:
            unit_word = "десятая" if fraction_number == 1 else "десятых"
        elif len(fraction_str) == 2:
            unit_word = "сотая" if fraction_number == 1 else "сотых"
        elif len(fraction_str) == 3:
            unit_word = "тысячная" if fraction_number == 1 else "тысячных"
        else:
            unit_word = "дробь"

        integer_words = "" if integer_part == 0 else convert_to_str(integer_part)
        fraction_words = convert_to_str(fraction_number)

        if integer_words:
            return f"{integer_words} и {fraction_words} {unit_word}"
        else:
            return f"{fraction_words} {unit_word}"
        
    if number < 20: 
        return "".join([i[0] for i in dict_of_numbers.items() if i[1] == str(number)]) 
    elif number >= 20: 
        des = str(number)[0] 
        cif = str(number)[1] 
        return "".join([i[0] for i in dict_of_big_numbers.items() if i[1] == str(des) + '0']) + " " + "".join([i[0] for i in dict_of_numbers.items() if i[1] == str(cif)])

print(calc(str(input())))