from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from routes.datos_endpoint import datos_bp
from routes.auth_endpoints import auth_bp

load_dotenv()

app = Flask(__name__)
CORS(app)

# Registrar rutas
app.register_blueprint(datos_bp)
app.register_blueprint(auth_bp)

@app.route('/')
def home():
    return {
        "message": "JSON de Talento Universitario",
        "endpoints": [
            "/api/datos-json",
            "/admin/create-user"
        ]
    }

# Esto solo se usa en local
if __name__ == '__main__':
    app.run(debug=True)