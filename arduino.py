from flask import Flask, render_template, jsonify
import serial
import time
import random

app = Flask(__name__)

pm25_value = 10

port = '/dev/ttyACM0'
baud_rate = 9600

ser = serial.Serial(port, baud_rate, timeout = 1)
time.sleep(2)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data')
def data():
    line = ser.readline().decode('utf-8').strip()

    global pm25_value

    pm25_value += random.uniform(-2,2)
    pm25_value = max(0, min(150, pm25_value))

    try:
        parts = line.split(",")

        humidity = float(parts[0])
        temp = float(parts[1])
        heat_index = float(parts[2])
        return jsonify({'humidity': humidity, 
                        'temperature': temp, 
                        'heat_index': heat_index,
                        'pm25': pm25_value})
    except:
        return jsonify({'humidity': None, 
                        'temperature': None,
                        'heat_index': None,
                        'pm25': None})

if __name__ == "__main__":
    app.run(debug=True)