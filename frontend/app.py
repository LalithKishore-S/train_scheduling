from flask import Flask, render_template, request, redirect, url_for
from train_scheduling.dp_solver import DPSolver
from train_scheduling.train_model import TrainSchedule, Train
from train_scheduling.config import CONFIG
import json
import os
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    schedule = TrainSchedule()

    # Load data from the uploaded file
    if file.filename.endswith('.json'):
        with open(file_path, 'r') as f:
            train_data = json.load(f)
            for train_info in train_data['trains']:
                arrival_time = datetime.strptime(train_info['arrival'], '%Y-%m-%d %H:%M:%S')
                departure_time = datetime.strptime(train_info['departure'], '%Y-%m-%d %H:%M:%S')
                train = Train(train_info['id'], arrival_time, departure_time, train_info['is_fixing'])
                schedule.add_train(train)
    
    elif file.filename.endswith('.csv'):
        df = pd.read_csv(file_path)
        for _, train_info in df.iterrows():
            arrival_time = pd.to_datetime(train_info['Arrival'])
            departure_time = pd.to_datetime(train_info['Departure'])
            train = Train(train_info['ID'], arrival_time, departure_time, train_info['Is Fixing'])
            schedule.add_train(train)

    elif file.filename.endswith('.xlsx'):
        df = pd.read_excel(file_path)
        for _, train_info in df.iterrows():
            arrival_time = pd.to_datetime(train_info['Arrival'])
            departure_time = pd.to_datetime(train_info['Departure'])
            train = Train(train_info['ID'], arrival_time, departure_time, train_info['Is Fixing'])
            schedule.add_train(train)

    else:
        return "Unsupported file format. Please upload a JSON, CSV, or Excel file.", 400

    # Solve the scheduling problem
    solver = DPSolver(schedule, CONFIG)
    solver.solve()

    # Combine fixing and non-fixing trains
    all_trains_combined = schedule.fixing_trains + schedule.non_fixing_trains

    # Sort the combined trains by arrival time
    all_trains_combined.sort(key=lambda train: train.arrival_time)

    return render_template('results.html', trains=all_trains_combined)

if __name__ == "__main__":
    app.run(debug=True)
