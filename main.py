from flask import Flask
from api_routes import init_api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "SECRET KEY"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
init_api(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True, use_reloader=False)
