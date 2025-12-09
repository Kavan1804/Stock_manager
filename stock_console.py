
from datetime import datetime
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart
from os import path
import stock_data


# Main Menu
def main_menu(stock_list):
    choice = ""
    while choice != "0":
        clear_screen()
        print("Stock Analyzer ")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        choice = input("Enter Menu Option: ")

        while choice not in ["1", "2", "3", "4", "5", "0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Stock Analyzer")
            print("1 - Manage Stocks (Add, Update, Delete, List)")
            print("2 - Add Daily Stock Data (Date, Price, Volume)")
            print("3 - Show Report")
            print("4 - Show Chart")
            print("5 - Manage Data (Save, Load, Retrieve)")
            print("0 - Exit Program")
            choice = input("Enter Menu Option: ")

        if choice == "1":
            manage_stocks(stock_list)
        elif choice == "2":
            add_stock_data(stock_list)
        elif choice == "3":
            display_report(stock_list)
        elif choice == "4":
            display_chart(stock_list)
        elif choice == "5":
            manage_data(stock_list)
        else:
            clear_screen()
            print("Goodbye")


def manage_stocks(stock_list):
    choice = ""
    while choice != "0":
        clear_screen()
        print("Manage Stocks ")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        choice = input("Enter Menu Option: ")

        while choice not in ["1", "2", "3", "4", "0"]:
            clear_screen()
            print("Invalid Option - Try again")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            choice = input("Enter Menu Option: ")

        if choice == "1":
            add_stock(stock_list)
        elif choice == "2":
            update_shares(stock_list)
        elif choice == "3":
            delete_stock(stock_list)
        elif choice == "4":
            list_stocks(stock_list)
        else:
            print("Returning to Main Menu")


def add_stock(stock_list):
    choice = ""
    while choice != "0":
        clear_screen()
        print("Add Stock ")
        print("0 - Return to Manage Stocks")
        symbol = input("Enter Stock Symbol (or 0 to cancel): ").upper()
        if symbol == "0":
            choice = "0"
            continue
        name = input("Enter Company Name: ")
        try:
            shares = float(input("Enter Number of Shares: "))
        except ValueError:
            print("Invalid number of shares.")
            input("Press Enter to continue...")
            continue
        stock_list.append(Stock(symbol, name, shares))
        print("Stock Added!")
        choice = input("Press Enter to add another stock or 0 to return: ")


def update_shares(stock_list):
    choice = ""
    while choice != "0":
        clear_screen()
        print("Update Shares")
        print("1 - Buy Shares")
        print("2 - Sell Shares")
        print("0 - Return to Manage Stocks")
        choice = input("Enter Menu Option: ")

        while choice not in ["1", "2", "0"]:
            clear_screen()
            print("Invalid Option - Try again")
            print("1 - Buy Shares")
            print("2 - Sell Shares")
            print("0 - Return to Manage Stocks")
            choice = input("Enter Menu Option: ")

        if choice == "1":
            buy_stock(stock_list)
        elif choice == "2":
            sell_stock(stock_list)
        else:
            print("Returning to Manage Stocks")


def buy_stock(stock_list):
    clear_screen()
    print("Buy Shares ")
    if not stock_list:
        print("No stocks in portfolio.")
        input("Press Enter to continue...")
        return

    print("Stock List: [", end="")
    print(", ".join(stock.symbol for stock in stock_list), end="")
    print("]")

    symbol = input("Enter Stock Symbol to Buy: ").upper()
    stock = next((s for s in stock_list if s.symbol.upper() == symbol), None)

    if stock is None:
        print("Symbol not found.")
        input("Press Enter to continue...")
        return

    try:
        shares_to_buy = float(input("Enter Number of Shares to Buy: "))
    except ValueError:
        print("Invalid number of shares.")
        input("Press Enter to continue...")
        return

    stock.buy(shares_to_buy)
    print("Shares updated.")
    input("Press Enter to continue...")


def sell_stock(stock_list):
    clear_screen()
    print("Sell Shares ")
    if not stock_list:
        print("No stocks in portfolio.")
        input("Press Enter to continue...")
        return

    print("Stock List: [", end="")
    print(", ".join(stock.symbol for stock in stock_list), end="")
    print("]")

    symbol = input("Enter Stock Symbol to Sell: ").upper()
    stock = next((s for s in stock_list if s.symbol.upper() == symbol), None)

    if stock is None:
        print("Symbol not found.")
        input("Press Enter to continue...")
        return

    try:
        shares_to_sell = float(input("Enter Number of Shares to Sell: "))
    except ValueError:
        print("Invalid number of shares.")
        input("Press Enter to continue...")
        return

    if shares_to_sell > stock.shares:
        print("Not enough shares to sell.")
        input("Press Enter to continue...")
        return

    stock.sell(shares_to_sell)
    print("Shares updated.")
    input("Press Enter to continue...")


def delete_stock(stock_list):
    clear_screen()
    print("Delete Stock ")
    if not stock_list:
        print("No stocks to delete.")
        input("Press Enter to continue...")
        return

    print("Stock List: [", end="")
    print(", ".join(stock.symbol for stock in stock_list), end="")
    print("]")

    symbol = input("Enter Stock Symbol to Delete: ").upper()
    index = next((i for i, s in enumerate(stock_list) if s.symbol.upper() == symbol), None)

    if index is None:
        print("Symbol not found.")
    else:
        del stock_list[index]
        print("Stock deleted.")

    input("Press Enter to continue...")


