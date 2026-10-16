# 🧠 BrainScan AI

> **AI-assisted brain tumour classification from MRI scans — MedTech Maroc**

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.20-orange)](https://www.tensorflow.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-green)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red)](https://streamlit.io/)
[![MLflow](https://img.shields.io/badge/MLflow-3.17-blue)](https://mlflow.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue)](https://docs.docker.com/compose/)

---

## ⚠️ Important Disclaimer

**BrainScan AI is a research and educational prototype.**  
It is **not** a validated clinical diagnostic system and must **not** be used for actual medical decisions.  
All diagnostic conclusions must be reviewed and confirmed by a qualified medical professional.

---

## 1. Project Overview

BrainScan AI is an innovative Moroccan MedTech project that applies deep learning to the automatic classification of brain MRI images.

The system aims to:

- **Classify** MRI scans into one of four categories: Glioma, Meningioma, Pituitary Tumour, or No Tumour.
- **Assist** radiologists and neurosurgeons in rapid, consistent interpretation of brain MRI results.
- **Reduce** diagnostic time and human error through automated, probabilistic analysis.

---

## 2. Problem Statement

Early and accurate detection of brain tumours is critical for improving patient outcomes. Manual analysis of MRI scans is time-consuming, subject to observer variability, and requires highly specialised expertise. BrainScan AI demonstrates how a CNN-based model can augment — not replace — the radiologist's workflow with an automated pre-screening step.

---

## 3. Features

| Feature | Description |
|---|---|
| 🔬 **CNN Classifier** | Custom 4-class convolutional neural network trained on labelled brain MRI data |
| 📊 **Probability output** | Softmax probabilities per class with confidence score |
| 🖥️ **Streamlit UI** | Interactive medical dashboard for uploading MRI images and viewing results |
| ⚡ **FastAPI inference** | REST endpoint (`POST /predict`) accepting image uploads |
| 📈 **MLflow tracking** | Experiment logging and model registry via MLflow server |
| 🐳 **Dockerised stack** | FastAPI + Streamlit + MLflow + PostgreSQL via Docker Compose |
| 📓 **Jupyter notebooks** | End-to-end ML pipeline in five documented notebooks |
| 🔍 **Hyperparameter search** | Grid search over learning rate, batch size, and dropout rate |

---

## 4. Technology Stack

| Layer | Library / Tool |
|---|---|
| Deep learning framework | TensorFlow 2.20, Keras ≥ 3.10 |
| Computer vision | OpenCV (`opencv-python-headless`), Pillow |
| Data processing | NumPy, scikit-learn, imbalanced-learn |
| Visualisation | Matplotlib, Seaborn |
| Experiment tracking | MLflow 3.17 |
| Inference API | FastAPI ≥ 0.111, Uvicorn |
| Interactive UI | Streamlit ≥ 1.35 |
| Containerisation | Docker, Docker Compose |
| Database backend | PostgreSQL 17 (MLflow metadata store) |
| Database UI | pgAdmin 4 |

---

## 5. Project Structure

```
BrainScan/
├── api/
│   ├── __init__.py
│   └── main.py                     # FastAPI inference service
├── app/
│   ├── __init__.py
│   └── main.py                     # Streamlit diagnostic dashboard
├── data/
│   └── README.md                   # Dataset placement instructions (data not committed)
├── docker/
│   ├── app/
│   │   └── Dockerfile              # FastAPI + Streamlit image
│   └── mlflow/
│       └── Dockerfile              # MLflow tracking server image
├── model/
│   ├── classification_report.txt   # Per-class precision / recall / F1
│   ├── confusion_matrix.png        # Confusion matrix heatmap
│   ├── learning_curves.png         # Train vs. validation accuracy & loss
│   ├── model_architecture.png      # CNN layer diagram
│   ├── optimization_classification_report.txt
│   ├── optimization_confusion_matrix.png
│   ├── learning_curves_optimized.png
│   ├── optimisation_predictions_sample.png
│   ├── predictions_sample.png
│   └── training_history.json       # Per-epoch metrics (accuracy, loss, lr)
├── notebooks/
│   ├── 01_data_loading_preprocessing.ipynb
│   ├── 02_eda_visualization.ipynb
│   ├── 03_model_training.ipynb
│   ├── 04_evaluation.ipynb
│   └── 05_optimization.ipynb
├── requirements/
│   ├── app/
│   │   └── requirements.txt        # FastAPI + Streamlit + ML stack
│   └── mlflow/
│       └── requirements.txt        # MLflow server + PostgreSQL driver
├── .dockerignore
├── .env.example                    # Safe environment variable template
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

## 6. Dataset Requirements

The dataset is **not included** in this repository. Place it in the `data/` directory following this layout:

```
data/
├── glioma/
├── meningioma/
├── notumor/
└── pituitary/
```

**Supported image extensions:** `.jpg`, `.jpeg`, `.png`, `.bmp`  
Files with unsupported extensions are automatically skipped during loading.

**Recommended source:** [Brain Tumour MRI Dataset on Kaggle](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset)

---

## 7. Environment Configuration

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Open `.env` and replace every `replace_me` placeholder with a real value.  
**Never commit the `.env` file** — it is excluded by `.gitignore`.

Key variables to configure:

| Variable | Purpose |
|---|---|
| `MLFLOW_POSTGRES_USER` / `PASSWORD` | MLflow metadata database credentials |
| `PGADMIN_EMAIL` / `PASSWORD` | pgAdmin web UI credentials |
| `API_ADMIN_KEY` | FastAPI administration key |
| `AIRFLOW_FERNET_KEY` | Fernet encryption key for Airflow secrets |
| `APP_UID` / `APP_GID` | Match your local user ID (`id -u`, `id -g`) |

---

## 8. Installation and Setup

### Option A — Docker (recommended)

```bash
# 1. Clone the repository
git clone <repo-url>
cd BrainScan

# 2. Configure environment
cp .env.example .env
# Edit .env with your values

# 3. Place the dataset under data/ (see section 6)

# 4. Build and start all services
docker compose up --build -d

# 5. Check service health
docker compose ps
```

Services exposed after startup:

| Service | URL |
|---|---|
| FastAPI (Swagger UI) | http://localhost:8000/docs |
| Streamlit dashboard | http://localhost:8501 |
| MLflow UI | http://localhost:5000 |
| pgAdmin | http://localhost:5050 |

### Option B — Local virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements/app/requirements.txt
```

---

## 9. Data Preprocessing (Notebook 01)

`notebooks/01_data_loading_preprocessing.ipynb`

Steps implemented:

1. **Extension validation** — skip non-image files.
2. **Class discovery** — read class names from sub-directory names.
3. **Image loading** — `cv2.imread` with try/except for corrupt files.
4. **Resizing** — all images resized to **224 × 224 px** with `cv2.resize`.
5. **Shuffling** — combined image/label list shuffled with a fixed random seed.
6. **NumPy conversion** — images cast to `float32` arrays.
7. **Label encoding** — `LabelEncoder` + `to_categorical` (one-hot).
8. **Train / test split** — 80 % train / 20 % test, stratified.
9. **Pixel normalisation** — divided by 255 → range [0, 1].
10. **Serialisation** — tensors saved to `data/processed/` as `.npy` files.

---

## 10. Exploratory Data Analysis (Notebook 02)

`notebooks/02_eda_visualization.ipynb`

- Class distribution bar chart.
- Representative sample images per class.
- Pixel intensity histogram per class.
- Class imbalance ratio computation.
- Balanced `class_weight` dictionary computed with `compute_class_weight`.

---

## 11. CNN Architecture (Notebook 03)

`notebooks/03_model_training.ipynb`

The BrainScan CNN is a sequential convolutional network:

```
Input (224 × 224 × 3)
│
├── Conv2D(32, 3×3, ReLU)  →  MaxPooling2D(2×2)
├── Conv2D(64, 3×3, ReLU)  →  MaxPooling2D(2×2)
├── Conv2D(128, 3×3, ReLU) →  MaxPooling2D(2×2)
│
├── Flatten
├── Dense(256, ReLU)
├── Dropout(0.4)
│
└── Dense(4, Softmax)  →  predicted class probabilities
```

**Compilation:**

| Setting | Value |
|---|---|
| Optimiser | Adam (lr = 1e-3, with ReduceLROnPlateau) |
| Loss | Categorical cross-entropy |
| Metric | Accuracy |

---

## 12. Model Training (Notebook 03)

Key training configuration:

| Hyperparameter | Value |
|---|---|
| Epochs | 20 |
| Batch size | 32 |
| Dropout rate | 0.4 |
| Initial learning rate | 1e-3 |

**Callbacks:**

- `ModelCheckpoint` — saves the best model by `val_accuracy` to `model/brainscan_cnn_best.keras`.
- `EarlyStopping` — monitors `val_loss`, patience = 5.
- `ReduceLROnPlateau` — halves the learning rate when `val_loss` stagnates.

Training is logged to MLflow under the experiment name defined in `.env`.

---

## 13. Model Evaluation (Notebook 04)

`notebooks/04_evaluation.ipynb`

| Metric | Value |
|---|---|
| Test accuracy | **98 %** |
| Macro F1-score | 0.97 |
| Glioma F1 | 0.97 |
| Meningioma F1 | 0.95 |
| No-tumour F1 | 0.99 |
| Pituitary F1 | 0.99 |

Evaluation artefacts saved to `model/`:

- `confusion_matrix.png`
- `classification_report.txt`
- `learning_curves.png`
- `predictions_sample.png`

---

## 14. Hyperparameter Optimisation (Notebook 05)

`notebooks/05_optimization.ipynb`

A grid search over learning rate `{1e-3, 5e-4}`, batch size `{32, 64}`, and dropout rate `{0.3, 0.4}` with `ImageDataGenerator` augmentation (rotation, flips, zoom) was conducted.

All runs are tracked in MLflow.

**Conclusion:** The baseline model (no augmentation, lr=1e-3, batch=32, dropout=0.4) achieved higher or comparable accuracy with significantly lower training cost. The baseline model is used in production.

---

## 15. Prediction and Inference

### Via the REST API

```bash
curl -X POST http://localhost:8000/predict \
     -F "file=@path/to/mri_scan.jpg"
```

**Response:**

```json
{
  "predicted_class": "glioma",
  "confidence": 0.9999,
  "probabilities": {
    "glioma": 0.9999,
    "meningioma": 0.0001,
    "notumor": 0.0000,
    "pituitary": 0.0000
  }
}
```

### Via Python (`api/main.py`)

```python
from api.main import predict_image

result = predict_image("path/to/mri_scan.jpg")
print(result["predicted_class"], result["confidence"])
```

`predict_image(path)` reads the image with OpenCV, resizes it to 224 × 224, normalises pixel values to [0, 1], and returns the softmax probability for each class.

### Other endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | API and model status |
| `/classes` | GET | List of recognised class names |
| `/predict` | POST | Classify an uploaded MRI image |
| `/docs` | GET | Interactive Swagger UI |

---

## 16. Streamlit Application

```bash
# With Docker (already running on port 8501):
open http://localhost:8501

# Without Docker:
streamlit run app/main.py
```

The dashboard provides:

- **MRI upload** — drag-and-drop or file picker (JPG, PNG, BMP).
- **Image preview** with resolution metadata.
- **One-click analysis** — submits the image to the FastAPI backend.
- **Result banner** — colour-coded diagnosis badge with confidence percentage.
- **Probability chart** — horizontal bar chart showing softmax scores for all four classes.
- **Sidebar** — class reference guide and live API health indicator.

---

## 17. Model and Artefact Locations

| File | Content |
|---|---|
| `model/brainscan_cnn_best.keras` | Best checkpoint saved during training |
| `model/brainscan_cnn.keras` | Final model after full training run |
| `model/brainscan_cnn_optimized.h5` | Best model from hyperparameter search |
| `model/training_history.json` | Per-epoch accuracy, loss, and learning rate |
| `model/classification_report.txt` | Per-class precision / recall / F1 |
| `model/confusion_matrix.png` | Confusion matrix heatmap |
| `model/learning_curves.png` | Training and validation curves |
| `model/model_architecture.png` | CNN layer diagram |

> **Note:** `.keras` and `.h5` model binaries are excluded from Git.  
> They are generated by running notebook **03** and are tracked via MLflow.

---

## 18. Troubleshooting

### Model not found on API startup

Ensure `model/brainscan_cnn_best.keras` or `model/brainscan_cnn.keras` exists.  
Run notebook **03** to train and save the model, then restart the `fastapi` container:

```bash
docker compose restart fastapi
```

### Dataset loading fails in notebook 01

Verify the dataset is placed in `data/` with the correct class sub-directory names.  
Check that image files have supported extensions (`.jpg`, `.jpeg`, `.png`, `.bmp`).

### Keras / TensorFlow version mismatch

The containers use Python 3.11 with TensorFlow 2.20. If loading a model trained with a different version causes errors, retrain from notebook **03** inside the container:

```bash
docker compose exec fastapi bash
jupyter notebook --no-browser ...
```

### MLflow connection refused

Ensure the `mlflow` service is healthy before starting notebooks:

```bash
docker compose ps mlflow
```

### `use_container_width` deprecation warning in Streamlit

The application uses `width="stretch"` on `st.image` and `st.button`, which is the correct API for Streamlit ≥ 1.35. If you see this warning with an older version, upgrade Streamlit.

---

## 19. Limitations and Responsible Use

- The model was trained on a single publicly available dataset. Performance may degrade on scans from different MRI machines, protocols, or patient populations.
- Meningioma is the most challenging class (lowest F1); misclassification between meningioma and other classes should be anticipated.
- No clinical validation has been performed. Do not use outputs for real medical decisions.
- The model predicts from a static image slice. Clinical diagnosis uses full volumetric sequences and patient history.

---

## 20. Future Improvements

- Integrate additional MRI sequences (T2, FLAIR, contrast-enhanced).
- Implement Grad-CAM saliency maps to visually explain predictions.
- Explore transfer learning with pretrained architectures (EfficientNet, ResNet).
- Add a DICOM file reader for clinical image formats.
- Implement proper k-fold cross-validation for more reliable performance estimates.
- Containerise notebook execution for fully reproducible training.

---

## 21. License

No open-source license is currently applied to this repository.  
All rights reserved — BrainScan AI, MedTech Maroc, 2026.  
Contact the repository owner for usage permissions.
