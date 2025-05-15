# Note Manager

Простое кроссплатформенное десктоп-приложение для создания, редактирования и удаления текстовых заметок.
## Стек и зависимости
- **Python** 3.7+  
- **PyQt6** для графического интерфейса  
- **SQLAlchemy** + встроенный **SQLite** для хранения данных

## Функциональность
1. **Главное окно**
   - Список заметок в виде таблицы (QTableView + QAbstractTableModel)  
   - Поиск по названию  
   - Сортировка по дате создания или дате обновления  
   - Кнопки управления:  
     - **Создать**  
     - **Редактировать**  
     - **Удалить** (с подтверждением)  
     - **Обновить**  

2. **Диалог создания/редактирования заметки**
   - Поле «Название» (до 50 символов)  
   - Многострочный QTextEdit для текста заметки  
   - Кнопки «Сохранить» / «Отменить»  

3. **Темы оформления**
   - Доступные темы: `light`, `dark`, `pastel_light`, `solarized_dark`, `purple`, `orange`  
   - Выбор темы через меню «Тема» 

4. **Хранение данных**
   - Файл базы данных `notes.db` в корне проекта  
   - Таблица `notes` со столбцами:
     - `id` (PK, autoincrement)  
     - `title` (String(50), NOT NULL)  
     - `content` (Text, NOT NULL)  
     - `created_at` (DateTime)  
     - `updated_at` (DateTime)  

## Структура проекта

```

note\_manager/
├── db.py               # инициализация SQLite + SQLAlchemy
├── main.py             # точка входа, загрузка темы, запуск QApplication
├── table\_model.py      # QAbstractTableModel для отображения списка заметок
├── models/
│   └── note.py         # ORM-модель Note
├── themes/             # QSS-файлы тем оформления
│   ├── dark.qss
│   ├── light.qss
│   ├── pastel\_light.qss
│   ├── orange.qss
│   ├── purple.qss
│   └── solarized\_dark.qss
└── views/
├── main\_window\.py  # главное окно приложения
└── note\_dialog.py  # диалог создания/редактирования заметки

````

## Установка и запуск

1. **Клонировать репозиторий** или распаковать архив и перейти в папку проекта:
   ```bash
   cd note_manager


2. **(Рекомендовано) Создать виртуальное окружение**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Linux/Mac
   .\venv\Scripts\Activate.ps1   # Windows PowerShell
   ```

3. **Установить зависимости**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Запустить приложение**:

   ```bash
   python main.py
   ```

   При первом запуске автоматически создаётся файл базы данных `notes.db`.

