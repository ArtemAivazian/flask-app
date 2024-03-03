from flask import Flask, render_template

app = Flask(__name__)  # Vytvoření instance třídy Flask

# View funkce pro endpoint '/login' etc. namapovani funkce login() na dir /login
@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/dashboard')
def register():
    return render_template("dashboard.html")

# Spuštění webové aplikace na adrese 0.0.0.0:3000 v debug režimu
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3000', debug=True, use_reloader=False)