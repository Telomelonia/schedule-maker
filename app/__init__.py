from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    from .routes.scheduler import scheduler_bp
    app.register_blueprint(scheduler_bp, url_prefix='/scheduler')

    return app
