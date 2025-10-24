from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re
import os

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Model paths
MODEL_PATH = 'simple_model.pkl'
VECTORIZER_PATH = 'simple_vectorizer.pkl'

# Global variables
model = None
vectorizer = None

def load_model():
    """Load the trained model and vectorizer"""
    global model, vectorizer
    try:
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
        print("✓ Model and vectorizer loaded successfully")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

def clean_text(text):
    """Clean input text"""
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })

@app.route('/api/predict', methods=['OPTIONS'])
def handle_options():
    response = jsonify({'status': 'ok'})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict if news is fake or real"""
    if model is None or vectorizer is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text or len(text.strip()) < 10:
            return jsonify({'error': 'Text too short'}), 400
        
        # Clean and predict
        cleaned = clean_text(text)
        vec = vectorizer.transform([cleaned])
        prediction = model.predict(vec)[0]
        proba = model.predict_proba(vec)[0]
        
        return jsonify({
            'prediction': 'REAL' if prediction == 1 else 'FAKE',
            'confidence': float(max(proba) * 100),
            'probabilities': {
                'fake': float(proba[0] * 100),
                'real': float(proba[1] * 100)
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("FAKE NEWS DETECTION API")
    print("="*60)
    
    if load_model():
        print("\n✓ API ready!")
        print("Starting Flask server on http://localhost:5000")
        print("="*60 + "\n")
        app.run(debug=True, port=5000, host='0.0.0.0')
    else:
        print("\n❌ Failed to start. Please check the error above.")
        print("="*60 + "\n")