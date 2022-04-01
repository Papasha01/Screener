# while True:
#     try:
#          x = int(input("Пожалуйста, введите целое число: "))
#          break
#     except Exception:
#          print("Это не целое число. Попробуйте снова...")

try:
    for i in range(3):
        print(3/i)
except:
    print("Деление на 0")
    print("Исключение было обработано")