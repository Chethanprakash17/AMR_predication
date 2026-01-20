"""
AMR Risk Prediction - Machine Learning Model Module
Implements a mock XGBoost classifier for demonstration purposes
"""

import numpy as np
from typing import Dict, List, Tuple

class AMRPredictionModel:
    """
    Mock XGBoost model for AMR risk prediction
    In a real implementation, this would load a trained scikit-learn model
    """
    
    def __init__(self):
        """Initialize the model with feature importance scores"""
        self.feature_importance = {
            'prior_antibiotics': 0.18,
            'broad_spectrum': 0.15,
            'age': 0.12,
            'mechanical_ventilation': 0.11,
            'icu_los': 0.10,  # Not used in current features but listed in importance
            'lactate': 0.09,
            'wbc': 0.08,
            'creatinine': 0.07,
            'comorbidity_score': 0.06,
            'heart_rate': 0.04
        }
        
        # Feature names expected in the model
        self.feature_names = [
            'age', 'gender_M', 'admission_type_EMERGENCY', 'admission_type_URGENT',
            'diabetes', 'ckd', 'copd', 'cancer', 'immunosuppression',
            'prior_antibiotics', 'broad_spectrum',
            'heart_rate', 'temperature', 'systolic_bp', 'diastolic_bp', 'spo2',
            'wbc', 'creatinine', 'lactate',
            'mechanical_ventilation'
        ]
    
    def preprocess_input(self, patient_data: Dict) -> np.ndarray:
        """
        Preprocess patient data into feature vector
        
        Args:
            patient_data: Dictionary containing patient information
        
        Returns:
            Numpy array of features
        """
        # One-hot encode gender
        gender_M = 1 if patient_data.get('gender') == 'M' else 0
        
        # One-hot encode admission type
        admission_type_EMERGENCY = 1 if patient_data.get('admission_type') == 'EMERGENCY' else 0
        admission_type_URGENT = 1 if patient_data.get('admission_type') == 'URGENT' else 0
        
        # Construct feature vector in the correct order
        features = [
            patient_data.get('age', 0),
            gender_M,
            admission_type_EMERGENCY,
            admission_type_URGENT,
            patient_data.get('diabetes', 0),
            patient_data.get('ckd', 0),
            patient_data.get('copd', 0),
            patient_data.get('cancer', 0),
            patient_data.get('immunosuppression', 0),
            patient_data.get('prior_antibiotics', 0),
            patient_data.get('broad_spectrum', 0),
            patient_data.get('heart_rate', 0),
            patient_data.get('temperature', 0),
            patient_data.get('systolic_bp', 0),
            patient_data.get('diastolic_bp', 0),
            patient_data.get('spo2', 0),
            patient_data.get('wbc', 0),
            patient_data.get('creatinine', 0),
            patient_data.get('lactate', 0),
            patient_data.get('mechanical_ventilation', 0)
        ]
        
        return np.array(features).reshape(1, -1)
    
    def predict_amr_risk(self, patient_data: Dict) -> Dict:
        """
        Predict AMR risk for a patient
        
        Args:
            patient_data: Dictionary containing patient information
        
        Returns:
            Dictionary with prediction results
        """
        # Preprocess input
        features = self.preprocess_input(patient_data)
        
        # Mock prediction logic (demonstrates risk factors)
        # In reality, this would be: model.predict_proba(features)
        
        # Base risk
        base_risk = 0.30
        
        # Adjust risk based on key features
        risk_score = base_risk
        
        # Prior antibiotic exposure (strongest predictor)
        if patient_data.get('prior_antibiotics', 0) == 1:
            risk_score += 0.15
        
        if patient_data.get('broad_spectrum', 0) == 1:
            risk_score += 0.12
        
        # Age factor (>65 increases risk)
        age = patient_data.get('age', 0)
        if age >= 75:
            risk_score += 0.10
        elif age >= 65:
            risk_score += 0.06
        
        # Mechanical ventilation
        if patient_data.get('mechanical_ventilation', 0) == 1:
            risk_score += 0.08
        
        # Comorbidities
        comorbidity_count = (
            patient_data.get('diabetes', 0) +
            patient_data.get('ckd', 0) +
            patient_data.get('copd', 0) +
            patient_data.get('cancer', 0) +
            patient_data.get('immunosuppression', 0)
        )
        risk_score += comorbidity_count * 0.04
        
        # Severity indicators (lactate, WBC)
        if patient_data.get('lactate', 0) > 2.0:
            risk_score += 0.06
        
        if patient_data.get('wbc', 0) > 12.0 or patient_data.get('wbc', 0) < 4.0:
            risk_score += 0.04
        
        # Renal function (elevated creatinine)
        if patient_data.get('creatinine', 0) > 1.5:
            risk_score += 0.05
        
        # Emergency admission
        if patient_data.get('admission_type') == 'EMERGENCY':
            risk_score += 0.03
        
        # Cap at 0.95 to avoid certainty
        risk_score = min(risk_score, 0.95)
        
        # Add small random variation to make predictions more realistic
        # (In reality, this would come from model uncertainty)
        noise = np.random.uniform(-0.02, 0.02)
        risk_score = max(0.05, min(0.95, risk_score + noise))
        
        return {
            'amr_risk_probability': round(risk_score, 3),
            'risk_category': self._categorize_risk(risk_score),
            'confidence_score': 0.82  # Model AUROC
        }
    
    def _categorize_risk(self, probability: float) -> str:
        """Categorize risk level based on probability"""
        if probability < 0.30:
            return 'Low'
        elif probability < 0.60:
            return 'Moderate'
        else:
            return 'High'
    
    def get_feature_importance(self) -> List[Tuple[str, float]]:
        """
        Get feature importance scores
        
        Returns:
            List of (feature_name, importance_score) tuples sorted by importance
        """
        return sorted(self.feature_importance.items(), key=lambda x: x[1], reverse=True)


# Global model instance
_model_instance = None

def get_model() -> AMRPredictionModel:
    """Get or create the global model instance"""
    global _model_instance
    if _model_instance is None:
        _model_instance = AMRPredictionModel()
    return _model_instance
