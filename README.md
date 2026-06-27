# 🛡️ Network Intrusion Detection System

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![Scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange?logo=scikit-learn)](https://scikit-learn.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-black?logo=flask)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-green)]()

ML-based Intrusion Detection System that classifies network traffic as **normal or attack** (DoS, Probe, R2L, U2R) using Random Forest on the NSL-KDD dataset. Supports **CLI** and **REST API** interfaces.

---

## 📦 For Beginners (Clone to Prediction in 2 Minutes)

```bash
# Step 1: Clone
git clone https://github.com/mohitoza08/intrusion-detection-project.git
cd intrusion-detection-project

# Step 2: Install dependencies
pip install pandas numpy scikit-learn flask

# Step 3: Run prediction
python predict.py --src_bytes 100 --service http --flag SF
```

**Output:**
```
Prediction: 0 (Normal)
Attack Type: 0 (Normal)
```

---

## 📋 Features

| Feature | Description |
|---------|-------------|
| **Binary Classification** | Normal vs Attack — 76.8% test accuracy |
| **Multi-class Classification** | DoS / Probe / R2L / U2R — 72.4% test accuracy |
| **CLI Tool** | Single prediction or batch CSV processing |
| **REST API** | Flask server for integration with other tools |
| **Pre-trained Models** | Ready to use — no training required |
| **41 Network Features** | Protocol, service, flags, byte counts, error rates, host stats |

## 🗂️ Project Structure

```
intrusion-detection-project/
├── predict.py                 # CLI tool (single + batch mode)
├── app.py                     # Flask REST API
├── models/
│   ├── rf_binary.pkl          # Binary classifier (Normal vs Attack)
│   └── rf_multiclass.pkl      # Multi-class classifier (DoS/Probe/R2L/U2R)
├── src/
│   ├── train_binary.py        # Train binary model from scratch
│   ├── train_multiclass.py    # Train multi-class model from scratch
│   ├── eda.py                 # Exploratory data analysis
│   └── viz_multiclass.py      # Feature importance + confusion matrix
├── data/                      # NSL-KDD dataset (training + test)
└── README.md
```

## 💻 CLI Usage

### Single Prediction

Classify one network traffic record:

```bash
python predict.py --src_bytes 100 --dst_bytes 100 --protocol_type tcp --service http --flag SF
```

**Output:**
```
Prediction: 0 (Normal)
Attack Type: 0 (Normal)
```

### Attack Traffic Detection

```bash
python predict.py --src_bytes 0 --dst_bytes 0 --protocol_type tcp --service private --flag REJ
```

**Output:**
```
Prediction: 1 (Attack)
Attack Type: 1 (DoS)
```

### Batch CSV Prediction

Predict on multiple records from a CSV file:

```bash
python predict.py --csv traffic.csv --output results.csv
```

**Input CSV format** (must include these columns):
```
duration,src_bytes,dst_bytes,protocol_type,service,flag
0,100,100,tcp,http,SF
0,0,0,tcp,private,REJ
```

**Output CSV** adds `prediction` (0 = Normal, 1 = Attack) and `label` columns.

### All CLI Options

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--src_bytes` | int | 0 | Source bytes |
| `--dst_bytes` | int | 0 | Destination bytes |
| `--protocol_type` | str | tcp | Protocol (tcp, udp, icmp) |
| `--service` | str | http | Service type (http, ftp, ssh, private, etc.) |
| `--flag` | str | SF | Connection flag (SF, REJ, S0, SH, etc.) |
| `--csv` | str | - | Path to CSV file for batch prediction |
| `--output` | str | predictions.csv | Output CSV file path |

## 🌐 API Usage

### Start Server

```bash
python app.py
```

Server starts at `http://127.0.0.1:5000`

### Make a Prediction Request

```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"duration":0,"src_bytes":100,"dst_bytes":100,"protocol_type":"tcp","service":"http","flag":"SF"}'
```

### Response

```json
{"prediction": 0}
```

---

## 📊 Performance

| Model | Validation Accuracy | Test Accuracy |
|-------|-------------------|---------------|
| Binary (Normal vs Attack) | **99.9%** | **76.8%** |
| Multi-class (DoS / Probe / R2L / U2R) | **99.9%** | **72.4%** |

### Multi-class Detailed Report

| Class | Precision | Recall | F1-Score | Records |
|-------|-----------|--------|----------|---------|
| Normal | 0.65 | 0.97 | 0.78 | 9,711 |
| DoS | 0.92 | 0.98 | 0.95 | 5,076 |
| Probe | 0.64 | 1.00 | 0.78 | 1,106 |
| R2L | 0.99 | 0.05 | 0.10 | 2,199 |
| U2R | 0.00 | 0.00 | 0.00 | 37 |

> **Note:** Low R2L/U2R scores are due to very few training samples — a common challenge with the NSL-KDD dataset.

## 🧠 Algorithm

**Random Forest Classifier** with 100 trees.

### Why Random Forest over Logistic Regression?

Network traffic has **non-linear relationships** — protocol interactions, error rates, and flag combinations don't follow simple linear boundaries. Random Forest:
- Captures complex feature interactions via ensemble of decision trees
- Handles mixed data types (categorical + numerical) without scaling
- Provides built-in **feature importance** to identify top attack indicators
- Robust to outliers and overfitting due to averaging

### Top Predictive Features

`serror_rate`, `dst_host_srv_count`, `dst_host_count`, `same_srv_rate`, `flag` status, `protocol_type`

## 📚 Dataset — NSL-KDD

Improved version of the KDD'99 dataset with redundant and duplicate records removed.

| Split | Records | Description |
|-------|---------|-------------|
| Training | 125,973 | Labeled network connections for model training |
| Test | 22,544 | Held-out data for evaluation |
| Features | 41 | Mixed categorical + numerical |
| Attack Classes | 4 | DoS, Probe, R2L, U2R |

## 🔧 Retrain Models (Optional)

To train models from scratch on your own:

```bash
python src/train_binary.py
python src/train_multiclass.py
```

---
Made with ❤️ for AI Security
