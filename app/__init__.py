from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from app.routes.scheduler import scheduler_bp
    app.register_blueprint(scheduler_bp)
    
    return app