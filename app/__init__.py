from flask import Flask

def create_app():
    app = Flask(__name__)
    from .routes import main  # Adjusted to import the Blueprint
    app.register_blueprint(main)
    return app