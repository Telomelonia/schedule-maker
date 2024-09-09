from flask import Flask, redirect, url_for

def create_app():
    app = Flask(__name__,static_folder='static', static_url_path='/static')
    app.secret_key = 'random@123'
    
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    @app.before_first_request
    def before_first_request():
        # Clear session data
        with app.app_context():
            from flask import session
            session.clear()
    
    return app