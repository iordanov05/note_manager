import sys
from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow
from db import init_db

# Функция для загрузки QSS-файла со стилями оформления
def load_stylesheet(theme="dark"):
    try:
        # Пытаемся открыть файл темы (например, themes/dark.qss)
        with open(f"themes/{theme}.qss", "r", encoding="utf-8") as f:
            return f.read()  # Возвращаем содержимое файла как строку
    except FileNotFoundError:
        # Если файл не найден, возвращаем пустую строку (без стилей)
        return ""

# Главная функция приложения
def main():
    # Инициализация базы данных (создание таблиц и т. д.)
    init_db()

    # Создаём экземпляр приложения Qt
    app = QApplication(sys.argv)

    # Выбираем тему оформления — доступные: "light", "dark", "pastel_light", "orange", "purple"  "themes\solarized_dark.qss"
    theme = "orange" 
    app.setStyleSheet(load_stylesheet(theme))  # Применяем тему через QSS

    # Создаём и показываем главное окно
    window = MainWindow()
    window.show()

    # Запускаем главный цикл приложения
    sys.exit(app.exec())

# Точка входа в программу
if __name__ == "__main__":
    main()
