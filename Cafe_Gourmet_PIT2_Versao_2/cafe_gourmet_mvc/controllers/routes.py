import os
from functools import wraps
from flask import Blueprint, render_template, request, jsonify, session
from models import product, order

routes = Blueprint("main", __name__)

def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return jsonify(error="Acesso restrito. Entre com a conta administrativa."), 401
        return function(*args, **kwargs)
    return wrapper

@routes.get("/")
def index():
    return render_template("index.html")

@routes.get("/api/session")
def session_status():
    return jsonify(logged_in=bool(session.get("admin_logged_in")))

@routes.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    username = os.environ.get("CAFE_ADMIN_USER", "admin")
    password = os.environ.get("CAFE_ADMIN_PASSWORD", "cafe123")
    if data.get("username") == username and data.get("password") == password:
        session["admin_logged_in"] = True
        return jsonify(message="Login realizado com sucesso.")
    return jsonify(error="Usuário ou senha incorretos."), 401

@routes.post("/api/logout")
def logout():
    session.clear()
    return jsonify(message="Você saiu do painel administrativo.")

@routes.get("/api/products")
def products_list():
    return jsonify(product.all_products())

@routes.post("/api/products")
@admin_required
def products_create():
    try:
        return jsonify(id=product.create_product(request.get_json(silent=True) or {}), message="Produto cadastrado."), 201
    except ValueError as e:
        return jsonify(error=str(e)), 400

@routes.patch("/api/products/<int:product_id>")
@admin_required
def products_update(product_id):
    data = request.get_json(silent=True) or {}
    if "active" not in data:
        return jsonify(error="Nenhuma alteração informada."), 400
    if not product.set_active(product_id, data["active"]):
        return jsonify(error="Produto não encontrado."), 404
    return jsonify(message="Produto atualizado.")

@routes.delete("/api/products/<int:product_id>")
@admin_required
def products_delete(product_id):
    if not product.delete_product(product_id):
        return jsonify(error="Produto não encontrado."), 404
    return jsonify(message="Produto excluído.")

@routes.get("/api/orders")
@admin_required
def orders_list():
    return jsonify(order.all_orders())

@routes.get("/api/orders/<int:order_id>/tracking")
def order_tracking(order_id):
    phone = request.args.get("phone", "")
    result = order.find_customer_order(order_id, phone)
    if not result:
        return jsonify(error="Não encontramos um pedido com esses dados. Confira o número e o telefone."), 404
    return jsonify(result)

@routes.post("/api/orders")
def orders_create():
    try:
        order_id = order.create_order(request.get_json(silent=True) or {})
        return jsonify(id=order_id, message="Pedido registrado com sucesso."), 201
    except ValueError as e:
        return jsonify(error=str(e)), 400

@routes.patch("/api/orders/<int:order_id>")
@admin_required
def orders_update(order_id):
    data = request.get_json(silent=True) or {}
    try:
        if not order.update_status(order_id, data.get("status")):
            return jsonify(error="Pedido não encontrado."), 404
    except ValueError as e:
        return jsonify(error=str(e)), 400
    return jsonify(message="Status atualizado.")
