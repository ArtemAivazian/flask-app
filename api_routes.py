import logging
import serial
from datetime import datetime

from flask import request, jsonify, abort, render_template, redirect

from models import User, Measurements

from utils import update_setting


logging.basicConfig(level=logging.INFO)


# Funkce API:
def register_routes(app, db, bcrypt):
    @app.route('/api/settings/sending-period', methods=['POST'])
    def update_sending_period():
        data = request.json
        if 'sending_period' not in data:
            abort(400, description="Missing 'sending_period' in request body.")

        sending_period = data['sending_period']

        port = '/dev/tty.usbmodem1101'
        baudrate = 115200
        serial_connection = serial.Serial(port, baudrate)
        # Assuming you have a function or method to update settings
        update_setting('sending_period', sending_period, serial_connection)  # Update the setting

        logging.info(f'Sending period updated to: {sending_period} seconds')
        return jsonify({"message": "Sending period updated successfully"}), 200

    #Vložení hodnoty {“timestamp”: value, “temp”: value} pomocí vhodně zvolené metody.
    @app.route('/api/measurements', methods=['POST'])
    def add_measurement():
        data = request.json
        if not data or 'temp' not in data:
            abort(400, description="Missing 'temp' in request body.")
        timestamp = datetime.now()
        temp = data['temp']

        new_measurement = Measurements(timestamp=timestamp, temp=temp)
        db.session.add(new_measurement)
        db.session.commit()
        logging.info(f'New measurement added: {new_measurement}')
        return jsonify({
            'measurement_id': new_measurement.measurement_id,
            'timestamp': new_measurement.timestamp.strftime("%Y-%m-%d %H:%M"),
            'temp': new_measurement.temp
        }), 201

    #Získání poslední hodnoty {“timestamp”: value, “temp”: value}.
    @app.route('/api/measurements/last', methods=['GET'])
    def get_last_measurement():
        last_measurement = Measurements.query \
            .order_by(Measurements.timestamp.desc()).first()
        if last_measurement:
            measurement_data = {
                'timestamp': last_measurement.timestamp.strftime('%Y-%m-%d %H:%M'),
                'temp': last_measurement.temp
            }
            logging.info(f'Fetching the last measurement: {last_measurement}')
            return jsonify(measurement_data), 200
        else:
            return jsonify({'error': 'No measurements available'}), 404

    # Získání posledních X naměřených hodnot.
    @app.route('/api/measurements/last/<int:num>', methods=['GET'])
    def get_last_x_measurements(num):
        if num <= 0:
            return jsonify({"error": "Number must be a positive"}), 400

        last_measurements = Measurements.query \
            .order_by(Measurements.timestamp.desc()).limit(num).all()

        if last_measurements:
            measurements_data = [{
                "timestamp": measurement.timestamp.strftime("%Y-%m-%d %H:%M"),
                "temp": measurement.temp
            } for measurement in last_measurements]
            logging.info(f"Fetching the last {num} measurements.")
            return jsonify(measurements_data), 200
        else:
            return jsonify({"error": "No measurements available"}), 404

    # Smazání nejstarších Y naměřených hodnot.
    @app.route('/api/measurements/delete_oldest/<int:num>', methods=['DELETE'])
    def delete_oldest_measurements(num):
        if num <= 0:
            return jsonify({"error": "Number must be a positive integer"}), 400

        oldest_measurements = Measurements.query \
            .order_by(Measurements.timestamp.asc()) \
            .limit(num).all()

        if not oldest_measurements or len(oldest_measurements) < num:
            return jsonify({"error": "Not enough measurements to delete"}), 404

        for measurement in oldest_measurements:
            db.session.delete(measurement)
        db.session.commit()

        logging.info(f"Deleted the oldest {num} measurements.")
        return jsonify({"message": f"Deleted oldest {num} measurements"}), 200

    @app.route('/api/dashboard')
    def dashboard():
        username = 'username@cvut.cz'

        return render_template("dashboard.html", username=username)

    @app.route('/api/login', methods=['POST', 'GET'])
    def login():
        if request.method == 'GET':
            return render_template("login.html")
        elif request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            user = User.query.filter_by(email=email).first()

            if not user:
                return jsonify({"error": "Invalid email or password"}), 401

            if bcrypt.check_password_hash(user.password, password):
                return redirect('/api/dashboard')
            else:
                return jsonify({"error": "Invalid email or password"}), 401

    @app.route('/api/logout')
    def logout():
        return redirect('/api/login')

    @app.route('/api/register', methods=['POST', 'GET'])
    def register():
        if request.method == 'GET':
            return render_template("register.html")
        elif request.method == 'POST':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            #check if user with email already exists

            user = User.query.filter_by(email=email).first()
            if user:
                return jsonify({"error": "Email already registered"}), 400

            if password != confirm_password:
                return jsonify({"error": "Passwords do not match"}), 400

            # hash password
            hashed_password = bcrypt.generate_password_hash(password)

            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()

            return redirect('/api/login')

    @app.route('/api/delete/<uid>', methods=['DELETE'])
    def delete_user(uid):
        User.query.filter_by(id=uid).delete()

        db.session.commit()

    @app.route('/')
    def users():
        all_users = User.query.all()
        return str(all_users)
