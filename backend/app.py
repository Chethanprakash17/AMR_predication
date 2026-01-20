"""
AMR Risk Prediction - Flask Backend Application
Serves HTML templates and provides prediction API endpoints
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from model import get_model

# Initialize Flask app
app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

# Enable CORS for local development
CORS(app)

# Load ML model
model = get_model()


# ==================== Web Page Routes ====================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/about-amr')
def about_amr():
    """About AMR page"""
    return render_template('about_amr.html')

@app.route('/dataset')
def dataset():
    """Dataset & Methodology page"""
    return render_template('dataset.html')

@app.route('/prediction')
def prediction():
    """Prediction Demo page"""
    return render_template('prediction.html')

@app.route('/explainability')
def explainability():
    """Explainability page"""
    return render_template('explainability.html')

@app.route('/results')
def results():
    """Results & Evaluation page"""
    return render_template('results.html')

@app.route('/limitations')
def limitations():
    """Limitations & Ethics page"""
    return render_template('limitations.html')

@app.route('/team')
def team():
    """Team & References page"""
    return render_template('team.html')


# ==================== API Routes ====================

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict AMR risk for a patient
    
    Request Body (JSON):
        {
            "age": 65,
            "gender": "M",
            "admission_type": "EMERGENCY",
            "diabetes": 1,
            "ckd": 0,
            "copd": 0,
            "cancer": 0,
            "immunosuppression": 0,
            "prior_antibiotics": 1,
            "broad_spectrum": 1,
            "heart_rate": 95,
            "temperature": 38.5,
            "systolic_bp": 110,
            "diastolic_bp": 70,
            "spo2": 94,
            "wbc": 14.5,
            "creatinine": 1.8,
            "lactate": 2.5,
            "mechanical_ventilation": 1
        }
    
    Response (JSON):
        {
            "amr_risk_probability": 0.72,
            "risk_category": "High",
            "confidence_score": 0.82,
            "message": "Prediction successful"
        }
    """
    try:
        # Get patient data from request
        patient_data = request.get_json()
        
        if not patient_data:
            return jsonify({
                'error': 'No patient data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['age', 'gender', 'admission_type']
        missing_fields = [field for field in required_fields if field not in patient_data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Get prediction from model
        prediction_result = model.predict_amr_risk(patient_data)
        
        # Add success message
        prediction_result['message'] = 'Prediction successful'
        
        return jsonify(prediction_result), 200
        
    except Exception as e:
        app.logger.error(f'Prediction error: {str(e)}')
        return jsonify({
            'error': 'An error occurred during prediction',
            'details': str(e)
        }), 500


@app.route('/api/feature-importance', methods=['GET'])
def feature_importance():
    """
    Get feature importance scores from the model
    
    Response (JSON):
        {
            "feature_importance": [
                {"feature": "prior_antibiotics", "importance": 0.18},
                {"feature": "broad_spectrum", "importance": 0.15},
                ...
            ]
        }
    """
    try:
        importance_list = model.get_feature_importance()
        
        # Format as list of dictionaries
        formatted_importance = [
            {'feature': feature, 'importance': score}
            for feature, score in importance_list
        ]
        
        return jsonify({
            'feature_importance': formatted_importance
        }), 200
        
    except Exception as e:
        app.logger.error(f'Feature importance error: {str(e)}')
        return jsonify({
            'error': 'An error occurred retrieving feature importance'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'AMR Risk Prediction API is running'
    }), 200


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    app.logger.error(f'Internal error: {error}')
    return jsonify({
        'error': 'Internal server error'
    }), 500


# ==================== Main ====================

if __name__ == '__main__':
    print("=" * 60)
    print("AMR Risk Prediction System - Flask Backend")
    print("Experiential Learning (EL) Phase-2 Project")
    print("=" * 60)
    print("\nStarting Flask development server...")
    print("Access the website at: http://localhost:5000")
    print("\nAvailable pages:")
    print("  - Home:              http://localhost:5000/")
    print("  - About AMR:         http://localhost:5000/about-amr")
    print("  - Dataset:           http://localhost:5000/dataset")
    print("  - Prediction Demo:   http://localhost:5000/prediction")
    print("  - Explainability:    http://localhost:5000/explainability")
    print("  - Results:           http://localhost:5000/results")
    print("  - Limitations:       http://localhost:5000/limitations")
    print("  - Team:              http://localhost:5000/team")
    print("\nAPI Endpoints:")
    print("  - POST /api/predict")
    print("  - GET  /api/feature-importance")
    print("  - GET  /api/health")
    print("\nPress CTRL+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
