import random

chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
number = input('Кол-во паролей:' + "\n")
length = input('Кол-во символов в пароле:' + "\n")
number = int(number)
length = int(length)

for n in range(number):
    password = ''
    for i in range(length):
        password += random.choice(chars)
    print(password)
