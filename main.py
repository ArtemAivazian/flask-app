from flask import Flask
from api_routes import init_api

app = Flask(__name__)

init_api(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True, use_reloader=False)
