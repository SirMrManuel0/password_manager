import math
import sys

# Function to generate a cryptographic key from a given password
def oneHash(password):
    """
    Generates a list of keys based on the provided password using a series of transformations.

    Args:
    password (str): The input password.

    Returns:
    list: A list of generated keys.
    """
    sys.set_int_max_str_digits(0)
    password = text_in_numbers(password) # Convert password to a list of ASCII values
    temp = ""

    for i in password:
        temp += i

    password = temp
    temp = ""
    count = 0

    # Create a new string by interleaving characters of the password
    for i in password:
        temp += i + password[count]
        count += 1
        if count == len(password):
            count = 0


    count = len(password)
    
    # Insert the original password into the new string
    temp = temp[:count] + password + temp[count:]
    try:
        temp = str(int(temp[:15]) + int(temp[18:])) # Attempt to perform addition
    except:
        temp = str(int(temp) ** 2) # Square the value if addition fails


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

    # Insert underscores in the key string at regular intervals
    while amount > 0:
        key = key[:amount * 3] + "_" + key[amount * 3:]
        amount -= 1

    # Split the key string into a list using underscores as separators
    key = key[::3].split("_")
    temp = key
    key = list()
    
    # Remove any empty strings from the list
    for i in temp:
        if i == "":
            continue

        key.append(i)
    
    return key

# Function to encrypt text using a given key
def encrypt(text, key):
    """
    Encrypts a given text using the provided key.

    Args:
    text (str): The text to be encrypted.
    key (list): The encryption key as a list of integers.

    Returns:
    str: The encrypted text.
    """
    arr_text = text_in_numbers(text) # Convert text to a list of ASCII values
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

    arr_text = numbers_in_text(arr_text) # Convert back to text
    return str(arr_text)


# Function to convert a list of ASCII values back into text
def numbers_in_text(numbers):
    """
    Converts a list of numbers to a string of characters.

    Args:
    numbers (list): List of numeric values.

    Returns:
    str: A string formed by converting the numbers to characters.
    """
    return ''.join(chr(int(i)) for i in numbers)


# Function to convert text into a list of corresponding ASCII values
def text_in_numbers(text):
    """
    Converts a text string to a list of numeric values representing the character codes.

    Args:
    text (str): The input text to be converted.

    Returns:
    list: A list of numeric values representing the character codes of the text.
    """
    text_in_number = [str(ord(i)) for i in text]
    return text_in_number

# Function to decrypt text using a given key
def decrypt(text, key):
    """
    Decrypts an encrypted text using the provided key.

    Args:
    text (str): The encrypted text to be decrypted.
    key (list): The decryption key as a list of integers.

    Returns:
    str: The decrypted text.
    """
    arr_text = text_in_numbers(text) # Convert encrypted text to a list of ASCII values
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
    arr_text = numbers_in_text(arr_text) # Convert back to text
    return str(arr_text)

# Function to generate a cryptographic key based on two input strings
def twoOneKey(first, second):
    """
    Generates a list of keys based on two input strings (first and second).

    Args:
    first (str): The first input string.
    second (str): The second input string.

    Returns:
    list: A list of generated keys.
    """
    
    if len(first) <= 4:
        first += "laenger"
    
    first = text_in_numbers(first) # Convert the first input string to a list of ASCII values
    first = "".join(i for i in first) # Join the ASCII values into a single string
    
    second = text_in_numbers(second) # Convert the second input string to a list of ASCII values
    second = "".join(i for i in second) # Join the ASCII values into a single string
    
    
    temp = ""
    count = 0

    # Create a new string by interleaving characters from the first and second input strings
    for i in first:
        temp += i + second[count]
        count += 1
        if count == len(second):
            count = 0

    temp2 = temp[0: 18]
    temp = temp[18:]
    
    
    temp = int(temp) + int(temp2)
    temp = str(temp)

    temp2 = ""
    count = 0

    for i in temp:
        temp2 += i + first[count]
        count += 1
        if count == len(first):
            count = 0

    temp = temp2

    temp2 = temp[0: 18]
    temp = temp[18:]

    temp = int(temp) + int(temp2)
    temp = str(temp)

    key = temp

    temp2 = ""
    count = 0

    for i in temp:
        temp2 += i + first[count::2]
        count += 1
        if count == len(first):
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

    amount = math.floor(len(key) / 3)

    # Insert underscores in the key string at regular intervals
    while amount > 0:
        key = key[:amount * 3] + "_" + key[amount * 3:]

        amount -= 1
    
    # Split the key string into a list using underscores as separators
    key = key.split("_")
    
    temp = key
    key = list()
    
    # Remove any empty strings from the list
    for i in temp:
        if i == "":
            continue
        
        key.append(i)
        
    return key
    
