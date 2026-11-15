from datetime import datetime
from .database import get_db

STATUSES = {"Recebido", "Em preparo", "Pronto para retirada", "Saiu para entrega", "Concluído", "Cancelado"}

def all_orders():
    with get_db() as conn:
        orders = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
        result = []
        for order in orders:
            item_rows = conn.execute("SELECT product_name,unit_price,quantity FROM order_items WHERE order_id=?", (order["id"],)).fetchall()
            item = dict(order)
            item["items"] = [dict(x) for x in item_rows]
            result.append(item)
        return result

def find_customer_order(order_id, phone):
    # Consulta restrita: o cliente precisa informar o número do pedido e o telefone cadastrado.
    digits = "".join(ch for ch in str(phone) if ch.isdigit())
    with get_db() as conn:
        row = conn.execute("SELECT id, customer_name, phone, subtotal, delivery_fee, total, status, created_at FROM orders WHERE id=?", (order_id,)).fetchone()
        if not row or "".join(ch for ch in row["phone"] if ch.isdigit()) != digits:
            return None
        result = dict(row)
        result["items"] = [dict(x) for x in conn.execute("SELECT product_name,unit_price,quantity FROM order_items WHERE order_id=?", (order_id,)).fetchall()]
        return result

def create_order(data):
    name = str(data.get("name", "")).strip()
    phone = str(data.get("phone", "")).strip()
    address = str(data.get("address", "")).strip()
    note = str(data.get("note", "")).strip()
    items = data.get("items", [])
    if not name or not phone or not address or not isinstance(items, list) or not items:
        raise ValueError("Preencha nome, telefone, endereço e adicione pelo menos um produto.")
    with get_db() as conn:
        subtotal = 0.0
        valid = []
        for item in items:
            try:
                product_id = int(item.get("product_id"))
                quantity = int(item.get("quantity"))
            except (TypeError, ValueError, AttributeError):
                raise ValueError("Item do pedido inválido.")
            if quantity < 1:
                raise ValueError("A quantidade deve ser maior que zero.")
            product_row = conn.execute("SELECT id,name,price FROM products WHERE id=? AND active=1", (product_id,)).fetchone()
            if not product_row:
                raise ValueError("Um dos produtos não está disponível.")
            subtotal += product_row["price"] * quantity
            valid.append((product_row["id"], product_row["name"], product_row["price"], quantity))
        fee = 5.00
        total = subtotal + fee
        cur = conn.execute("INSERT INTO orders(customer_name,phone,address,note,subtotal,delivery_fee,total,status,created_at) VALUES(?,?,?,?,?,?,?,?,?)",
            (name, phone, address, note, subtotal, fee, total, "Recebido", datetime.now().strftime("%d/%m/%Y %H:%M")))
        order_id = cur.lastrowid
        conn.executemany("INSERT INTO order_items(order_id,product_id,product_name,unit_price,quantity) VALUES(?,?,?,?,?)",
            [(order_id, pid, pname, price, qty) for pid, pname, price, qty in valid])
        return order_id

def update_status(order_id, status):
    if status not in STATUSES:
        raise ValueError("Status inválido.")
    with get_db() as conn:
        cur = conn.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))
        return cur.rowcount > 0
