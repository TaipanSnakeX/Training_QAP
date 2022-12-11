ticket = int(input('Введите количество билетов: '))
price = 0.0
for i in range(ticket):
    age = int(input('Введите возраст: '))
    if age < 18:
        price = price + 0
    elif 18 <= age < 25:
        price = price + 990
    else: price = price + 1390
if ticket > 3:
        price = price * 0.9
print('Итого'+ ' ' + str(round(price)) + ' ' + 'руб.')