# encoding: utf-8

from app import app
from app import db

if __name__ == '__main__':
    db.create_all()
    app.run(threaded = True, debug = True)
