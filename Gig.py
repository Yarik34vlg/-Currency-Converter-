import requests
import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime

# Сначала создадим окно

window = tk.Tk()
window.title("Currency Converter")
window.geometry("650x500")
window.resizable(False, False)
window.configure(bg="#f5f5f5")


# Фрэйм для красоты

Frame = tk.Frame(window, bg="#ffffff")
Frame.pack(fill=tk.X, padx=20)


# Узнаем сумму и валюту у пользователя

enter_label = tk.Label(
    Frame, text="Введите сумму:", fg="#212121", bg="#ffffff", font="Arial 14"
)
enter_label.pack(padx=20, pady=20)


entry = tk.Entry(Frame, width=30)
entry.pack(padx=20, pady=20)

currencies = ["USD", "EUR", "GBP", "CNY", "JPY"]

input_Combo = ttk.Combobox(Frame, values=currencies)
input_Combo.place(x=400, y=88)
input_Combo.set("USD")


# Узнаем в какую валюту нужно переконвертировать

currency_label = tk.Label(
    Frame,
    text="Выберите валюту для конвертации:",
    fg="#212121",
    bg="#ffffff",
    font="Arial 14",
)
currency_label.pack(pady=40)


output_Combo = ttk.Combobox(Frame, values=currencies)
output_Combo.pack()
output_Combo.set("EUR")


# Перед кнопкой создадим функцию для неё


def convert():
    try:
        amount = float(entry.get())
        before = input_Combo.get().strip().upper()
        after = output_Combo.get().strip().upper()

        if before == after:
            result_label.config(text="Ошибка: выберите разные валюты!")

        if amount < 0:
            result_label.config(text="Ошибка: нельзя конвертировать отрицательные числа!")

        url = f"https://api.frankfurter.app/latest?from={before}"

        response = requests.get(url)

        data = response.json()

        rate = data["rates"][after]

        result = amount * rate

        result_label.config(text=f"Результат: {result}")

        data_to_save = {
            "Дата": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Из": before,
            "В": after,
            "Количество": amount,
            "Результат": result
        }
        
        try:
            with open("history.json", "a", encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)
                print("Результат сохранён в файл'history.json'.")

        except FileNotFoundError:
            print("Ошибка: файла'history.json' не существует.")


    except ValueError:
        result_label.config(text="Ошибка: введите число!")


result_frame = tk.Frame(window, bg="#ffffff")
result_frame.pack(fill=tk.X, padx=20, pady=20)


result_label = tk.Label(
    result_frame, text="Результат:", fg="#212121", bg="#ffffff", font="Arial 14"
)
result_label.pack(pady=20)


# Кнопка для конвертации

Convertor = tk.Button(
    Frame, text="Конвертировать", bg="#4caf50", fg="#ffffff", font="Arial 14", width=20
)
Convertor.pack(pady=40)
Convertor.bind("<Button-1>", lambda event: convert())


window.mainloop()