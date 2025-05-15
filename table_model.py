from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex

# Класс NoteTableModel реализует модель таблицы для отображения заметок в QTableView
class NoteTableModel(QAbstractTableModel):
    def __init__(self, notes=None):
        super().__init__()
        # Список заметок (note должен быть объектом с атрибутами title, created_at, updated_at)
        self.notes = notes or []

    # Возвращает количество строк в таблице (то есть количество заметок)
    def rowCount(self, parent=QModelIndex()):
        return len(self.notes)

    # Возвращает количество колонок — у нас их три: название, дата создания, дата обновления
    def columnCount(self, parent=QModelIndex()):
        return 3  # title, created_at, updated_at

    # Возвращает данные для отображения в конкретной ячейке таблицы
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        # Проверка, что индекс допустим
        if not index.isValid() or not (0 <= index.row() < len(self.notes)):
            return None

        # Получаем заметку по строке
        note = self.notes[index.row()]
        column = index.column()

        # Если роль отображения (т.е. обычный текст), возвращаем нужные данные
        if role == Qt.ItemDataRole.DisplayRole:
            if column == 0:
                # Название заметки
                return note.title
            elif column == 1:
                # Дата создания в формате ГГГГ-ММ-ДД ЧЧ:ММ
                return note.created_at.strftime("%Y-%m-%d %H:%M")
            elif column == 2:
                # Дата обновления в том же формате
                return note.updated_at.strftime("%Y-%m-%d %H:%M")

        # Для других ролей ничего не возвращаем
        return None

    # Возвращает заголовки колонок (или строк, если orientation == Vertical)
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        # Отображаем только текстовые заголовки
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        # Если горизонтальная ориентация (то есть заголовки колонок)
        if orientation == Qt.Orientation.Horizontal:
            # Заголовки колонок по порядку
            headers = ["Название", "Создано", "Обновлено"]
            if 0 <= section < len(headers):
                return headers[section]

        return None

    # Получить заметку по номеру строки
    def get_note(self, row):
        if 0 <= row < len(self.notes):
            return self.notes[row]
        return None

    # Обновить список заметок и перерисовать таблицу
    def update_notes(self, notes):
        # Уведомляем представление о начале массового изменения данных
        self.beginResetModel()
        self.notes = notes  # Обновляем внутренний список
        self.endResetModel()  # Уведомляем об окончании обновления
