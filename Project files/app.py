from flask import Flask, request, render_template
import os
import random
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Mock prediction function (simulates MobileNetV2 inference)
def predict_blood_cell(image_path):
    # List of possible blood cell types
    cell_types = ['Eosinophil', 'Lymphocyte', 'Monocyte', 'Neutrophil']
    # Simulate prediction by randomly selecting a cell type and confidence
    return {
        'cell_type': random.choice(cell_types),
        'confidence': random.uniform(0.85, 0.99)  # Random confidence between 85-99%
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'file' not in request.files:
            return render_template('index.html', error='No file uploaded')
        
        file = request.files['file']
        
        # Check if file is valid
        if file.filename == '':
            return render_template('index.html', error='No file selected')
        
        if file and allowed_file(file.filename):
            # Save the uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Get mock prediction
            prediction = predict_blood_cell(file_path)
            
            # Render template with results
            return render_template(
                'index.html',
                image_url=f'uploads/{filename}',
                cell_type=prediction['cell_type'],
                confidence=f"{prediction['confidence']:.2%}",
                error=None
            )
    
    # Render template for GET request
    return render_template('index.html', image_url=None, cell_type=None, confidence=None, error=None)

if __name__ == '__main__':
    app.run(debug=True)