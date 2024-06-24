from gui import Application
from data_analyzer import DataAnalyzer

if __name__ == "__main__":
    analyzer = DataAnalyzer()
    app = Application(analyzer)
    app.mainloop()
