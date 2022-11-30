from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base

sqlite_db_name = "books_dz24.sqlite"


def init_dict():
    return [{'name': 'Удавы и питоны Уход и содержание',
             'author': ['Крицкий А.'],
             'year': 2009,
             'publisher': 'Профиздат'},
            {'name': 'Алгоритмы неформально. Инструкция для ' +
                     'начинающих питонистов',
             'author': ['Брэдфорд Такфилд'],
             'year': '2022',
             'publisher': 'Питер'},
            {'name': 'Изучаем Python. Том 1',
             'author': ['Марк Лутц'],
             'year': '2019',
             'publisher': 'Диалектика'},
            {'name': 'Изучаем Python. Том 2',
             'author': ['Марк Лутц'],
             'year': '2020',
             'publisher': 'Вильямс'},
            {'name': 'Искусственный интеллект и компьютерное зрение. ' +
                     'Реальные проекты на Python, Keras и TensorFlow',
             'author': ['Коул Анирад',
                        'Казам Мехер',
                        'Ганджу Сиддха'],
             'year': '2023',
             'publisher': 'Питер'},
            {'name': 'Высокопроизводительные Python-приложения. ' +
                     'Практическое руководство по эффективному ' +
                     'программированию',
             'author': ['Горелик Миша',
                        'Йен Освальд'],
             'year': '2022',
             'publisher': 'Бомбора'},
            {'name': 'Учим Python, делая крутые игры',
             'author': ['Эл Свейгарт'],
             'year': '2021',
             'publisher': 'Бомбора'},
            {'name': 'Автоматизация рутинных задач с помощью Python',
             'author': ['Эл Свейгарт'],
             'year': '2021',
             'publisher': 'Диалектика'},
            {'name': 'Простой Python. Современный стиль ' +
                     'программирования',
             'author': ['Билл Любанович'],
             'year': '2021',
             'publisher': 'Питер'},
            {'name': 'Простой Python. Современный стиль ' +
                     'программирования',
             'author': ['Билл Любанович'],
             'year': '2016',
             'publisher': 'Питер'},
            {'name': 'Цель на 360. Управляй судьбой',
             'author': ['Пелехатый М.М.',
                        'Спирица Е.'],
             'year': '2023',
             'publisher': 'Питер'}]


# Алгоритм.
# Источник:
# https://ru.wikibooks.org/wiki/SQLAlchemy#Создание_таблицы_в_базе_данных

# Вариант 1. Классическое объявление - пишем отдельно таблицу,
# отдельно класс и делаем маппинг (отображение класса на таблицу).
# Требуется редко, если надо разделить задачи.
#
#         # Импортировали движок
#         from sqlalchemy import create_engine
#         # Подцепляемся к базе
#         engine = create_engine('sqlite:///:memory:', echo=True)
# - Создаём таблицы в базе данных
#         from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
#         metadata = MetaData()
#         users_table = Table('users', metadata,
#                             Column('id', Integer, primary_key=True),
#                             Column('name', String),
#                             Column('fullname', String),
#                             Column('password', String)
#                             )
#   Для MySQL, длина должна быть передана строкам, как здесь:
#         Column('name', String(50))
# - пошлем базе команду CREATE TABLE
#         metadata.create_all(engine)
# - Определение класса Python для отображения в таблицу
#         class User(object):
#         def __init__(self, name, fullname, password):
#           self.name = name
#           self.fullname = fullname
#           self.password = password
#
#         def __repr__(self):
#           return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)
# - Настройка отображения. Сливаем таблицу user_table и класс User.
#   Применим функцию mapper, чтобы создать отображение между users_table и User.
#         from sqlalchemy.orm import mapper
#         mapper(User, users_table)
#   Дальше, работая с объектами пользователя будем иметь возможность их сохранить в БД
#   по принципу: объект <==> строка в таблице БД

# Вариант 2. Декларативное создание таблицы, класса и отображения за один раз
#         from sqlalchemy import Column, Integer, String, create_engine
#         from sqlalchemy.ext.declarative import declarative_base
#
#         engine = create_engine('sqlite:///:memory:', echo=True)
#
#         Base = declarative_base()
#
#         class User(Base):
#             __tablename__ = 'users'
#             id = Column(Integer, primary_key=True)
#             name = Column(String)
#             fullname = Column(String)
#             password = Column(String)
#
#             def __init__(self, name, fullname, password):
#                 self.name = name
#                 self.fullname = fullname
#                 self.password = password
#
#             def __repr__(self):
#                 return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)
#
#         # Создание таблицы
#         Base.metadata.create_all(engine)
#   Имеющиеся метаданные MetaData также доступны:
#         metadata = Base.metadata

engine = create_engine('sqlite:///' + sqlite_db_name, echo=True)

Base = declarative_base()


# cursor.execute("""CREATE TABLE IF NOT EXISTS
#                 Authors (
#                     Id          INTEGER PRIMARY KEY,
#                     Author_Name TEXT
#                     )
#             """)
class Authors(Base):
    """
    CREATE TABLE "Authors" (
        "Id" INTEGER NOT NULL,
        "Author_Name" VARCHAR,
        PRIMARY KEY ("Id")
    )
    """
    __tablename__ = 'Authors'
    Id = Column(Integer, primary_key=True)
    Author_Name = Column(String)

    def __init__(self, author_name=''):
        # инициализатор объекта класса
        self.Author_Name = author_name

    def __repr__(self):
        # Метод для оператора print (программное представление объекта) - repr(obj)
        return "<Authors('%s','%s')>" % (self.Id, self.Author_Name)

    def __str__(self):
        # строковое представление объекта - str(obj)
        return "<Authors('%s','%s')>" % (self.Id, self.Author_Name)


