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
    "девятнацать": "19"    
}

dict_of_big_numbers = {
    "двацать": "20",
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
    "умножить": "*"
}

def calc(string: str) -> int:
    list_string_numbers = string.split()
    string_end = ""
    for index, element in enumerate(list_string_numbers):
        if element in dict_of_numbers:
            string_end += dict_of_numbers[element]
        elif element in dict_of_operations:
            string_end += dict_of_operations[element]
        elif element in dict_of_big_numbers:
            if list_string_numbers[index + 1] in dict_of_numbers: 
                string_end += dict_of_big_numbers[element] + "+"
            else:
                string_end += dict_of_big_numbers[element]
    return eval(string_end)


# def convert_to_str(number):
#     if len(str(number)) > 1:

