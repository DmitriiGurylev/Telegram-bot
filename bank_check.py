def exchange_valute(data, value, from_first, to_second):  # function which converts valute
    first_value = data["Valute"][from_first]["Value"] / data["Valute"][from_first]["Nominal"]
    second_value = data["Valute"][to_second]["Value"] / data["Valute"][to_second]["Nominal"]
    if second_value != 0:
        return float(value) * float(first_value) / float(second_value)
