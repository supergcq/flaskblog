# coding:utf-8
from flask_script import Manager

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()