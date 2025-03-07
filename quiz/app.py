from flask import Flask
# from flask_bootstrap import Bootstrap5

app = Flask( __name__ )
# app.config['BOOTSTRAP_SERVE_LOCAL'] = True
# bootstrap = Bootstrap5(app)


import os.path
from flask_sqlalchemy import SQLAlchemy

def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__), 
            p)
        )

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + mkpath('./SQLAlchemy.db')
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'b517abb5-43b3-4afb-8546-6aa06af4d87c'

from flask_cors import CORS
cors = CORS(app, resources={r"/quiz/api/v1.0/*": {"origins": "*"}})

