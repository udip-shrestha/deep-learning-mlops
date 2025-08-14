from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pathlib import Path
from cnnClassifier.utils.helper import decode_image  
import os


from cnnClassifier.utils.helper import decode_image  # function name is decode_image
from cnnClassifier.pipeline.predict import PredictionPipeline

# Optional locale envs; 
os.environ["LANG"] = "en_US.UTF-8"
os.environ["LC_ALL"] = "en_US.UTF-8"

app = Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        # Load model once
        self.classifier = PredictionPipeline(self.filename)

clApp = ClientApp()

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/train", methods=["GET", "POST"])
def trainRoute():
    # This is a placeholder for training logic
    os.system("dvc repro")
    # os.system("python main.py")
    return "Training done successfully!"

@app.route("/predict", methods=["POST"])
def predictRoute():
    payload = request.get_json()
    b64 = payload.get("image", "")

    # If the base64 string has a header like 'data:image/jpeg;base64,'
    if "," in b64:
        b64 = b64.split(",", 1)[1]

    # helper.decode_image expects a Path
    decode_image(b64, Path(clApp.filename))

    result = clApp.classifier.predict()  # returns dict: {"label": ..., "confidence": ...}
    return jsonify(result)

if __name__ == "__main__":
    # debug=False avoids double-loading model on Windows autoreload
    app.run(host="0.0.0.0", port=8080, debug=False)
