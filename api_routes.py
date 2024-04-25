from flask import request, jsonify, abort, render_template
from datetime import datetime
import logging
from config import measurements


logging.basicConfig(level=logging.INFO)

# Funkce API:
def init_api(app):

    #Vložení hodnoty {“timestamp”: value, “temp”: value} pomocí vhodně zvolené metody. 
    @app.route('/api/measurements', methods=['POST'])
    def add_measurement():
        data = request.json
        if not data or 'temp' not in data:
            abort(400, description="Missing 'temp' in request body.")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_measurement = {
            'timestamp': timestamp, 
            'temp': data['temp']
        }
        measurements.append(new_measurement)
        logging.info(f"New measurement added: {new_measurement}")  
        return jsonify(measurements[-1]), 201


    #Získání poslední hodnoty {“timestamp”: value, “temp”: value}.
    @app.route('/api/measurements/last', methods=['GET'])
    def get_last_measurement():
        if measurements:
            last_measurement = measurements[-1]
            logging.info(f"Fetching the last measurement: {last_measurement}")
            return jsonify(measurements[-1]), 200
        else:
            return jsonify({"error": "No measurements available"}), 404

    # Získání posledních X naměřených hodnot.
    @app.route('/api/measurements/last/<int:num>', methods=['GET'])
    def get_last_x_measurements(num):
        if num <= 0:
            return jsonify({"error": "Number must be a positive"}), 400
        logging.info(f"Fetching the last {num} measurements.")
        return jsonify(measurements[-num:]), 200

    # Smazání nejstarších Y naměřených hodnot.
    @app.route('/api/measurements/delete_oldest/<int:num>', methods=['DELETE'])
    def delete_oldest_measurements(num):
        if num <= 0:
            return jsonify({"error": "Number must be a positive integer"}), 400
        if num > len(measurements):
            return jsonify({"error": "Number exceeds the number of stored measurements"}), 400
        logging.info(f"Deleting the oldest {num} measurements.")
        del measurements[:num]
        return jsonify({"message": f"Deleted oldest {num} measurements"}), 200

    #show login page
    @app.route('/login')
    def login():
        return render_template("login.html")

    #show register page
    @app.route('/register')
    def register():
        return render_template("register.html")

    #show dashboard
    @app.route('/dashboard')
    def dashboard():
        from config import measurements
        username = "aivazart@fel.cvut.cz"
        return render_template("dashboard.html", username=username, measurements=measurements)

