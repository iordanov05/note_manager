from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout,
    QLineEdit, QComboBox, QTableView, QMessageBox, QApplication
)
from PyQt6.QtGui import QAction

from table_model import NoteTableModel
from models.note import Note
from views.note_dialog import NoteDialog
from db import Session

class MainWindow(QMainWindow):
    """Главное окно приложения для управления заметками.
    
    Реализует весь основной функционал:
    - Отображение списка заметок в таблице с возможностью сортировки и поиска
    - Создание, редактирование и удаление заметок
    - Взаимодействие с базой данных через SQLAlchemy
    - Автоматическое обновление данных при изменениях
    
    Интерфейс включает:
    - Панель поиска и сортировки
    - Таблицу с настройками отображения
    - Панель управления с кнопками действий
    - Диалоговые окна для работы с заметками
    """
    def __init__(self):
        """Инициализирует главное окно приложения для управления заметками.

        Создает и настраивает пользовательский интерфейс, включая:
        - Основные параметры окна (заголовок, размер)
        - Подключение к базе данных через SQLAlchemy Session
        - Поисковую панель с:
          * Поле ввода для поиска по названию заметок
          * Выпадающий список для выбора сортировки (по дате создания/обновления)
        - Таблицу для отображения заметок с настройками:
          * Модель данных NoteTableModel
          * Поведение выделения строк
          * Настройки ширины колонок (растягивание, автоматический подбор)
        - Панель кнопок управления с действиями:
          * Создание новой заметки
          * Редактирование выбранной заметки
          * Удаление выбранной заметки
          * Обновление списка заметок

        Устанавливает соединения сигналов:
        - Изменение текста поиска → автоматическое обновление списка
        - Изменение сортировки → автоматическое обновление списка
        - Нажатия кнопок → вызов соответствующих методов

        По завершении инициализации автоматически загружает список заметок."""
        super().__init__()
        self.setWindowTitle("Менеджер заметок")
        self.resize(700, 500)

        self.session = Session()

        # Виджеты
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        search_bar = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию...")
        self.search_input.textChanged.connect(self.refresh_notes)

        self.sort_box = QComboBox()
        self.sort_box.addItems(["По дате создания", "По дате обновления"])
        self.sort_box.currentIndexChanged.connect(self.refresh_notes)

        search_bar.addWidget(self.search_input)
        search_bar.addWidget(self.sort_box)

        layout.addLayout(search_bar)

        # Таблица
        self.table_view = QTableView()
        self.model = NoteTableModel()
        self.table_view.setModel(self.model)
        self.table_view.setSelectionBehavior(self.table_view.SelectionBehavior.SelectRows)
        layout.addWidget(self.table_view)


        self.table_view.setModel(self.model)

        # Настройка ширины колонок
        header = self.table_view.horizontalHeader()
        header.setStretchLastSection(True)  # Последняя колонка занимает оставшееся место
        
        # Установка фиксированной ширины (по индексам колонок)
        header.setSectionResizeMode(0, self.table_view.horizontalHeader().ResizeMode.Stretch)  # Название
        header.setSectionResizeMode(1, self.table_view.horizontalHeader().ResizeMode.ResizeToContents)  # Создано
        header.setSectionResizeMode(2, self.table_view.horizontalHeader().ResizeMode.ResizeToContents)  # Обновлено
        
        

        # Кнопки
        button_bar = QHBoxLayout()

        self.create_btn = QPushButton("Создать")
        self.edit_btn = QPushButton("Редактировать")
        self.delete_btn = QPushButton("Удалить")
        self.refresh_btn = QPushButton("Обновить")

        self.create_btn.clicked.connect(self.create_note)
        self.edit_btn.clicked.connect(self.edit_note)
        self.delete_btn.clicked.connect(self.delete_note)
        self.refresh_btn.clicked.connect(self.refresh_notes)

        for btn in [self.create_btn, self.edit_btn, self.delete_btn, self.refresh_btn]:
            button_bar.addWidget(btn)

        layout.addLayout(button_bar)
        central.setLayout(layout)

        self.refresh_notes()

        self.create_theme_menu()




    def get_selected_note(self):
        """Возвращает выбранную в таблице заметку.
    
        Проверяет выделенные строки в таблице и возвращает соответствующую заметку.
        Если ничего не выбрано, возвращает None.
    
        Returns:
            Note | None: Объект выбранной заметки или None, если ничего не выбрано.
        """
        indexes = self.table_view.selectionModel().selectedRows()
        if indexes:
            row = indexes[0].row()
            return self.model.get_note(row)
        return None

    def create_note(self):
        """Создает новую заметку через диалоговое окно.
    
        Открывает диалог для ввода данных новой заметки. 
        Если диалог завершен успешно (OK), добавляет новую заметку в БД
        и обновляет список заметок.
        """
        dialog = NoteDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if data:
                note = Note(**data)
                self.session.add(note)
                self.session.commit()
                self.refresh_notes()

    def edit_note(self):
        """Редактирует выбранную заметку через диалоговое окно.
        
        Проверяет, выбрана ли заметка для редактирования. Если нет - показывает предупреждение.
        При успешном завершении диалога обновляет данные заметки в БД
        и обновляет список заметок.
        """
        note = self.get_selected_note()
        if not note:
            QMessageBox.warning(self, "Ошибка", "Выберите заметку.")
            return
        dialog = NoteDialog(self, note)
        if dialog.exec():
            data = dialog.get_data()
            if data:
                note.title = data["title"]
                note.content = data["content"]
                self.session.commit()
                self.refresh_notes()

    def delete_note(self):
        """Удаляет выбранную заметку с подтверждением.
        
        Проверяет, выбрана ли заметка для удаления. Если нет - показывает предупреждение.
        Перед удалением запрашивает подтверждение пользователя.
        При подтверждении удаляет заметку из БД и обновляет список заметок.
        """
        note = self.get_selected_note()
        if not note:
            QMessageBox.warning(self, "Ошибка", "Выберите заметку.")
            return
        reply = QMessageBox.question(
            self,
            "Удаление",
            f"Удалить заметку '{note.title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.session.delete(note)
            self.session.commit()
            self.refresh_notes()

    def refresh_notes(self):
        """Обновляет список заметок с учетом фильтрации и сортировки.
    
        Выполняет следующие действия:
        1. Получает базовый запрос всех заметок из БД
        2. Применяет фильтрацию по поисковому запросу (если он введен) - ищет вхождение текста в заголовке
        3. Применяет сортировку в зависимости от выбранного варианта:
        - "По дате создания" - сортирует по убыванию даты создания (новые сначала)
        - Иначе - сортирует по убыванию даты обновления (недавно измененные сначала)
        4. Обновляет данные в модели представления полученными заметками
        
        Используемые параметры из UI:
            search_input (QLineEdit): Поле ввода для поиска заметок
            sort_box (QComboBox): Выпадающий список с вариантами сортировки
        """
        query = self.session.query(Note)

        search_text = self.search_input.text().strip()
        if search_text:
            query = query.filter(Note.title.contains(search_text))

        sort_option = self.sort_box.currentText()
        if sort_option == "По дате создания":
            query = query.order_by(Note.created_at.desc())
        else:
            query = query.order_by(Note.updated_at.desc())

        notes = query.all()
        self.model.update_notes(notes)


    def create_theme_menu(self):
        """
        Создаёт выпадающее меню в меню-баре для выбора цветовой темы интерфейса.

        В меню добавляются пункты с названиями доступных тем.
        При выборе темы вызывается метод set_theme с соответствующим именем темы.
        """
        theme_menu = self.menuBar().addMenu("Тема")

        themes = ["light", "dark", "pastel_light", "solarized_dark", "purple", "orange"]  # список твоих .qss файлов
        for theme_name in themes:
            action = QAction(theme_name.capitalize(), self)
            action.triggered.connect(lambda _, t=theme_name: self.set_theme(t))
            theme_menu.addAction(action)

    def set_theme(self, theme_name):
        """
        Загружает и применяет QSS-файл соответствующей темы.

        :param theme_name: Имя темы (без расширения .qss), соответствующее файлу в папке themes.
        Если файл не найден, выводит сообщение в консоль.
        """
        try:
            with open(f"themes/{theme_name}.qss", "r", encoding="utf-8") as f:
                qss = f.read()
                QApplication.instance().setStyleSheet(qss)
        except FileNotFoundError:
            print(f"Файл темы themes/{theme_name}.qss не найден")
