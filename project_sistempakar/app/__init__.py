from flask import Flask, render_template, request, session, redirect, url_for
from app.config import Config
from app.utils.settings import get_settings

def create_app():
    # Set template and static folder to the root project directory
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)

    from app.controllers.main_controller import main_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.admin_controller import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_settings():
        return dict(app_settings=get_settings())
        
    @app.before_request
    def check_maintenance():
        settings = get_settings()
        
        # Bypass maintenance for static files and admin/auth routes
        if request.path.startswith('/static') or request.path.startswith('/admin') or request.path.startswith('/login') or request.path.startswith('/logout'):
            return None
            
        # Admin can access normal pages even in maintenance mode
        if session.get('role') == 'admin':
            return None
            
        if settings.get('maintenance_mode', False) and request.path != '/maintenance':
            return redirect(url_for('maintenance'))

    @app.route('/maintenance')
    def maintenance():
        settings = get_settings()
        if not settings.get('maintenance_mode', False):
            return redirect(url_for('main.index') if not session.get('role') else url_for('main.diagnosis'))
        return render_template('maintenance.html')

    @app.after_request
    def add_header(response):
        # Jangan disable cache untuk file statis (CSS/JS/Gambar)
        if request.path.startswith('/static'):
            return response
            
        # Mencegah browser menyimpan cache halaman (Fix bug tombol Back setelah Logout)
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return app
