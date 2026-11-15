import os
from flask import Flask
from models.database import init_db
from controllers.routes import routes

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("CAFE_SECRET_KEY", "chave-local-de-demonstracao-trocar-em-producao")
    app.register_blueprint(routes)
    return app

app = create_app()

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)
