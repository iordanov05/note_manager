from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Note(Base):
    """Модель для представления заметок в базе данных.
    
    Атрибуты:
        id (int): Уникальный идентификатор заметки. Автоматически инкрементируется.
        title (str): Заголовок заметки. Максимальная длина - 50 символов. Обязательное поле.
        content (str): Содержимое заметки в текстовом формате. Обязательное поле.
        created_at (datetime): Дата и время создания заметки. Устанавливается автоматически при создании.
        updated_at (datetime): Дата и время последнего обновления заметки. 
            Автоматически обновляется при каждом изменении записи.
            
    Таблица:
        __tablename__ (str): Название таблицы в базе данных - 'notes'.
    """
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
