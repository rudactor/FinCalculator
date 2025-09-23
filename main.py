dict_of_numbers = {
    "один": "1",
    "два": "2",
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
    "девятнадцать": "19"    
}

dict_of_big_numbers = {
    "двадцать": "20",
    "тридцать": "30",
    "сорок": "40",
    "пятьдесят": "50",
    "шестьдесят": "60",
    "семьдесять": "70",
    "восемьдесять": "80",
    "девяносто": '90'
}

dict_of_operations = {
    "плюс": "+",
    "минус": "-",
    "разделить_на": "//",
    "умножить_на": "*"
}

fraction_units = {
    "десятая": 1, "десятых": 1,
    "сотая": 2, "сотых": 2,
    "тысячная": 3, "тысячных": 3
}


def calc(string: str) -> int:
    string = string.replace(" на", "_на")
    list_string_numbers = string.split()
    print(list_string_numbers)
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
    print(string_end)
    result = eval(string_end)
    print(result)
    if abs(result) > 100:
        return "Число больше ста"
    return convert_to_str(result)


def convert_to_str(number):
    if number < 0:
        return "минус " + convert_to_str(abs(number))
    
    if number < 20:
        return "".join([i[0] for i in dict_of_numbers.items() if i[1] == str(number)])
    elif number >= 20:
        des = str(number)[0]
        cif = str(number)[1]
        return "".join([i[0] for i in dict_of_big_numbers.items() if i[1] == str(des) + '0']) + " " + "".join([i[0] for i in dict_of_numbers.items() if i[1] == str(cif)])
        
print(calc(str(input())))