def list_stocks(stock_list):
    clear_screen()
    print("Stocks Being Tracked ")
    if not stock_list:
        print("No stocks in portfolio.")
    else:
        for stock in stock_list:
            print(f"{stock.symbol} - {stock.name} ({stock.shares} shares)")
    input("Press Enter to continue...")


def add_stock_data(stock_list):
    clear_screen()
    print("Add Daily Stock Data ")
    if not stock_list:
        print("No stocks available. Add stocks first.")
        input("Press Enter to continue...")
        return

    print("Stock List: [", end="")
    print(", ".join(stock.symbol for stock in stock_list), end="")
    print("]")

    symbol = input("Enter Stock Symbol: ").upper()
    stock = next((s for s in stock_list if s.symbol.upper() == symbol), None)

    if stock is None:
        print("Symbol not found.")
        input("Press Enter to continue...")
        return

    more = "Y"
    while more.upper() == "Y":
        date_str = input("Enter Date (m/d/yy): ")
        price_str = input("Enter Closing Price: ")
        volume_str = input("Enter Volume: ")
        try:
            date_value = datetime.strptime(date_str, "%m/%d/%y")
            price = float(price_str)
            volume = float(volume_str)
        except ValueError:
            print("Invalid date or numeric value.")
            more = input("Try again? (Y/N): ")
            continue

        stock.add_data(DailyData(date_value, price, volume))
        print("Daily data added.")
        more = input("Add another record? (Y/N): ")


def display_report(stock_list):
    clear_screen()
    print("Stock Report ")
    if not stock_list:
        print("No stocks in portfolio.")
    else:
        for stock in stock_list:
            print(f"\n{stock.symbol} - {stock.name} ({stock.shares} shares)")
            if not stock.DataList:
                print("  No daily data.")
                continue

            stock.DataList.sort(key=lambda d: d.date)
            print("  Date       Close     Volume")
            for daily in stock.DataList:
                print(
                    f"  {daily.date.strftime('%m/%d/%y'):10} "
                    f"{daily.close:8.2f} "
                    f"{int(daily.volume):10}"
                )
    input("\nPress Enter to continue...")


def display_chart(stock_list):
    if not stock_list:
        print("No stocks in portfolio.")
        input("Press Enter to continue...")
        return

    print("Stock List: [", end="")
    print(", ".join(stock.symbol for stock in stock_list), end="")
    print("]")

    symbol = input("Enter Stock Symbol to Chart: ").upper()
    display_stock_chart(stock_list, symbol)
    input("Press Enter to continue...")


def manage_data(stock_list):
    choice = ""
    while choice != "0":
        clear_screen()
        print("Manage Data ")
        print("1 - Save to Database")
        print("2 - Load from Database")
        print("3 - Retrieve Data From Web")
        print("4 - Import From CSV File")
        print("0 - Return to Main Menu")
        choice = input("Enter Menu Option: ")

        while choice not in ["1", "2", "3", "4", "0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Manage Data ---")
            print("1 - Save to Database")
            print("2 - Load from Database")
            print("3 - Retrieve Data From Web")
            print("4 - Import From CSV File")
            print("0 - Return to Main Menu")
            choice = input("Enter Menu Option: ")

        if choice == "1":
            stock_data.save_stock_data(stock_list)
            print("Data saved to database.")
            input("Press Enter to continue...")
        elif choice == "2":
            stock_data.load_stock_data(stock_list)
            print("Data loaded from database.")
            input("Press Enter to continue...")
        elif choice == "3":
            retrieve_from_web(stock_list)
        elif choice == "4":
            import_csv(stock_list)
        else:
            print("Returning to Main Menu")


def retrieve_from_web(stock_list):
    clear_screen()
    print("Retrieve Data From Web ")
    if not stock_list:
        print("No stocks in portfolio. Add stocks first.")
        input("Press Enter to continue...")
        return

    start_date = input("Enter Starting Date (m/d/yy): ")
    end_date = input("Enter Ending Date (m/d/yy): ")

    try:
        records = stock_data.retrieve_stock_web(start_date, end_date, stock_list)
        print(f"{records} records retrieved.")
    except RuntimeWarning:
        print("Cannot Get Data from Web. Check Path for Chrome Driver.")

    input("Press Enter to continue...")


def import_csv(stock_list):
    clear_screen()
    print("Import From CSV File ")
    if not stock_list:
        print("No stocks in portfolio. Add stocks first.")
        input("Press Enter to continue...")
        return

    symbol = input("Enter Stock Symbol: ").upper()
    filename = input("Enter CSV Filename (full path): ")

    if filename == "":
        print("Filename cannot be blank.")
        input("Press Enter to continue...")
        return

    try:
        stock_data.import_stock_web_csv(stock_list, symbol, filename)
        print(f"Data imported for {symbol}.")
    except FileNotFoundError:
        print("File not found. Please check the path.")
    except Exception as error:
        print("Error importing CSV:", error)

    input("Press Enter to continue...")


def main():
    if not path.exists("stocks.db"):
        stock_data.create_database()
    stock_list = []
    main_menu(stock_list)


if __name__ == "__main__":
    main()
