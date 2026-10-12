# Dataset Directory — BrainScan AI

This directory is **not included in version control** because the dataset files are too large.

## Expected Structure

Place the brain MRI dataset here, organised by class label:

```
data/
├── glioma/          # MRI scans of glioma tumours
├── meningioma/      # MRI scans of meningioma tumours
├── notumor/         # Healthy MRI scans (no tumour)
└── pituitary/       # MRI scans of pituitary tumours
```

## Dataset Source

The project was developed with the [Brain Tumour MRI Dataset](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset) available on Kaggle.

## Supported Image Formats

- `.jpg` / `.jpeg`
- `.png`
- `.bmp`

Files with any other extension are automatically skipped during preprocessing.

## Expected Volume

Each class folder typically contains several hundred to a few thousand images.  
The preprocessing notebook (`notebooks/01_data_loading_preprocessing.ipynb`) will verify the contents and report any skipped files.

## After Placing the Dataset

Run notebook **01** to generate the preprocessed tensors that subsequent notebooks and the training pipeline depend on:

```bash
cd notebooks
jupyter notebook 01_data_loading_preprocessing.ipynb
```

Processed tensors (`X_train.npy`, `X_test.npy`, `y_train.npy`, `y_test.npy`, `label_classes.npy`)
will be saved to `data/processed/`.
