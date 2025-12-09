
from os import path
from tkinter import *
from tkinter import ttk, messagebox, simpledialog, filedialog

import stock_data
from stock_class import Stock
from utilities import display_stock_chart, sortStocks, sortDailyData


class StockApp:
    def __init__(self):
        self.stock_list = []

        if not path.exists("stocks.db"):
            stock_data.create_database()

        self.root = Tk()
        self.root.title("Kavan Stock Manager")

        self.menubar = Menu(self.root)

        file_menu = Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Load Data", command=self.load)
        file_menu.add_command(label="Save Data", command=self.save)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)
        self.menubar.add_cascade(label="File", menu=file_menu)

        web_menu = Menu(self.menubar, tearoff=0)
        web_menu.add_command(label="Retrieve Data From Web", command=self.scrape_web_data)
        web_menu.add_command(label="Import From CSV File", command=self.importCSV_web_data)
        self.menubar.add_cascade(label="Web", menu=web_menu)

        chart_menu = Menu(self.menubar, tearoff=0)
        chart_menu.add_command(label="Display Chart", command=self.display_chart)
        self.menubar.add_cascade(label="Chart", menu=chart_menu)

        self.root.config(menu=self.menubar)

        main = ttk.Frame(self.root, padding=5)
        main.pack(fill=BOTH, expand=True)

        left = ttk.Frame(main, padding=5)
        left.pack(side=LEFT, fill=Y)

        right = ttk.Frame(main, padding=5)
        right.pack(side=LEFT, fill=BOTH, expand=True)

        ttk.Label(left, text="Stocks").pack(anchor="w")

        list_wrap = ttk.Frame(left)
        list_wrap.pack(fill=Y, expand=True)

        self.stock_listbox = Listbox(list_wrap, height=15, exportselection=False)
        self.stock_listbox.pack(side=LEFT, fill=Y)

        scroll = ttk.Scrollbar(list_wrap, orient=VERTICAL, command=self.stock_listbox.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.stock_listbox.config(yscrollcommand=scroll.set)
        self.stock_listbox.bind("<<ListboxSelect>>", self.update_data)

        self.heading_label = ttk.Label(
            right,
            text="Select a stock",
            font=("TkDefaultFont", 12, "bold")
        )
        self.heading_label.pack(anchor="w", pady=(0, 5))

        self.tab_control = ttk.Notebook(right)
        self.tab_control.pack(fill=BOTH, expand=True)

        self.main_tab = ttk.Frame(self.tab_control)
        self.history_tab = ttk.Frame(self.tab_control)
        self.report_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.main_tab, text="Main")
        self.tab_control.add(self.history_tab, text="History")
        self.tab_control.add(self.report_tab, text="Report")

        self.setup_main_tab()
        self.setup_history_tab()
        self.setup_report_tab()

        self.root.mainloop()

    def setup_main_tab(self):
        body = ttk.Frame(self.main_tab, padding=5)
        body.pack(fill=BOTH, expand=True)

        add_section = ttk.LabelFrame(body, text="Add Stock", padding=5)
        add_section.pack(fill=X, pady=(0, 5))

        ttk.Label(add_section, text="Symbol:").grid(row=0, column=0, sticky="e")
        self.symbol_entry = ttk.Entry(add_section, width=10)
        self.symbol_entry.grid(row=0, column=1, sticky="w")

        ttk.Label(add_section, text="Name:").grid(row=1, column=0, sticky="e")
        self.name_entry = ttk.Entry(add_section, width=25)
        self.name_entry.grid(row=1, column=1, sticky="w")

        ttk.Label(add_section, text="Shares:").grid(row=2, column=0, sticky="e")
        self.shares_entry = ttk.Entry(add_section, width=10)
        self.shares_entry.grid(row=2, column=1, sticky="w")

        ttk.Button(add_section, text="Add Stock", command=self.add_stock).grid(
            row=3, column=0, columnspan=2, pady=(5, 0)
        )

        update = ttk.LabelFrame(body, text="Update Shares", padding=5)
        update.pack(fill=X)

        ttk.Label(update, text="Shares:").grid(row=0, column=0, sticky="e")
        self.update_shares_entry = ttk.Entry(update, width=10)
        self.update_shares_entry.grid(row=0, column=1, sticky="w")

        ttk.Button(update, text="Buy", command=self.buy_shares).grid(
            row=1, column=0, pady=(5, 0), sticky="we"
        )
        ttk.Button(update, text="Sell", command=self.sell_shares).grid(
            row=1, column=1, pady=(5, 0), sticky="we"
        )
        ttk.Button(update, text="Delete Stock", command=self.delete_stock).grid(
            row=2, column=0, columnspan=2, pady=(5, 0), sticky="we"
        )

    def setup_history_tab(self):
        self.history_text = Text(self.history_tab, width=60, height=20)
        self.history_text.pack(fill=BOTH, expand=True)

    def setup_report_tab(self):
        self.report_text = Text(self.report_tab, width=60, height=20)
        self.report_text.pack(fill=BOTH, expand=True)

    def load(self):
        self.stock_listbox.delete(0, END)
        stock_data.load_stock_data(self.stock_list)
        sortStocks(self.stock_list)
        for s in self.stock_list:
            self.stock_listbox.insert(END, s.symbol)
        messagebox.showinfo("Load Data", "Data Loaded")

    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data", "Data Saved")

    def update_data(self, _=None):
        self.display_stock_data()

    def display_stock_data(self):
        if not self.stock_listbox.curselection():
            return
        sym = self.stock_listbox.get(self.stock_listbox.curselection())
        for stock in self.stock_list:
            if stock.symbol == sym:
                self.heading_label.config(text=f"{stock.name} - {stock.shares} Shares")
                self.history_text.delete("1.0", END)
                self.report_text.delete("1.0", END)

                self.history_text.insert(END, "- Date -   - Price -   - Volume -\n")
                self.history_text.insert(END, "=================================\n")

                sortDailyData(self.stock_list)

                for d in stock.DataList:
                    self.history_text.insert(
                        END,
                        f"{d.date.strftime('%m/%d/%y')}   ${d.close:,.2f}   {int(d.volume)}\n"
                    )

                if stock.DataList:
                    prices = [d.close for d in stock.DataList]
                    self.report_text.insert(END, f"Symbol: {stock.symbol}\n")
                    self.report_text.insert(END, f"Name: {stock.name}\n")
                    self.report_text.insert(END, f"Shares: {stock.shares}\n")
                    self.report_text.insert(END, f"Current Price: ${prices[-1]:,.2f}\n")
                    self.report_text.insert(END, f"Position Value: ${prices[-1] * stock.shares:,.2f}\n")
                    self.report_text.insert(END, f"High Close: ${max(prices):,.2f}\n")
                    self.report_text.insert(END, f"Low Close: ${min(prices):,.2f}\n")
                    self.report_text.insert(END, f"Average Close: ${sum(prices)/len(prices):,.2f}\n")
                break

    def add_stock(self):
        try:
            sym = self.symbol_entry.get().upper().strip()
            name = self.name_entry.get().strip()
            shares = float(self.shares_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Shares must be a number")
            return

        new = Stock(sym, name, shares)
        self.stock_list.append(new)
        sortStocks(self.stock_list)

        self.stock_listbox.delete(0, END)
        for s in self.stock_list:
            self.stock_listbox.insert(END, s.symbol)

        self.symbol_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.shares_entry.delete(0, END)

    def buy_shares(self):
        self._change_shares("buy")

    def sell_shares(self):
        self._change_shares("sell")

    def _change_shares(self, action):
        if not self.stock_listbox.curselection():
            messagebox.showwarning("No Selection", "Select a stock first.")
            return
        sym = self.stock_listbox.get(self.stock_listbox.curselection())
        for stock in self.stock_list:
            if stock.symbol == sym:
                try:
                    val = float(self.update_shares_entry.get())
                except ValueError:
                    messagebox.showerror("Input Error", "Shares must be a number")
                    return
                if action == "sell" and val > stock.shares:
                    messagebox.showerror("Sell Shares", "Not enough shares to sell.")
                    return
                if action == "buy":
                    stock.buy(val)
                else:
                    stock.sell(val)
                self.heading_label.config(text=f"{stock.name} - {stock.shares} Shares")
        if action == "buy":
            messagebox.showinfo("Buy Shares", "Shares Purchased")
        else:
            messagebox.showinfo("Sell Shares", "Shares Sold")
        self.update_shares_entry.delete(0, END)
        self.display_stock_data()

    def delete_stock(self):
        if not self.stock_listbox.curselection():
            messagebox.showwarning("No Selection", "Select a stock first.")
            return
        sym = self.stock_listbox.get(self.stock_listbox.curselection())
        self.stock_list = [s for s in self.stock_list if s.symbol != sym]
        self.stock_listbox.delete(0, END)
        for s in self.stock_list:
            self.stock_listbox.insert(END, s.symbol)
        self.heading_label.config(text="Select a stock")
        self.history_text.delete("1.0", END)
        self.report_text.delete("1.0", END)
        messagebox.showinfo("Delete Stock", f"{sym} Deleted")

    def scrape_web_data(self):
        start = simpledialog.askstring("Starting Date", "Enter Starting Date (m/d/yy)")
        end = simpledialog.askstring("Ending Date", "Enter Ending Date (m/d/yy)")
        if not start or not end:
            return
        try:
            count = stock_data.retrieve_stock_web(start, end, self.stock_list)
        except RuntimeWarning:
            messagebox.showerror("Cannot Get Data from Web", "Check Path for Chrome Driver")
            return
        self.display_stock_data()
        messagebox.showinfo("Get Data From Web", f"{count} records retrieved")

    def importCSV_web_data(self):
        if not self.stock_listbox.curselection():
            messagebox.showwarning("No Selection", "Select a stock first.")
            return
        sym = self.stock_listbox.get(self.stock_listbox.curselection())
        file = filedialog.askopenfilename(
            title=f"Select {sym} File to Import",
            filetypes=[("CSV Files", "*.csv")]
        )
        if file:
            stock_data.import_stock_web_csv(self.stock_list, sym, file)
            self.display_stock_data()
            messagebox.showinfo("Import Complete", f"{sym} Import Complete")

    def display_chart(self):
        if not self.stock_listbox.curselection():
            messagebox.showwarning("No Selection", "Select a stock first.")
            return
        sym = self.stock_listbox.get(self.stock_listbox.curselection())
        display_stock_chart(self.stock_list, sym)


def main():
    StockApp()


if __name__ == "__main__":
    main()
