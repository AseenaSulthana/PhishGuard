from urllib.parse import urlparse
import numpy as np
from flask import Flask, render_template, request, jsonify
import joblib

app = Flask(__name__)

# Load your trained model
model = joblib.load('trained_model96.joblib')

# Function to extract features from URL
def extract_features(url):
    parsed_url = urlparse(url)
    features = {}

    # Extract domain length
    features['domain_length'] = len(parsed_url.netloc)

    # Extract path length
    features['path_length'] = len(parsed_url.path)

    # Extract number of segments in the path
    features['num_segments'] = len(parsed_url.path.split('/'))

    # Extract whether 'https' is used
    features['is_https'] = 1 if parsed_url.scheme == 'https' else 0

    # Add missing features and set their values to 0
    missing_features = ['feature5', 'feature6', ...]  # Add missing feature names here
    for feature in missing_features:
        features[feature] = 0

    return features

# Function to convert features to numerical form
def convert_to_numerical(features):
    # Convert features dictionary to list of values
    feature_values = list(features.values())
    # Convert list to 1D numpy array
    feature_array = np.array(feature_values).reshape(1, -1)
    return feature_array

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    link = data['link']
    # Preprocess the link (similar to preprocessing done during model training)
    url_features = extract_features(link)
    
    # Print the extracted features for debugging
    print("Extracted Features:", url_features)

    numerical_features = convert_to_numerical(url_features)
    
    # Print the numerical features for debugging
    print("Numerical Features:", numerical_features)

    # Make prediction using the loaded model
    try:
        prediction = model.predict(numerical_features, check_input=False)[0]
        # Return the result
        print(prediction)
        if prediction == 1:
            result = 'Safe'
        else:
            result = 'Unsafe'
        print("Prediction:", result)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})
    except Exception as e:
        return jsonify({'error': str(e)})

# Route to serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# Route to serve the styles.css file
@app.route('/styles.css')
def styles():
    return app.send_static_file('styles.css')

if __name__ == '__main__':
    app.run(debug=True)
