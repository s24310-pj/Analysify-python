from tkinter import messagebox

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class DataAnalyzer:
    def __init__(self):
        self.data = None

    def load_data(self, file_path):
        self.data = pd.read_csv(file_path)

    def get_summary(self):
        if self.data is not None:
            summary = self.data.describe().loc[['mean', 'min', 'max']]
            summary = summary.round(2)
            return summary
        return None

    def filter_data(self, column, value):
        if self.data is not None:
            return self.data[self.data[column].astype(str).str.contains(value)]
        else:
            return None

    def convert_categorical(self, column):
        if self.data is not None and column in self.data.columns:
            self.data[column] = self.data[column].astype('category').cat.codes
            return True
        else:
            return False

    def plot_data(self, column1, column2, plot_type):
        if self.data is not None:
            if plot_type == "Line":
                self.plot_line(column1, column2)
            elif plot_type == "Bar":
                self.plot_bar(column1, column2)
            elif plot_type == "Scatter":
                self.plot_scatter(column1, column2)
            elif plot_type == "Pie":
                self.plot_pie(column1)
        else:
            messagebox.showwarning("Ostrzeżenie", "Nie załadowano danych")

    def plot_pie(self, column):
        if self.data is not None and column in self.data.columns:
            self.data[column].value_counts().plot.pie(autopct='%1.1f%%')
            plt.ylabel('')
            plt.title(f'Pie Chart of {column}')
            plt.show()

    def plot_line(self, column1, column2):
        if self.data is not None and column1 in self.data.columns and column2 in self.data.columns:
            sns.lineplot(data=self.data, x=column1, y=column2)
            plt.title(f'Line Plot of {column1} vs {column2}')
            plt.show()

    def plot_bar(self, column1, column2):
        if self.data is not None and column1 in self.data.columns and column2 in self.data.columns:
            sns.barplot(data=self.data, x=column1, y=column2)
            plt.title(f'Bar Plot of {column1} vs {column2}')
            plt.show()

    def plot_scatter(self, column1, column2):
        if self.data is not None and column1 in self.data.columns and column2 in self.data.columns:
            sns.scatterplot(data=self.data, x=column1, y=column2)
            plt.title(f'Scatter Plot of {column1} vs {column2}')
            plt.show()

    def plot_pie_make(self):
        self.plot_pie('Make')

    def plot_bar_hp_cylinders(self):
        if self.data is not None:
            avg_hp_cylinders = self.data.groupby('Engine Cylinders')['Engine HP'].mean().reset_index()
            sns.barplot(data=avg_hp_cylinders, x='Engine Cylinders', y='Engine HP')
            plt.title('Średni HP vs Cylindry')
            plt.xlabel('Liczba cylindrów')
            plt.ylabel('Średnia moc silnika (HP)')
            plt.show()

    def plot_line_year_hp(self):
        self.plot_line('Year', 'Engine HP')

    def plot_bar_make_count(self):
        if self.data is not None and 'Make' in self.data.columns:
            make_counts = self.data['Make'].value_counts().reset_index()
            make_counts.columns = ['Make', 'Count']
            plt.figure(figsize=(10, 8))
            sns.barplot(data=make_counts, x='Make', y='Count')
            plt.title('Liczba samochodów wg producenta')
            plt.xlabel('Producent')
            plt.ylabel('Liczba samochodów')
            plt.xticks(rotation=90)
            plt.show()
