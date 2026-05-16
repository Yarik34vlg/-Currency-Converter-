import requests
import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime

window = tk.Tk()
window.title("Currency Converter")
window.geometry("800x680")
window.resizable(False, False)
window.configure(bg="#f5f5f5")

Frame = tk.Frame(window, bg="#ffffff")
Frame.pack(fill=tk.X, pady=20)

enter_label = tk.Label(
    Frame, text="Введите сумму:", fg="#212121", bg="#ffffff", font="Arial 14"
)
enter_label.pack(pady=20)

entry = tk.Entry(Frame, width=30)
entry.pack(pady=10)

currencies = ["USD", "EUR", "GBP", "CNY", "JPY", "RUB"]

input_Combo = ttk.Combobox(Frame, values=currencies)
input_Combo.pack(pady=5)
input_Combo.set("USD")
currency_label = tk.Label(
    Frame,
    text="Выберите валюту для конвертации:",
    fg="#212121",
    bg="#ffffff",
    font="Arial 14",
)
currency_label.pack(pady=20)

output_Combo = ttk.Combobox(Frame, values=currencies)
output_Combo.pack(pady=5)
output_Combo.set("EUR")

result_label = tk.Label(
    window, text="Результат: ---", bg="#f5f5f5", fg="#212121", font="Arial 14 bold"
)
result_label.pack(pady=20)

def convert():
    try:
        amount = float(entry.get())
        before = input_Combo.get().strip().upper()
        after = output_Combo.get().strip().upper()
    except ValueError:
        result_label.config(text="Ошибка: введите число!")
        return

    if before == after:
        result_label.config(text="Ошибка: выберите разные валюты!")
        return

    if amount <= 0:
        result_label.config(text="Ошибка: сумма должна быть положительной!")
        return
    API_KEY = "cur_live_tjYFiBLBAr5QalMdtbZ8wiMJgUd1RJiqmhWl9LL5"

    url = f"https://api.currencyapi.com/v3/latest?apikey={API_KEY}&base_currency={before}&currencies={after}"

    
    response = requests.get(url)

    if response.status_code != 200:
        result_label.config(text="Ошибка API: проверьте ключ или валюты")
        return

    data = response.json()

    if after not in data["data"]:
        result_label.config(text=f"Ошибка: валюта {after} не найдена")
        return

    rate = data["data"][after]["value"]
    result = amount * rate
    result_label.config(text=f"Результат: {round(result, 2)} {after}")

#Сохраняем в историю
    data_to_save = {
        "Дата": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Из": before,
        "В": after,
        "Сумма": amount,
        "Результат": round(result, 2)
    }

    try:
        with open("history.json", "r", encoding="utf-8") as f:
            history = json.load(f)
    except:
        history = []

    history.append(data_to_save)

    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


Convertor = tk.Button(
    Frame, text="Конвертировать", bg="#4ca57e", fg="#ffffff", 
    font="Arial 14", width=20, command=convert
)
Convertor.pack(pady=20)

#Таблица истории
history_frame = tk.LabelFrame(window, text="История операций", bg="#ffffff")
history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

columns = ("Дата", "Из", "В", "Сумма", "Результат")
history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=6)

for col in columns:
    history_tree.heading(col, text=col)
    history_tree.column(col, width=100)

history_tree.pack(fill=tk.BOTH, expand=True)

def load_history_to_table():
    for row in history_tree.get_children():
        history_tree.delete(row)
    try:
        with open("history.json", "r", encoding="utf-8") as f:
            history = json.load(f)
            for item in history:
                history_tree.insert("", "end", values=(
                    item.get("Дата", ""),
                    item.get("Из", ""),
                    item.get("В", ""),
                    item.get("Сумма", ""),
                    item.get("Результат", "")
                ))
    except:
        pass

load_btn = tk.Button(history_frame, text="Загрузить историю", command=load_history_to_table)
load_btn.pack(pady=5)

load_history_to_table()
window.mainloop()