# 🛡️ Network Intrusion Detection System

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![Scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange?logo=scikit-learn)](https://scikit-learn.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-black?logo=flask)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-green)]()

ML-based IDS that detects network intrusions (DoS, Probe, R2L, U2R) using Random Forest on the NSL-KDD dataset. Supports **CLI** and **REST API** interfaces.

---

## 🚀 Quick Start

```bash
pip install pandas numpy scikit-learn flask
python predict.py --src_bytes 100 --service http --flag SF
# Output: Prediction: 0 (Normal) | Attack Type: 0 (Normal)
```

## 📋 Features

| Feature | Description |
|---------|-------------|
| **Binary Classification** | Normal vs Attack — 76.8% test accuracy |
| **Multi-class Classification** | DoS / Probe / R2L / U2R — 72.4% test accuracy |
| **CLI Tool** | Single prediction or batch CSV processing |
| **REST API** | Flask server for integration with other tools |
| **41 Network Features** | Protocol, service, flags, byte counts, error rates, host stats |

## 🗂️ Project Structure

```
ids-project/
├── predict.py                 # CLI tool (single + batch mode)
├── app.py                     # Flask REST API
├── models/
│   ├── rf_binary.pkl          # Binary classifier (Normal vs Attack)
│   └── rf_multiclass.pkl      # Multi-class classifier (DoS/Probe/R2L/U2R)
├── src/
│   ├── train_binary.py        # Train binary model
│   ├── train_multiclass.py    # Train multi-class model
│   ├── eda.py                 # Exploratory data analysis
│   └── viz_multiclass.py      # Feature importance + confusion matrix
├── data/                      # NSL-KDD dataset
└── README.md
```

## 💻 CLI Usage

### Single Prediction

```bash
python predict.py --src_bytes 100 --dst_bytes 100 --protocol_type tcp --service http --flag SF
```

**Output:**
```
Prediction: 0 (Normal)
Attack Type: 0 (Normal)
```

### Suspicious Traffic Example

```bash
python predict.py --src_bytes 0 --dst_bytes 0 --protocol_type tcp --service private --flag REJ
```

**Output:**
```
Prediction: 1 (Attack)
Attack Type: 1 (DoS)
```

### Batch CSV Prediction

```bash
python predict.py --csv traffic.csv --output results.csv
```

Input CSV must include columns: `duration`, `src_bytes`, `dst_bytes`, `protocol_type`, `service`, `flag`

Output CSV adds `prediction` (0/1) and `label` (Normal/Attack) columns.

## 🌐 API Usage

Start the server:
```bash
python app.py
```

### Request
```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"duration":0,"src_bytes":100,"dst_bytes":100,"protocol_type":"tcp","service":"http","flag":"SF"}'
```

### Response
```json
{"prediction": 0}
```

## 📊 Performance

| Model | Validation Accuracy | Test Accuracy |
|-------|-------------------|---------------|
| Binary (Normal vs Attack) | 99.9% | 76.8% |
| Multi-class (DoS / Probe / R2L / U2R) | 99.9% | 72.4% |

### Multi-class Classification Report

| Class | Precision | Recall | F1-Score |
|-------|-----------|--------|----------|
| Normal | 0.65 | 0.97 | 0.78 |
| DoS | 0.92 | 0.98 | 0.95 |
| Probe | 0.64 | 1.00 | 0.78 |
| R2L | 0.99 | 0.05 | 0.10 |
| U2R | 0.00 | 0.00 | 0.00 |

## 🧠 Algorithm — Random Forest

- **Why RF over Logistic Regression?** Network traffic has non-linear relationships — URL patterns, protocol interactions, and error rates don't follow linear decision boundaries. RF captures complex feature interactions via ensemble of decision trees.
- **Feature Importance:** Built-in feature importance helps identify top attack indicators (e.g., `serror_rate`, `dst_host_srv_count`, `flag` status).

## 📚 Dataset

**NSL-KDD** — Improved version of KDD'99 dataset, removing redundant and duplicate records.

| Split | Records |
|-------|---------|
| Training | 125,973 |
| Test | 22,544 |
| Features | 41 (categorical + numerical) |

## 🧪 Test It Yourself

```bash
# Normal traffic
python predict.py --src_bytes 100 --dst_bytes 200 --service http --flag SF

# DoS attack simulation
python predict.py --src_bytes 0 --dst_bytes 0 --service private --flag REJ

# Batch mode with sample data
python predict.py --csv test.csv --output result.csv
```

## 📌 To-Do

- [ ] Real-time packet capture (scapy integration)
- [ ] Docker deployment
- [ ] XGBoost / Neural Network models
- [ ] Web dashboard

## 📄 License

MIT
