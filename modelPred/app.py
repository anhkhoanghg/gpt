from flask import Flask
from main import GetPrediction, OrderingTask
import os
import subprocess
from flask import Flask, jsonify, render_template, request, json
from os import system, chdir
import pandas as pd
app = Flask(__name__)


get_prediction_instance = GetPrediction()
ordering_task_instance = OrderingTask()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        entry = data['entry']
        result = get_prediction_instance.predict(entry)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/order_tasks', methods=['POST'])
def order_tasks():
    try:
        data = request.json
        task_list = data['tasks']
        result = ordering_task_instance.ordering(task_list)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
