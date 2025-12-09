
import sqlite3
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime
from utilities import clear_screen, sortDailyData
from stock_class import Stock, DailyData


def create_database():
    db_name = "stocks.db"
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    create_stocks_table_sql = """
        CREATE TABLE IF NOT EXISTS stocks (
            symbol TEXT NOT NULL PRIMARY KEY,
            name   TEXT,
            shares REAL
        );
    """

    create_dailydata_table_sql = """
        CREATE TABLE IF NOT EXISTS dailyData (
            symbol TEXT NOT NULL,
            date   TEXT NOT NULL,
            price  REAL NOT NULL,
            volume REAL NOT NULL,
            PRIMARY KEY (symbol, date)
        );
    """

    cursor.execute(create_stocks_table_sql)
    cursor.execute(create_dailydata_table_sql)


def save_stock_data(stock_list):
    db_name = "stocks.db"
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    insert_stock_sql = """
        INSERT INTO stocks (symbol, name, shares)
        VALUES (?, ?, ?);
    """

    insert_dailydata_sql = """
        INSERT INTO dailyData (symbol, date, price, volume)
        VALUES (?, ?, ?, ?);
    """

    for stock in stock_list:
        stock_values = (stock.symbol, stock.name, stock.shares)
        try:
            cursor.execute(insert_stock_sql, stock_values)
            cursor.execute("COMMIT;")
        except Exception:
            pass

        for daily_record in stock.DataList:
            daily_values = (
                stock.symbol,
                daily_record.date.strftime("%m/%d/%y"),
                daily_record.close,
                daily_record.volume,
            )
            try:
                cursor.execute(insert_dailydata_sql, daily_values)
                cursor.execute("COMMIT;")
            except Exception:
                pass


def load_stock_data(stock_list):
    stock_list.clear()
    db_name = "stocks.db"
    connection = sqlite3.connect(db_name)

    stock_cursor = connection.cursor()
    select_stocks_sql = """
        SELECT symbol, name, shares
        FROM stocks;
    """
    stock_cursor.execute(select_stocks_sql)
    stock_rows = stock_cursor.fetchall()

    for symbol, name, shares in stock_rows:
        new_stock = Stock(symbol, name, shares)

        daily_cursor = connection.cursor()
        select_daily_sql = """
            SELECT date, price, volume
            FROM dailyData
            WHERE symbol = ?;
        """
        daily_cursor.execute(select_daily_sql, (new_stock.symbol,))
        daily_rows = daily_cursor.fetchall()

        for date_str, price, volume in daily_rows:
            daily_record = DailyData(
                datetime.strptime(date_str, "%m/%d/%y"),
                float(price),
                float(volume),
            )
            new_stock.add_data(daily_record)

        stock_list.append(new_stock)

    sortDailyData(stock_list)


def retrieve_stock_web(start_date, end_date, stock_list):
    start_timestamp = str(int(time.mktime(time.strptime(start_date, "%m/%d/%y"))))
    end_timestamp = str(int(time.mktime(time.strptime(end_date, "%m/%d/%y"))))
    record_count = 0

    for stock in stock_list:
        symbol = stock.symbol

        url = (
            "https://finance.yahoo.com/quote/"
            + symbol
            + "/history?period1=" + start_timestamp
            + "&period2=" + end_timestamp
            + "&interval=1d&filter=history&frequency=1d"
        )

        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        try:
            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(60)
            driver.get(url)
        except Exception:
            raise RuntimeWarning("Chrome Driver Not Found")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        table = soup.find("table", attrs={"data-test": "historical-prices"})
        if not table:
            table = soup.find("table")
        if not table:
            continue

        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            cell_text = [c.text for c in cells]

            if len(cell_text) == 7:
                try:
                    date_value = datetime.strptime(cell_text[0], "%b %d, %Y")
                    close_value = float(cell_text[5].replace(",", ""))
                    volume_value = float(cell_text[6].replace(",", ""))
                except ValueError:
                    continue

                daily_record = DailyData(date_value, close_value, volume_value)
                stock.add_data(daily_record)
                record_count += 1

    return record_count


def import_stock_web_csv(stock_list, symbol, filename):
    for stock in stock_list:
        if stock.symbol == symbol:
            with open(filename, newline="") as stock_file:
                csv_reader = csv.reader(stock_file, delimiter=",")
                next(csv_reader, None)

                for row in csv_reader:
                    if not row or len(row) < 3:
                        continue

                    date_str = row[0].strip()
                    close_str = row[1].strip()
                    volume_str = row[2].strip()

                    try:
                        date_value = datetime.strptime(date_str, "%m/%d/%Y")
                        close_value = float(close_str.replace("$", "").replace(",", ""))
                        volume_value = float(volume_str.replace(",", ""))
                    except ValueError:
                        continue

                    daily_record = DailyData(date_value, close_value, volume_value)
                    stock.add_data(daily_record)

            break


def main():
    clear_screen()
    print("This module will handle data storage and retrieval.")


if __name__ == "__main__":
    main()
