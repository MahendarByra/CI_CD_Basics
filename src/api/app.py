from flask import Flask, request
from flask import render_template_string,url_for
import joblib
import numpy as np
import os

app = Flask(__name__, static_url_path='/static')

# Load model and encoder
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../saved_models/iris_rf_model.joblib')
ENCODER_PATH = os.path.join(os.path.dirname(__file__), '../../saved_models/label_encoder.joblib')

model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Flower Classifier</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    {{ content|safe }}
</body>
</html>
'''


@app.route('/')
def home():
    content = '''
    <h2>Welcome to the Flower Classifier</h2>
    <img src="{}" alt="Flower Image" style="width:300px; display:block; margin: 20px auto;">
    <a href="/predict"><button>Prediction</button></a>
    '''.format(url_for('static', filename='flower.jpg'))
    return render_template_string(HTML_TEMPLATE, content=content)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            sepal_length = float(request.form['sepal_length'])
            sepal_width = float(request.form['sepal_width'])
            petal_length = float(request.form['petal_length'])
            petal_width = float(request.form['petal_width'])

            features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
            prediction = model.predict(features)
            label = encoder.inverse_transform(prediction)[0]

            content = f'''
                <h2>Prediction Result: <span style="color:green">{label}</span></h2>
                <a href="/predict"><button>Try Another</button></a>
                <a href="/"><button>Home</button></a>
            '''
            return render_template_string(HTML_TEMPLATE, content=content)

        except Exception as e:
            content = f'''
                <h3 style="color:red">Error: {str(e)}</h3>
                <a href="/predict"><button>Try Again</button></a>
            '''
            return render_template_string(HTML_TEMPLATE, content=content)

    # GET request
    content = '''
        <h2>Enter Flower Measurements</h2>
        <form method="post">
            <label>Sepal Length (cm):</label><br>
            <input type="text" name="sepal_length"><br>
            <label>Sepal Width (cm):</label><br>
            <input type="text" name="sepal_width"><br>
            <label>Petal Length (cm):</label><br>
            <input type="text" name="petal_length"><br>
            <label>Petal Width (cm):</label><br>
            <input type="text" name="petal_width"><br><br>
            <input type="submit" value="Predict">
        </form>
    '''
    return render_template_string(HTML_TEMPLATE, content=content)


if __name__ == '__main__':
    app.run(debug=True)
