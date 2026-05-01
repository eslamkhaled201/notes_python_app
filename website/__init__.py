from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import pymysql

db = SQLAlchemy()
DB_NAME = "notesdb"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = (f"mysql+pymysql://myuser:mypassword@webserver:3306/{DB_NAME}")
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite://user:password@localhost:3306/{DB_NAME}'
    create_database_if_not_exists(DB_NAME)
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app



def create_database(app):
    # ✅ For MariaDB, you don’t check file existence — just ensure DB exists
    with app.app_context():
        db.create_all()
        print('Created Database!')

def create_database_if_not_exists(db_name):
    """Connect with root/admin and create DB if missing."""
    try:
        conn = pymysql.connect(
            host="webserver",
            user="myuser",          # use root/admin here
            password="mypassword"
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Database '{db_name}' ensured.")
    except Exception as e:
        print(f"Could not ensure database: {e}")
#def create_database(app):
#    if not path.exists('website/' + DB_NAME):
#        db.create_all(app=app)
#        print('Created Database!')
