# AI-Based Early AMR Risk Prediction in ICU Patients

## Project Overview

This is an **Experiential Learning (EL) Phase-2** academic project that demonstrates an end-to-end AI workflow for predicting antimicrobial resistance (AMR) risk in ICU patients using early Electronic Health Record (EHR) data from the first 24 hours of admission.

**⚠ IMPORTANT:** This is a research prototype developed for academic purposes only and is **NOT** intended for real clinical use.

## Project Team

- **Nandan Reddy S** - 1RV24CS163
- **Mallikarjun** - 1RV24CI064
- **Venkata Sai Vijay Kuncham** - 1RV24CS314
- **Chethan Prakash B N** - 1RV24CD017
- **Vasa Shashank** - 1RV24CS312

**Institution:** RV University, Bengaluru, India

## Features

- 8 comprehensive web pages covering all aspects of the project
- Interactive prediction demo with detailed input form
- Mock XGBoost ML model demonstrating clinical risk factors
- Feature importance visualization and explainability
- Comprehensive documentation of limitations and ethics
- Clean, academic UI design suitable for faculty presentation

## Project Structure

```
EL_website/
├── static/
│   ├── css/
│   │   └── style.css              # Main stylesheet
│   ├── js/
│   │   └── main.js                # Client-side JavaScript
│   └── images/
│       ├── feature_importance.png # Feature importance chart
│       ├── roc_curve.png          # ROC curve visualization
│       └── workflow_diagram.png   # System workflow diagram
├── templates/
│   ├── base.html                  # Base template
│   ├── index.html                 # Home page
│   ├── about_amr.html             # About AMR
│   ├── dataset.html               # Dataset & Methodology
│   ├── prediction.html            # Prediction Demo
│   ├── explainability.html        # Explainability
│   ├── results.html               # Results & Evaluation
│   ├── limitations.html           # Limitations & Ethics
│   └── team.html                  # Team & References
├── backend/
│   ├── app.py                     # Flask application
│   ├── model.py                   # ML model implementation
│   └── requirements.txt           # Python dependencies
└── README.md                      # This file
```

## Technology Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **ML Framework:** NumPy (mock implementation)
- **Dataset:** MIMIC-IV ICU Clinical Database (PhysioNet)

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

Navigate to the backend directory and install required packages:

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Run the Flask Application

From the backend directory:

```bash
python app.py
```

Or from the project root:

```bash
python backend/app.py
```

### Step 3: Access the Website

Open your web browser and navigate to:

```
http://localhost:5000
```

## Available Pages

1. **Home** (`/`) - Project overview and introduction
2. **About AMR** (`/about-amr`) - Educational content on antimicrobial resistance
3. **Dataset & Methodology** (`/dataset`) - MIMIC-IV dataset and feature engineering
4. **Prediction Demo** (`/prediction`) - Interactive AMR risk prediction form
5. **Explainability** (`/explainability`) - Feature importance and model transparency
6. **Results & Evaluation** (`/results`) - Model performance metrics
7. **Limitations & Ethics** (`/limitations`) - Technical limitations and ethical considerations
8. **Team & References** (`/team`) - Team information and academic citations

## API Endpoints

- **POST** `/api/predict` - Predict AMR risk from patient data
- **GET** `/api/feature-importance` - Retrieve feature importance scores
- **GET** `/api/health` - Health check endpoint

## Model Details

The system uses a **mock XGBoost classifier** that demonstrates clinical risk factor logic:

- **Input Features:** 20 features including demographics, comorbidities, vitals, labs, and ICU context
- **Output:** AMR risk probability (0-1) with risk categorization (Low/Moderate/High)
- **Performance:** Simulates AUROC = 0.82, Recall = 0.78

**Note:** This is a demonstration model using rule-based logic to simulate realistic predictions. In a real deployment, this would be replaced with a trained scikit-learn XGBoost model.

## Dataset Information

This project references the **MIMIC-IV Clinical Database**:

- **Source:** Beth Israel Deaconess Medical Center
- **Provider:** PhysioNet / MIT Lab for Computational Physiology
- **Access:** Requires CITI training and PhysioNet credentialing
- **Citation:** Johnson et al. (2023). MIMIC-IV (version 2.2). PhysioNet.

## Limitations

This is an **academic prototype** with significant limitations:

- Retrospective dataset (2008-2019)
- Single-center data
- No organism-specific predictions
- No real-time hospital integration
- No clinical trial validation
- Mock model implementation (not trained on actual data)

**See the Limitations & Ethics page for comprehensive discussion.**

## Ethical Considerations

- ✅ Educational and research purposes only
- ✅ Transparent about limitations
- ✅ No treatment automation
- ✅ Emphasizes human oversight
- ❌ NOT for real clinical use
- ❌ NOT validated in clinical trials
- ❌ NOT FDA approved

## Usage Guidelines

### Appropriate Uses
- Classroom demonstrations
- Academic presentations
- Learning ML workflows
- Understanding healthcare AI ethics

### Inappropriate Uses
- ❌ Actual patient treatment decisions
- ❌ Real healthcare deployment
- ❌ Commercial applications
- ❌ Replacing medical expertise

## Development Notes

### Adding New Features

The codebase is structured for easy extension:

- Add new routes in `backend/app.py`
- Create new templates in `templates/`
- Add styling in `static/css/style.css`
- Extend client-side logic in `static/js/main.js`

### Model Replacement

To replace the mock model with a real trained model:

1. Train a scikit-learn XGBoost on MIMIC-IV data
2. Save the model using `joblib` or `pickle`
3. Update `model.py` to load the saved model
4. Ensure feature preprocessing matches training

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify the port in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Missing Dependencies
Ensure all dependencies are installed:

```bash
pip install -r backend/requirements.txt
```

### Template Not Found
Make sure you're running `app.py` from the correct directory so Flask can find the templates folder.

## References

See the **Team & References** page for comprehensive academic citations including:

- MIMIC-IV database documentation
- AMR research literature
- Machine learning in healthcare papers
- Clinical decision support systems
- AI ethics guidelines

## License

This is an academic project developed for educational purposes at RV University. The MIMIC-IV dataset is used under PhysioNet credentialing requirements.

## Contact

This project was developed as part of the Experiential Learning (EL) Phase-2 curriculum at RV University (2024-2025).

---

**Academic Disclaimer:** This system is a research prototype developed for academic purposes only and is not intended for real clinical use. All predictions are simulated for demonstration purposes.
