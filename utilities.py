import matplotlib.pyplot as plt
from os import system, name


def clear_screen():
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")


def sortStocks(stock_list):
    stock_list.sort(key=lambda stock_item: stock_item.symbol.upper())


def sortDailyData(stock_list):
    for stock in stock_list:
        stock.DataList.sort(key=lambda daily_record: daily_record.date)


def display_stock_chart(stock_list, symbol):
    selected_stock = next(
        (s for s in stock_list if s.symbol.upper() == symbol.upper()), None
    )
    if selected_stock is None or not selected_stock.DataList:
        print("No data available to chart for symbol:", symbol)
        return

    selected_stock.DataList.sort(key=lambda record: record.date)

    date_values = [record.date for record in selected_stock.DataList]
    close_prices = [record.close for record in selected_stock.DataList]

    plt.figure()
    plt.plot(date_values, close_prices)
    plt.title(f"{selected_stock.symbol} Closing Price History")
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.grid(True)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.show()
