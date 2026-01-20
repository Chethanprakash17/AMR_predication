// =====================================================
// AMR Risk Prediction - Client-Side JavaScript
// =====================================================

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const resultSection = document.getElementById('resultSection');
    const submitBtn = document.getElementById('submitBtn');
    
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
});

/**
 * Handle prediction form submission
 */
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const submitBtn = document.getElementById('submitBtn');
    const resultSection = document.getElementById('resultSection');
    
    // Disable submit button and show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading"></span> Predicting...';
    
    // Hide previous results
    resultSection.classList.remove('show');
    
    // Collect form data
    const formData = collectFormData();
    
    try {
        // Send prediction request to backend
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error('Prediction request failed');
        }
        
        const result = await response.json();
        
        // Display results
        displayPredictionResult(result);
        
    } catch (error) {
        console.error('Error:', error);
        displayError('An error occurred while processing your request. Please try again.');
    } finally {
        // Re-enable submit button
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Predict AMR Risk';
    }
}

/**
 * Collect and structure form data
 */
function collectFormData() {
    const formData = {
        // Demographics
        age: parseInt(document.getElementById('age').value),
        gender: document.getElementById('gender').value,
        admission_type: document.getElementById('admission_type').value,
        
        // Comorbidities (0 or 1 based on checkbox)
        diabetes: document.getElementById('diabetes').checked ? 1 : 0,
        ckd: document.getElementById('ckd').checked ? 1 : 0,
        copd: document.getElementById('copd').checked ? 1 : 0,
        cancer: document.getElementById('cancer').checked ? 1 : 0,
        immunosuppression: document.getElementById('immunosuppression').checked ? 1 : 0,
        
        // Antibiotic history
        prior_antibiotics: parseInt(document.getElementById('prior_antibiotics').value),
        broad_spectrum: parseInt(document.getElementById('broad_spectrum').value),
        
        // Vital signs
        heart_rate: parseFloat(document.getElementById('heart_rate').value),
        temperature: parseFloat(document.getElementById('temperature').value),
        systolic_bp: parseFloat(document.getElementById('systolic_bp').value),
        diastolic_bp: parseFloat(document.getElementById('diastolic_bp').value),
        spo2: parseFloat(document.getElementById('spo2').value),
        
        // Laboratory values
        wbc: parseFloat(document.getElementById('wbc').value),
        creatinine: parseFloat(document.getElementById('creatinine').value),
        lactate: parseFloat(document.getElementById('lactate').value),
        
        // ICU context
        mechanical_ventilation: parseInt(document.getElementById('mechanical_ventilation').value)
    };
    
    return formData;
}

/**
 * Display prediction results
 */
function displayPredictionResult(result) {
    const resultSection = document.getElementById('resultSection');
    const riskScoreDisplay = document.getElementById('riskScoreDisplay');
    const riskPercentage = document.getElementById('riskPercentage');
    const riskLevel = document.getElementById('riskLevel');
    const interpretationText = document.getElementById('interpretationText');
    
    // Get risk score (convert to percentage)
    const riskScore = result.amr_risk_probability;
    const riskPercent = (riskScore * 100).toFixed(1);
    
    // Determine risk level
    let riskCategory, riskClass;
    if (riskScore < 0.30) {
        riskCategory = 'Low Risk';
        riskClass = 'low';
    } else if (riskScore < 0.60) {
        riskCategory = 'Moderate Risk';
        riskClass = 'moderate';
    } else {
        riskCategory = 'High Risk';
        riskClass = 'high';
    }
    
    // Update display
    riskPercentage.textContent = `${riskPercent}%`;
    riskLevel.textContent = `AMR ${riskCategory}`;
    riskScoreDisplay.className = `risk-score ${riskClass}`;
    
    // Generate interpretation text
    interpretationText.innerHTML = generateInterpretation(riskScore, riskCategory);
    
    // Show results with smooth scroll
    resultSection.classList.add('show');
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Generate interpretation text based on risk score
 */
function generateInterpretation(riskScore, riskCategory) {
    let interpretation = `<p>The model predicts an AMR risk probability of <strong>${(riskScore * 100).toFixed(1)}%</strong> 
        for this patient based on the provided clinical data from the first 24 hours of ICU admission.</p>`;
    
    if (riskScore < 0.30) {
        interpretation += `<p><strong>${riskCategory}:</strong> This patient has a relatively low predicted likelihood of 
        antimicrobial resistance. However, standard antimicrobial stewardship principles should still be followed, and 
        empirical antibiotic selection should be based on local antibiograms and clinical guidelines.</p>`;
    } else if (riskScore < 0.60) {
        interpretation += `<p><strong>${riskCategory}:</strong> This patient shows a moderate predicted risk of antimicrobial 
        resistance. Consider incorporating this information alongside clinical judgment when selecting empirical antibiotic therapy. 
        Close monitoring and culture results remain essential for optimal treatment decisions.</p>`;
    } else {
        interpretation += `<p><strong>${riskCategory}:</strong> This patient has a high predicted likelihood of antimicrobial 
        resistance. This elevated risk may warrant consideration of broader-spectrum empirical therapy while awaiting definitive 
        culture and susceptibility testing. Enhanced infection control precautions may also be appropriate.</p>`;
    }
    
    interpretation += `<p style="margin-top: 1rem; font-style: italic; color: var(--text-light);">
        Remember: This prediction is based on statistical patterns in historical data and should be interpreted in the context 
        of the individual patient's clinical presentation, local resistance patterns, and institutional guidelines. Microbiology 
        culture results remain the gold standard for guiding targeted antimicrobial therapy.</p>`;
    
    return interpretation;
}

/**
 * Display error message
 */
function displayError(message) {
    const resultSection = document.getElementById('resultSection');
    const riskScoreDisplay = document.getElementById('riskScoreDisplay');
    const interpretationText = document.getElementById('interpretationText');
    
    riskScoreDisplay.className = 'risk-score';
    riskScoreDisplay.innerHTML = '<h3 style="color: var(--risk-high);">Error</h3>';
    interpretationText.innerHTML = `<p style="color: var(--risk-high);">${message}</p>`;
    
    resultSection.classList.add('show');
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Basic form validation (browser provides default validation, this is extra)
 */
function validateForm(formData) {
    // Age validation
    if (formData.age < 18 || formData.age > 100) {
        alert('Age must be between 18 and 100 years');
        return false;
    }
    
    // Vital signs validation
    if (formData.heart_rate < 40 || formData.heart_rate > 200) {
        alert('Heart rate must be between 40 and 200 bpm');
        return false;
    }
    
    if (formData.temperature < 35 || formData.temperature > 42) {
        alert('Temperature must be between 35°C and 42°C');
        return false;
    }
    
    if (formData.spo2 < 50 || formData.spo2 > 100) {
        alert('SpO2 must be between 50% and 100%');
        return false;
    }
    
    return true;
}