# cursor.execute("""CREATE TABLE IF NOT EXISTS
#                 Books (
#                     Id               INTEGER PRIMARY KEY,
#                     Book_Name        TEXT,
#                     Publication_Year INTEGER,
#                     Publisher_Id     INTEGER REFERENCES Publishers (Id)
#                     )
#             """)
class Books(Base):
    """
    CREATE TABLE "Books" (
        "Id" INTEGER NOT NULL,
        "Book_Name" VARCHAR,
        "Publication_Year" INTEGER,
        "Publisher_Id" INTEGER,
        PRIMARY KEY ("Id"),
        FOREIGN KEY("Publisher_Id") REFERENCES "Publishers" ("Id")
    )
    """
    __tablename__ = 'Books'
    Id = Column(Integer, primary_key=True)
    Book_Name = Column(String)
    Publication_Year = Column(Integer)
    Publisher_Id = Column(Integer, ForeignKey('Publishers.Id'))

    def __init__(self, book_name='', publication_year=None, publisher_id=None):
        # инициализатор объекта класса
        self.Book_Name = book_name
        self.Publication_Year = publication_year
        self.Publisher_Id = publisher_id

    def __repr__(self):
        # Метод для оператора print (программное представление объекта) - repr(obj)
        return "<Books('%s','%s','%s','%s')>" % (self.Id,
                                                 self.Book_Name,
                                                 self.Publication_Year,
                                                 self.Publisher_Id)

    def __str__(self):
        # строковое представление объекта - str(obj)
        return "<Books('%s','%s','%s','%s')>" % (self.Id,
                                                 self.Book_Name,
                                                 self.Publication_Year,
                                                 self.Publisher_Id)


# cursor.execute("""CREATE TABLE IF NOT EXISTS
#                 Publishers (
#                     Id             INTEGER PRIMARY KEY,
#                     Publisher_Name TEXT
#                     )
#             """)
class Publishers(Base):
    """
    CREATE TABLE "Publishers" (
        "Id" INTEGER NOT NULL,
        "Publisher_Name" VARCHAR,
        PRIMARY KEY ("Id")
    )
    """
    __tablename__ = 'Publishers'
    Id = Column(Integer, primary_key=True)
    Publisher_Name = Column(String)

    def __init__(self, publisher_name=''):
        # инициализатор объекта класса
        self.Publisher_Name = publisher_name

    def __repr__(self):
        # Метод для оператора print (программное представление объекта) - repr(obj)
        return "<Publishers('%s','%s')>" % (self.Id, self.Publisher_Name)

    def __str__(self):
        # строковое представление объекта - str(obj)
        return "<Publishers('%s','%s')>" % (self.Id, self.Publisher_Name)


# cursor.execute("""CREATE TABLE IF NOT EXISTS
#                Books_Authors (
#                     Id        INTEGER PRIMARY KEY,
#                     Book_Id   INTEGER REFERENCES Books (Id),
#                     Author_Id INTEGER REFERENCES Authors (Id)
#                     )
#             """)
class Books_Authors(Base):
    """
        CREATE TABLE "Books_Authors" (
            "Id" INTEGER NOT NULL,
            "Book_Id" INTEGER,
            "Author_Id" INTEGER,
            PRIMARY KEY ("Id"),
            FOREIGN KEY("Book_Id") REFERENCES "Books" ("Id"),
            FOREIGN KEY("Author_Id") REFERENCES "Authors" ("Id")
        )
    """
    __tablename__ = 'Books_Authors'
    Id = Column(Integer, primary_key=True)
    Book_Id = Column(Integer, ForeignKey('Books.Id'))
    Author_Id = Column(Integer, ForeignKey('Authors.Id'))

    def __init__(self, book_id='', author_id=''):
        # инициализатор объекта класса
        self.Book_Id = book_id
        self.Author_Id = author_id

    def __repr__(self):
        # Метод для оператора print (программное представление объекта) - repr(obj)
        return "<Books_Authors('%s','%s','%s')>" % (self.Id, self.Book_Id, self.Author_Id)

    def __str__(self):
        # строковое представление объекта - str(obj)
        return "<Books_Authors('%s','%s','%s')>" % (self.Id, self.Book_Id, self.Author_Id)
# """
#     CREATE TABLE "Books_Authors" (
#         "Id" INTEGER NOT NULL,
#         "Book_Id" INTEGER,
#         "Author_Id" INTEGER,
#         PRIMARY KEY ("Id"),
#         FOREIGN KEY("Book_Id") REFERENCES "Books" ("Id"),
#         FOREIGN KEY("Author_Id") REFERENCES "Authors" ("Id")
#     )
# """
# Books_Authors = Table('Books_Authors', Base.metadata,
#                       Column('Id', Integer, primary_key=True),
#                       Column('Book_Id', Integer, ForeignKey('Books.Id')),
#                       Column('Author_Id', Integer, ForeignKey('Authors.Id'))
#                       )

# Создание таблиц
Base.metadata.create_all(engine)
