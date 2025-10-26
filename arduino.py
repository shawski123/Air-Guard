from flask import Flask, render_template, jsonify, request
import serial, time, random
from ai import get_ai_response

app = Flask(__name__)

pm25_value = 10
prev_temp = prev_humidity = prev_heat_index = prev_pm25 = None

port = '/dev/ttyACM0'
baud_rate = 9600
ser = serial.Serial(port, baud_rate, timeout=1)
time.sleep(2)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data')
def data():
    global pm25_value, prev_temp, prev_humidity, prev_pm25, prev_heat_index

    line = ser.readline().decode('utf-8').strip()
    pm25_value += random.uniform(-2, 2)
    pm25_value = max(0, min(150, pm25_value))

    try:
        parts = line.split(",")
        humidity = float(parts[0])
        temp = float(parts[1])
        heat_index = float(parts[2])
    except:
        return jsonify({'humidity': None, 'temperature': None, 'heat_index': None, 'pm25': None, 'ai_message': None})

    ai_message = None
    if prev_temp is not None:
        if (
            abs(temp - prev_temp) > 5 or
            abs(humidity - prev_humidity) > 10 or
            abs(pm25_value - prev_pm25) > 15 or
            abs(heat_index - prev_heat_index) > 6
        ):
            ai_message = get_ai_response("Monitor change alert", temp, humidity, heat_index, pm25_value)

    prev_temp, prev_humidity, prev_pm25, prev_heat_index = temp, humidity, pm25_value, heat_index

    return jsonify({
        'temperature': temp,
        'humidity': humidity,
        'heat_index': heat_index,
        'pm25': pm25_value,
        'ai_message': ai_message
    })

@app.route("/ask_ai", methods=["POST"])
def ask_ai():
    data = request.get_json()
    question = data.get("question", "")
    global prev_temp, prev_humidity, prev_heat_index, prev_pm25

    answer = get_ai_response(
        question,
        prev_temp or 0,
        prev_humidity or 0,
        prev_heat_index or 0,
        prev_pm25 or 0
    )
    # Return field named "response" to match your frontend
    return jsonify({"response": answer})


if __name__ == "__main__":
    app.run(debug=True)
