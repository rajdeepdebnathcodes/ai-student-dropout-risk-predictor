from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

# Load trained model
model = joblib.load("model/dropout_model.pkl")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    attendance = data["attendance"]
    study_hours = data["study_hours"]
    assignments = data["assignments"]
    gpa = data["gpa"]
    participation = data["participation"]

    # Calculate risk score
    risk_score = (100 - attendance) + (6 - study_hours) * 5 + (100 - assignments) * 0.5 + (10 - gpa) * 3

    if risk_score < 80:
        result = "LOW RISK"
    elif risk_score < 140:
        result = "MODERATE RISK"
    else:
        result = "HIGH RISK"

    return jsonify({"prediction": result})


if __name__ == "__main__":
    app.run(debug=True)