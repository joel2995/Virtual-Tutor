from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import time
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Serve static files from the frontend directory
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_frontend(path):
    # Adjust the path to point to the frontend directory one level up
    return send_from_directory('../frontend', path)

@app.route('/api/process-image', methods=['POST'])
def process_image():
    # Check if image is in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image = request.files['image']
    
    # Simulate processing time
    time.sleep(2)
    
    # In a real application, you would process the image here
    # For now, we'll return dummy measurements
    measurements = {
        'bust': round(random.uniform(80, 100), 1),
        'waist': round(random.uniform(60, 80), 1),
        'hips': round(random.uniform(85, 105), 1),
        'shoulder_width': round(random.uniform(35, 45), 1),
        'arm_length': round(random.uniform(50, 65), 1),
        'inseam': round(random.uniform(70, 85), 1),
        'height': round(random.uniform(150, 180), 1)
    }
    
    return jsonify({
        'success': True,
        'measurements': measurements
    })

@app.route('/api/customize', methods=['POST'])
def customize():
    data = request.json
    
    if not data or 'measurements' not in data or 'prompt' not in data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    measurements = data['measurements']
    prompt = data['prompt']
    
    # Simulate processing time
    time.sleep(3)
    
    # In a real application, you would generate custom stitching info based on the prompt
    # For now, we'll return dummy data
    stitching_info = {
        'fabricRequirements': f'You will need 2.5 meters of main fabric and 1 meter of lining fabric for this {prompt.split()[0]} dress. Choose a medium-weight fabric with some drape for the best results.',
        'customMeasurements': [
            f'Bust: {measurements.get("bust", 90)} cm + 2 cm ease',
            f'Waist: {measurements.get("waist", 70)} cm + 1.5 cm ease',
            f'Hips: {measurements.get("hips", 95)} cm + 3 cm ease',
            'Seam allowance: 1.5 cm throughout',
            f'Sleeve length: {measurements.get("arm_length", 60)} cm - 1 cm for cuff',
            f'Garment length: {measurements.get("height", 165) * 0.6} cm from shoulder to hem'
        ],
        'steps': [
            'Cut the fabric according to the pattern pieces.',
            'Sew the shoulder seams of the bodice front and back.',
            'Attach the sleeves to the armholes.',
            'Sew the side seams of the bodice and sleeves.',
            'Sew the skirt panels together at the side seams.',
            'Attach the skirt to the bodice at the waistline.',
            'Insert the zipper at the center back.',
            'Finish the neckline with facing or bias binding.',
            'Hem the sleeves and skirt.',
            'Press all seams and add any final embellishments.'
        ],
        'notes': f'This design is customized for your measurements. The {prompt} style works well with your body type. Consider using a fabric with some stretch for better comfort.'
    }
    
    # Generate dummy image references
    relevant_images = [
        {
            'url': 'https://example.com/dress1.jpg',
            'title': f'{prompt.split()[0].capitalize()} Dress - Front View',
            'sourceUrl': 'https://example.com/dress1'
        },
        {
            'url': 'https://example.com/dress2.jpg',
            'title': f'{prompt.split()[0].capitalize()} Dress - Back View',
            'sourceUrl': 'https://example.com/dress2'
        },
        {
            'url': 'https://example.com/dress3.jpg',
            'title': f'{prompt.split()[0].capitalize()} Dress - Detail View',
            'sourceUrl': 'https://example.com/dress3'
        }
    ]
    
    return jsonify({
        'success': True,
        'stitchingInfo': stitching_info,
        'relevantImages': relevant_images
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)