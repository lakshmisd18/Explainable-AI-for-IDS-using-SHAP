# Explainable AI-Based Intrusion Detection System using SHAP

## Overview

The Explainable AI-Based Intrusion Detection System (XAI-IDS) is a web-based cybersecurity application that detects malicious network traffic using a Random Forest Classifier and explains every prediction using SHAP (SHapley Additive Explanations).

Unlike traditional Intrusion Detection Systems that only classify traffic as normal or malicious, this system provides transparent explanations for every prediction, helping security analysts understand why a particular packet was classified as an attack.

---

## Problem Statement

Traditional Intrusion Detection Systems often operate as black-box models, producing predictions without explaining the reasoning behind them. This lack of transparency makes it difficult for security analysts to verify alerts, investigate attacks, and reduce false positives.

This project addresses this issue by integrating Explainable AI techniques into network intrusion detection.

---

## Objectives

- Detect malicious network traffic in real time.
- Classify packets as **Normal** or **Attack**.
- Explain predictions using SHAP values.
- Display live monitoring through an interactive dashboard.
- Improve trust and transparency in machine learning-based intrusion detection.

---

## Features

- Real-time network packet monitoring
- Random Forest-based intrusion detection
- Explainable AI using SHAP
- Interactive dashboard
- Live packet logs
- Feature importance visualization
- Accuracy metrics
- Confusion Matrix
- Secure login system
- Responsive web interface

---

## System Architecture

```
Live Network Traffic
        │
        ▼
 Packet Capture (Scapy)
        │
        ▼
 Data Preprocessing
        │
        ▼
 Random Forest Classifier
        │
        ├────────────► Prediction (Normal / Attack)
        │
        ▼
     SHAP Explainer
        │
        ▼
 Flask Backend
        │
        ▼
 Flask-SocketIO
        │
        ▼
 Interactive Dashboard
```

---

## Technology Stack

### Programming Language

- Python

### Machine Learning

- Scikit-learn
- Random Forest Classifier
- Joblib

### Explainable AI

- SHAP

### Backend

- Flask
- Flask-SocketIO

### Network Packet Capture

- Scapy

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Visualization

- Chart.js

---

## Project Workflow

1. Capture live network packets using Scapy.
2. Preprocess captured packet features.
3. Predict whether traffic is Normal or Attack using Random Forest.
4. Generate SHAP explanations for each prediction.
5. Stream results to the web dashboard.
6. Display live logs, charts, and explanations.

---

## Folder Structure

```
Explainable_IDS_SHAP/
│
├── app.py
├── train.py
├── predict.py
├── requirements.txt
├── README.md
│
├── model/
│   ├── random_forest_model.pkl
│   └── label_encoder.pkl
│
├── data/
│   └── dataset.csv
│
├── templates/
│   ├── index.html
│   └── login.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── utils/
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/Explainable_IDS_SHAP.git

cd Explainable_IDS_SHAP
```

### Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux/Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Project

Train the model (if required)

```bash
python train.py
```

Run the Flask application

```bash
python app.py
```

Open your browser

```
http://127.0.0.1:5000
```

---

## Output

The dashboard displays:

- Live Network Traffic
- Prediction Results
- Normal vs Attack Classification
- SHAP Feature Importance
- Accuracy Chart
- Confusion Matrix
- Packet Logs
- Login Authentication

---

## Expected Results

- Accurate detection of malicious packets.
- Transparent AI predictions using SHAP.
- Reduced false positives.
- Faster threat analysis.
- Improved decision-making for network administrators.

---

## Future Enhancements

- Deep Learning-based intrusion detection.
- Multi-class attack classification.
- Cloud deployment.
- Email and SMS alert system.
- Threat intelligence integration.
- Support for larger network datasets.
- User management with role-based authentication.

---

## References

1. Lundberg, S. M., & Lee, S. I. (2017). A Unified Approach to Interpreting Model Predictions.
2. Tavallaee et al. (2009). A Detailed Analysis of the KDD CUP 99 Dataset.
3. Buczak & Guven (2015). Survey of Machine Learning Methods for Cybersecurity.
4. SHAP Documentation
5. Flask Documentation
6. Scikit-learn Documentation
7. Scapy Documentation

---

## Authors

**Lakshmi SD**

RV College of Engineering

Department of Computer Science and Engineering

---

## License

This project is developed for academic and educational purposes.
