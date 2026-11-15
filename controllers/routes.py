from flask import Blueprint, render_template, request, jsonify
from models import product, order

routes = Blueprint("main", __name__)

@routes.get("/")
def index(): return render_template("index.html")

@routes.get("/api/products")
def products_list(): return jsonify(product.all_products())

@routes.post("/api/products")
def products_create():
    try: return jsonify(id=product.create_product(request.get_json(silent=True) or {}), message="Produto cadastrado."), 201
    except ValueError as e: return jsonify(error=str(e)), 400

@routes.patch("/api/products/<int:product_id>")
def products_update(product_id):
    data=request.get_json(silent=True) or {}
    if "active" not in data: return jsonify(error="Nenhuma alteração informada."), 400
    if not product.set_active(product_id,data["active"]): return jsonify(error="Produto não encontrado."), 404
    return jsonify(message="Produto atualizado.")

@routes.delete("/api/products/<int:product_id>")
def products_delete(product_id):
    if not product.delete_product(product_id): return jsonify(error="Produto não encontrado."), 404
    return jsonify(message="Produto excluído.")

@routes.get("/api/orders")
def orders_list(): return jsonify(order.all_orders())

@routes.post("/api/orders")
def orders_create():
    try: return jsonify(id=order.create_order(request.get_json(silent=True) or {}), message="Pedido registrado com sucesso."), 201
    except ValueError as e: return jsonify(error=str(e)), 400

@routes.patch("/api/orders/<int:order_id>")
def orders_update(order_id):
    data=request.get_json(silent=True) or {}
    try:
        if not order.update_status(order_id,data.get("status")): return jsonify(error="Pedido não encontrado."), 404
    except ValueError as e: return jsonify(error=str(e)), 400
    return jsonify(message="Status atualizado.")
