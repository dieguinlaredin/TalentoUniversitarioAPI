from flask import Flask, redirect
from routes.datos_endpoint import datos_bp
from routes.auth_endpoints import auth_bp

app = Flask(__name__)

# Registrar rutas
app.register_blueprint(datos_bp)
app.register_blueprint(auth_bp)

@app.route('/')
def home():
    return redirect('/api/datos-json')

# Esto solo se usa en local
if __name__ == '__main__':
    app.run(debug=True)