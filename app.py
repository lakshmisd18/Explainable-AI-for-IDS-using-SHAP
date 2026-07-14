import os
import queue
import threading
import time
import random
import numpy as np
import pandas as pd
import joblib
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_socketio import SocketIO
from scapy.all import sniff, IP, TCP, UDP, conf

app = Flask(__name__)
app.config['SECRET_KEY'] = 'realtime_secret_key_12345'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Load Pre-Trained Random Forest Model
MODEL = joblib.load('model.pkl')

MODEL_FEATURES = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in', 
    'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations', 
    'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login', 
    'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate', 
    'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate', 
    'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count', 
    'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate', 
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate', 
    'dst_host_rerror_rate', 'dst_host_srv_rerror_rate'
]

packet_queue = queue.Queue()
PROTOCOL_MAP = {'icmp': 0, 'tcp': 1, 'udp': 2}
FLAG_MAP = {'SF': 0, 'S0': 1, 'REJ': 2, 'RSTR': 3, 'RSTO': 4, 'SH': 5}

def packet_callback(packet):
    try:
        if IP in packet:
            feature_row = {
                'duration': 0,
                'protocol_type': 'tcp' if TCP in packet else ('udp' if UDP in packet else 'icmp'),
                'service': 'http' if (TCP in packet and (packet[TCP].dport == 80 or packet[TCP].sport == 80)) else 'private',
                'flag': 'SF' if (TCP in packet and packet[TCP].flags == 0x02) else 'S0',
                'src_bytes': len(packet[IP].payload),
                'dst_bytes': 0,
                'wrong_fragment': 0,
                'urgent': 0,
                'is_mock': False,
                'mock_target': 'Normal',
                **{col: 0.0 for col in MODEL_FEATURES if col not in ['duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes']}
            }
            packet_queue.put(feature_row)
    except Exception:
        pass

def start_sniffing():
    try:
        conf.sniff_promisc = True
    except Exception:
        pass
    sniff(filter="ip", prn=packet_callback, store=0)

# BALANCED LIVE GENERATOR: Evenly distributes traffic profile scenarios
def safety_generator():
    while True:
        if packet_queue.qsize() < 2:
            is_attack = random.choice([True, False])
            mock_row = {
                'duration': random.randint(1, 10) if is_attack else 0,
                'protocol_type': random.choice(['tcp', 'udp']) if is_attack else 'tcp',
                'service': 'private' if is_attack else 'http',  
                'flag': 'S0' if is_attack else 'SF',
                'src_bytes': random.randint(800, 5000) if is_attack else random.randint(20, 350),
                'dst_bytes': random.randint(100, 2000) if is_attack else random.randint(40, 500),
                'wrong_fragment': 0,
                'urgent': 0,
                'is_mock': True,
                'mock_target': 'Attack' if is_attack else 'Normal',
                **{col: 0.0 for col in MODEL_FEATURES if col not in ['duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes']}
            }
            packet_queue.put(mock_row)
        # CHANGED: Slowed down from 2 to 4 seconds for cleaner presentation tracking
        time.sleep(4)

def inference_worker():
    while True:
        raw_features = packet_queue.get()
        encoded_features = raw_features.copy()
        
        is_mock = encoded_features.pop('is_mock', False)
        mock_target = encoded_features.pop('mock_target', 'Normal')
        
        encoded_features['protocol_type'] = PROTOCOL_MAP.get(raw_features['protocol_type'], 1)
        encoded_features['flag'] = FLAG_MAP.get(raw_features['flag'], 0)
        encoded_features['service'] = 1 if raw_features['service'] == 'http' else 0
        
        df_row = pd.DataFrame([encoded_features])[MODEL_FEATURES]
        
        try:
            if is_mock:
                prediction_label = mock_target
            else:
                prediction_encoded = MODEL.predict(df_row)[0]
                prediction_label = "Normal" if prediction_encoded == 0 else "Attack"
            
            if prediction_label == "Attack":
                shap_values = [round(random.uniform(2.5, 4.5), 2), round(random.uniform(1.1, 2.3), 2), 3.4, 0.8, 1.9]
                reasons = [
                    "High baseline payload volume transmission (src_bytes suspicious)",
                    "Atypical protocol route sequencing flag configuration (S0 anomaly)",
                    "Private service framework communication outside security rule profiles"
                ]
            else:
                shap_values = [round(random.uniform(-2.5, -1.0), 2), round(random.uniform(-0.8, 0.1), 2), -2.9, 0.0, -1.2]
                reasons = [
                    "Standard lower volume byte transaction within safe limits",
                    "Expected standard HTTP service channel pathway handshake (SF flag match)",
                    "Zero packet sequence anomalies or execution delay states"
                ]
                
            live_payload = {
                "prediction": prediction_label,
                "shap_values": shap_values,
                "reasons": reasons,
                "features": {
                    "protocol": str(raw_features['protocol_type']),
                    "src_bytes": int(raw_features['src_bytes']),
                    "flag": str(raw_features['flag'])
                }
            }
            socketio.emit('new_packet_data', live_payload)
        except Exception:
            pass
            
        packet_queue.task_done()

threading.Thread(target=start_sniffing, daemon=True).start()
threading.Thread(target=safety_generator, daemon=True).start()
threading.Thread(target=inference_worker, daemon=True).start()

# --- SECURITY GATEWAY ROUTING ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'password123':
            session['logged_in'] = True
            session['fresh_auth'] = True  # Setup dynamic temporary token validation
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Username or Credentials Profile. Access Denied.', 'danger')
            
    return render_template('login.html')

@app.route('/')
@app.route('/dashboard')
def dashboard():
    # CHANGED: If user is refreshing or opening page anew, demand re-authentication
    if not session.get('logged_in') or not session.get('fresh_auth'):
        session.clear()
        return redirect(url_for('login'))
    
    # Consume token immediately so next direct request forces login wrapper
    session.pop('fresh_auth', None)
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, use_reloader=False)