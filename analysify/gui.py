import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from data_analyzer import DataAnalyzer


class Application(tk.Tk):
    def __init__(self, analyzer):
        super().__init__()
        self.analyzer = analyzer
        self.title("Analysify")
        self.geometry("800x600")

        self.configure(bg='#423f3b')

        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):

        button_font = ("Arial", 18)
        button_font_small = ("Arial", 12)

        self.load_button = tk.Button(self, text="Załaduj Plik Z Danymi", command=self.load_csv, bg='#77dd77',
                                     fg='white', width=60, font=button_font)
        self.load_button.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.summary_button = tk.Button(self, text="Pokaż Podsumowanie Danych", command=self.show_summary, bg='#55cbcd',
                                        fg='white', width=25, font=button_font, state='disabled')
        self.summary_button.place(relx=0.25, rely=0.25, anchor=tk.CENTER)

        self.records_button = tk.Button(self, text="Eksploruj Zbiór Danych", command=self.show_records, bg='#55cbcd',
                                        fg='white', width=25, font=button_font, state='disabled')
        self.records_button.place(relx=0.75, rely=0.25, anchor=tk.CENTER)

        self.filter_button = tk.Button(self, text="Filtruj Dane", command=self.filter_data, bg='#55cbcd', fg='white',
                                       width=25, font=button_font, state='disabled')
        self.filter_button.place(relx=0.25, rely=0.4, anchor=tk.CENTER)

        self.convert_button = tk.Button(self, text="Przekształć na wart. numeryczne", command=self.convert_categorical,
                                        bg='#55cbcd', fg='white', width=25, font=button_font, state='disabled')
        self.convert_button.place(relx=0.75, rely=0.4, anchor=tk.CENTER)

        self.plot_button = tk.Button(self, text="Rysuj Wykres", command=self.plot_data, bg='#55cbcd', fg='white',
                                     width=60, font=button_font, state='disabled')
        self.plot_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        self.example_label = tk.Label(self, text="Przykładowe Wykresy:", bg='#423f3b', fg='white', font=button_font)
        self.example_label.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

        self.plot_pie_make = tk.Button(self, text="Wykres Kołowy: Make", command=self.analyzer.plot_pie_make,
                                       bg='#55cbcd', fg='white',
                                       width=35, font=button_font_small, state='disabled')
        self.plot_pie_make.place(relx=0.25, rely=0.75, anchor=tk.CENTER)

        self.plot_hp_cylinders = tk.Button(self, text="Wykres Słupkowy: Średni HP vs Cylindry",
                                           command=self.analyzer.plot_bar_hp_cylinders,
                                           bg='#55cbcd', fg='white', width=35, font=button_font_small, state='disabled')
        self.plot_hp_cylinders.place(relx=0.75, rely=0.75, anchor=tk.CENTER)

        self.plot_year_hp = tk.Button(self, text="Wykres Liniowy: Year vs Engine HP",
                                      command=self.analyzer.plot_line_year_hp,
                                      bg='#55cbcd', fg='white', width=35, font=button_font_small, state='disabled')
        self.plot_year_hp.place(relx=0.25, rely=0.85, anchor=tk.CENTER)

        self.plot_make_count = tk.Button(self, text="Wykres Słupkowy: Make vs Count",
                                         command=self.analyzer.plot_bar_make_count,
                                         bg='#55cbcd', fg='white', width=35, font=button_font_small, state='disabled')
        self.plot_make_count.place(relx=0.75, rely=0.85, anchor=tk.CENTER)

    def on_closing(self):
        self.destroy()

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.analyzer.load_data(file_path)
            messagebox.showinfo("Info", "Dane załadowane poprawnie")
            self.enable_buttons()

    def enable_buttons(self):
        self.summary_button.config(state='normal')
        self.records_button.config(state='normal')
        self.filter_button.config(state='normal')
        self.convert_button.config(state='normal')
        self.plot_button.config(state='normal')
        self.plot_pie_make.config(state='normal')
        self.plot_hp_cylinders.config(state='normal')
        self.plot_year_hp.config(state='normal')
        self.plot_make_count.config(state='normal')

    def show_summary(self):
        summary = self.analyzer.get_summary()
        if summary is not None:
            self.show_table(summary.reset_index())
        else:
            messagebox.showwarning("Ostrzeżenie", "Nie załadowano danych")

    def show_records(self):
        if self.analyzer.data is not None:
            self.show_table(self.analyzer.data)
        else:
            messagebox.showwarning("Ostrzeżenie", "Nie załadowano danych")

    def show_table(self, df):
        window = tk.Toplevel(self)
        window.title("Tabela Danych")

        frame = ttk.Frame(window)
        frame.pack(fill='both', expand=True)

        tree = ttk.Treeview(frame, columns=list(df.columns), show='headings')
        tree.pack(side='left', fill='both', expand=True)

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        vsb.pack(side='right', fill='y')
        tree.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(window, orient="horizontal", command=tree.xview)
        hsb.pack(side='bottom', fill='x')
        tree.configure(xscrollcommand=hsb.set)

        self._data = df
        self._tree = tree
        self._sort_col = None
        self._sort_ascending = True

        def sort_column(col):
            if self._sort_col == col:
                self._sort_ascending = not self._sort_ascending
            else:
                self._sort_ascending = True
            self._sort_col = col
            self._data = self._data.sort_values(by=[col], ascending=self._sort_ascending)
            update_treeview()

        for col in df.columns:
            tree.heading(col, text=col, command=lambda _col=col: sort_column(_col))
            tree.column(col, anchor='center')

        def update_treeview():
            for row in tree.get_children():
                tree.delete(row)
            for row in self._data.itertuples():
                tree.insert("", "end", values=row[1:])

        update_treeview()

    def show_column_selection_dialog(self, callback, multiple=False):
        if self.analyzer.data is None:
            messagebox.showwarning("Ostrzeżenie", "Nie załadowano danych")
            return

        columns = list(self.analyzer.data.columns)

        def on_select():
            selected_columns = [col_var.get() for col_var in column_vars]
            callback(selected_columns)
            dialog.destroy()

        dialog = tk.Toplevel(self)
        dialog.title("Wybierz Kolumnę")

        column_vars = [tk.StringVar(value=columns[0]) for _ in range(2 if multiple else 1)]
        for i, column_var in enumerate(column_vars):
            label = tk.Label(dialog, text=f"Wybierz kolumnę {i + 1}:")
            label.pack(pady=5)
            option_menu = ttk.OptionMenu(dialog, column_var, columns[0], *columns)
            option_menu.pack(pady=5)

        select_button = ttk.Button(dialog, text="Zatwierdź", command=on_select)
        select_button.pack(pady=10)

        dialog.protocol("WM_DELETE_WINDOW", lambda: dialog.destroy())
        dialog.bind('<Return>', lambda event: on_select())

        dialog.mainloop()

    def show_plot_type_selection_dialog(self, callback):
        plot_types = ["Line", "Bar", "Scatter", "Pie"]

        def on_select():
            selected_plot_type = plot_type_var.get()
            if selected_plot_type:
                callback(selected_plot_type, dialog)

        dialog = tk.Toplevel(self)
        dialog.title("Typ Wykresu")

        plot_type_var = tk.StringVar(value=plot_types[0])

        label = tk.Label(dialog, text="Wybierz typ wykresu:")
        label.pack(pady=5)

        option_menu = ttk.OptionMenu(dialog, plot_type_var, plot_types[0], *plot_types)
        option_menu.pack(pady=5)

        select_button = ttk.Button(dialog, text="Zatwierdź", command=on_select)
        select_button.pack(pady=10)

        dialog.protocol("WM_DELETE_WINDOW", lambda: dialog.destroy())
        dialog.bind('<Return>', lambda event: on_select())

        dialog.mainloop()

    def filter_data(self):
        def callback(selected_columns):
            if selected_columns:
                column = selected_columns[0]
                value = simpledialog.askstring("Wprowadzanie",
                                               f"Wprowadź wartośc po której filtrować kolumnę {column}:")
                if column and value:
                    filtered_data = self.analyzer.filter_data(column, value)
                    if filtered_data is not None:
                        self.show_table(filtered_data)
                    else:
                        messagebox.showwarning("Ostrzeżenie", "Nie załadowano danych")

        self.show_column_selection_dialog(callback)

    def plot_data(self):
        def plot_type_callback(plot_type, dialog):
            dialog.destroy()
            if plot_type == "Pie":
                self.show_column_selection_dialog(lambda columns: self.analyzer.plot_data(columns[0], None, plot_type),
                                                  multiple=False)
            else:
                self.show_column_selection_dialog(
                    lambda columns: self.analyzer.plot_data(columns[0], columns[1], plot_type), multiple=True)

        self.show_plot_type_selection_dialog(plot_type_callback)

    def convert_categorical(self):
        def callback(selected_columns):
            column = selected_columns[0] if selected_columns else None
            if column and self.analyzer.convert_categorical(column):
                messagebox.showinfo("Info", f"Kolumna '{column}' przekształcona na numeryczną")
            else:
                messagebox.showwarning("Ostrzeżenie", f"Nie udało się przekształcić kolumny '{column}'")

        self.show_column_selection_dialog(callback)


if __name__ == "__main__":
    analyzer = DataAnalyzer()
    app = Application(analyzer)
    app.mainloop()
