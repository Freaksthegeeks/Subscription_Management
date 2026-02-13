from flask import Flask
from config import SECRET_KEY
import os
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.client_routes import client_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(client_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT', 10000)))
