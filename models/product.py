from datetime import datetime
from .database import get_db

def all_products():
    with get_db() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM products ORDER BY id").fetchall()]

def create_product(data):
    name = str(data.get("name", "")).strip()
    category = str(data.get("category", "")).strip()
    description = str(data.get("description", "")).strip()
    emoji = str(data.get("emoji", "☕")).strip() or "☕"
    try: price = float(data.get("price"))
    except (TypeError, ValueError): raise ValueError("Informe um preço válido.")
    if not name or not category or price < 0: raise ValueError("Nome, categoria e preço válido são obrigatórios.")
    with get_db() as conn:
        cur = conn.execute("INSERT INTO products(name,category,price,emoji,description,featured,active,created_at) VALUES(?,?,?,?,?,0,1,?)",
            (name,category,price,emoji,description,datetime.now().isoformat(timespec="seconds")))
        return cur.lastrowid

def set_active(product_id, active):
    with get_db() as conn:
        cur=conn.execute("UPDATE products SET active=? WHERE id=?", (1 if active else 0, product_id))
        return cur.rowcount > 0

def delete_product(product_id):
    with get_db() as conn:
        cur=conn.execute("DELETE FROM products WHERE id=?", (product_id,))
        return cur.rowcount > 0
