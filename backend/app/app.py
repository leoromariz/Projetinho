# backend/app/app.py

from flask import Flask, jsonify
from flask_cors import CORS
from backend.app.routes.social_media_usage import social_media_bp
from backend.config.settings import settings

def create_app():
    app = Flask(__name__)
    CORS(app)  # Habilita CORS para todas as origens por padrão. Considere restringir em produção.

    # Registra o Blueprint para as rotas da API
    app.register_blueprint(social_media_bp, url_prefix=settings.API_V1_STR)

    @app.route("/")
    def index():
        return jsonify({"message": f"Welcome to the {settings.PROJECT_NAME}"})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000) # O Flask por padrão roda na porta 5000