from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'random@123'
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
