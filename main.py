import sqlite3

connection = sqlite3.connect('library_system.db')
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("DROP TABLE IF EXISTS loans")
cursor.execute("DROP TABLE IF EXISTS books")
cursor.execute("DROP TABLE IF EXISTS members")

cursor.execute("""
CREATE TABLE members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    membership_type TEXT CHECK(membership_type IN ('Standard', 'Premium', 'Student')),
    join_date TEXT DEFAULT CURRENT_TIMESTAMP,
    city TEXT
)
""")

cursor.execute("""
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT,
    published_year INTEGER,
    pages INTEGER,
    is_available BOOLEAN DEFAULT 1
)
""")

cursor.execute("""
CREATE TABLE loans (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    loan_date TEXT NOT NULL,
    return_date TEXT,
    status TEXT CHECK(status IN ('active', 'returned', 'overdue')),
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
)
""")

members_data = [(f"Имя Фамилия {i}", f"user{i}@email.com", "Standard", "2024-01-01", "Москва") for i in range(1, 31)]
cursor.executemany("INSERT INTO members (full_name, email, membership_type, join_date, city) VALUES (?,?,?,?,?)", members_data)

books_data = [(f"Название книги {i}", f"Автор {i}", "Жанр", 2000 + i, 150 + i, 1) for i in range(1, 31)]
cursor.executemany("INSERT INTO books (title, author, genre, published_year, pages, is_available) VALUES (?,?,?,?,?,?)", books_data)

loans_data = [(i, i, "2024-10-01", "2024-10-15", "returned") for i in range(1, 31)]
cursor.executemany("INSERT INTO loans (member_id, book_id, loan_date, return_date, status) VALUES (?,?,?,?,?)", loans_data)

connection.commit()
connection.close()
