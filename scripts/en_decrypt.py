import math
import sys

def master_key_maker(password):
    sys.set_int_max_str_digits(0)
    password = text_in_numbers(password)
    temp = ""
    for i in password:
        temp += i
    password = temp

    temp = ""
    count = 0

    for i in password:
        temp += i + password[count]
        count += 1
        if count == len(password):
            count = 0

    count = len(password)

    temp = temp[:count] + password + temp[count:]

    temp = str(int(temp[:15]) + int(temp[18:]))

    key = temp

    temp2 = ""
    count = 0

    for i in temp:
        temp2 += i + password[count::2]
        count += 1
        if count == len(password):
            count = 0

    key += temp2

    temp = key

    halfKey = round(len(key) / 2)

    temp2 = temp[0: halfKey]
    temp = temp[halfKey:]

    temp = int(temp) + int(temp2)
    temp = str(temp)

    key = temp

    key = str(key)

    key = str(int(key) ** 2)

    amount = math.floor(len(key) / 3)

    while amount > 0:
        key = key[:amount * 3] + "_" + key[amount * 3:]

        amount -= 1
    key = key[::3].split("_")
    temp = key
    key = list()
    for i in temp:
        if i == "":
            continue
        key.append(i)
    
    return key

def encrypt(text, key):
    arr_text = text_in_numbers(text)
    ii = 0
    for i in range(0, len(arr_text)):
        if ii < (len(key) - 1):
            arr_text[i] = int(arr_text[i]) + int(key[ii])
        else:
            ii = 0
            arr_text[i] = int(arr_text[i]) + int(key[ii])
        if int(arr_text[i]) >= 1114112:
            arr_text[i] = int(arr_text[i]) - 1114112
        ii += 1
    arr_text = numbers_in_text(arr_text)
    return str(arr_text)

def numbers_in_text(numbers):
    ret_numbers = ""
    for i in numbers:
        ret_numbers += chr(int(i))
    return ret_numbers

def text_in_numbers(text):
    text_in_number = ""
    for i in text:
        text_in_number += f"{str(ord(i))}_"
    return text_in_number.split('_')[:-1]


def decrypt(text, key):
    arr_text = text_in_numbers(text)
    ii = 0
    for i in range(0, len(arr_text)):
        if ii < (len(key) - 1):
            arr_text[i] = int(arr_text[i]) - int(key[ii])
        else:
            ii = 0
            arr_text[i] = int(arr_text[i]) - int(key[ii])
        if int(arr_text[i]) < 0:
            arr_text[i] = int(arr_text[i]) + 1114112
        ii += 1
    arr_text = numbers_in_text(arr_text)
    return str(arr_text)