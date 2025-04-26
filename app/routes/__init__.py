def register_routes(app):
    from .main import main_bp
    from .auth import auth_bp
    from .admin_dashboard import admin_dashboard_bp
    from .user_dashboard import user_dashboard_bp
    from .users import users_bp
    from .admin_users import admin_users_bp
    from .admin_entreprise import admin_enterprises_bp
    from .tickets import tickets_bp
    from .messages import messages_bp
    from .prediction import prediction_bp
    from .monitoring import monitoring_bp
    from .admin_tickets import admin_tickets_bp
    from .user_tickets import user_tickets_bp
    from .admin_chat import admin_chat_bp
    from .user_chat import user_chat_bp
    

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_dashboard_bp)
    app.register_blueprint(user_dashboard_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(admin_users_bp)
    app.register_blueprint(admin_enterprises_bp)
    app.register_blueprint(admin_tickets_bp)
    app.register_blueprint(user_tickets_bp)
    app.register_blueprint(admin_chat_bp)
    app.register_blueprint(user_chat_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(monitoring_bp)
