import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "cafe_gourmet.db"

SEED_PRODUCTS = [
    ("Cappuccino da casa", "Cafés", 12.90, "☕", "Café espresso com leite vaporizado e toque de chocolate.", 1),
    ("Café espresso", "Cafés", 7.50, "☕", "Intenso, encorpado e preparado na hora.", 1),
    ("Mocha cremoso", "Cafés", 14.50, "🍫", "A combinação de café, leite e chocolate.", 1),
    ("Chá gelado", "Bebidas", 9.00, "🧋", "Bebida refrescante e saborosa.", 0),
    ("Suco natural", "Bebidas", 10.00, "🧃", "Suco preparado com fruta.", 0),
    ("Croissant", "Lanches", 11.90, "🥐", "Massa leve e crocante.", 0),
    ("Sanduíche artesanal", "Lanches", 18.90, "🥪", "Pão macio com recheio preparado na casa.", 0),
    ("Brownie", "Sobremesas", 10.50, "🍰", "Brownie de chocolate com textura macia.", 0),
    ("Cheesecake", "Sobremesas", 15.00, "🍰", "Sobremesa cremosa com base crocante.", 0),
]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with get_db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, category TEXT NOT NULL,
            price REAL NOT NULL CHECK(price >= 0), emoji TEXT DEFAULT '☕', description TEXT,
            featured INTEGER NOT NULL DEFAULT 0, active INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT, customer_name TEXT NOT NULL, phone TEXT NOT NULL,
            address TEXT NOT NULL, note TEXT, subtotal REAL NOT NULL, delivery_fee REAL NOT NULL,
            total REAL NOT NULL, status TEXT NOT NULL DEFAULT 'Recebido', created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER NOT NULL, product_id INTEGER,
            product_name TEXT NOT NULL, unit_price REAL NOT NULL, quantity INTEGER NOT NULL CHECK(quantity > 0),
            FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE SET NULL
        );
        """)
        if conn.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
            now = datetime.now().isoformat(timespec="seconds")
            conn.executemany("INSERT INTO products(name,category,price,emoji,description,featured,active,created_at) VALUES(?,?,?,?,?,?,1,?)",
                [(n,c,p,e,d,f,now) for n,c,p,e,d,f in SEED_PRODUCTS])
