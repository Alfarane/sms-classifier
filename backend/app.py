from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from nltk.corpus import stopwords
import string
from nltk.stem import PorterStemmer
ps = PorterStemmer()
import pickle
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the model and vectorizer
try:
    model = pickle.load(open('model.pkl', 'rb'))
    vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
    print("Model and vectorizer loaded successfully")
except Exception as e:
    print(f"Error loading model or vectorizer: {e}")


# Define the transform_text function
def transform_text(text):
    # lower case
    text = text.lower()

    # tokenize
    text = nltk.word_tokenize(text)

    # remove special characters and numbers
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    # list cloning
    text = y[:]
    y.clear()

    # remove stop words
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    # stemming
    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        if not data or 'sms' not in data:
            return jsonify({'error': 'No SMS text provided'}), 400

        sms_text = data['sms']

        # Transform the text
        transformed_text = transform_text(sms_text)

        # Vectorize the text
        vectorized_text = vectorizer.transform([transformed_text])

        # Predict
        prediction = model.predict(vectorized_text)[0]

        # Get prediction probability
        prediction_proba = max(model.predict_proba(vectorized_text)[0]) * 100

        result = {
            'prediction': 'spam' if prediction == 1 else 'ham',
            'confidence': round(prediction_proba, 2)
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
