import sqlite3
import hashlib
import tkinter as tk
from tkinter import messagebox, simpledialog

# Database Connection
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create Tables (Users & Books)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    available INTEGER DEFAULT 1
)
''')

conn.commit()

# Function to Hash Passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to Add a New User (Run Once, Then Comment Out)
def add_user(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        print(f"✅ User '{username}' added successfully!")
    except sqlite3.IntegrityError:
        print(f"❌ Username '{username}' already exists!")

# Uncomment to Add Users (Run Once, Then Comment It Out)
add_user("admin", "admin123")
add_user("librarian", "lib123")

# Function to Handle Login
def login():
    username = entry_username.get()
    password = entry_password.get()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result and hash_password(password) == result[0]:
        messagebox.showinfo("Login Success", f"Welcome, {username}!")
        login_window.destroy()
        open_library_menu(username)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Function to Add a Book
def add_book():
    title = simpledialog.askstring("Add Book", "Enter book title:")
    author = simpledialog.askstring("Add Book", "Enter author name:")
    
    if title and author:
        cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
        conn.commit()
        messagebox.showinfo("Success", "Book added successfully!")

# Function to View Books
def view_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    
    if books:
        book_list = "\n".join([f"{book[0]}. {book[1]} by {book[2]} - {'Available' if book[3] else 'Borrowed'}" for book in books])
    else:
        book_list = "No books available."

    messagebox.showinfo("Books Available", book_list)

# Function to Borrow a Book
def borrow_book():
    book_id = simpledialog.askinteger("Borrow Book", "Enter book ID to borrow:")
    
    cursor.execute("SELECT available FROM books WHERE id=?", (book_id,))
    book = cursor.fetchone()
    
    if book and book[0] == 1:
        cursor.execute("UPDATE books SET available=0 WHERE id=?", (book_id,))
        conn.commit()
        messagebox.showinfo("Success", "Book borrowed successfully!")
    else:
        messagebox.showerror("Error", "Book not available.")

# Function to Return a Book
def return_book():
    book_id = simpledialog.askinteger("Return Book", "Enter book ID to return:")
    
    cursor.execute("SELECT available FROM books WHERE id=?", (book_id,))
    book = cursor.fetchone()
    
    if book and book[0] == 0:
        cursor.execute("UPDATE books SET available=1 WHERE id=?", (book_id,))
        conn.commit()
        messagebox.showinfo("Success", "Book returned successfully!")
    else:
        messagebox.showerror("Error", "Invalid book ID or already returned.")

# Function to Delete a Book (Admin only)
def delete_book():
    book_id = simpledialog.askinteger("Delete Book", "Enter book ID to delete:")
    
    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    messagebox.showinfo("Success", "Book deleted successfully!")

# Function to Open Library Menu
def open_library_menu(username):
    menu_window = tk.Tk()
    menu_window.title("Library Management System - Menu")
    menu_window.geometry("400x350")

    label_welcome = tk.Label(menu_window, text=f"Welcome, {username}!", font=("Arial", 14))
    label_welcome.pack(pady=10)

    btn_view_books = tk.Button(menu_window, text="View Books", command=view_books)
    btn_view_books.pack(pady=5)

    btn_borrow = tk.Button(menu_window, text="Borrow a Book", command=borrow_book)
    btn_borrow.pack(pady=5)

    btn_return = tk.Button(menu_window, text="Return a Book", command=return_book)
    btn_return.pack(pady=5)

    if username == "admin" or username == "librarian":
        btn_add_book = tk.Button(menu_window, text="Add Book", command=add_book)
        btn_add_book.pack(pady=5)

        btn_delete_book = tk.Button(menu_window, text="Delete Book", command=delete_book)
        btn_delete_book.pack(pady=5)

    btn_logout = tk.Button(menu_window, text="Logout", command=menu_window.destroy)
    btn_logout.pack(pady=10)

    menu_window.mainloop()

# GUI for Login
login_window = tk.Tk()
login_window.title("Library Management System - Login")
login_window.geometry("300x200")

label_username = tk.Label(login_window, text="Username:")
label_username.pack()
entry_username = tk.Entry(login_window)
entry_username.pack()

label_password = tk.Label(login_window, text="Password:")
label_password.pack()
entry_password = tk.Entry(login_window, show="*")
entry_password.pack()

btn_login = tk.Button(login_window, text="Login", command=login)
btn_login.pack(pady=10)

login_window.mainloop()
