from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

database_name = "trivia"
database_path = "postgres://{}@{}/{}".format('zachariah:123456','localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app,db)
    db.create_all()