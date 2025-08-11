import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

# EuroSAT class names in alphabetical order 
CLASS_NAMES = [
    "AnnualCrop",
    "Forest",
    "HerbaceousVegetation",
    "Highway",
    "Industrial",
    "Pasture",
    "PermanentCrop",
    "Residential",
    "River",
    "SeaLake",
]

MODEL_PATH = os.path.join("artifacts", "training", "model.h5")
IMG_SIZE = (224, 224)

class PredictionPipeline:
    def __init__(self, filename: str):
        self.filename = filename
        # Load once per instance; if call predict a lot, move this to a module-level cache
        self.model = tf.keras.models.load_model(MODEL_PATH)

    def _load_and_preprocess(self, path: str) -> np.ndarray:
        """Load image and apply the same preprocessing used in training."""
        img = image.load_img(path, target_size=IMG_SIZE)             # RGB by default
        arr = image.img_to_array(img).astype("float32") / 255.0      # rescale like training
        return np.expand_dims(arr, axis=0)                           # shape: (1, 224, 224, 3)

    def predict(self):
        x = self._load_and_preprocess(self.filename)
        probs = self.model.predict(x, verbose=0)[0]                  # shape: (10,)
        idx = int(np.argmax(probs))
        label = CLASS_NAMES[idx]
        confidence = float(probs[idx])

        # If you want a minimal response (top-1):
        return {
            "label": label,
            "confidence": round(confidence, 4),
        }

        # return this, if full probabilities are needed:
        # return {
        #     "predictions": {name: float(p) for name, p in zip(CLASS_NAMES, probs)},
        #     "label": label,
        #     "confidence": round(confidence, 4),
        # }
