import pprint
# import sqlite3 as sl   # подключаем SQLite

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.operators import exists

from init_value import init_dict, sqlite_db_name, Publishers, Authors, Books, Books_Authors

if __name__ == '__main__':
    source_dict = init_dict()

    # Часть 12.14: Объединение таблиц в SQL и базах данных SQLite: JOIN и SELECT
    # https://zametkinapolyah.ru/zametki-o-mysql/chast-12-14-obedinenie-tablic-v-sql-i-bazax-dannyx-sqlite-join-i-select.html

    # Как подружить Python и базы данных SQL. Подробное руководство
    # https://proglib.io/p/kak-podruzhit-python-i-bazy-dannyh-sql-podrobnoe-rukovodstvo-2020-02-27

    # Создаём и наполняем базу данных SQLite в Python
    # https://thecode.media/sqlite-py/

    # подключение к базе
    engine = create_engine('sqlite:///' + sqlite_db_name, echo=False)
    # Заполняем таблицы
    Session = sessionmaker(bind=engine)

    # create a Session
    # когда необходимо общение с базой, создается объект класса Session.
    # Сессия здесь ассоциирована с SQLite, но у нее еще нет открытых соединений
    # с этой базой. При первом использовании она получает соединение из набора
    # соединений, который поддерживается engine и удерживает его до тех пор,
    # пока мы не применим все изменения и/или не закроем объект сессии.
    #
    # Транзакция неявно стартует как только Session начинает общаться с базой
    # данных и остается открытой до тех пор, пока Session не коммитится,
    # откатывается или закрывается.
    # Создавать объект Session нужно будет каждый раз при взаимодействии с базой.
    session = Session()

    # заполняем таблицы Publishers и Authors
    for item in source_dict:
        # заполняем таблицу Publishers
        # cur.execute('SELECT * FROM Publishers WHERE Publisher_Name = :publisher', item)
        # Метод count() возвращает количество элементов в результате.
        count_rows = session.query(Publishers.Id).filter(Publishers.Publisher_Name == item['publisher']).count()
        if count_rows == 0:  # Если список пуст, значит нет издателя с таким наименованием
            # cur.execute('INSERT INTO Publishers (Publisher_Name) VALUES(:publisher)', item)
            # В сессию добавляются объекты.
            # Но добавление объектов не влияет на запись в базу, а лишь готовит объекты к
            # сохранению в следующем commit(). Проверить это можно, получив первичные ключи
            # объектов.
            # Значение атрибута id обоих объектов — None. Это значит, что они еще не
            # сохранены в базе данных.
            session.add(Publishers(item['publisher']))

        # заполняем таблицу Authors
        for author in item['author']:
            # cur.execute('SELECT * FROM Authors WHERE Author_Name = :author', {'author': author})
            count_rows = session.query(Authors.Id).filter(Authors.Author_Name == author).count()

            if count_rows == 0:  # Если список пуст, значит нет издателя с таким наименованием
                #  Метод execute принимает в качестве параметров
                #  кортеж. Запятая нужна после author.
                # cur.execute('INSERT INTO Authors (Author_Name) VALUES(?)', (author,))
                session.add(Authors(author))

    # Метод commit() сбрасывает все оставшиеся изменения в базу и фиксирует
    # транзакции. Ресурсы подключений, что использовались в сессии, снова
    # освобождаются и возвращаются в набор. Последовательные операции с
    # сессией произойдут в новой транзакции, которая снова запросит себе
    # ресурсов по первому требованию.
    session.commit()  # Зафиксировали изменения в БД (применение всех изменений в таблицах БД)

    # заполняем таблицу Books
    for item in source_dict:
        # cur.execute('SELECT Id FROM Publishers WHERE Publisher_Name = :publisher', item)
        # Метод first()возвращает первый результат запроса или None,
        # если последний не вернул данных.
        # Метод all() вернет все записи в виде списка кортежей
        rows_lst = session.query(Publishers.Id).filter(Publishers.Publisher_Name == item['publisher']).all()
        print(f'rows_lst: {rows_lst}')
        # if len(rows_tpl) == 0:
        # Возвращается список кортежей или пустой список
        # Пример не пустого списка: [(2,)]
        if len(rows_lst) > 1:
            print("Ошибка заполнения таблицы Books.")
            pprint.pprint(item)
            continue
        elif len(rows_lst) == 0:
            # Если список пуст, значит нет издателя с таким наименованием
            # Теоретически, такая ситуация должна отсутствовать при штатной работе и базой
            # cur.execute('INSERT INTO Publishers (Publisher_Name) VALUES(:publisher)', item)
            # session_publisher = Session()
            publisher = Publishers(item['publisher'])
            session.add(publisher)
            # https://stackoverflow.com/questions/1316952/sqlalchemy-flush-and-get-inserted-id
            session.flush()  # Зафиксировали изменения в БД (применение всех изменений в таблицах БД)
            session.refresh(publisher)
            row_id = publisher.Id
        else:
            # Присутствует единственная запись
            # Результат такой: [(2,)]
            row_id = rows_lst[0][0]
        # Проверяем, что такая книга уже имеется.
        # Если книга отсутствует - добавляем. Иначе - пропускаем.
        # test_row_id = cur.execute('''SELECT Id FROM Books WHERE (Book_Name = :name) and
        #                                                    (Publication_Year = :year) and
        #                                                    (Publisher_Id = :publisher_id)
        #                           ''',
        #                           {**item, 'publisher_id': row_id}).fetchone()

        # Варианты синтаксиса (Operators.__and__() (Python “&” operator)):
        # https://docs.sqlalchemy.org/en/14/core/operators.html#conjunction-operators
        # вариант 1. Использование and_().
        # from sqlalchemy import and_
        #
        # stmt = select(users_table).where(
        #                 and_(
        #                     users_table.c.name == 'wendy',
        #                     users_table.c.enrolled == True
        #                 )
        #             )
        # вариант 2. Использование &.
        # stmt = select(users_table).where(
        #                 (users_table.c.name == 'wendy') &
        #                 (users_table.c.enrolled == True)
        #                 )
        #             )
        # вариант 3. Использование filter(), когда разделённые
        # запятой условия воспринимаются как связанные через AND
        # https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.filter
        # Multiple criteria may be specified as comma separated; the effect is that they
        # will be joined together using the and_() function:
        # session.query(MyClass).filter(MyClass.name == 'some name',
        #                               MyClass.id > 5)
        #
        # вариант 4. Использование вложенных filter()
        # method sqlalchemy.sql.expression.Select.filter(*criteria)
        # A synonym for the Select.where() method.
        # источник: https://docs.sqlalchemy.org/en/14/core/selectable.html#sqlalchemy.sql.expression.Select.filter
        # stmt = select(users_table).filter(
        #                            users_table.c.name == 'wendy').filter(
        #                                                           users_table.c.enrolled == True)
        #
        # вопрос-ответ по теме:
        # https://stackoverflow.com/questions/9091668/sqlalchemy-sql-expression-with-multiple-where-conditions

        test_row_id = session.query(Books.Id).filter((Books.Book_Name == item['name']) &
                                                     (Books.Publication_Year == item['year']) &
                                                     (Books.Publisher_Id == row_id)).count()
        # Метод cursor.fetchone() извлекает следующую строку из набора результатов запроса,
        # возвращая одну последовательность или None, если больше нет доступных данных.
        if test_row_id == 0:
            # cur.execute('''INSERT INTO Books (Book_Name,
            #                                   Publication_Year,
            #                                   Publisher_Id)
            #                            VALUES(:name,
            #                                   :year,
            #                                   :publisher_id)
            #             ''',
            #             # {'name': item['name'],
            #             #  'year': item['year'],
            #             #  'publisher_id': row_id})
            #             #       a = {1: 'aaa', 2: 'bbbb', 3: 'ccccc'}
            #             #       print({**a, 'publisher_id': 3})
            #             #       Вывод: {1: 'aaa', 2: 'bbbb', 3: 'ccccc', 'publisher_id': 3}
            #             {**item, 'publisher_id': row_id})
            session.add(Books(book_name=item['name'],
                              publication_year=item['year'],
                              publisher_id=row_id))
            session.commit()  # Зафиксировали изменения в БД (применение всех изменений в таблицах БД)
    # session.commit()  # Зафиксировали изменения в БД (применение всех изменений в таблицах БД)

    # заполняем таблицу Books_Authors
    # Книги требуется искать по совокупности параметров:
    # Book_Name, Publication_Year, Publisher_Id
    # Специфика в том, что книга с одним и тем же наименованием
    # и даже тем же годом может выходить в разных издательствах.
    for item in source_dict:
        # Определили код издателя.
        # cur.execute('SELECT Id FROM Publishers WHERE Publisher_Name = :publisher', item)
        rows_lst = session.query(Publishers.Id).filter(Publishers.Publisher_Name == item['publisher']).all()
        # Считаем, что с базой всё нормально и проверки на внешнее вмешательство не делаем.
        # То есть, запись присутствует и только в единственном числе.
        # Присутствует единственная запись
        # Результат такой: [(2,)]
        row_id = rows_lst[0][0]
        # row_id - это идентификатор (код) издателя в таблице Publishers.
        # cur.execute('''SELECT Id FROM Books WHERE (Book_Name = :name) and
        #                                           (Publication_Year = :year) and
        #                                           (Publisher_Id = :publisher_id)''',
        #             {**item, 'publisher_id': row_id})
        test_row_id = session.query(Books.Id).filter((Books.Book_Name == item['name']) &
                                                     (Books.Publication_Year == item['year']) &
                                                     (Books.Publisher_Id == row_id)).first()
        # Считаем, что с базой всё нормально и проверки на внешнее вмешательство не делаем.
        # То есть, запись присутствует и только в единственном числе.
        # Результат такой: (1,)
        # В отличии от метода cur.fetchall(), где результат в виде списка кортежей: [(2,)]
        book_id = test_row_id[0]

        # заполняем таблицу Authors
        for author in item['author']:
            # cur.execute('SELECT Id FROM Authors WHERE Author_Name = :author', {'author': author})
            # author_id = cur.fetchone()[0]
            test_row_id = session.query(Authors.Id).filter(Authors.Author_Name == author).first()
            author_id = test_row_id[0]
            # Проверяем - имеется ли такая запись или нет.
            # Если отсутствует, добавляем
            # cur.execute('''SELECT Id FROM Books_Authors
            #                         WHERE Book_Id = :book_id
            #                               AND
            #                               Author_Id = :author_id''',
            #             {'book_id': book_id, 'author_id': author_id})
            # row_id = cur.fetchone()
            row_id = session.query(Books_Authors.Id).filter((Books_Authors.Book_Id == book_id)
                                                            &
                                                            (Books_Authors.Author_Id == author_id)).first()

            if row_id is None:
                # cur.execute('''INSERT INTO Books_Authors (Book_Id, Author_Id)
                #                       VALUES(:book_id, :author_id)''',
                #             {'book_id': book_id, 'author_id': author_id})
                session.add(Books_Authors(book_id=book_id,
                                          author_id=author_id))
    session.commit()  # Зафиксировали изменения в БД (применение всех изменений в таблицах БД)

    # Делаем выборку только книг.
    # Формат выборки: список из кортежей, примерно так:
    # [('Удавы и питоны Уход и содержание', 2009, 'Профиздат'),
    #  ('Алгоритмы неформально. Инструкция для начинающих питонистов', 2022, 'Питер'),
    #  ('Изучаем Python. Том 1', 2019, 'Диалектика'),
    #  ('Изучаем Python. Том 2', 2020, 'Вильямс'),
    #  ...
    # ]
    # cur.execute("""SELECT
    #                   Book_Name,
    #                   Publication_Year as Year,
    #                   Publisher_Name
    #                FROM
    #                   Books
    #                   INNER JOIN Publishers ON Publisher_Id = Publishers.Id
    #             """)
    # result = session.query(Books.Book_Name,
    #                        Books.Publication_Year.label('Year'),
    #                        Books.Publisher_Name).filter((Books_Authors.Book_Id == book_id)
    #                                                     &
    #                                                     (Books_Authors.Author_Id == author_id))
    result = session.query(Books.Book_Name.label('Book_Name'),
                           Books.Publication_Year.label('Year'),
                           Publishers.Publisher_Name).join(Publishers, Books.Publisher_Id == Publishers.Id)
    print(result.statement)

    # result = session.query(Books.Book_Name,
    #                        Books.Publication_Year.label('Year'),
    #                        Books.Publisher_Name).filter((Books_Authors.Book_Id == book_id)
    #                                                     &
    #                                                     (Books_Authors.Author_Id == author_id)).all()
    # Выводим результат
    print('Работаем с колонками, а не кортежами')
    print(f"result[0]['Book_Name']: {result[0]['Book_Name']}")
    print(f"result[0]['Year']: {result[0]['Year']}")
    print(f"result[0]['Publisher_Name']: {result[0]['Publisher_Name']}")
    print('result:', result)
    print('result[0]:', result[0])
    # Перебирать можно через цикл: for item in result:
    result = result.all()
    print(result)
    print(result[0])
    print(f"result[0][0] - 'Book_Name': {result[0][0]}")
    print(f"result[0][1] - 'Year': {result[0][1]}")
    print(f"result[0][2] - 'Publisher_Name': {result[0][2]}")
    print(result)


    # Делаем выборку наименований книг и авторов.
    # Формат выборки: список из кортежей, примерно так:
    # [('Удавы и питоны Уход и содержание', 'Крицкий А.'),
    #  ('Алгоритмы неформально. Инструкция для начинающих питонистов', 'Брэдфорд Такфилд'),
    # ...
    #  ('Цель на 360. Управляй судьбой', 'Пелехатый М.
    # ]
    # cur.execute("""SELECT
    #                   Book_Name,
    #                   Author_Name
    #                FROM
    #                   Books
    #                   INNER JOIN Books_Authors ON Books.Id = Books_Authors.Book_Id
    #                   INNER JOIN Authors ON Books_Authors.Author_Id = Authors.Id
    #             """)
    # https://www.cyberforum.ru/ms-access/thread2218485.html
    # result = cur.fetchall()
    # print(result)
    result = session.query(Books.Book_Name.label('Book_Name'),
                           Authors.Author_Name.label('Author_Name')) \
                     .join(Books_Authors, Books.Id == Books_Authors.Book_Id) \
                     .join(Authors, Books_Authors.Author_Id == Authors.Id)

    # SELECT
    #        "Books"."Book_Name" AS "Book_Name",
    #        "Authors"."Author_Name" AS "Author_Name"
    # FROM
    #        "Books"
    #        JOIN "Books_Authors" ON "Books"."Id" = "Books_Authors"."Book_Id"
    #        JOIN "Authors" ON "Books_Authors"."Author_Id" = "Authors"."Id"
    print(result.statement)
    # [('Удавы и питоны Уход и содержание', 'Крицкий А.'),
    #  ('Алгоритмы неформально. Инструкция для начинающих питонистов', 'Брэдфорд Такфилд'),
    #  ('Изучаем Python. Том 1', 'Марк Лутц'),
    #  ('Изучаем Python. Том 2', 'Марк Лутц'),
    #  ('Искусственный интеллект и компьютерное зрение. Реальные проекты на Python, Keras и TensorFlow', 'Коул Анирад'),
    #  ('Искусственный интеллект и компьютерное зрение. Реальные проекты на Python, Keras и TensorFlow', 'Казам Мехер'),
    #  ('Искусственный интеллект и компьютерное зрение. Реальные проекты на Python, Keras и TensorFlow', 'Ганджу Сиддха'),
    #  ('Высокопроизводительные Python-приложения. Практическое руководство по эффективному программированию', 'Горелик Миша'),
    #  ('Высокопроизводительные Python-приложения. Практическое руководство по эффективному программированию', 'Йен Освальд'),
    #  ('Учим Python, делая крутые игры', 'Эл Свейгарт'),
    #  ('Автоматизация рутинных задач с помощью Python', 'Эл Свейгарт'),
    #  ('Простой Python. Современный стиль программирования', 'Билл Любанович'),
    #  ('Простой Python. Современный стиль программирования', 'Билл Любанович'),
    #  ('Цель на 360. Управляй судьбой', 'Пелехатый М.М.'),
    #  ('Цель на 360. Управляй судьбой', 'Спирица Е.')]
    print(result.all())
