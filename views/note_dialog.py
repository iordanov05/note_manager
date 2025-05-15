from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QTextEdit,
    QDialogButtonBox, QLabel, QMessageBox
)

class NoteDialog(QDialog):
    
    """Диалоговое окно для создания/редактирования заметки.
    
    Окно содержит поля для ввода названия и текста заметки, 
    а также кнопки подтверждения/отмены действия.

    Args:
        parent (QWidget, optional): Родительский виджет. По умолчанию None.
        note (Note, optional): Существующая заметка для редактирования. 
            Если None - создается новая заметка. По умолчанию None.
    """
    def __init__(self, parent=None, note=None):
        """Инициализирует диалоговое окно для работы с заметкой.

        Настраивает интерфейс в зависимости от режима (создание/редактирование):
        - Устанавливает соответствующий заголовок окна
        - Создает и размещает элементы управления
        - Для режима редактирования заполняет поля данными из заметки
        - Добавляет стандартные кнопки подтверждения/отмены
        """
        super().__init__(parent)
        self.setWindowTitle("Редактировать заметку" if note else "Новая заметка")
        self.resize(400, 300)

        self.note = note

        self.title_input = QLineEdit()
        self.title_input.setMaxLength(50)

        self.text_input = QTextEdit()

        if note:
            self.title_input.setText(note.title)
            self.text_input.setPlainText(note.content)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Название:"))
        layout.addWidget(self.title_input)
        layout.addWidget(QLabel("Текст заметки:"))
        layout.addWidget(self.text_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_data(self):
        
        """Получает и валидирует данные из полей ввода.
        
        Returns:
            dict | None: Словарь с данными заметки в формате:
                {
                    "title": str - заголовок заметки,
                    "content": str - текст заметки
                }
                Возвращает None если данные не прошли валидацию.
                
        Note:
            - Проверяет что заголовок не пустой
            - Удаляет лишние пробелы в начале/конце текста
            - Показывает предупреждение если заголовок пустой
        """
        title = self.title_input.text().strip()
        content = self.text_input.toPlainText().strip()

        if not title:
            QMessageBox.warning(self, "Ошибка", "Название не может быть пустым.")
            return None

        return {
            "title": title,
            "content": content
        }
