from flask import Flask, render_template

app = Flask(__name__)  # Vytvoření instance třídy Flask

# Template data
measurements = [
    {"timestamp": "2024-03-03 12:00", "temp": 20.5},
    {"timestamp": "2024-03-03 12:30", "temp": 21.0},
    {"timestamp": "2024-03-03 13:00", "temp": 20.8},
    {"timestamp": "2024-03-03 13:30", "temp": 21.2},
    {"timestamp": "2024-03-03 14:00", "temp": 20.9},
]

# View funkce pro endpoint '/login' etc. namapovani funkce login() na dir /login
@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/dashboard')
def dashboard():
    # for example
    username = "aivazart@fel.cvut.cz"
    return render_template("dashboard.html", username=username, measurements=measurements)

# Spuštění webové aplikace na adrese 0.0.0.0:3000 v debug režimu
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3000', debug=True, use_reloader=False)