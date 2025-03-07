from flask import Flask, request, jsonify, render_template
import requests
from query_from_api import run_query_from_api

app = Flask(__name__, template_folder='templates', static_folder='static')

# URL của ngrok trên Kaggle
kaggle_base_url = 'https://6c7e-35-185-201-212.ngrok-free.app/'

# Endpoint để gọi model trên Kaggle
@app.route('/predict', methods=['POST'])
def call_kaggle_predict():
    input_data = request.json.get('input_text', '')

    try:
        response = requests.post(f"{kaggle_base_url}/predict", json={'input_text': input_data})
        #print(response.json())
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(response.json())

# Endpoint để gọi generate_answer trên Kaggle
@app.route('/generate_answer', methods=['POST'])
def call_kaggle_generate_query():
    data = request.json
    question = data.get('question', '')
   
    try:
        response = requests.post(f"{kaggle_base_url}/generate_answer", json={'question': question})
        response.raise_for_status()
        api_response = response.json()
        
        print("📌 API Response từ Kaggle:", api_response)  # Debug log

       
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
    
    return jsonify(api_response)

# Endpoint giao diện chat
@app.route('/')
def chat():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
