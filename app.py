from flask import Flask
from main import GetPrediction, OrderingTask
import os
from flask import Flask, jsonify, render_template, request, json
from flask_cors import CORS

import pandas as pd
app = Flask(__name__)
CORS(app)

get_prediction_instance = GetPrediction()
ordering_task_instance = OrderingTask()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # data = request.json
        data = request.get_json()

        # Check if the 'entry' key is present in the JSON data
        if 'entry' not in data:
            return jsonify({'error': 'Missing entry key in JSON data'})

        entry = data['entry']
        result = get_prediction_instance.predict(entry)
        print(entry)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})
    


@app.route('/order_tasks', methods=['POST'])
def order_tasks():
    try:
        data = request.get_json()
        task_list = data['entry']
        result = ordering_task_instance.ordering(task_list)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
