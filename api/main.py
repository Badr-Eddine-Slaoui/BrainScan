import os
from pathlib import Path

import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from tensorflow.keras.models import load_model

IMG_SIZE = (224, 224)
MODEL_DIR = Path(__file__).resolve().parent.parent / "model"
if (MODEL_DIR / "brainscan_cnn_best.keras").exists():
    MODEL_PATH = MODEL_DIR / "brainscan_cnn_best.keras"
elif (MODEL_DIR / "brainscan_cnn.keras").exists():
    MODEL_PATH = MODEL_DIR / "brainscan_cnn.keras"
elif (MODEL_DIR / "brainscan_cnn_optimized.keras").exists():
    MODEL_PATH = MODEL_DIR / "brainscan_cnn_optimized.keras"
else:
    MODEL_PATH = MODEL_DIR / "brainscan_cnn_best.keras"
LABELS_PATH = MODEL_DIR.parent / "data" / "processed" / "label_classes.npy"

app = FastAPI(
    title="BrainScan AI",
    description="API de classification de tumeurs cérébrales sur images IRM",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_model = None
_classes = None


def get_model():
    global _model, _classes
    if _model is None:
        if not MODEL_PATH.exists():
            raise RuntimeError(f"Modèle introuvable : {MODEL_PATH}")
        _model = load_model(str(MODEL_PATH), compile=False)
        _classes = np.load(str(LABELS_PATH), allow_pickle=True)
    return _model, _classes


def predict_image(path: str) -> dict:
    model, classes = get_model()

    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Impossible de lire l'image : {path}")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, IMG_SIZE)
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)

    probs = model.predict(img, verbose=0)[0]
    pred_idx = int(np.argmax(probs))

    return {
        "predicted_class": str(classes[pred_idx]),
        "confidence": float(probs[pred_idx]),
        "probabilities": {str(classes[i]): float(probs[i]) for i in range(len(classes))},
    }


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": _model is not None}


@app.get("/classes")
def list_classes():
    _, classes = get_model()
    return {"classes": classes.tolist()}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Le fichier doit être une image.")

    tmp_path = f"/tmp/{file.filename}"
    try:
        contents = await file.read()
        with open(tmp_path, "wb") as f:
            f.write(contents)

        result = predict_image(tmp_path)
        return result

    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.on_event("startup")
def _load_model_on_startup():
    try:
        get_model()
    except RuntimeError:
        pass
