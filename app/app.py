from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route("/")
def home():
    return "ML Model is Running"

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    try:
        input_features = np.array(data["features"])
        # If there is only one input set
        if(len(input_features.shape) == 1 and input_features.shape[0] == 4):
            input_features = input_features.reshape(1, -1)
            prediction = model.predict(input_features)
            prob = model.predict_proba(input_features)

            return jsonify({
                "prediction": int(prediction[0]),
                "confidence": np.max(prob[0])
                })
        if(input_features.shape[1] == 4):
            prediction = model.predict(input_features)
            return jsonify({
                "prediction": prediction.tolist()
                })
        else:
            return jsonify({"error": "Invalid input format"}), 400
    except:
        # 400 Bad Request
        return jsonify({"error": "Invalid input format"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000) #check your port number ( if it is in use, change the port number)
