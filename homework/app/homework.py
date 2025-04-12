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

def check_input(input_features):
    '''
    length of input_features should be 12
    '''
    if len(input_features) != 12:
        return False
    
    '''
    [0:6] are binary features
    mainroad	guestroom	basement	hotwaterheating	airconditioning	prefarea
    yes no
    '''
    binary_features = input_features[0:6]
    for feature in binary_features:
        if feature not in ["yes", "no"]:
            return False
    
    '''
    [6] are categorical features
    furnishingstatus
    unfurnished semi-furnished furnished
    '''
    categorical_feature = input_features[6]
    if categorical_feature not in ["unfurnished", "semi-furnished", "furnished"]:
        return False
    
    '''
    [7:12] are numerical features
    area	bedrooms	bathrooms	stories	parking
    numerical
    '''
    numerical_features = input_features[7:12]
    for feature in numerical_features:
        if not feature.isnumeric():
            return False
    
    return True
    
def transform_features(input_features):
    '''
    Transform the input features to the format that the model expects
    '''
    transformed_features = []
    
    # Binary features
    binary_mapping = {"yes": 1, "no": 0}
    transformed_features.extend([binary_mapping[feature] for feature in input_features[0:6]])
    
    # Categorical feature
    categorical_mapping = {'furnished': 1, "semi-furnished": 2, "unfurnished": 3}
    transformed_features.append(categorical_mapping[input_features[6]])
    
    # Numerical features
    transformed_features.extend([float(feature) for feature in input_features[7:12]])
    
    return np.array(transformed_features).reshape(1, -1)
    

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    try:
        input_features = data["features"]
        input_features = np.array(input_features)
        if(len(input_features.shape) == 1 and input_features.shape[0] == 12):
            input_features = input_features.reshape(1, -1)
            if check_input(input_features[0]):
                # Transform the input features to the format that the model expects
                transformed_features = transform_features(input_features[0])
                # Make prediction
                prediction = model.predict(transformed_features)
                return jsonify({
                    "prediction": int(prediction[0])
                    })
            else:
                return jsonify({"error": "Invalid input format"}), 400
        elif input_features.shape[1] == 12:
            output = []
            for feature in input_features:
                if check_input(feature):
                    # Transform the input features to the format that the model expects
                    transformed_features = transform_features(feature)
                    # Make prediction
                    prediction = model.predict(transformed_features)
                    output.append(int(prediction[0]))
                else:
                   return jsonify({"error": "Invalid input format"}), 400 
            return jsonify({
                "prediction": output
                })     
    except:
        return jsonify({"error": "Invalid input format"}), 400
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000) #check your port number ( if it is in use, change the port number)
